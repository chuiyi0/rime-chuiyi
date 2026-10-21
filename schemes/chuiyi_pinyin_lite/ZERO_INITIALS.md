# 轻量版1.1.0零声母规则

按小鹤双拼方式处理零声母，所有声调共用编码。原 MATRIX.md 保留为原始记录，以下映射优先生效。

| 拼音 | 编码 |
| --- | --- |
| a | aa |
| e | ee |
| o | oo |
| ai | ai |
| ei | ei |
| ao | ao |
| ou | ou |
| an | an |
| en | en |
| er | er |
| ang | ah |
| eng | eg |
| ong | os |

y、w开头的拼音和其余带声母拼音保持原轻量版编码。er使用er，ri仍按原声调规则使用ri/rp。原oe/oy/oj等零声母编码不再保留为别名。

参考：https://github.com/rime/rime-double-pinyin/blob/master/double_pinyin_flypy.schema.yaml

为保留现有配置及学习记录，schema ID继续使用 chuiyi_pinyin_lite_1_0；显示名称及发布版本为1.1.0。
