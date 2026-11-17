# 吹衣带调拼音 · 轻量版 1.1.0

**新手推荐版本。** 声调区分比常规版少，零声母和小鹤双拼一样，上手更快。

方案标识：`chuiyi_pinyin_lite_1_0`（为了保留已有用户的学习记录，标识沿用 1_0，显示名称是 1.1.0）

[下载 ZIP](https://github.com/chuiyi0/rime-chuiyi/releases/download/lite-v1.1.0/chuiyi-pinyin-lite-1.1.0.zip) · [安装](INSTALL.md) · [练习表](TUTORIAL.md) · [编码矩阵](MATRIX.md) · [零声母规则](ZERO_INITIALS.md) · [更新记录](RELEASE.md) · [返回首页](../../README.md)

## 规则

- 每个字按两个键：第一键是声母，第二键是韵母。`zh → v`，`ch → i`，`sh → u`。
- **只有三类韵母区分声调，而且只分「四声 / 非四声」：**

  | 韵母 | 非四声 | 四声 |
  |---|---|---|
  | i | `i` | `p` |
  | u | `w` | `u` |
  | e / ei / ie | `e` | `t` |

- 其他韵母不分声调，例如 un → `y`，iu → `q`，ou → `z`，an → `j`。完整对应见 [编码矩阵](MATRIX.md)。
- yan 的各个声调统一按 `yj`。
- 零声母照小鹤双拼：安 `an`，欧 `ou`，额 `ee`，昂 `ah`。见 [零声母规则](ZERO_INITIALS.md)。

## 例子

| 拼音 | 按键 | 拼音 | 按键 |
|---|---|---|---|
| yī（衣） | `yi` | yì（意） | `yp` |
| wú（无） | `ww` | wù（物） | `wu` |
| bēi（杯） | `be` | bèi（被） | `bt` |
| dùn（顿） | `dy` | liú（刘） | `lq` |
| lóu（楼） | `lz` | ōu（欧） | `ou` |

同一个编码可能对应好几个字，候选按词频排列。按 `[` / `]` 翻页，按空格选第一个，按数字键选其他候选。逐音节对照表见 `mapping.tsv`。

## 测试情况

已通过 Windows Rime 引擎 33 项抽查（yan 编码、t/y 对调、零声母、ju/jv 多码等），记录见 `windows-smoke.json`。安卓尚未完整实测。

## 来源

见 [NOTICE.md](NOTICE.md)。
