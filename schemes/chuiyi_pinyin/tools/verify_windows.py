"""Compile and query librime in an isolated directory (Windows; no installed user data)."""
import argparse,ctypes as C,hashlib,json,re,shutil,os
from pathlib import Path
from encoding import code
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--library',required=True,type=Path)
    ap.add_argument('--shared-data',required=True,type=Path)
    args=ap.parse_args()
    box=ROOT/'local-validation';box.mkdir(exist_ok=True)
    for name in ['chuiyi_pinyin.schema.yaml','chuiyi_pinyin.dict.yaml']:shutil.copy2(ROOT/name,box/name)
    shutil.copytree(ROOT/'chuiyi_pinyin_dicts',box/'chuiyi_pinyin_dicts',dirs_exist_ok=True)
    class Traits(C.Structure):
        _fields_=[('data_size',C.c_int)]+[(n,C.c_char_p) for n in ['shared_data_dir','user_data_dir','distribution_name','distribution_code_name','distribution_version','app_name']]+[('modules',C.POINTER(C.c_char_p)),('min_log_level',C.c_int),('log_dir',C.c_char_p),('prebuilt_data_dir',C.c_char_p),('staging_dir',C.c_char_p)]
    class Candidate(C.Structure):_fields_=[('text',C.c_char_p),('comment',C.c_char_p),('reserved',C.c_void_p)]
    class Iterator(C.Structure):_fields_=[('ptr',C.c_void_p),('index',C.c_int),('candidate',Candidate)]
    dll_dir=os.add_dll_directory(str(args.library.resolve().parent))
    dll=C.CDLL(str(args.library.resolve()))
    def fn(name,result,*types):
        symbol='Rime'+''.join(part.title() for part in name.split('_'))
        function=getattr(dll,symbol)
        function.restype=result;function.argtypes=list(types)
        return function
    traits=Traits();traits.data_size=C.sizeof(Traits)-C.sizeof(C.c_int)
    traits.shared_data_dir=str(args.shared_data.resolve()).encode();traits.user_data_dir=str(box.resolve()).encode()
    traits.app_name=b'rime.chuiyi_pinyin_validation';traits.min_log_level=2;traits.log_dir=str(box.resolve()).encode()
    fn('setup',None,C.POINTER(Traits))(C.byref(traits));fn('initialize',None,C.POINTER(Traits))(C.byref(traits))
    fn('deployer_initialize',None,C.POINTER(Traits))(C.byref(traits))
    checks=[]
    try:
        assert fn('deploy_config_file',C.c_int,C.c_char_p,C.c_char_p)(b'default.yaml',b'config_version')
        assert fn('deploy_schema',C.c_int,C.c_char_p)(str((box/'chuiyi_pinyin.schema.yaml').resolve()).encode('utf-8'))
        sid=fn('create_session',C.c_size_t)();assert sid
        assert fn('select_schema',C.c_int,C.c_size_t,C.c_char_p)(sid,b'chuiyi_pinyin')
        fn('set_option',None,C.c_size_t,C.c_char_p,C.c_int)(sid,b'ascii_mode',0)
        def rank(keys,word):
            fn('clear_composition',None,C.c_size_t)(sid)
            for k in keys:fn('process_key',C.c_int,C.c_size_t,C.c_int,C.c_int)(sid,ord(k),0)
            it=Iterator();found=None
            if fn('candidate_list_begin',C.c_int,C.c_size_t,C.POINTER(Iterator))(sid,C.byref(it)):
                n=0
                while fn('candidate_list_next',C.c_int,C.POINTER(Iterator))(C.byref(it)):
                    n+=1
                    if it.candidate.text.decode()==word:found=n;break
                    if n>=10000:break
                fn('candidate_list_end',None,C.POINTER(Iterator))(C.byref(it))
            return found
        cases=[('我','wo3'),('你','ni3'),('我们','wo3 men5'),('中国','zhong1 guo2'),('继续','ji4 xu4'),('积蓄','ji1 xu4'),('爸爸','ba4 ba5'),('爸爸','ba4 ba4'),('妈妈','ma1 ma5'),('妈妈','ma1 ma1'),('妹妹','mei4 mei5'),('妹妹','mei4 mei4'),('欧','ou1'),('偶','ou3'),('而','er2'),('二','er4'),('日','ri4'),('绿','lv4'),('女','nv3'),('虐','nve4'),('略','lve4'),('落','luo4'),('觉','jue2'),('哦','o2')]
        for w,p in cases:
            keys=''.join(code(x) for x in p.split());r=rank(keys,w)
            checks.append({'word':w,'phones':p,'code':keys,'rank':r,'passed':r is not None})
        # Neutral default group must not globally introduce tone-4 aliases.
        for w,keys in [('妈','mx'),('妹','me')]:
            r=rank(keys,w);checks.append({'word':w,'code':keys,'expected':'absent','rank':r,'passed':r is None})
        fn('destroy_session',C.c_int,C.c_size_t)(sid)
        files=[ROOT/'chuiyi_pinyin.schema.yaml',ROOT/'chuiyi_pinyin.dict.yaml',*sorted((ROOT/'chuiyi_pinyin_dicts').glob('*.dict.yaml'))]
        report={'method':'Windows installed librime; isolated data; actual schema compilation and candidate enumeration','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'windows_live_test':False,'windows_installed_engine_test':True,'android_device_test':False}
        (ROOT.parents[1]/'docs/testing/windows-engine-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False,indent=2))
        assert report['passed']==report['total']
    finally:fn('finalize',None)()
if __name__=='__main__':main()

