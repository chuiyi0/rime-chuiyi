# 安装

将以下文件放进Rime用户目录，保留文件夹结构；替换同名文件前先备份。

```text
chuiyi_1.schema.yaml
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
```

Windows小狼毫和安卓同文输入法使用同一套文件。安卓需按客户端设置导入用户目录，尚未实机验证。

更新时替换以上文件并重新部署，保留个人用户词典。
