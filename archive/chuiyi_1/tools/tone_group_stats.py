"""Reproduce a lexical (not keyboard-code) collision comparison for design D."""
import argparse
import hashlib
import json
import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SELECTED_FINALS = {'i', 'u', 'e', 'ie', 'ei'}


def rows(path):
    body = path.read_text(encoding='utf-8-sig').split('\n...\n', 1)[1]
    for line in body.splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        fields = line.split('\t')
        if len(fields) >= 3 and fields[2].isdigit():
            yield fields[0], tuple(fields[1].split()), int(fields[2])


def final(syllable):
    # Standard orthographic finals; retain apical i in the i class.
    if syllable.startswith('y'):
        return {'i': 'i', 'a': 'ia', 'ao': 'iao', 'e': 'ie', 'ou': 'iu',
                'an': 'ian', 'in': 'in', 'ang': 'iang', 'ing': 'ing',
                'ong': 'iong', 'u': 'v', 'ue': 've', 'uan': 'van',
                'un': 'vn'}[syllable[1:]]
    if syllable.startswith('w'):
        return {'u': 'u', 'a': 'ua', 'o': 'uo', 'ai': 'uai', 'ei': 'ui',
                'an': 'uan', 'en': 'un', 'ang': 'uang', 'eng': 'ueng'}[syllable[1:]]
    match = re.fullmatch(r'(zh|ch|sh|[bpmfdtnlgkhjqxrzcs])(.+)', syllable)
    if not match:
        return syllable
    initial, result = match.groups()
    if initial in {'j', 'q', 'x'} and result.startswith('u'):
        result = 'v' + result[1:]
    return result


def d_signature(phones):
    return tuple((p[:-1], ('1' if p[-1] == '1' else
                           '23' if p[-1] in '23' else '45')
                  if final(p[:-1]) in SELECTED_FINALS else '*') for p in phones)


def han_word(word):
    return len(word) >= 2 and all('\u3400' <= c <= '\u4dbf' or
                                 '\u4e00' <= c <= '\u9fff' or
                                 '\U00020000' <= c <= '\U0002fa1f' for c in word)


def calculate():
    upstream = ROOT / 'sources/upstream/base.dict.yaml'
    toned = ROOT / 'chuiyi_dicts/base.dict.yaml'
    weights, spellings = {}, defaultdict(set)
    for word, phones, weight in rows(upstream):
        if han_word(word) and len(phones) == len(word):
            weights[word] = max(weight, weights.get(word, 0))
            spellings[word].add(phones)
    # Rank words before joining tones, so missing tones cannot change the sample.
    selected = sorted(weights, key=lambda w: (-weights[w], w))[:2500]
    assert len(selected) == 2500
    selected_set = set(selected)
    readings = defaultdict(set)
    for word, phones, _ in rows(toned):
        if word not in selected_set:
            continue
        assert all(re.fullmatch('[a-z]+[1-5]', p) for p in phones)
        plain = tuple(p[:-1] for p in phones)
        if plain in spellings[word]:
            readings[word].add(phones)
    missing = {w: [' '.join(p) for p in sorted(spellings[w] -
               {tuple(ph[:-1] for ph in r) for r in readings[w]})]
               for w in selected}
    missing = {w: p for w, p in missing.items() if p}
    groups = defaultdict(set)
    for word in selected:
        for plain in spellings[word]:
            groups[plain].add(word)
    plain_pairs = {pair for words in groups.values()
                   for pair in combinations(sorted(words), 2)}
    covered = {w for w in selected if w not in missing}
    pairs = {pair for pair in plain_pairs if set(pair) <= covered}
    full = {w: readings[w] for w in covered}
    design_d = {w: {d_signature(r) for r in readings[w]} for w in covered}
    full_remaining = {p for p in pairs if full[p[0]] & full[p[1]]}
    d_remaining = {p for p in pairs if design_d[p[0]] & design_d[p[1]]}
    assert full_remaining <= d_remaining <= pairs
    return {
        'input_sha256': {p.relative_to(ROOT).as_posix(): hashlib.sha256(
                            p.read_text(encoding='utf-8-sig').encode('utf-8')).hexdigest()
                         for p in (upstream, toned)},
        'selected_words': len(selected),
        'selection_sha256': hashlib.sha256(('\n'.join(selected) + '\n').encode()).hexdigest(),
        'minimum_selected_weight': weights[selected[-1]],
        'fully_covered_words': len(covered),
        'missing_plain_readings': missing,
        'all_selected_plain_collision_pairs': len(plain_pairs),
        'covered_plain_collision_pairs': len(pairs),
        'full_tone_remaining_pairs': len(full_remaining),
        'd_remaining_pairs': len(d_remaining),
        'd_resolved_pairs': len(pairs - d_remaining),
        'd_resolved_fraction': len(pairs - d_remaining) / len(pairs) if pairs else None,
        'd_remaining_word_pairs': sorted(d_remaining),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write UTF-8 JSON to this path')
    args = parser.parse_args()
    result = json.dumps(calculate(), ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(result, encoding='utf-8')
    else:
        print(result, end='')
