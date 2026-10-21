# 吹衣带调拼音 1.2 入门

每音节两字母，多音节直接相连，不输入声调数字。

左侧第一列是声母编码、第二列是声母；上方第一行是韵母编码、下面一行是韵母。按单元格所在行列取码。空表头继承左侧最近非空表头的完整规则。

**iop4：i=一声，o=二三声，p=四声，轻声默认 i。** wu4 和 ey4 仍只有四声使用第二字母。其他单字母列不分调。

an→j；ian→m；o/ve/uo→x；ai/ia→d；a→a；in/ua→b。其他列见[完整矩阵](MATRIX.md)。

jian/qian/xian/yan 分别按 g/k/h/w 行 i 列取码；lv 使用 fi/fo/fp，旧 fe/fi 特例不再适用；er 与 ri 共用 ri/ro/rp。

双字词第二音节在词库标轻声时，可输入该音节任意声调对应的编码。桌子 vxzi/vxzo/vxzp 均可，单字轻声默认用一声组；不会为单字或三字以上词语新增这项容错。

练习：离 lo，力 lp，简 go，建 gp，家 jd，花 hb，天 tm，我们 wxmf，衣服 yifw/yifu。雷只保留 lei2 → le。

[完整规则与下载](../../README.md) · [逐音节表](mapping.tsv) · [安装](INSTALL.md)
