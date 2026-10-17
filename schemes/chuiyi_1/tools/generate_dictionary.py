"""Build from local Ice pinyin and frequencies, with author-confirmed encoding."""
import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from encoding import update_schema

ROOT = Path(__file__).resolve().parent.parent
MARKS = {'\u0304':'1','\u0301':'2','\u030c':'3','\u0300':'4'}

def numeric(raw):
    letters, tone = '', '5'
    for c in unicodedata.normalize('NFD', raw.lower().strip()):
        if c in MARKS:
            tone = MARKS[c]
        elif c == '\u0308' and letters.endswith('u'):
            letters = letters[:-1] + 'v'
        elif unicodedata.category(c) != 'Mn':
            letters += c
    return letters + tone

def ice_rows(path):
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        f = line.split('\t')
        if len(f) >= 3 and f[2].isdigit() and not f[0].startswith('#'):
            yield f[0], f[1], int(f[2])

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sources', type=Path, default=ROOT/'sources/upstream')
    ap.add_argument('--output', type=Path, default=ROOT/'generated')
    args = ap.parse_args()
    schema = update_schema((ROOT/'chuiyi_1.schema.yaml').read_text(encoding='utf-8'))
    mapping = dict(re.findall(r"(?m)^\s*-\s*'xform/\^([a-z]+[1-5])\$/([a-z]{2})/'\s*$", schema))
    assert len(mapping) == 2040
    paths = {n:args.sources/n for n in ['8105.dict.yaml','base.dict.yaml','pinyin.txt','large_pinyin.txt','kTGHZ2013.txt','kMandarin_8105.txt']}
    baseline = ROOT/'sources/baseline/chuiyi_1_test.dict.yaml'
    inputs = dict(paths, baseline=baseline)
    hashes = {n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in inputs.items()}
    weights = {}
    chars = set()
    for name in ['8105.dict.yaml','base.dict.yaml']:
        for w,p,wt in ice_rows(paths[name]):
            weights[w,p] = max(wt, weights.get((w,p), 0))
            if len(w) == 1:
                chars.add(w)
    refs = defaultdict(set)
    for line in paths['large_pinyin.txt'].read_text(encoding='utf-8-sig').splitlines():
        if line.startswith('#') or ': ' not in line:
            continue
        w, raw = line.split(': ',1)
        phones = tuple(numeric(p) for p in raw.split())
        if len(phones) == len(w):
            refs[w].add(phones)
    entries, counts = {}, Counter()
    missing = set()

    def add(w, phones, wt, reason):
        if any(p not in mapping for p in phones):
            missing.update(p for p in phones if p not in mapping)
            counts['unmapped_reading_attempts'] += 1
            return
        key = w, ' '.join(phones)
        if key not in entries:
            counts[reason] += 1
        entries[key] = max(wt, entries.get(key, 0))

    # Retain phrase history; restrict standalone readings to Ice plain pinyin.
    body = baseline.read_text(encoding='utf-8-sig').split('\n...\n',1)[1]
    for line in body.splitlines():
        w,p,wt = line.split('\t')
        plain = ' '.join(x[:-1] for x in p.split())
        if len(w)==1 and (w,plain) not in weights:
            counts['filtered_baseline_single_readings'] += 1
            continue
        add(w, tuple(p.split()), weights.get((w,plain),int(wt)), 'baseline_rows')
    # Prefer standard character readings when either pronunciation source covers a character.
    # pinyin-data includes broad variants (including unmarked/rare readings); adding every
    # variant as a standalone character can create false candidates such as 家 under jx.
    preferred = []
    for name in ['kTGHZ2013.txt','kMandarin_8105.txt']:
        data = defaultdict(set)
        for line in paths[name].read_text(encoding='utf-8-sig').splitlines():
            m = re.match(r'^U\+([0-9A-Fa-f]+):\s*([^#]+)',line)
            if m and not any(mark in m[2] for mark in ['?', '->', '<-']):
                char = chr(int(m[1],16))
                for raw in re.split(r'[,，\s]+',m[2].strip()):
                    phone = numeric(raw)
                    if phone in mapping:
                        data[char,phone[:-1]].add(phone)
        preferred.append(data)
    preferred_by_char = defaultdict(set)
    # Prefer mainland Mandarin (kMandarin_8105); use the Taiwan source only
    # for characters not covered there. This avoids treating an unmarked
    # secondary spelling such as 家's "jia" as an extra neutral-tone reading.
    for (char, _plain), phones in preferred[1].items():
        preferred_by_char[char].update(phones)
    for (char, _plain), phones in preferred[0].items():
        if char not in preferred_by_char:
            preferred_by_char[char].update(phones)

    # Supplement readings from pinyin-data only when they agree with authoritative
    # character sources, or when neither source has a reading for that character.
    single_readings = defaultdict(set)
    for line in paths['pinyin.txt'].read_text(encoding='utf-8-sig').splitlines():
        m = re.match(r'^U\+([0-9A-Fa-f]+):\s*([^#]+)',line)
        if not m:
            continue
        w = chr(int(m[1],16))
        candidates = set()
        for raw in m[2].strip().split(','):
            phone = numeric(raw)
            if phone in mapping:
                candidates.add(phone)
        authoritative = preferred_by_char.get(w, set())
        for phone in sorted(candidates):
            if authoritative and phone not in authoritative:
                continue
            key = (w, phone[:-1])
            single_readings[key].add(phone)
            if w in chars and key in weights:
                add(w,(phone,),weights[key],'single_source_additions')
    unresolved = []
    unresolved_reasons = Counter()
    for (w,plain),wt in weights.items():
        if len(w) == 1:
            continue
        matched = False
        for phones in sorted(refs.get(w,())):
            if ' '.join(p[:-1] for p in phones) != plain:
                continue
            if any(p not in mapping for p in phones):
                continue
            matched = True
            add(w,phones,wt,'phrase_source_additions')
        if not matched:
            plains = plain.split()
            choices = [single_readings[c,p] for c,p in zip(w,plains)]
            used_preference = False
            for i,(c,p) in enumerate(zip(w,plains)):
                if len(choices[i]) != 1:
                    for data in preferred:
                        options = data.get((c,p),set())
                        if len(options) == 1:
                            choices[i] = options
                            used_preference = True
                            break
            if len(plains) == len(w) and all(len(options) == 1 for options in choices):
                add(w,tuple(next(iter(options)) for options in choices),wt,
                    'preferred_reading_phrases' if used_preference else 'fixed_reading_phrases')
            else:
                unresolved.append(f'{w}\t{plain}\t{wt}')
                unresolved_reasons['length_mismatch' if len(plains)!=len(w) else
                                   'missing_reading' if any(not o for o in choices) else
                                   'ambiguous_tones'] += 1
    # Add citation-tone counterparts to existing yi/bu sandhi readings.
    # No speculative all-character pronunciation Cartesian products.
    for (w,p),wt in list(entries.items()):
        if len(w) < 2:
            continue
        phones = p.split()
        if len(w) != len(phones):
            continue
        citation = tuple('yi1' if c == '一' and ph in {'yi2','yi4'} else
                         'bu4' if c == '不' and ph == 'bu2' else ph
                         for c,ph in zip(w,phones))
        if citation != tuple(phones):
            add(w,citation,wt,'citation_counterparts')
    assert ('不是','bu2 shi4') in entries and ('不是','bu4 shi4') in entries
    assert entries['不是','bu2 shi4'] == entries['不是','bu4 shi4'] == weights['不是','bu shi']
    assert ('不','bu2') in entries and ('一','yi2') in entries
    assert all((w,p) in entries for w,p,wt in
               (line.split('\t') for line in body.splitlines()) if len(w)>1)
    assert ('前','qian2') in entries and ('前','jian3') not in entries
    assert all((w,p[:-1]) in weights for w,p in entries if len(w)==1)
    assert all(entries[k] >= 0 for k in entries)
    args.output.mkdir(parents=True,exist_ok=True)
    tables_dir = args.output/'chuiyi_dicts'
    tables_dir.mkdir(exist_ok=True)
    table_counts = {}
    reconstructed = {}
    for table in ['chars','base']:
        selected = {key:wt for key,wt in entries.items() if (len(key[0]) == 1) == (table == 'chars')}
        header = f'# 雾凇词频基础；来源见 NOTICE.md\n---\nname: chuiyi_dicts/{table}\nversion: "0.5.0-dev"\nsort: by_weight\n...\n'
        path = tables_dir/f'{table}.dict.yaml'
        path.write_text(header+''.join(f'{w}\t{p}\t{wt}\n' for (w,p),wt in sorted(selected.items())),encoding='utf-8')
        for row in path.read_text(encoding='utf-8').split('\n...\n',1)[1].splitlines():
            w,p,wt = row.split('\t')
            assert (w,p) not in reconstructed
            reconstructed[w,p] = int(wt)
        table_counts[table] = len(selected)
    assert reconstructed == entries, 'Split tables differ from generated dictionary'
    main_dict = '# 吹衣方案一：主词典\n---\nname: chuiyi_1\nversion: "0.5.0-dev"\nsort: by_weight\nimport_tables:\n  - chuiyi_dicts/chars\n  - chuiyi_dicts/base\n...\n'
    (args.output/'chuiyi_1.dict.yaml').write_text(main_dict,encoding='utf-8')
    new_schema = schema
    (args.output/'chuiyi_1.schema.yaml').write_text(new_schema,encoding='utf-8')
    (args.output/'unresolved.tsv').write_text('词语\t原拼音\t词频\n'+'\n'.join(unresolved)+'\n',encoding='utf-8-sig')
    report = {'version':'0.5.0-dev','input_sha256':hashes,'counts':dict(counts),
              'entries':len(entries),'tables':table_counts,'split_roundtrip_verified':True,'unresolved_ice_phrase_rows':len(unresolved),
              'unresolved_reasons':dict(unresolved_reasons),
              'unmapped_syllables':sorted(missing),
              'policy':'Single-character readings prefer kMandarin_8105, fall back to kTGHZ2013 for uncovered characters, then use pinyin-data only when neither covers the character; phrase readings use whole source or common-tone inference; preserve phrase sandhi and citation counterparts. Neutral tone accepts tone-1 and tone-4 codes.',
              'not_installed':True}
    (args.output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['entries','counts','unresolved_ice_phrase_rows','unmapped_syllables']},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
