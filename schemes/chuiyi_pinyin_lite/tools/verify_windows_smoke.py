"""Twenty native Windows Rime samples; no changes to installed input methods."""
import argparse,ctypes as C,hashlib,json,os,shutil
from pathlib import Path
from encoding import load_matrix
ROOT=Path(__file__).resolve().parents[1]
ID='chuiyi_pinyin_lite_1_0'
class Traits(C.Structure):
    _fields_=[('size',C.c_int)]+[(n,C.c_char_p) for n in ['shared','user','distribution_name','distribution_code','distribution_version','app']]+[('modules',C.POINTER(C.c_char_p)),('min_log_level',C.c_int),('log_dir',C.c_char_p),('prebuilt',C.c_char_p),('staging',C.c_char_p)]
class Candidate(C.Structure):
    _fields_=[('text',C.c_char_p),('comment',C.c_char_p),('reserved',C.c_void_p)]
class Iterator(C.Structure):
    _fields_=[('ptr',C.c_void_p),('index',C.c_int),('candidate',Candidate)]
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--library',type=Path,required=True)
    ap.add_argument('--shared-data',type=Path,required=True)
    ap.add_argument('--workdir',type=Path,required=True)
    args=ap.parse_args();box=args.workdir.resolve();box.mkdir(parents=True,exist_ok=True)
    for name in [ID+'.schema.yaml',ID+'.dict.yaml']:shutil.copy2(ROOT/name,box/name)
    shutil.copytree(ROOT/(ID+'_dicts'),box/(ID+'_dicts'),dirs_exist_ok=True)
    dll_dir=os.add_dll_directory(str(args.library.resolve().parent));dll=C.CDLL(str(args.library.resolve()))
    def fn(name,result,*types):
        f=getattr(dll,'Rime'+''.join(x.title() for x in name.split('_')));f.restype=result;f.argtypes=list(types);return f
    t=Traits();t.size=C.sizeof(t)-4;t.shared=str(args.shared_data.resolve()).encode();t.user=str(box).encode();t.app=b'rime.lite.smoke';t.min_log_level=2
    fn('setup',None,C.POINTER(Traits))(C.byref(t));fn('initialize',None,C.POINTER(Traits))(C.byref(t));fn('deployer_initialize',None,C.POINTER(Traits))(C.byref(t))
    checks=[]
    try:
        assert fn('deploy_config_file',C.c_int,C.c_char_p,C.c_char_p)(b'default.yaml',b'config_version')
        assert fn('deploy_schema',C.c_int,C.c_char_p)(str(box/(ID+'.schema.yaml')).encode())
        sid=fn('create_session',C.c_size_t)();assert fn('select_schema',C.c_int,C.c_size_t,C.c_char_p)(sid,ID.encode())
        fn('set_option',None,C.c_size_t,C.c_char_p,C.c_int)(sid,b'ascii_mode',0)
        mapping=load_matrix()['mapping']
        cases=[('的','de5',None),('我','wo3',None),('你','ni3',None),('一','yi1',None),('意','yi4',None),('五','wu3',None),('物','wu4',None),('北','bei3',None),('被','bei4',None),('而','er2',None),('二','er4',None),('女','nv3',None),('绿','lv4',None),('决','jue2',None),('句','ju4',None),('句','ju4','jv'),('下','xia4',None),('我们','wo3 men5',None),('中国','zhong1 guo2',None),('需要','xu1 yao4',None)]
        for word,phones,override in cases:
            keys=override or ''.join(mapping[p] for p in phones.split())
            fn('clear_composition',None,C.c_size_t)(sid)
            for char in keys:fn('process_key',C.c_int,C.c_size_t,C.c_int,C.c_int)(sid,ord(char),0)
            iterator=Iterator();rank=None
            if fn('candidate_list_begin',C.c_int,C.c_size_t,C.POINTER(Iterator))(sid,C.byref(iterator)):
                for i in range(10000):
                    if not fn('candidate_list_next',C.c_int,C.POINTER(Iterator))(C.byref(iterator)):break
                    if iterator.candidate.text.decode()==word:rank=i+1;break
                fn('candidate_list_end',None,C.POINTER(Iterator))(C.byref(iterator))
            checks.append({'word':word,'phones':phones,'code':keys,'rank':rank,'passed':rank is not None})
        inputs=[ROOT/(ID+'.schema.yaml'),ROOT/(ID+'.dict.yaml'),*sorted((ROOT/(ID+'_dicts')).glob('*.dict.yaml'))]
        report={'version':'1.0.0','method':'native Windows librime, isolated data, twenty candidate samples','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
        (ROOT/'windows-smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,ensure_ascii=True),flush=True);assert report['passed']==report['total']
    finally:fn('finalize',None)()
if __name__=='__main__':main()
