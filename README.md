# 吹衣带调拼音 · Rime 中文输入方案

**每个汉字音节用两个字母输入；对最值得区分的声调做有限分组，减少常见重码。**

设计：**吹衣OVO** · 当前主推：**吹衣带调拼音 1.0-dev** · Rime 方案 ID：`chuiyi_pinyin`（开发版）

## 📦 下载（第一次来请从这里开始）

**[⬇️ 下载吹衣带调拼音 1.0-dev 完整安装 ZIP](https://github.com/chuiyi0/rime-chuiyi/releases/download/v1.0.0-dev/chuiyi_pinyin-1.0-dev.zip)**

[查看版本发布页](https://github.com/chuiyi0/rime-chuiyi/releases/tag/v1.0.0-dev) ｜ [全部发布版本](https://github.com/chuiyi0/rime-chuiyi/releases)

> 请下载上面的 **`chuiyi_pinyin-1.0-dev.zip` 安装包**，里面有生成好的词库，**不需要 Python**。GitHub 的绿色 **Code → Download ZIP** 下载的是**开发源码**，不等于可直接安装的完整词库包。
>
> 若版本发布仍在自动生成中、下载链接暂时找不到文件，可先看[源码生成办法](DEVELOPMENT.md)，不要把源码 ZIP 当安装包。

## 🚀 安装，只需三步

本项目是 **Rime 输入方案，不是独立 APK 或 EXE**。请先安装 Rime 客户端，例如 Windows 小狼毫、Android 中州韵／同文。

1. **下载并解压完整安装 ZIP**。
2. 把下面三项放进 **Rime 用户文件夹的根目录**（不是新建一个子文件夹）：
   - `chuiyi_pinyin.schema.yaml`
   - `chuiyi_pinyin.dict.yaml`
   - 整个 `chuiyi_pinyin_dicts` 文件夹
3. 在你现有的 `default.custom.yaml` 的 `patch.schema_list` **保留原有方案，追加** `- schema: chuiyi_pinyin`，然后**重新部署**并选择“吹衣带调拼音 1.0-dev”。

✅ **[Windows 详细安装与回退](schemes/chuiyi_pinyin/INSTALL.md)** ｜ **[Android 导入注意事项](schemes/chuiyi_pinyin/INSTALL.md#android-中州韵--同文rime-客户端)**

> 安装前备份原 Rime 配置，不要删除原有词典与用户数据。Android 实机仍需验证；遇到问题请注明客户端版本与输入编码。

## ⌨️ 试试打字

| 输入文字 | 键入编码 | 说明 |
|---|---|---|
| 我 | `wo` | 单字两键 |
| 我们 | `womf` | 两音节直接相连 |
| 积蓄 | `jixy` | 第一字 jī |
| 继续 | `jlxy` | 第一字 jì |
| 妈妈 | `mama` 或 `mamx` | 已收录重叠词兼容轻声 |
| 妹妹 | `mwmw` 或 `mwme` | 同上 |

基本规则：大部分声母直接沿用，`zh → v`、`ch → i`、`sh → u`；第二键表示韵母，并对少部分韵母区分声调组，**不用输入声调数字**。

## 📚 教程、编码与数据（按用途找）

| 我想做什么 | 打开这个文件 |
|---|---|
| 5 分钟了解规则 | **[图文入门教程](schemes/chuiyi_pinyin/TUTORIAL.md)** |
| 查询某个韵母的编码 | **[完整编码矩阵](schemes/chuiyi_pinyin/MATRIX.md)** |
| 查找所有拼音 → 两字母映射 | [逐音节映射表（TSV）](schemes/chuiyi_pinyin/mapping.tsv) |
| 看 2500 常用字声调分布与编码冲突数据 | **[2500 字分析报告](docs/research/tone-2500.md)** |
| 查看作者最初的统计数据 | [原始声调比例表](docs/research/original-tone-table.md) |
| 遇到问题或想参与开发 | [测试记录](schemes/chuiyi_pinyin/TESTING.md) · [生成源码的方法](DEVELOPMENT.md) |
| 安卓同文输入法深色键盘与三选一长按 | **[Trime 手机主题（0.1 测试版）](trime/themes/chuiyi_sogou_xiaomi_dark/README.md)** |

**这次统计的重点**：2500 字样本下，在静态单字归并模型中，选择性声调编码相较不分声调减少约 **31.9%** 的同码字对；这不是实际打字速度或候选命中率的百分比。数据来源与假设都写在[研究报告](docs/research/tone-2500.md)中。

## 🗂️ 仓库文件怎么找？

```text
README.md                        ← 从这里开始：下载 / 安装 / 教程
docs/research/                    ← 声调统计、分析资料
schemes/chuiyi_pinyin/           ← 当前 1.0-dev 方案（源码、规则、测试）
schemes/chuiyi_1/                ← 旧版「吹衣方案一」及并击实验（保留）
trime/themes/                   ← 同文输入法安卓键盘皮肤（与编码方案分开）
.github/workflows/               ← 生成可直接安装的版本 ZIP
DEVELOPMENT.md                    ← 开发者如何从源码打包
```

旧版**不是**当前推荐下载： [旧版介绍](schemes/chuiyi_1/README.md) ｜ [并击实验](schemes/chuiyi_1/CHORD_EXPERIMENT.md) ｜ [旧版声调研究](schemes/chuiyi_1/TONE_COLLISION_STATS.md)。

> **待开发，不是现有功能**：当第二个汉字通过并击输入时直接上屏。见[统计与功能规划](docs/research/tone-2500.md#7-保留的待办并击直接上屏)。

## 作者、版权及来源

编码原创设计：**吹衣OVO**；GPT 协助数据处理、代码与文档。项目开发版欢迎反馈，问题请带上想输入的字词、编码、实际候选以及 Rime 客户端。

[依赖与来源声明](NOTICE.md) · [GPL-3.0 许可证](LICENSE)
