"""Compile and check generated files in a separate local Rime data directory."""
import argparse
import ctypes as C
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from encoding import code as expected_code

ROOT = Path(__file__).resolve().parent.parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime',required=True,type=Path)
    parser.add_argument('--api-header',required=True,type=Path)
    args = parser.parse_args()
    sandbox = ROOT/'local-validation'
    sandbox.mkdir(exist_ok=True)
    generated = ROOT/'generated'
    for name in ['chuiyi_1.schema.yaml','chuiyi_1.dict.yaml']:
        shutil.copy2(generated/name,sandbox/name)
    shutil.copytree(generated/'chuiyi_dicts',sandbox/'chuiyi_dicts',dirs_exist_ok=True)
    class Traits(C.Structure):
        _fields_ = [('data_size',C.c_int)]+[(n,C.c_char_p) for n in
            ['shared_data_dir','user_data_dir','distribution_name','distribution_code_name','distribution_version','app_name']]+[
            ('modules',C.POINTER(C.c_char_p)),('min_log_level',C.c_int),('log_dir',C.c_char_p),
            ('prebuilt_data_dir',C.c_char_p),('staging_dir',C.c_char_p)]
    class Candidate(C.Structure):
        _fields_=[('text',C.c_char_p),('comment',C.c_char_p),('reserved',C.c_void_p)]
    class Iterator(C.Structure):
        _fields_=[('ptr',C.c_void_p),('index',C.c_int),('candidate',Candidate)]
    header=args.api_header.read_text(encoding='utf-8-sig')
    body=header.split('typedef struct RIME_FLAVORED(rime_api_t) {',1)[1].split('} RIME_FLAVORED(RimeApi);',1)[0]
    names=re.findall(r'\(\*(\w+)\)',body)
    class API(C.Structure):
        _fields_=[('data_size',C.c_int)]+[(n,C.c_void_p) for n in names]
    directory_handle=os.add_dll_directory(str(args.runtime))
    dll=C.CDLL(str(args.runtime/'rime.dll'))
    dll.rime_get_api.restype=C.POINTER(API)
    api=dll.rime_get_api().contents
    def fn(name,result,*types):
        assert getattr(API,name).offset < api.data_size+4
        return C.CFUNCTYPE(result,*types)(getattr(api,name))
    traits=Traits()
    traits.data_size=C.sizeof(Traits)-C.sizeof(C.c_int)
    traits.shared_data_dir=str(args.runtime/'data').encode('utf-8')
    traits.user_data_dir=str(sandbox).encode('utf-8')
    traits.app_name=b'rime.chuiyi_validation'
    traits.min_log_level=2
    traits.log_dir=str(sandbox).encode('utf-8')
    fn('setup',None,C.POINTER(Traits))(C.byref(traits))
    fn('initialize',None,C.POINTER(Traits))(C.byref(traits))
    fn('deployer_initialize',None,C.POINTER(Traits))(C.byref(traits))
    try:
        assert fn('deploy_config_file',C.c_int,C.c_char_p,C.c_char_p)(b'default.yaml',b'config_version')
        assert fn('deploy_schema',C.c_int,C.c_char_p)(str(sandbox/'chuiyi_1.schema.yaml').encode('utf-8'))
        sid=fn('create_session',C.c_size_t)()
        assert sid and fn('select_schema',C.c_int,C.c_size_t,C.c_char_p)(sid,b'chuiyi_1')
        fn('set_option',None,C.c_size_t,C.c_char_p,C.c_int)(sid,b'ascii_mode',0)
        mapping=dict(re.findall(r"(?m)^\s*-\s*'xform/\^([a-z]+[1-5])\$/([a-z]{2})/'\s*$",
                                (generated/'chuiyi_1.schema.yaml').read_text(encoding='utf-8')))
        cases=[('我','wo3'),('你','ni3'),('我们','wo3 men5'),('中国','zhong1 guo2'),
               ('银行','yin2 hang2'),('音乐','yin1 yue4'),('不是','bu2 shi4'),('不是','bu4 shi4')]
        # Include fixed and preferred fallback rows to verify freshly expanded vocabulary.
        for line in (generated/'chuiyi_dicts/base.dict.yaml').read_text(encoding='utf-8').splitlines():
            fields=line.split('\t')
            if len(fields)==3 and fields[0] in {'计算机','输入法','中华人民共和国','图书馆','数据库'}:
                cases.append((fields[0],fields[1]))
        cases += [('前','qian2'),('绿','lv4'),('妈妈','ma1 ma5'),
                  ('弯','wan1'),('完','wan2'),('晚','wan3'),('万','wan4'),
                  ('汪','wang1'),('王','wang2'),('往','wang3'),('旺','wang4')]
        checks=[]
        def candidate_rank(code,word):
            fn('clear_composition',None,C.c_size_t)(sid)
            for key in code:
                fn('process_key',C.c_int,C.c_size_t,C.c_int,C.c_int)(sid,ord(key),0)
            it=Iterator(); rank=None
            if fn('candidate_list_begin',C.c_int,C.c_size_t,C.POINTER(Iterator))(sid,C.byref(it)):
                n=0
                while fn('candidate_list_next',C.c_int,C.POINTER(Iterator))(C.byref(it)):
                    n+=1
                    if (it.candidate.text or b'').decode('utf-8')==word:
                        rank=n; break
                    assert n<10000
                fn('candidate_list_end',None,C.POINTER(Iterator))(C.byref(it))
            return rank
        for word,phones in dict.fromkeys(cases):
            fn('clear_composition',None,C.c_size_t)(sid)
            code=''.join(mapping[p] for p in phones.split())
            for key in code:
                fn('process_key',C.c_int,C.c_size_t,C.c_int,C.c_int)(sid,ord(key),0)
            it=Iterator(); found=False; rank=None
            if fn('candidate_list_begin',C.c_int,C.c_size_t,C.POINTER(Iterator))(sid,C.byref(it)):
                n=0
                while fn('candidate_list_next',C.c_int,C.POINTER(Iterator))(C.byref(it)):
                    n+=1
                    if (it.candidate.text or b'').decode('utf-8')==word:
                        found=True; rank=n; break
                    assert n<10000
                fn('candidate_list_end',None,C.POINTER(Iterator))(C.byref(it))
            checks.append({'word':word,'phones':phones,'code':code,'passed':found,'rank':rank})
        for word,phone in [('吗','ma5'),('呢','ne5')]:
            for tone in ['1','4']:
                spelling = mapping[phone[:-1]+tone]
                rank = candidate_rank(spelling,word)
                checks.append({'word':word,'code':spelling,'neutral_alias':tone,'passed':rank is not None,'rank':rank})
        checks.append({'word':'前','code':'go','expected':'absent','passed':candidate_rank('go','前') is None})
        for old,word in [('wd','弯'),('wd','完'),('wd','晚'),('wd','万'),
                         ('wn','汪'),('wn','王'),('wn','往'),('wn','旺')]:
            checks.append({'word':word,'code':old,'expected':'absent','passed':candidate_rank(old,word) is None})
        mapping_checks = {p: value==expected_code(p) for p,value in mapping.items()}
        assert len(mapping_checks)==2040 and all(mapping_checks.values())
        expected={'jian1':'jj','jian2':'jj','jian3':'jm','jian4':'jm','qian2':'qj',
                  'xian2':'xj','yan2':'yj','zhi1':'vi','zhi4':'vp','chi1':'ii','shi1':'ui',
                  'lv1':'fi','lv4':'fp','guan1':'gd','guang1':'gn','gui1':'gv',
                  'wan1':'wj','wan2':'wj','wan3':'wm','wan4':'wm','wan5':'wm',
                  'wang1':'wh','wang2':'wh','wang3':'wl','wang4':'wl','wang5':'wl'}
        assert all(mapping[p]==value for p,value in expected.items())
        assert "- 'derive/5$/1/'" in (generated/'chuiyi_1.schema.yaml').read_text(encoding='utf-8')
        fn('destroy_session',C.c_int,C.c_size_t)(sid)
        report={'method':'Local Rime engine; isolated compilation and user data; no installed scheme changes',
                'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'mapping_checks':len(mapping_checks),
                'inputs':{n:hashlib.sha256((generated/n).read_bytes()).hexdigest() for n in
                          ['chuiyi_1.schema.yaml','chuiyi_1.dict.yaml','chuiyi_dicts/chars.dict.yaml','chuiyi_dicts/base.dict.yaml']}}
        (generated/'engine-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:report[k] for k in ['passed','total','mapping_checks']},ensure_ascii=False))
        if report['passed']!=report['total']:
            print(json.dumps([c for c in checks if not c['passed']],ensure_ascii=False))
        assert report['passed']==report['total'], 'Some input checks failed'
    finally:
        fn('finalize',None)()

if __name__=='__main__':
    main()
