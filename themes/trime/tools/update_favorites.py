# Update ONLY the favorite-theme buttons in Trime skin files.
# Edit favorite_themes.json, then run: python update_favorites.py
# Supports 0..8 pinned themes. This does not modify the keyboard layout.
from pathlib import Path
import json
import re
import subprocess
from datetime import datetime

ROOT=Path(__file__).resolve().parent
IDS=["07","02","04","06","03","10","08","11","01","05","09","12"]
INFO={
 "01":("☁ 云瓷白","吹衣 · 01 云瓷白","0xffc4d4ec","0xff31475d"),
 "02":("💎 冰川蓝","吹衣 · 02 冰川蓝","0xff62aeef","0xff092949"),
 "03":("🍑 奶杏","吹衣 · 03 奶杏","0xffffab78","0xff573021"),
 "04":("🍃 薄荷茶","吹衣 · 04 薄荷茶","0xff6ac8a5","0xff12372f"),
 "05":("🪨 石墨灰","吹衣 · 05 石墨灰","0xff4b5360","0xffe9f0f8"),
 "06":("🌊 深海蓝","吹衣 · 06 深海蓝","0xff287ca6","0xfff3fdff"),
 "07":("🌸 樱花糖","吹衣 · 07 樱花糖","0xffed659a","0xffffffff"),
 "08":("🌌 黑曜夜","吹衣 · 08 黑曜夜","0xff4a4a75","0xfff4ebff"),
 "09":("📄 清纸白","吹衣 · 09 清纸白","0xffe9e9ee","0xff3b4555"),
 "10":("💜 暮光紫","吹衣 · 10 暮光紫","0xff9970cb","0xffffffff"),
 "11":("✨ 琥珀纸","吹衣 · 11 琥珀纸","0xffffc35a","0xff62401a"),
 "12":("🫧 雾玻璃","吹衣 · 12 雾玻璃","0xffb5bbef","0xff34395b"),
}
favorite=json.loads((ROOT/"favorite_themes.json").read_text(encoding="utf-8"))["favorites"]
if len(favorite)>8 or len(favorite)!=len(set(favorite)) or any(x not in INFO for x in favorite):
 raise ValueError("favorites must be 0..8 unique IDs from 01..12")

actions=""
for j,k in enumerate(favorite):
 label,name,color,fg=INFO[k]
 actions+=f'  cy_fav_{j}: '+'{label: '+json.dumps(label,ensure_ascii=False)+', send: FUNCTION, command: set_theme, option: '+json.dumps(name,ensure_ascii=False)+'}\n'

head='''  themes:
    name: "吹衣彩色主题"
    ascii_mode: 0
    columns: 10
    width: 25
    height: 36
    lock: true
    keys:
'''
for j in range(8):
 if j>=len(favorite):head+='      - {width: 25}\n'
 else:
  label,name,color,fg=INFO[favorite[j]]
  head+=f'      - {{click: cy_fav_{j}, label: '+json.dumps(label,ensure_ascii=False)+f', width: 25, key_back_color: {color}, key_text_color: {fg}, key_border_color: {color}'+'}\n'
head+='''      - {click: cy_back, label: "← 返回", width: 25}
      - {click: Theme_settings, label: "全部主题", width: 25}
      - {click: Color_settings, label: "当前配色", width: 25}
      - {click: cy_theme_58, label: "原版键盘", width: 25}
      - {click: cy_back, width: 16, label: "返回"}
      - {click: cy_numbers, width: 14, label: "123"}
      - {click: ",", width: 9.75, label: "，"}
      - {click: space, width: 24, label: "吹衣拼音"}
      - {click: ".", width: 9.75, label: "。"}
      - {click: Mode_switch, width: 11, label: "中/英"}
      - {click: Return, width: 15.5, label: "↵"}
'''
names=["chuiyi_sogou_58mm_toolbar.trime.yaml"]+[f"cy_{i:02d}_{n}.trime.yaml" for i,n in enumerate([
 "cloud-white","glacier-blue","cream-apricot","mint-tea","graphite","deep-sea",
 "sakura","obsidian","paper-white","dusk-purple","amber-paper","mist-glass"],1)]
shared="/sdcard/Android/data/com.osfans.trime/files/shared/"
back=ROOT/"favorite_backup"/datetime.now().strftime("%Y%m%d_%H%M%S")
patch=ROOT/"favorite_patched"
back.mkdir(parents=True,exist_ok=True);patch.mkdir(parents=True,exist_ok=True)
uploads=[]
for name in names:
 original=back/name
 subprocess.run(["adb","pull",shared+name,str(original)],check=True,stdout=subprocess.DEVNULL)
 s=original.read_text(encoding="utf-8-sig")
 s,n=re.subn(r'(?m)^(  Keyboard_themes:.*\n)(?:  cy_fav_\d+:.*\n)*(?=  cy_theme_58:)',lambda m:m.group(1)+actions,s)
 if n!=1:raise RuntimeError(f"Cannot locate favorites keys in {name}")
 begin=s.index("  themes:\n")
 end=s.index("  us_intl:\n",begin)
 s=s[:begin]+head+s[end:]
 # Bump the real Rime config version so the updated favorites are compiled.
 rows=s.splitlines(keepends=True)
 for i,row in enumerate(rows):
  if row.startswith("config_version: "):
   parts=row.split(":",1)[1].strip().strip('"').split(".")
   rows[i]=f'config_version: "{int(parts[0])}.{int(parts[1])+1}"\n'
   break
 else:
  raise RuntimeError(f"Missing config_version in {name}")
 s="".join(rows)
 dest=patch/name
 dest.write_text(s,encoding="utf-8",newline="\n")
 uploads.append((name,dest))
# Syntax-check all skins BEFORE any adb push.
validator=Path(r"C:\Users\chuiyi\AppData\Local\npm-cache\_npx\4b4c857f6efdfb61\node_modules\js-yaml\index.js")
if not validator.is_file():
 raise RuntimeError("YAML validator is unavailable; refused to modify phone.")
js="const fs=require('fs'),yaml=require("+json.dumps(str(validator))+");yaml.load(fs.readFileSync(process.argv[1],'utf8'));"
for _,item in uploads:
 subprocess.run(["node","-e",js,str(item)],check=True,stdout=subprocess.DEVNULL)
print("YAML_OK",len(uploads))
print("PLAN_READY",len(favorite),"favorites in",len(uploads),"skins")
for name,local in uploads:
 subprocess.run(["adb","push",str(local),shared+name],check=True,stdout=subprocess.DEVNULL)
print("UPDATED",len(uploads),"skins. On phone go to Keyboard Style > Theme; switch to a different theme and back. Deploy alone may not refresh the active theme.")