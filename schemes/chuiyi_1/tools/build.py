"""Build portable Rime source files from the frozen v0.3.6 baseline.

This packages an existing dictionary; it does not regenerate it from upstream.
Uses only the Python standard library and never writes to the installed Rime.
"""
import hashlib
import json
import re
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'sources' / 'baseline'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build_baseline():
    provenance = json.loads((BASE / 'manifest.json').read_text(encoding='utf-8'))
    for name, expected in provenance['sha256'].items():
        assert sha(BASE / name) == expected, f'Baseline changed: {name}'
    schema = (BASE / 'chuiyi_1_test.schema.yaml').read_text(encoding='utf-8-sig')
    dictionary = (BASE / 'chuiyi_1_test.dict.yaml').read_text(encoding='utf-8-sig')
    mapping = dict(re.findall(r"(?m)^\s*-\s*'xform/\^([a-z]+[1-5])\$/([a-z]{2})/'\s*$", schema))
    assert len(mapping) == 2040
    assert all(mapping[p] == mapping[p[:-1]+'4'] for p in mapping if p.endswith('5'))
    header, sep, body = dictionary.partition('\n...\n')
    assert sep
    rows = body.splitlines()
    seen = set()
    for row in rows:
        word, phones, weight = row.split('\t')
        assert word and weight.isdigit()
        assert all(p in mapping for p in phones.split()), (word, phones)
        assert (word, phones) not in seen, (word, phones)
        seen.add((word, phones))
    schema = schema.replace('# 吹衣方案一：临时验证方案（不影响正式 chuiyi_1）', '# 吹衣方案一：Rime 方案开发版')
    schema = schema.replace('chuiyi_1_test_v036', 'chuiyi_1').replace('chuiyi_1_test', 'chuiyi_1')
    schema = schema.replace('吹衣方案一（隔离测试）', '吹衣方案一')
    schema = schema.replace('仅用于测试声调映射、词组、独立用户词典，非正式版', '自定义声调编码；雾凇词库基础；开发版')
    header = header.replace('# 自动生成的扩展测试词库，仅供隔离测试', '# 吹衣方案一词库；雾凇词条和词频基础，详见 NOTICE.md')
    header = header.replace('name: chuiyi_1_test', 'name: chuiyi_1')
    result = header + sep + body
    assert result.partition('\n...\n')[2] == body
    assert dict(re.findall(r"(?m)^\s*-\s*'xform/\^([a-z]+[1-5])\$/([a-z]{2})/'\s*$", schema)) == mapping
    (ROOT / 'chuiyi_1.schema.yaml').write_text(schema, encoding='utf-8')
    (ROOT / 'chuiyi_1.dict.yaml').write_text(result, encoding='utf-8')
    report = {'baseline':'0.3.6', 'dictionary_rows':len(rows), 'mapping_rules':len(mapping),
              'dictionary_body_unchanged':True, 'mapping_unchanged':True,
              'outputs':{n:sha(ROOT/n) for n in ('chuiyi_1.schema.yaml','chuiyi_1.dict.yaml')}}
    (ROOT / 'build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

def main():
    parser = argparse.ArgumentParser(description='Generate current Rime files, or explicitly restore the old baseline.')
    parser.add_argument('--baseline',action='store_true')
    args = parser.parse_args()
    if args.baseline:
        build_baseline()
        return
    subprocess.run([sys.executable,str(ROOT/'tools/generate_dictionary.py')],check=True)
    for name in ['chuiyi_1.schema.yaml','chuiyi_1.dict.yaml']:
        shutil.copy2(ROOT/'generated'/name,ROOT/name)
    shutil.copytree(ROOT/'generated/chuiyi_dicts',ROOT/'chuiyi_dicts',dirs_exist_ok=True)
    shutil.copy2(ROOT/'generated/report.json',ROOT/'build-report.json')

if __name__ == '__main__':
    main()
