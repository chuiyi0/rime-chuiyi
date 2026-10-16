# 生成方案文件

需要Python 3，无额外依赖，在仓库目录运行：

```text
python schemes/chuiyi_1/tools/build.py
```

原始输入和基线放在该方案的 `sources/`，生成程序放在 `tools/`。

新增方案时使用单独目录和唯一的方案、词典、用户词典名称，例如 `schemes/chuiyi_2/`；不要覆盖方案一。各方案独立生成和安装，不要求同时启用。
