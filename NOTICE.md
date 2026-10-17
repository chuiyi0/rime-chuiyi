# 署名与来源

吹衣各方案的原创编码设计：吹衣OVO。词库整理与程序实现由GPT协助完成。

本项目新增程序及方案配置采用GPL-3.0；使用、修改和传播时保留署名、来源和许可声明，分发修改版本时遵守相应源码提供条件。上游独立材料保留原有许可。

- [雾凇拼音](https://github.com/iDvel/rime-ice)：单字、基础词条及词频；上游GPL-3.0。此项目修改了注音、编码映射与文件组织。
- [pinyin-data](https://github.com/mozillazg/pinyin-data)：单字注音和常用字音；版本 `9193766130af24d2ac54230be979b2e98ac66223`，上游仓库MIT。
- [phrase-pinyin-data](https://github.com/mozillazg/phrase-pinyin-data)：词组注音；本地数据版本0.19.0，上游仓库MIT。

上游许可证见 `LICENSES/`。原始词库文件头保留其详细来源。拼音汇总资料还涉及Unihan、汉典、CC-CEDICT等来源；上游仓库的MIT声明不取代这些来源的适用声明。当前仍需补齐相关数据声明，尚不能把本页当作全部来源许可均已核清的结论。

当前 `chuiyi_pinyin` 方案继承 `archive/chuiyi_1/chuiyi_dicts/` 的单字、基础词库及原词频，按新矩阵映射编码，并增加重复字轻声的词组兼容读法。输入文件 SHA-256 见 `schemes/chuiyi_pinyin/validation.json`。未接入雾凇 ext/tencent 扩展词库。

旧版 `chuiyi_1` 的编码、轻声兼容规则及生成来源保留在 `archive/chuiyi_1/`。
