# 开发与打包

在仓库根目录使用 Python 3 执行：

```sh
python schemes/chuiyi_pinyin/tools/build.py
```

输出为 `dist/chuiyi_pinyin-1.0-dev.zip`，包含方案、词库、安装说明和许可声明。

## 文件与依赖

- `schemes/chuiyi_pinyin/tools/encoding.py`：当前编码矩阵和重复字轻声规则。
- `archive/chuiyi_1/chuiyi_dicts/`：已提交的基础词库；当前方案仍以它为输入。
- `archive/chuiyi_1/chuiyi_1.schema.yaml`：生成当前方案时使用的基础配置。
- `mapping.tsv`、`MATRIX.md`、`validation.json` 及当前方案 YAML 由构建脚本生成；修改规则后重新构建。

旧版原始数据和工具保留在 `archive/chuiyi_1/`，用于追溯和重新生成基础词库。构建当前方案不需要运行旧版生成器。

引擎验证命令及历史结果见 [验证记录](docs/testing/README.md)。

## 自动发布

[打包工作流](.github/workflows/package-release.yml)在构建输入变更并合入 `main` 后生成 ZIP，更新 `v1.0.0-dev` 预发行版。也可以在 Actions 中手动运行“生成并发布吹衣带调拼音安装包”。

安装包按明确的文件清单打包；开发脚本、统计资料、测试报告及本地缓存留在源码仓库。
