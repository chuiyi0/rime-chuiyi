# 吹衣带调拼音

一套基于 [Rime（中州韵）](https://rime.im) 的**带调双拼**输入方案。设计：**吹衣OVO**。

- **双拼**：每个字固定按两个键，第一个键是声母，第二个键是韵母。
- **带调**：第二个键还能区分一部分声调，同音字因此少了很多，想要的字更容易排在前面。

比如「继续」和「积蓄」拼音都是 ji xu，在全拼里候选会混在一起。在吹衣带调拼音里：

| 词 | 拼音 | 按键 |
|---|---|---|
| 继续 | jì xù | `jpxu` |
| 积蓄 | jī xù | `jixu` |

`ji` 和 `jp` 的区别就在声调：一声按 `i`，四声按 `p`。

支持 Windows（小狼毫 Weasel）和安卓（同文输入法 Trime），也能用在其他 Rime 客户端上。

## 选哪个版本

两个版本都在维护，可以同时安装，随时切换。

| | 轻量版 1.1.0 | 常规版 1.3 |
|---|---|---|
| 适合谁 | **新手首选**，尤其是用过小鹤双拼的人 | 想让候选更准、愿意多记几条规则的人 |
| 声调区分 | 少：大多数韵母只分「四声 / 非四声」 | 多：i 韵母分成一声、二三声、四声三组 |
| 零声母（爱、安、欧…） | 和小鹤双拼一样：`ai`、`an`、`ou` | 统一用 `o` 开头：`od`、`oj`、`oz` |
| 学习负担 | 低 | 中 |
| 方案标识 | `chuiyi_pinyin_lite_1_0` | `chuiyi_pinyin_1_3` |

不知道选哪个就先装**轻量版**。

## 下载

ZIP 里已经包含生成好的词库，解压即可使用，**不需要安装 Python**。

- **轻量版 1.1.0**：[下载 ZIP](https://github.com/chuiyi0/rime-chuiyi/releases/download/lite-v1.1.0/chuiyi-pinyin-lite-1.1.0.zip) · [发布说明](https://github.com/chuiyi0/rime-chuiyi/releases/tag/lite-v1.1.0)
- **常规版 1.3**：[下载 ZIP](https://github.com/chuiyi0/rime-chuiyi/releases/download/v1.3/chuiyi_pinyin-1.3.zip) · [发布说明](https://github.com/chuiyi0/rime-chuiyi/releases/tag/v1.3)

> 页面上绿色的 **Code → Download ZIP** 下载的是开发源码，词库不完整，普通用户请用上面的链接。

## 安装（三步）

以下以常规版为例。装轻量版时，把文件名和方案标识换成 `chuiyi_pinyin_lite_1_0`。

**1. 复制文件。** 把 ZIP 里的这三样放进 Rime 用户文件夹：

- `chuiyi_pinyin_1_3.schema.yaml`（方案）
- `chuiyi_pinyin_1_3.dict.yaml`（词库入口）
- 整个 `chuiyi_pinyin_1_3_dicts` 文件夹（词库本体）

用户文件夹在哪：

- **Windows 小狼毫**：右键任务栏的小狼毫图标 →「用户文件夹」。
- **安卓同文**：在同文设置里找到用户目录，一般是 `rime` 文件夹。不同版本的位置可能不一样。

**2. 加入方案列表。** 打开用户文件夹里的 `default.custom.yaml`（没有就新建一个），在 `schema_list` 里加一行：

```yaml
patch:
  schema_list:
    - schema: chuiyi_pinyin_1_3        # 常规版
    - schema: chuiyi_pinyin_lite_1_0   # 轻量版（两个都要就都写上）
```

如果文件里已经有 `schema_list`，只把这一行加进去，不要再写一个 `patch:`。

**3. 重新部署。** 小狼毫：右键图标 →「重新部署」；同文：设置里点「部署」。部署完按 ``Ctrl+` `` 或 `F4` 切换到「吹衣带调拼音」。

想检查有没有装好，可以试打这几个：

| 按键 | 轻量版 | 常规版 1.3 |
|---|---|---|
| 「我们」 | `womf` | `wxmf` |
| 「被」 | `bt` | `bt` |
| 「顿」 | `dy` | `dy` |
| 「力」 | `lp` | `lp` |

更详细的步骤（含从旧版升级）：[常规版安装](schemes/chuiyi_pinyin/INSTALL.md) · [轻量版安装](schemes/chuiyi_pinyin_lite/INSTALL.md)

## 编码规则速查

每个字两个键：**第一键 = 声母，第二键 = 韵母（部分带声调）**。

声母基本照拼音按，有三个例外：`zh → v`，`ch → i`，`sh → u`。

### 两个版本相同的部分

- **e / ei / ie**：四声按 `t`，其他声调按 `e`。例：杯 `be`，被 `bt`，姐 `je`，借 `jt`。
- **u**：四声按 `u`，其他声调按 `w`。例：鲁 `lw`，路 `lu`。
- **un 按 `y`**（和小鹤双拼一样）。例：顿 `dy`，论 `ly`，准 `vy`。
- 常用韵母键：`an → j`，`ang → h`，`ing → k`，`eng → g`，`ao → c`，`en → f`，`ong → s`，`ou → z`，`ui → v`，`uan → r`，`iao → n`，`iang / uang → l`。

### 轻量版的特点

- **i**：四声按 `p`，其他声调按 `i`。例：衣 `yi`，意 `yp`。
- `iu → q`，`ia / ua → x`，`o / uo / ve → o`，`in → b`，`ian → m`。
- 零声母照小鹤双拼：安 `an`，欧 `ou`，额 `ee`，昂 `ah`。

完整表格：[轻量版编码矩阵](schemes/chuiyi_pinyin_lite/MATRIX.md) · [零声母规则](schemes/chuiyi_pinyin_lite/ZERO_INITIALS.md) · [练习表](schemes/chuiyi_pinyin_lite/TUTORIAL.md)

### 常规版 1.3 的特点

- **i 分三组**：一声和轻声按 `i`，二、三声按 `o`，四声按 `p`。例：衣 `yi`，移 / 以 `yo`，意 `yp`；离 / 理 `lo`，力 `lp`。
- `ian → m`，`ai / ia → d`，`in / ua → b`，`o / uo / ve → x`，`iu / ou → z`。
- **jian / qian / xian / yan** 分别借 `g / k / h / w` 行的 i 组：间 `gi`，简 `go`，建 `gp`。
- 零声母统一用 `o` 开头：安 `oj`，爱 `od`，欧 `oz`。
- 双字词的第二个字是轻声时，按任何声调都能打出来：桌子 `vxzi`、`vxzo`、`vxzp` 都行。

完整表格：[常规版编码矩阵](schemes/chuiyi_pinyin/MATRIX.md) · [入门练习](schemes/chuiyi_pinyin/TUTORIAL.md) · [逐音节对照表](schemes/chuiyi_pinyin/mapping.tsv)

## 安卓皮肤

为同文输入法 3.3.12 做了 12 套配色皮肤（浅色、深色、彩色、雾玻璃），键盘布局统一，只换颜色。

[皮肤说明与安装](themes/trime/README.md) · [预览页](themes/trime/showcase/index.html)（下载后用浏览器打开）

## 仓库里有什么

| 位置 | 内容 |
|---|---|
| `schemes/chuiyi_pinyin_lite/` | 轻量版：方案、编码表、打包脚本 |
| `schemes/chuiyi_pinyin/` | 常规版：方案、编码表、打包脚本、测试记录 |
| `schemes/chuiyi_1/` | 最早的「吹衣带调双拼」，已停止更新；常规版的词库从这里生成，所以保留 |
| `themes/trime/` | 同文输入法皮肤 |
| `docs/releases/` | 各版本更新记录 |
| `docs/research/` | 早期声调分组的统计研究 |
| `docs/archive/` | 旧版本的测试报告 |

想自己改编码、重新打包：见 [开发与打包](DEVELOPMENT.md)。

## 反馈

遇到打不出的字、候选不对，欢迎到 [Issues](https://github.com/chuiyi0/rime-chuiyi/issues) 反馈。请写上：用的哪个版本、输入的按键、想要的字、实际出现的候选。

## 署名与许可

- 编码设计：吹衣OVO。程序实现与文档整理由 AI（GPT、Claude）协助完成。
- 词条和词频基于 [雾凇拼音](https://github.com/iDvel/rime-ice)（GPL-3.0），注音参考 [pinyin-data](https://github.com/mozillazg/pinyin-data) 和 [phrase-pinyin-data](https://github.com/mozillazg/phrase-pinyin-data)（MIT）。
- 本项目采用 [GPL-3.0](LICENSE) 许可。转载、修改、分发时请保留作者署名、来源和许可证。详见 [来源声明](NOTICE.md)。
