# 开发与打包

普通用户请从[首页](README.md)下载完整 ZIP。

在仓库根目录运行（Python 3，无第三方依赖）：

```sh
python schemes/chuiyi_pinyin/tools/build.py
```

得到 dist/chuiyi_pinyin-1.1.1.zip。包内只含当前方案、生成词库、说明与许可证。

编码规则在 schemes/chuiyi_pinyin/tools/encoding.py；build.py 生成方案代数、mapping.tsv、MATRIX.md、词库及验证报告。运行标识 chuiyi_pinyin_1_1 沿用 1.1，本次显示版本是 1.1.1。

基础词库来自已提交的 schemes/chuiyi_1/chuiyi_dicts，构建不修改旧文件。先重建 1.0 已存在的读音，再为“双字词第二音节轻声”补充兼容读音，不给其他词条增加此规则。

GitHub Actions 在 main 的方案或发布工作流变化时构建、校验并发布 v1.1.1，也可手动触发。

历史研究在 docs/research，不作为新版性能结论。旧方案作为可复现来源保留，不是推荐下载。
