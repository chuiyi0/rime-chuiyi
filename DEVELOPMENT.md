# 开发与打包

普通用户从[首页](README.md)下载完整ZIP。

Python 3，无第三方依赖。命令：python schemes/chuiyi_pinyin/tools/build.py

输出 dist/chuiyi_pinyin-1.2.zip；当前方案标识 chuiyi_pinyin_1_2，用户词库与旧版分开。

编码唯一来源是 schemes/chuiyi_pinyin/tools/encoding.py 中的显式行列矩阵。build.py 从固定旧版词库生成新schema、词库、mapping.tsv、MATRIX.md和validation.json，不改旧源文件。

生成时保留1.0已有词库读音，再仅为双字词末字轻声添加声调兼容；已明确的单字雷lei4另作修正，其他多音字不批量删除。

GitHub Actions在main的当前方案/工作流变化时生成并发布v1.2完整ZIP。Windows校验可运行tools/verify_windows.py（--library、--shared-data）；手机必须自行生成编译缓存，不把Windows缓存当安卓验收。

旧版本、历史统计不作为1.2性能结论。旧方案作为可复现来源保留。
