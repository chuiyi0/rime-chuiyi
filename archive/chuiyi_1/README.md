# 吹衣带调双拼

> 旧版归档。当前版本见[项目首页](../../README.md)。

吹衣带调双拼是由 **吹衣OVO** 原创设计、基于 Rime 的中文输入方案。

每个音节使用两个字母编码，并将高频韵母拆分。轻声同时兼容对应的一声和四声编码，词语保留本调与变调输入。

例如：

- `jpxt → ji4xu4 → 继续`
- `jixt → ji1xu4 → 积蓄`
- `wr → wo → 我`

注：第二个字母代表韵母，其中 i、o、p 分别代表 i 的 1/5、2/3、4/5 声（5 是轻声）。

词条与词频以雾凇拼音词库为基础，注音整理和程序实现由 GPT 协助完成。可用于小狼毫等 Rime 客户端，安卓同文输入法尚待实机验证。

项目开源，欢迎使用、修改和反馈问题，转载或分发时请保留作者署名、来源及适用许可证。

项目地址：[https://github.com/chuiyi0/rime-chuiyi](https://github.com/chuiyi0/rime-chuiyi)

[使用教程与编码表](TUTORIAL.md) · [安装说明](INSTALL.md) · [来源声明](NOTICE.md)


## 可选并击实验

标准版不启用并击。桌面并击实验版使用独立的 `chuiyi_1_chord.schema.yaml`，规则和兼容性说明见 [CHORD_EXPERIMENT.md](CHORD_EXPERIMENT.md)。

词库生成已改为优先采用 `kMandarin_8105.txt` / `kTGHZ2013.txt` 中可核验的单字读音，避免把宽泛拼音数据中的非标准扩展读音加入单字候选；更新词库后需重新部署。 例如，“家”在内置单字词库中现只保留 `jia1`，已移除导致 `jx` 出现“家”的 `jia4/jia5/jie5` 条目。
