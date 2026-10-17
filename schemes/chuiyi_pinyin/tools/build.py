"""Reproducible build from checked-in scheme-one dictionaries; never touches it."""
import csv,hashlib,json,re,zipfile
from collections import defaultdict
from pathlib import Path
from encoding import MATRIX,COLUMNS,code,repeated_alias
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT.parents[1]/'archive/chuiyi_1'
VERSION='1.0-dev'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    inputs=[OLD/'chuiyi_1.schema.yaml',*sorted((OLD/'chuiyi_dicts').glob('*.dict.yaml'))]
    hashes={str(p.relative_to(ROOT.parents[1])):sha(p) for p in inputs}
    mapping={s+str(t):code(s+str(t)) for s in sorted(MATRIX) for t in range(1,6)}
    schema=(OLD/'chuiyi_1.schema.yaml').read_text(encoding='utf-8')
    start=schema.index('  algebra:\n')+len('  algebra:\n')
    end=schema.index('\ntranslator:',start)
    schema=schema[:start]+'\n'.join("    - 'xform/^%s$/%s/'"%(p,c) for p,c in mapping.items())+'\n'+schema[end:]
    schema=schema.replace('chuiyi_1','chuiyi_pinyin').replace('吹衣方案一','吹衣带调拼音 1.0-dev')
    schema=re.sub(r'  version: .*','  version: "1.0-dev"',schema,count=1)
    schema=re.sub(r'^#.*\n','',schema,flags=re.M)
    (ROOT/'chuiyi_pinyin.schema.yaml').write_text(schema,encoding='utf-8')
    (ROOT/'chuiyi_pinyin.dict.yaml').write_text('# See NOTICE.md for dictionary provenance.\n---\nname: chuiyi_pinyin\nversion: "1.0-dev"\nsort: by_weight\nimport_tables:\n  - chuiyi_pinyin_dicts/chars\n  - chuiyi_pinyin_dicts/base\n...\n',encoding='utf-8')
    target=ROOT/'chuiyi_pinyin_dicts';target.mkdir(exist_ok=True)
    omitted=[];aliases=0;total=0;words={};all_entries=set()
    for source in sorted((OLD/'chuiyi_dicts').glob('*.dict.yaml')):
        text=source.read_text(encoding='utf-8-sig');header,sep,body=text.partition('\n...\n');assert sep
        header=header.replace('chuiyi_dicts/','chuiyi_pinyin_dicts/').replace('"0.5.0-dev"','"1.0-dev"')
        entries={}
        for line in body.splitlines():
            if not line or line.startswith('#'):continue
            w,p,wt=line.split('\t');phones=tuple(p.split())
            missing=sorted(set(phones)-mapping.keys())
            if missing:
                omitted.append({'word':w,'phones':p,'unmapped':missing});continue
            entries[w,p]=max(int(wt),entries.get((w,p),0))
            alias=repeated_alias(w,phones)
            if alias!=phones:
                key=w,' '.join(alias)
                if key not in entries:aliases+=1
                entries[key]=max(int(wt),entries.get(key,0))
        rows=[f'{w}\t{p}\t{wt}' for (w,p),wt in sorted(entries.items())]
        (target/source.name).write_text(header+sep+'\n'.join(rows)+'\n',encoding='utf-8')
        total+=len(rows);all_entries.update(entries)
        for (w,p) in entries: words.setdefault(w,[]).append(p)
    # Full phone-to-code table and matrix make every intentional merger inspectable.
    with (ROOT/'mapping.tsv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,delimiter='\t',lineterminator='\n');writer.writerow(['pinyin','code','matrix_column'])
        writer.writerows((p,c,MATRIX[p[:-1]][1]) for p,c in mapping.items())
    matrix=['| 编码 | 声母 | '+' | '.join(x[0] for x in COLUMNS)+' |','|---|---|'+'---|'*len(COLUMNS),
            '| / | / | '+' | '.join(x[1] for x in COLUMNS)+' |']
    for first in 'bpmfdtnlgkhwjqxyviurz cso'.replace(' ',''):
        cells=[]
        for final,_,_ in COLUMNS:
            cells.append(' / '.join(s for s,(k,col,_) in MATRIX.items() if k==first and col==final))
        matrix.append('| '+first+' | '+{'v':'zh','i':'ch','u':'sh','o':'零声母'}.get(first,first)+' | '+' | '.join(cells)+' |')
    (ROOT/'MATRIX.md').write_text('# 编码矩阵\n\n'+ '\n'.join(matrix)+'\n\ner 放在 r 行 i 列；lv 保留在 f 行 i 列；ou 本来就在零声母 ou 列。所有空白数据格不生成音节。\n',encoding='utf-8')
    collisions=defaultdict(list)
    for s in sorted(MATRIX):
        for t in range(1,6): collisions[mapping[s+str(t)]].append(s+str(t))
    collisions={c:p for c,p in collisions.items() if len({x[:-1] for x in p})>1}
    checks={'o1':'oo','o4':'op','ou3':'oz','er2':'ri','er4':'rl','ri4':'rl','lv4':'fl','nv4':'ny','nve4':'np','lve4':'lp','luo4':'lp','jue4':'jp','biang2':'bh','cei4':'cw','fiao1':'fn','kei4':'kw','rua2':'rb','chua3':'ib','lo4':'lp','ba4':'bx','ba5':'bx','ma1':'ma','ma5':'mx','mei4':'mw','mei5':'me','jun4':'jq','yuan4':'yr'}
    for p,c in checks.items():assert mapping[p]==c,(p,mapping[p],c)
    assert repeated_alias('妈妈',('ma1','ma5'))==('ma1','ma1')
    assert repeated_alias('妹妹',('mei4','mei5'))==('mei4','mei4')
    assert repeated_alias('妈妈妈',('ma1','ma5','ma5'))==('ma1','ma1','ma1')
    assert repeated_alias('我们',('wo3','men5'))==('wo3','men5')
    repeat_results={w:[{'phones':p,'code':''.join(mapping[x] for x in p.split())} for p in words.get(w,[])] for w in ['爸爸','妈妈','妹妹','我们']}
    for w,p in [('爸爸','ba4 ba4'),('妈妈','ma1 ma1'),('妹妹','mei4 mei4')]:assert (w,p) in all_entries,(w,p)
    report={'version':VERSION,'syllables':len(MATRIX),'phone_mappings':len(mapping),'dictionary_rows':total,'repeat_aliases_added':aliases,'source_sha256':hashes,'omitted_rows':omitted,'cross_syllable_collisions':collisions,'repeat_examples':repeat_results,'mapping_assertions':len(checks),'engine_test_report':'docs/testing/engine-verification.json (verify input hashes)','source_unchanged':all(sha(p)==hashes[str(p.relative_to(ROOT.parents[1]))] for p in inputs)}
    (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    dist=ROOT.parents[1]/'dist';dist.mkdir(exist_ok=True)
    with zipfile.ZipFile(dist/'chuiyi_pinyin-1.0-dev.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['chuiyi_pinyin.schema.yaml','chuiyi_pinyin.dict.yaml','INSTALL.md']:
            z.write(ROOT/name,name)
        for name in ['chars.dict.yaml','base.dict.yaml']:
            p=target/name
            z.write(p,p.relative_to(ROOT))
        for name in ['LICENSE','NOTICE.md']:
            z.write(ROOT.parents[1]/name,name)
        for p in sorted((ROOT.parents[1]/'LICENSES').glob('*')):
            if p.is_file():z.write(p,'LICENSES/'+p.name)
    print(json.dumps({k:report[k] for k in ['syllables','phone_mappings','dictionary_rows','repeat_aliases_added','mapping_assertions','source_unchanged']},ensure_ascii=False))
    print('Omitted dictionary rows:',len(omitted))
if __name__=='__main__':main()
