"""Chuiyi scheme 1 mapping, confirmed by the author on 2026-10-17."""
import re

GROUPS = {
    'i':'iop', 'u':'uyt', 'v':'uyt',
    'e':'ewq', 'ei':'ewq', 'ie':'ewq',
    'an':'jm', 'ian':'jm', 'ao':'c',
    'ing':'gk', 'uai':'gk', 'eng':'gk',
    'in':'f', 'en':'f', 'ang':'hl', 'iang':'hl',
    'a':'ax', 'ua':'ax', 'ia':'ax', 'o':'r', 'uo':'r',
    'ong':'s', 'iong':'s', 'iu':'z', 'ou':'z', 'un':'b',
    'ai':'d', 'uan':'d', 'iao':'n', 'uang':'n', 'ui':'v',
}
Y_FINALS = {'i':'i','u':'u','e':'e','an':'an','ao':'ao','ing':'ing',
            'in':'in','ang':'ang','a':'a','o':'o','ue':'uo','ong':'ong',
            'ou':'ou','un':'un','uan':'uan'}
W_FINALS = {'u':'u','ei':'ei','eng':'eng','en':'en','a':'a','o':'o',
            'ai':'ai','an':'an','ang':'ang'}

def code(phone):
    syllable, tone = phone[:-1], int(phone[-1])
    if syllable == 'lv':
        first, final = 'f', 'i'
    elif syllable == 'o':
        first, final = 'r', 'o'
    elif syllable == 'er':
        first, final = 'o', 'o'
    elif syllable.startswith('y'):
        first, final = 'y', Y_FINALS[syllable[1:]]
    elif syllable.startswith('w'):
        first, final = 'w', W_FINALS[syllable[1:]]
    else:
        m = re.match(r'^(zh|ch|sh|[bpmfdtnlgkhjqxrzcs])(.+)$',syllable)
        if m:
            initial, final = m.groups()
            first = {'zh':'v','ch':'i','sh':'u'}.get(initial,initial)
            if final == 've':
                final = 'o'
            elif initial in {'j','q','x'} and final == 'ue':
                final = 'uo'
        else:
            first, final = 'o', syllable
    keys = GROUPS[final]
    if len(keys) == 3:
        second = keys[0] if tone == 1 else keys[1] if tone in {2,3} else keys[2]
    elif len(keys) == 2:
        second = keys[0] if tone in {1,2} else keys[1]
    else:
        second = keys
    return first + second

def update_schema(text):
    pattern = r"(?m)^\s*-\s*'xform/\^([a-z]+[1-5])\$/([a-z]{2})/'\s*$"
    phones = [m[0] for m in re.findall(pattern,text)]
    assert len(phones)==len(set(phones))==2040
    lines = ["    # Neutral tone accepts both tone-1 and tone-4 codes.",
             "    - 'derive/5$/1/'"]
    lines += [f"    - 'xform/^{p}$/{code(p)}/'" for p in sorted(phones)]
    start = text.index('  algebra:\n') + len('  algebra:\n')
    end = text.index('\ntranslator:',start)
    text = text[:start]+'\n'.join(lines)+'\n'+text[end:]
    return re.sub(r'(?m)^(\s*version:)\s*[^\n]+',r'\1 "0.5.0-dev"',text,count=1)
