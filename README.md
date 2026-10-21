# 吹衣带调拼音 1.1.1

每个汉字音节用两个字母输入，对部分韵母区分四声。设计：**吹衣OVO**。

## 下载与安装

**[下载 1.1.1 完整安装包](https://github.com/chuiyi0/rime-chuiyi/releases/download/v1.1.1/chuiyi_pinyin-1.1.1.zip)** · [版本发布页](https://github.com/chuiyi0/rime-chuiyi/releases/tag/v1.1.1)

安装包包含生成好的词库，无须 Python。绿色 **Code → Download ZIP** 下载的是开发源码。

1. 安装 Rime 客户端并备份用户文件夹。
2. 复制 `chuiyi_pinyin_1_1.schema.yaml`、`chuiyi_pinyin_1_1.dict.yaml` 和整个 `chuiyi_pinyin_1_1_dicts/` 到用户目录根部。
3. 在已有 `default.custom.yaml` 的 `patch.schema_list` 添加 `- schema: chuiyi_pinyin_1_1`，重新部署并选择 **吹衣带调拼音 1.1.1**。

[详细安装与升级](schemes/chuiyi_pinyin/INSTALL.md) · [入门教程](schemes/chuiyi_pinyin/TUTORIAL.md)

## 编码规则

| 韵母 | 一、二、三声及默认轻声 | 四声 |
|---|---|---|
| i | i | p |
| u / ü | w | u |
| e / ei / ie | e | y |
| an | j | m |

其他韵母：`ian→q；o/uo/ve→o；ai→d；a→a；ua/ia→x；in→b；ang→h；ing/uai→k；eng→g；ao→c；en→f；ong/iong→s；iu/ou→z；un→t；ui→v；uan→r；iao→n；iang/uang→l`。

声母通常不变，`zh/ch/sh→v/i/u`，零声母用 `o`，`y/w` 保留。

**特例：** `j/q/x+j/m` 对应 `jian/qian/xian`（四声用 m）；`lv` 用 `fe/fi`（四声用 fi）；`er` 与 `ri` 共用 `ri/rp`。

**轻声兼容仅针对双字词：** 词库把第二字标轻声时，允许该字使用其他声调对应编码；不把这项容错扩展到单字或三字以上词语。

| 输入编码 | 例字或词 |
|---|---|
| `le / lw / lu / ly` | 了 / 鲁 / 路 / 乐 |
| `jx / hx / tq / jm` | 家 / 花 / 天 / 建 |
| `fe / fi` | 吕 / 绿 |
| `vozi` 或 `vozp` | 桌子 |
| `yifw` 或 `yifu` | 衣服 |

候选可能因词频和多音字而同码，不保证固定排序。

## 文件导航

| 用途 | 入口 |
|---|---|
| 完整声韵编码矩阵 | [MATRIX.md](schemes/chuiyi_pinyin/MATRIX.md) |
| 逐音节与声调查询 | [mapping.tsv](schemes/chuiyi_pinyin/mapping.tsv) |
| 验证范围 | [TESTING.md](schemes/chuiyi_pinyin/TESTING.md) |
| 更新内容 | [1.1.1 更新记录](docs/releases/1.1.1.md) |
| 构建源码 | [DEVELOPMENT.md](DEVELOPMENT.md) |
| 历史方案和统计 | `schemes/chuiyi_1/`、`docs/research/` |

Windows 已进行本机 Rime 引擎测试，并由作者实际试用确认；Android 仍待实机验证。历史 2500 字统计针对旧编码，不作为 1.1.1 的冲突率结论。

[来源声明](NOTICE.md) · [GPL-3.0 许可证](LICENSE)
