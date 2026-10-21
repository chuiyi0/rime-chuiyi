# 安装与升级：吹衣带调拼音 1.2

[下载完整 ZIP](https://github.com/chuiyi0/rime-chuiyi/releases/download/v1.2/chuiyi_pinyin-1.2.zip)。这是 Rime 方案，不是独立 EXE/APK；先备份用户文件夹。

## Windows 小狼毫

1. 复制 chuiyi_pinyin_1_2.schema.yaml、chuiyi_pinyin_1_2.dict.yaml 和整个 chuiyi_pinyin_1_2_dicts 文件夹到 Rime 用户目录根部。
2. 在已有 default.custom.yaml 的 patch.schema_list 中添加新标识。只使用本方案时的最小配置：

```yaml
patch:
  schema_list:
    - schema: chuiyi_pinyin_1_2
```

已有其他方案时请合并，不要重复创建 patch。

3. 重新部署并选择“吹衣带调拼音 1.2”。测试 lo→离/理、lp→力、go→简、gp→建、vxzi/vxzo/vxzp→桌子。

## 从旧版升级

1.2 使用独立标识 chuiyi_pinyin_1_2 和用户词库，避免旧读音或旧测试词频干扰。确认新版可用后，从列表移除不需要的旧吹衣方案；旧用户数据建议先备份。

若仍显示旧规则，确认方案名为1.2并重新启动客户端。回退时恢复备份，不必覆盖或删除其他输入法的数据。

## Android 同文 / 中州韵

通过客户端设置查找用户资料目录或导入入口，复制同样三项内容并添加同一标识；用客户端的“部署”重新生成数据并选择1.2。用户目录随客户端版本变化，不假定固定目录。

此包不带 APK、皮肤或个人用户数据，也不修改键盘布局。手机编译缓存应由手机本机生成，不使用 Windows 编译文件覆盖。
