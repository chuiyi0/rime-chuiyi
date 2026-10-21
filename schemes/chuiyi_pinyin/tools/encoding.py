"""Explicit 1.1.1 column matrix; lv is an independent override."""
COLUMNS = [('i', 'ip4', 'bi pi mi lv di ti ni li ji qi xi yi zhi chi shi ri er zi ci si'),
 ('u', 'wu4', 'bu pu mu fu du tu nu lu gu ku hu wu ju qu xu yu zhu chu shu ru zu cu su'),
 ('ü', 'wu4', 'nv'),
 ('e', 'ey4', 'me de te ne le ge ke he ye zhe che she re ze ce se e'),
 ('ei', 'ey4', 'bei pei mei fei dei tei nei lei gei kei hei wei zhei shei zei cei ei'),
 ('ie', 'ey4', 'bie pie mie die tie nie lie jie qie xie'),
 ('an', 'jm4', 'ban pan man fan dan tan nan lan gan kan han wan yan zhan chan shan ran zan can san an jian qian xian'),
 ('ian', 'q', 'bian pian mian dian tian nian lian'),
 ('o', 'o', 'bo po mo fo wo yo o lo'),
 ('ve', 'o', 'nve lve jue que xue yue'),
 ('uo', 'o', 'duo tuo nuo luo guo kuo huo zhuo chuo shuo ruo zuo cuo suo'),
 ('ai', 'd', 'bai pai mai dai tai nai lai gai kai hai wai zhai chai shai zai cai sai ai'),
 ('a', 'a', 'ba pa ma fa da ta na la ga ka ha wa ya zha cha sha za ca sa a'),
 ('ua', 'x', 'gua kua hua zhua shua rua chua'),
 ('ia', 'x', 'dia lia jia qia xia'),
 ('in', 'b', 'bin pin min nin lin jin qin xin yin'),
 ('ang', 'h', 'bang pang mang fang dang tang nang lang gang kang hang wang yang zhang chang shang rang zang cang sang ang'),
 ('ing', 'k', 'bing ping ming ding ting ning ling jing qing xing ying'),
 ('uai', 'k', 'guai kuai huai zhuai chuai shuai'),
 ('eng', 'g', 'beng peng meng feng deng teng neng leng geng keng heng weng zheng cheng sheng reng zeng ceng seng eng'),
 ('ao', 'c', 'bao pao mao dao tao nao lao gao kao hao yao zhao chao shao rao zao cao sao ao'),
 ('en', 'f', 'ben pen men fen den nen gen ken hen wen zhen chen shen ren zen cen sen en'),
 ('ong', 's', 'dong tong nong long gong kong hong jiong qiong xiong yong zhong chong rong zong cong song ong'),
 ('iu', 'z', 'miu diu niu liu jiu qiu xiu'),
 ('ou', 'z', 'pou mou fou dou tou nou lou gou kou hou you zhou chou shou rou zou cou sou ou'),
 ('un', 't', 'dun tun lun gun kun hun zhun chun shun run zun cun sun jun qun xun yun'),
 ('ui', 'v', 'dui tui gui kui hui zhui chui shui rui zui cui sui'),
 ('uan', 'r', 'duan tuan nuan luan guan kuan huan juan quan xuan yuan zhuan chuan shuan ruan zuan cuan suan'),
 ('iao', 'n', 'biao piao miao diao tiao niao liao jiao qiao xiao fiao'),
 ('iang', 'l', 'niang liang jiang qiang xiang biang'),
 ('uang', 'l', 'guang kuang huang zhuang chuang shuang')]

def initial(s):
    if s=='lv': return 'f'
    if s=='er': return 'r'
    for full, key in [('zh','v'),('ch','i'),('sh','u')]:
        if s.startswith(full): return key
    return s[0] if s[0] in 'bpmfdtnlgkhw jqxy rzcs'.replace(' ','') else 'o'

MATRIX={}
for final, spec, syllables in COLUMNS:
    for s in syllables.split():
        assert s not in MATRIX, s
        MATRIX[s]=(initial(s),final,spec)

def code(phone):
    s,t=phone[:-1],int(phone[-1])
    if t not in range(1,6): raise ValueError(phone)
    if s=="lv": return "f"+("i" if t==4 else "e")
    first,final,spec=MATRIX[s]
    if len(spec)==1: second=spec
    elif spec=='a1x': second='a' if t==1 else 'x'
    else: second=spec[1] if t==4 else spec[0]
    return first+second

def repeated_alias(word, phones):
    """Only neutral repetitions inherit preceding character's encoding/tone."""
    result=list(phones)
    if len(word)!=len(result): return tuple(result)
    for i in range(1,len(result)):
        if word[i]==word[i-1] and result[i].endswith('5'):
            result[i]=result[i-1]
    return tuple(result)

def neutral_aliases(word, phones):
    """Only two-character words with a neutral final syllable receive new readings."""
    if len(word)!=2 or len(phones)!=2 or not phones[1].endswith("5"): return ()
    return tuple((phones[0],phones[1][:-1]+str(t)) for t in range(1,5))
