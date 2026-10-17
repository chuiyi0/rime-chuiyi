# 安装

将以下文件放进Rime用户目录，保留文件夹结构；替换同名文件前先备份。

```text
chuiyi_1.schema.yaml
chuiyi_1_chord.schema.yaml  # 可选：桌面并击实验版
chuiyi_1.dict.yaml
chuiyi_dicts/
  chars.dict.yaml
  base.dict.yaml
```

在客户端方案设置中启用“吹衣方案一”，重新部署后选用。

也可以在已有 `default.custom.yaml` 的 `patch` 下合并以下配置：

```yaml
patch:
  "schema_list/+":
    - schema: chuiyi_1
    - schema: chuiyi_1_chord  # 可选：复制了实验 schema 后再添加
```

标准版可用于 Windows 小狼毫和安卓同文输入法；安卓尚未实机验证。并击实验版请额外复制 `chuiyi_1_chord.schema.yaml`，优先在 Windows 小狼毫测试。手机端如无法并击，请继续使用标准版。

更新时替换以上文件并重新部署，保留个人用户词典。
