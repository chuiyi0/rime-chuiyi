# 吹衣带调拼音

吹衣OVO 设计的 Rime 中文输入方案。每个音节用两个字母输入，部分韵母按声调分组，用来区分“积蓄”和“继续”等同音词。

当前版本：**1.0-dev**，方案 ID：`chuiyi_pinyin`。

## 下载与安装

[下载 ZIP 安装包](https://github.com/chuiyi0/rime-chuiyi/releases/download/v1.0.0-dev/chuiyi_pinyin-1.0-dev.zip) · [版本发布页](https://github.com/chuiyi0/rime-chuiyi/releases/tag/v1.0.0-dev)

先安装 Rime 客户端，再按[安装说明](schemes/chuiyi_pinyin/INSTALL.md)添加方案。

## 输入示例

| 文字 | 编码 |
|---|---|
| 我 | `wo` |
| 我们 | `womf` |
| 积蓄 | `jixy` |
| 继续 | `jlxy` |
| 妈妈 | `mama` 或 `mamx` |
| 妹妹 | `mwmw` 或 `mwme` |

声母大多沿用拼音，`zh → v`、`ch → i`、`sh → u`；第二键表示韵母和声调组，不用输入声调数字。

[入门教程](schemes/chuiyi_pinyin/TUTORIAL.md) · [编码矩阵](schemes/chuiyi_pinyin/MATRIX.md) · [逐音节编码表](schemes/chuiyi_pinyin/mapping.tsv)

## 仓库目录

- [`schemes/chuiyi_pinyin/`](schemes/chuiyi_pinyin/)：当前方案、编码规则和生成工具。
- [`docs/`](docs/README.md)：开发验证记录和声调研究。
- [`archive/`](archive/README.md)：旧版方案、并击实验及原始词库。
- [`DEVELOPMENT.md`](DEVELOPMENT.md)：构建和打包方法。

反馈问题时，请附上想输入的字词、输入编码、实际候选及客户端版本。

编码设计：**吹衣OVO**；GPT 协助数据处理与程序实现。项目采用 [GPL-3.0](LICENSE)，词库来源及上游许可见 [NOTICE.md](NOTICE.md)。
