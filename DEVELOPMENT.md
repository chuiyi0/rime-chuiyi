# 源码开发与打包（给开发者）

> **普通使用者不需要看本页。** 直接返回[首页](README.md)下载已生成词库的 ZIP 安装包。

## 当前主推方案：吹衣带调拼音 1.0-dev

仓库根目录执行（Python 3，无额外构建依赖）：

```sh
python schemes/chuiyi_pinyin/tools/build.py
```

成功后得到 `dist/chuiyi_pinyin-1.0-dev.zip`。本方案源码依赖已提交的旧版基础词库，但不会覆盖旧版方案。输出 ZIP 内含 `chuiyi_pinyin.schema.yaml`、`chuiyi_pinyin.dict.yaml` 与 `chuiyi_pinyin_dicts/`，可复制到 Rime 用户目录安装。

如需更新对外下载包，仓库的 [GitHub Actions 打包发布工作流](.github/workflows/package-release.yml) 可通过 Actions → “生成并发布吹衣带调拼音安装包” → Run workflow 手动触发。发布到预发行标签 `v1.0.0-dev`；其 ZIP 是普通用户应下载的文件。

## 旧版：吹衣方案一

旧版 `chuiyi_1` 是另一套编码，请勿混装或覆盖新方案：

```sh
python schemes/chuiyi_1/tools/build.py
```

旧版原始输入与基线在 `schemes/chuiyi_1/sources/`，生成工具在 `schemes/chuiyi_1/tools/`。新方案独立文件位于 `schemes/chuiyi_pinyin/`；二者使用不同方案 ID。

## 文件整理原则

- **不要手动修改自动生成的 `mapping.tsv` 和矩阵等内容后忘记同步源代码**；生成规则在 `tools/encoding.py`。
- `docs/research/` 存研究文档，**不影响构建和输入法运行**。
- 旧版原文件保留，避免破坏依赖和正在使用它的用户。
- 提交到 GitHub 的源码不是完整的安装包；不要让普通用户必须自己运行 Python。

统计资料：[2500 字声调与冲突分析](docs/research/tone-2500.md)。
