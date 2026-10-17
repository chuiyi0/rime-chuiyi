"""Author's explicit 2026-10-17 matrix; blanks never invent syllables."""
# final label, key specification, explicit populated cells
COLUMNS = [
('i','il4','bi pi mi lv di ti ni li ji qi xi yi zhi chi shi ri er zi ci si'),
('u','uy4','bu pu mu fu du tu nu lu gu ku hu wu ju qu xu yu zhu chu shu ru zu cu su'),
('ü','uy4','nv'),
('e','ew4','me de te ne le ge ke he ye zhe che she re ze ce se e'),
('ei','ew4','bei pei mei fei dei tei nei lei gei kei hei wei zhei shei zei cei ei'),
('ie','ew4','bie pie mie die tie nie lie jie qie xie'),
('ian','jm4','bian pian mian dian tian nian lian jian qian xian'),
('an','jm4','ban pan man fan dan tan nan lan gan kan han wan yan zhan chan shan ran zan can san an'),
('o','op4','bo po mo fo nve lve wo yo o lo'),
('uo','op4','duo tuo nuo luo guo kuo huo jue que xue yue zhuo chuo shuo ruo zuo cuo suo'),
('ai','dq4','bai pai mai dai tai nai lai gai kai hai wai zhai chai shai zai cai sai ai'),
('vn','dq4','jun qun xun yun'),
('a','a1x','ba pa ma fa da ta na la ga ka ha wa ya zha cha sha za ca sa a'),
('ia','a1x','dia lia jia qia xia'),
('in','b','bin pin min nin lin jin qin xin yin'),
('ua','b','gua kua hua zhua shua rua chua'),
('ang','h','bang pang mang fang dang tang nang lang gang kang hang wang yang zhang chang shang rang zang cang sang ang'),
('iang','h','niang liang jiang qiang xiang biang'),
('ing','k','bing ping ming ding ting ning ling jing qing xing ying'),
('uai','k','guai kuai huai zhuai chuai shuai'),
('eng','g','beng peng meng feng deng teng neng leng geng keng heng weng zheng cheng sheng reng zeng ceng seng eng'),
('ao','c','bao pao mao dao tao nao lao gao kao hao yao zhao chao shao rao zao cao sao ao'),
('en','f','ben pen men fen den nen gen ken hen wen zhen chen shen ren zen cen sen en'),
('ong','s','dong tong nong long gong kong hong jiong qiong xiong yong zhong chong rong zong cong song ong'),
('iu','z','miu diu niu liu jiu qiu xiu'),
('ou','z','pou mou fou dou tou nou lou gou kou hou you zhou chou shou rou zou cou sou ou'),
('un','t','dun tun lun gun kun hun zhun chun shun run zun cun sun'),
('ui','v','dui tui gui kui hui zhui chui shui rui zui cui sui'),
('uan','r','duan tuan nuan luan guan kuan huan juan quan xuan yuan zhuan chuan shuan ruan zuan cuan suan'),
('iao','n','biao piao miao diao tiao niao liao jiao qiao xiao fiao'),
('uang','n','guang kuang huang zhuang chuang shuang'),
]

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
