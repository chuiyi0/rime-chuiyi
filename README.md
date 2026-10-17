# 吹衣 Rime 输入方案

## 吹衣带调双拼

吹衣带调双拼是由 **吹衣OVO** 原创设计、基于 Rime 的中文输入方案。

每个音节使用两个字母编码，并将高频韵母拆分。轻声同时兼容对应的一声和四声编码，词语保留本调与变调输入。

例如：

- `jpxt → ji4xu4 → 继续`
- `jixt → ji1xu4 → 积蓄`
- `wr → wo → 我`

注：第二个字母代表韵母，其中 i、o、p 分别代表 i 的 1/5、2/3、4/5 声（5 是轻声）。

词条与词频以雾凇拼音词库为基础，注音整理和程序实现由 GPT 协助完成。可用于小狼毫等 Rime 客户端，安卓同文输入法尚待实机验证。

项目开源，欢迎使用、修改和反馈问题，转载或分发时请保留作者署名、来源及适用许可证。

项目地址：[https://github.com/chuiyi0/rime-chuiyi](https://github.com/chuiyi0/rime-chuiyi)

[使用教程与完整编码表](schemes/chuiyi_1/TUTORIAL.md) · [安装说明](schemes/chuiyi_1/INSTALL.md) · [双字词无声调重码统计](schemes/chuiyi_1/TONE_COLLISION_STATS.md)

[D 方案声调分组与 2500 词近似统计](schemes/chuiyi_1/TONE_GROUP_D.md)：记录设计规则、可复现的词库统计及待实测项，不改变现行输入编码。

## 输入方案

| 方案 | 文件及说明 |
| --- | --- |
| 吹衣带调双拼（方案一） | [介绍与安装](schemes/chuiyi_1/README.md) |
| 吹衣方案一（并击实验） | [并击规则、示例与兼容性](schemes/chuiyi_1/CHORD_EXPERIMENT.md)；[实验 schema](schemes/chuiyi_1/chuiyi_1_chord.schema.yaml) |

每个方案放在独立目录，以后可继续添加其他方案。安装时只复制所选方案所需的文件。

[来源声明](NOTICE.md) · [GPL-3.0许可证](LICENSE)
