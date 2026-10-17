# 吹衣带调拼音

**每个拼音音节两个字母，高频音节用声调区分编码。**

吹衣带调拼音是由 **吹衣OVO** 原创设计、基于 Rime 的中文输入方案。它希望在缩短拼音编码的同时，区分“继续／积蓄”这类无调拼音相同、声调不同的词。

当前版本：**1.0-dev（开发版）** · 方案 ID：`chuiyi_pinyin`

**[介绍与入门教程](schemes/chuiyi_pinyin/TUTORIAL.md) · [完整编码表](schemes/chuiyi_pinyin/MATRIX.md) · [安装说明](schemes/chuiyi_pinyin/INSTALL.md)**

## 输入示例

| 想输入 | 编码 | 说明 |
| --- | --- | --- |
| 我 | `wo` | 一个音节，两键 |
| 我们 | `womf` | 词语编码连续输入 |
| 继续 | `jlxy` | jì xù |
| 积蓄 | `jixy` | jī xù；与“继续”区分 |

输入后查看候选，空格选择第一项，数字键选择对应候选。候选顺序会受词频和个人学习记录影响。

## 编码怎么记？

- **第一键通常表示声母**：大多保留拼音首字母；`zh → v`、`ch → i`、`sh → u`，零声母通常用 `o`。
- **第二键表示韵母及声调组**：例如 i 韵母的一、二、三声和轻声用 `i`，第四声用 `l`，所以 `jī → ji`、`jì → jl`。
- 有些韵母共用键位，有些不区分声调。具体以[完整编码表](schemes/chuiyi_pinyin/MATRIX.md)为准，**输入时不需要附加声调数字**。

普通轻声使用默认组。词库中已处理的重复字轻声词，可以重复前一个字的编码，也保留默认轻声编码，例如“妈妈”支持 `mama` 和 `mamx`。未收录的新造词暂不保证自动具有这种兼容码。

## 开始使用

这是一套 **Rime 输入方案**，需要先安装 Rime 客户端：Windows 用小狼毫，Android 使用支持 Rime 方案的中州韵／同文客户端。

**已有 ZIP 安装包：**

1. 解压后，将两份 `chuiyi_pinyin` YAML 文件和整个 `chuiyi_pinyin_dicts` 文件夹复制到 Rime 用户目录。
2. 在方案列表中加入 `chuiyi_pinyin`，保留原有方案，再重新部署。
3. 在方案选单选择 **“吹衣带调拼音 1.0-dev”**，试打 `mama`、`mwmw`、`jlxy`。

配置示例与手机导入步骤见[详细安装说明](schemes/chuiyi_pinyin/INSTALL.md)。安装前先备份配置。

**如果下载的是 GitHub 源码：**

仓库不重复保存新版生成词库，不能只复制两份 YAML。请先在完整仓库根目录用 Python 3 运行：

```text
python schemes/chuiyi_pinyin/tools/build.py
```

生成好的安装包位于 `dist/chuiyi_pinyin-1.0-dev.zip`。也可以向作者索取已经生成的 ZIP 安装包。

## 当前进展

- 新编码矩阵、声调分组和重复字轻声兼容规则已实现。
- 词条与词频继承本仓库的雾凇基础词库整理结果；尚未扩充为雾凇全量 ext/tencent。
- Linux 与作者 Windows 本机 Rime 引擎候选测试均为 **26/26 通过**；Windows 已安装并重新部署。
- 当前仍是开发版，桌面实际键入体验欢迎反馈；**Android 实机尚待验证**。

[查看测试记录](schemes/chuiyi_pinyin/TESTING.md) · [技术说明与生成方法](schemes/chuiyi_pinyin/README.md)

反馈问题时，请提供：**想输入的字词、实际按下的编码、出现的候选，以及使用的客户端。**

## 旧版与实验方案

旧版编码与新版不同，请按所选方案查看对应教程。

| 方案 | 入口 |
| --- | --- |
| 吹衣方案一／旧版带调双拼（`chuiyi_1`） | [方案介绍](schemes/chuiyi_1/README.md) · [旧版教程](schemes/chuiyi_1/TUTORIAL.md) · [安装说明](schemes/chuiyi_1/INSTALL.md) |
| 吹衣方案一（并击实验） | [实验说明](schemes/chuiyi_1/CHORD_EXPERIMENT.md) |

旧版相关资料：[双字词无声调重码统计](schemes/chuiyi_1/TONE_COLLISION_STATS.md) · [D 方案声调分组与统计](schemes/chuiyi_1/TONE_GROUP_D.md)

## 作者与许可

编码设计：**吹衣OVO**。GPT 协助注音整理、程序实现与检查。

项目开源，欢迎使用、修改和反馈。转载或分发时请保留作者署名、来源及适用许可证。

[来源声明](NOTICE.md) · [GPL-3.0 许可证](LICENSE)
