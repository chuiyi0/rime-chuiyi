"""Reproducible build from checked-in scheme-one dictionaries; never touches it."""
import csv,hashlib,json,re,shutil,zipfile
from collections import defaultdict
from pathlib import Path
from encoding import MATRIX,COLUMNS,code,repeated_alias,neutral_aliases
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT.parent/'chuiyi_1'
VERSION='1.2'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    inputs=[OLD/'chuiyi_1.schema.yaml',*sorted((OLD/'chuiyi_dicts').glob('*.dict.yaml'))]
    hashes={str(p.relative_to(ROOT.parents[1])):sha(p) for p in inputs}
    mapping={s+str(t):code(s+str(t)) for s in sorted(MATRIX) for t in range(1,6)}
    schema=(OLD/'chuiyi_1.schema.yaml').read_text(encoding='utf-8')
    start=schema.index('  algebra:\n')+len('  algebra:\n')
    end=schema.index('\ntranslator:',start)
    schema=schema[:start]+'\n'.join("    - 'xform/^%s$/%s/'"%(p,c) for p,c in mapping.items())+'\n'+schema[end:]
    schema=schema.replace('chuiyi_1','chuiyi_pinyin_1_2').replace('吹衣方案一','吹衣带调拼音 1.2')
    schema=re.sub(r'  version: .*','  version: "1.2"',schema,count=1)
    schema=re.sub(r'^#.*\n','',schema,flags=re.M)
    schema += '\neditor:\n  bindings:\n    Return: commit_raw_input\n    KP_Enter: commit_raw_input\n'
    (ROOT/'chuiyi_pinyin_1_2.schema.yaml').write_text(schema,encoding='utf-8')
    (ROOT/'chuiyi_pinyin_1_2.dict.yaml').write_text('# See NOTICE.md for dictionary provenance.\n---\nname: chuiyi_pinyin_1_2\nversion: "1.2"\nsort: by_weight\nimport_tables:\n  - chuiyi_pinyin_1_2_dicts/chars\n  - chuiyi_pinyin_1_2_dicts/base\n...\n',encoding='utf-8')
    target=ROOT/'chuiyi_pinyin_1_2_dicts';target.mkdir(exist_ok=True)
    omitted=[];reading_corrections=[];aliases=0;neutral_added=0;eligible=0;total=0;words={};all_entries=set()
    for source in sorted((OLD/'chuiyi_dicts').glob('*.dict.yaml')):
        text=source.read_text(encoding='utf-8-sig');header,sep,body=text.partition('\n...\n');assert sep
        header=header.replace('chuiyi_dicts/','chuiyi_pinyin_1_2_dicts/').replace('"0.5.0-dev"','"1.2"')
        entries={}
        for line in body.splitlines():
            if not line or line.startswith('#'):continue
            w,p,wt=line.split('\t');phones=tuple(p.split())
            if w=='雷' and phones==('lei4',):
                reading_corrections.append({'word':w,'removed':p,'reason':'retain common modern lei2 reading'});continue
            missing=sorted(set(phones)-mapping.keys())
            if missing:
                omitted.append({'word':w,'phones':p,'unmapped':missing});continue
            entries[w,p]=max(int(wt),entries.get((w,p),0))
            alias=repeated_alias(w,phones)
            if alias!=phones:
                key=w,' '.join(alias)
                if key not in entries:aliases+=1
                entries[key]=max(int(wt),entries.get(key,0))
        # Preserve all readings produced by 1.0, then add only the requested 2-char rule.
        baseline=dict(entries)
        for (w,p),wt in sorted(baseline.items()):
            alternatives=neutral_aliases(w,tuple(p.split()))
            if alternatives: eligible+=1
            for phones in alternatives:
                key=w,' '.join(phones)
                if key not in entries: entries[key]=wt;neutral_added+=1
        assert all(entries[k]==v for k,v in baseline.items())
        added=set(entries)-set(baseline)
        assert all(len(w)==2 and len(p.split())==2 for w,p in added)
        if source.name=='chars.dict.yaml': assert not added
        rows=[f'{w}\t{p}\t{wt}' for (w,p),wt in sorted(entries.items())]
        (target/source.name).write_text(header+sep+'\n'.join(rows)+'\n',encoding='utf-8')
        total+=len(rows);all_entries.update(entries)
        for (w,p) in entries: words.setdefault(w,[]).append(p)
    # Full phone-to-code table and matrix make every intentional merger inspectable.
    with (ROOT/'mapping.tsv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,delimiter='\t',lineterminator='\n');writer.writerow(['pinyin','code','matrix_column'])
        writer.writerows((p,c,MATRIX[p[:-1]][1]) for p,c in mapping.items())
    matrix=['| 编码 | 声母 | '+' | '.join(x[1] for x in COLUMNS)+' |','|---|---|'+'---|'*len(COLUMNS),
            '| / | / | '+' | '.join(x[0] for x in COLUMNS)+' |']
    for first in 'bpmfdtnlgkhwjqxyviurz cso'.replace(' ',''):
        cells=[]
        for final,_,_ in COLUMNS:
            cells.append(' / '.join(s for s,(k,col,_) in MATRIX.items() if k==first and col==final))
        matrix.append('| '+first+' | '+{'v':'zh','i':'ch','u':'sh','o':'零声母'}.get(first,first)+' | '+' | '.join(cells)+' |')
    (ROOT/'MATRIX.md').write_text('# 编码矩阵\n\n'+ '\n'.join(matrix)+'\n\niop4：i=一声及默认轻声，o=二三声，p=四声。wu4/ey4：只有四声用第二键，其余用第一键。空表头继承左侧完整规则，下表写全继承值。jian/qian/xian/yan 按 g/k/h/w 行 i 列编码；lv 在 f 行 i 列使用 fi/fo/fp；er 和 ri 共组。双字词第二音节标轻声时兼容其他声调，单字不增加此项容错。单字雷仅保留 lei2。\n',encoding='utf-8')
    collisions=defaultdict(list)
    for s in sorted(MATRIX):
        for t in range(1,6): collisions[mapping[s+str(t)]].append(s+str(t))
    collisions={c:p for c,p in collisions.items() if len({x[:-1] for x in p})>1}
    checks={'li1': 'li', 'li2': 'lo', 'li3': 'lo', 'li4': 'lp', 'li5': 'li', 'le1': 'le', 'le4': 'ly', 'le5': 'le', 'lu1': 'lw', 'lu4': 'lu', 'lv1': 'fi', 'lv2': 'fo', 'lv3': 'fo', 'lv4': 'fp', 'lv5': 'fi', 'jian1': 'gi', 'jian2': 'go', 'jian3': 'go', 'jian4': 'gp', 'qian1': 'ki', 'qian4': 'kp', 'xian1': 'hi', 'xian4': 'hp', 'yan1': 'wi', 'yan2': 'wo', 'yan4': 'wp', 'an4': 'oj', 'tian4': 'tm', 'o4': 'ox', 'nve4': 'nx', 'luo4': 'lx', 'jia1': 'jd', 'jia4': 'jd', 'hua2': 'hb', 'jiang4': 'jl', 'guang1': 'gl', 'jun4': 'jt', 'yuan4': 'yr', 'ai4': 'od', 'wu2': 'ww', 'de4': 'dy', 'yi4': 'yp', 'zhi2': 'vo', 'er2': 'ro', 'er4': 'rp'}
    for p,c in checks.items():assert mapping[p]==c,(p,mapping[p],c)
    assert repeated_alias('妈妈',('ma1','ma5'))==('ma1','ma1')
    assert repeated_alias('妹妹',('mei4','mei5'))==('mei4','mei4')
    assert repeated_alias('妈妈妈',('ma1','ma5','ma5'))==('ma1','ma1','ma1')
    assert repeated_alias('我们',('wo3','men5'))==('wo3','men5')
    repeat_results={w:[{'phones':p,'code':''.join(mapping[x] for x in p.split())} for p in words.get(w,[])] for w in ['爸爸','妈妈','妹妹','我们']}
    for w,p in [('爸爸','ba4 ba4'),('妈妈','ma1 ma1'),('妹妹','mei4 mei4')]:assert (w,p) in all_entries,(w,p)
    assert neutral_aliases('子',('zi5',))==()
    assert neutral_aliases('桌子们',('zhuo1','zi5','men5'))==()
    report={'reading_corrections':reading_corrections,'neutral_aliases_added':neutral_added,'eligible_neutral_entries':eligible,'schema_id':'chuiyi_pinyin_1_2','version':VERSION,'syllables':len(MATRIX),'phone_mappings':len(mapping),'dictionary_rows':total,'repeat_aliases_added':aliases,'source_sha256':hashes,'omitted_rows':omitted,'cross_syllable_collisions':collisions,'repeat_examples':repeat_results,'mapping_assertions':len(checks),'engine_test_report':'engine-verification.json (when present; verify input hashes)','source_unchanged':all(sha(p)==hashes[str(p.relative_to(ROOT.parents[1]))] for p in inputs)}
    (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    dist=ROOT.parents[1]/'dist';dist.mkdir(exist_ok=True)
    with zipfile.ZipFile(dist/'chuiyi_pinyin-1.2.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in [ROOT/'chuiyi_pinyin_1_2.schema.yaml',ROOT/'chuiyi_pinyin_1_2.dict.yaml',*sorted(target.glob('*.dict.yaml')),*[ROOT/n for n in ['INSTALL.md','TUTORIAL.md','MATRIX.md','mapping.tsv','TESTING.md','validation.json']]]:
            if p.is_file() and '__pycache__' not in str(p) and 'local-validation' not in str(p):z.write(p,p.relative_to(ROOT))
        for name in ['LICENSE','NOTICE.md']:
            z.write(ROOT.parents[1]/name,'licenses/'+name)
        for p in (ROOT.parents[1]/'LICENSES').glob('*'):z.write(p,'LICENSES/'+p.name)
    print(json.dumps({k:report[k] for k in ['syllables','phone_mappings','dictionary_rows','repeat_aliases_added','mapping_assertions','source_unchanged']},ensure_ascii=False))
    print('Omitted dictionary rows:',len(omitted))
if __name__=='__main__':main()
