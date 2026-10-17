# 吹衣带调拼音 1.0-dev

作者：吹衣OVO。独立方案 ID：`chuiyi_pinyin`。旧版 `chuiyi_1` 保留原名与文件。

每个音节两个字母；本版按作者 2026-10-17 的新矩阵生成。开发版不代表 Windows、Android 实机验证已完成。

## 声调规则

| 表头 | 默认键：1、2、3、5 | 四声键 |
|---|---|---|
| il4 | i | l |
| uy4 | u | y |
| ew4 | e | w |
| jm4 | j | m |
| op4 | o | p |
| dq4 | d | q |

`a1x`：一声用 a，2、3、4、5 声用 x。单字母列所有声调共用该键。数字是设计注释，不是实际按键。空白表头继承左侧组，数据格空白不产生音节。

- `lv → fi / fl` 是特例，保留在 f 行。
- `nve / nuo`、`lve / luo / lo` 共组；`jue / que / xue / yue` 沿用 uo 列规则。
- `o → oo / op`；`er / ri → ri / rl`；`ou → oz`，ou 本来就在矩阵中。
- 已加入 `biang、cei、fiao、kei、rua、chua、lo` 的映射。映射存在不等于词库中一定有相应汉字；稀有字取决于继承词库覆盖，本版不凭空编造读音词条。
- 其余所有映射见 [矩阵](MATRIX.md) 和 [逐声调映射](mapping.tsv)。共组产生的不同拼音重码见 [验证报告](validation.json) 的 `cross_syllable_collisions`，属于矩阵明确指定的合并。

## 轻声

普通轻声只使用默认组，不全局兼容四声或一声。词库中相邻汉字相同且后字为轻声时，增加沿用前字编码的词组别名，保留原来的默认轻声读法。

| 词语 | 默认编码 | 重复字兼容编码 |
|---|---|---|
| 爸爸 ba4 ba5 | bxbx | bxbx（原本相同） |
| 妈妈 ma1 ma5 | mamx | mama |
| 妹妹 mei4 mei5 | mwme | mwmw |
| 我们 wo3 men5 | womf | 不增加别名 |

只增加词组读法，不增加单字变调读法。已有词库里的词组变调读法继续保留。新造词或用户词典中未处理的重复词，不保证自动具有该兼容码；重新生成词库时会处理已收录词条。

本次增加 142 条重复字轻声兼容读法。词条和词频复用仓库现有 chars/base，未扩充为雾凇全量 ext/tencent。用户词典、prism、词典名称均与旧方案隔离。

[安装步骤](INSTALL.md) · [测试说明](TESTING.md) · [来源与许可](NOTICE.md)

## 可复现生成

在完整仓库根目录运行：

```text
python schemes/chuiyi_pinyin/tools/build.py
```

使用旧方案已提交的词库作输入，输出新方案及 `dist/chuiyi_pinyin-1.0-dev.zip`。不运行旧版生成器，不改旧版文件，不访问本地已安装输入法。需 Python 3；引擎验证额外需要 PyYAML 与 librime。
