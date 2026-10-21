"""Reject device-identifying fields and private machine paths in release archives."""
import argparse,json,re,zipfile
from pathlib import Path

FORBIDDEN_FIELDS={'device','device_model','serial','serial_number','device_id','installation_id','username'}
def inspect_archive(path):
    findings=[]
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.endswith('/'):continue
            try:text=archive.read(name).decode('utf-8-sig')
            except UnicodeError:continue
            if re.search(r'[A-Za-z]:[\\/]Users[\\/](?![<%])[^\\/\s]+',text):
                findings.append((name,'private user path'))
            if name.endswith('.json'):
                try:value=json.loads(text)
                except ValueError:continue
                def walk(v):
                    if isinstance(v,dict):
                        for k,x in v.items():
                            if k in FORBIDDEN_FIELDS and x:
                                findings.append((name,'identifying metadata field'))
                            walk(x)
                    elif isinstance(v,list):
                        for x in v:walk(x)
                walk(value)
    return findings

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    args=parser.parse_args()
    errors=inspect_archive(args.archive)
    if errors:
        for path,category in errors:print(path+': '+category)
        raise SystemExit(1)
    print('Release privacy checks passed')
