# 吹衣带调拼音 1.2

每个汉字音节用两个字母输入。设计：**吹衣OVO**。

## 下载与安装
提供两个版本
**常规版本：[下载 1.2 完整安装包](https://github.com/chuiyi0/rime-chuiyi/releases/download/v1.2/chuiyi_pinyin-1.2.zip)** · [发布页](https://github.com/chuiyi0/rime-chuiyi/releases/tag/v1.2)
**轻量学习负担版：[下载吹衣带调拼音轻量版 1.1.0](https://github.com/chuiyi0/rime-chuiyi/releases/download/lite-v1.1.0/chuiyi-pinyin-lite-1.1.0.zip)** · [轻量版发布说明](https://github.com/chuiyi0/rime-chuiyi/releases/tag/lite-v1.1.0)
ZIP 包含生成好的词库。绿色 Code → Download ZIP 是开发源码。

将以下文件放入 Rime 用户目录
- `chuiyi_pinyin_1_2.schema.yaml`
- `chuiyi_pinyin_1_2.dict.yaml`
- 整个 `chuiyi_pinyin_1_2_dicts/`

在 `default.custom.yaml` 中的 `patch.schema_list`添加
- `- schema: chuiyi_pinyin_1_2`，重新部署并选择 **吹衣带调拼音 1.2**。

[详细安装](schemes/chuiyi_pinyin/INSTALL.md) · [入门](schemes/chuiyi_pinyin/TUTORIAL.md)

## 声调分组

| 韵母 | 一声 | 二、三声 | 四声 | 默认轻声 |
|---|---|---|---|---|
| i | i | o | p | i |
| u / ü | w | w | u | w |
| e / ei / ie | e | e | y | e |

其他韵母：`an→j；ian→m；o/ve/uo→x；ai/ia→d；a→a；in/ua→b；ang→h；ing/uai→k；eng→g；ao→c；en→f；ong/iong→s；iu/ou→z；un→t；ui→v；uan→r；iao→n；iang/uang→l`。

声母通常不变，`zh/ch/sh→v/i/u`，零声母用 `o`，`y/w` 保留。

## 按表格位置取码

`jian/qian/xian/yan` 放在 **g/k/h/w 行、i 列**，分别使用 `gi/go/gp、ki/ko/kp、hi/ho/hp、wi/wo/wp`。`lv` 在 f 行 i 列，使用 `fi/fo/fp`，取代旧版 fe/fi 特例。`er` 与 `ri` 共用 `ri/ro/rp`。

**轻声兼容仅针对双字词第二字：** 词库第二音节标轻声时，允许使用其他声调编码；i 列可用 i/o/p。单字轻声仍使用默认一声组，不把此项新增容错扩展到单字或三字以上词语。

| 编码 | 例字或词 |
|---|---|
| `li / lo / lp` | 一声及轻声 / 离、理 / 力 |
| `le / lw / lu / ly` | 了 / 鲁 / 路 / 乐 |
| `gi / go / gp` | 间 / 简 / 建 |
| `jd / hb / tm` | 家 / 花 / 天 |
| `fo / fp` | 吕 / 绿 |
| `vxzi / vxzo / vxzp` | 桌子 |
| `yifw / yifu` | 衣服 |
| `wxmf` | 我们 |

例字只说明读音编码，候选可能因词频和多音字而同码。“雷”单字仅保留常用 lei2（le），去掉额外 lei4；未批量删除其他多音字。

## 文件导航

[完整编码矩阵](schemes/chuiyi_pinyin/MATRIX.md) · [逐音节编码](schemes/chuiyi_pinyin/mapping.tsv) · [测试记录](schemes/chuiyi_pinyin/TESTING.md) · [更新记录](docs/releases/1.2.md) · [开发与打包](DEVELOPMENT.md)

旧方案保存在 schemes/chuiyi_1，作为可复现词库来源；历史统计在 docs/research，不作为 1.2 性能结论。

[来源声明](NOTICE.md) · [GPL-3.0 许可证](LICENSE)

## 验证状态

Windows：45项检查通过，覆盖467组单字编码和8,999条字音对应。同文3.3.12已本机编译，2,075条映射与电脑一致；手机实际候选请试打确认。详见[Windows测试](schemes/chuiyi_pinyin/windows-engine-verification.json)和[手机部署记录](schemes/chuiyi_pinyin/android-verification.json)。
