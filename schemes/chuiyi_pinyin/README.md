# 吹衣带调拼音 · 常规版 1.3

方案标识：`chuiyi_pinyin_1_3`

[返回首页](../../README.md) · [安装](INSTALL.md) · [入门练习](TUTORIAL.md) · [编码矩阵](MATRIX.md) · [逐音节对照表](mapping.tsv) · [测试记录](TESTING.md) · [更新记录](../../docs/releases/1.3.md)

## 这个文件夹里有什么

| 文件 | 说明 |
|---|---|
| `chuiyi_pinyin_1_3.schema.yaml` | 方案文件（由脚本生成） |
| `chuiyi_pinyin_1_3.dict.yaml` | 词库入口（由脚本生成） |
| `MATRIX.md` / `mapping.tsv` | 编码表：表格版 / 逐音节版（由脚本生成） |
| `validation.json` | 打包时的自动检查结果 |
| `engine-verification.json` | 用真实 Rime 引擎编译并试打的结果 |
| `tools/encoding.py` | **编码规则的唯一来源**，改键位只改这里 |
| `tools/build.py` | 生成词库并打包 ZIP |
| `tools/verify_engine.py` / `verify_windows.py` | 用 Rime 引擎验证（Linux / Windows） |
| `android/` | 安卓可选补丁：只打一个首字母时也能出候选 |

词库 `chuiyi_pinyin_1_3_dicts/` 体积较大，不放进仓库，运行 `build.py` 时生成，也包含在发布的 ZIP 里。
