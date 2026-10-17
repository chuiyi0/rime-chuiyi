# 安装吹衣带调拼音

[下载 ZIP 安装包](https://github.com/chuiyi0/rime-chuiyi/releases/download/v1.0.0-dev/chuiyi_pinyin-1.0-dev.zip)，解压后安装。

以下步骤适用于 Windows 小狼毫。安装前先备份 Rime 用户文件夹。

## 1. 复制文件

右击小狼毫托盘图标，打开“用户文件夹”，把以下三项复制进去：

```text
chuiyi_pinyin.schema.yaml
chuiyi_pinyin.dict.yaml
chuiyi_pinyin_dicts/
```

两份 YAML 和词库文件夹应直接放在用户文件夹中。

## 2. 添加方案

如果没有 `default.custom.yaml`，新建这个文件，写入：

```yaml
patch:
  schema_list:
    - schema: chuiyi_pinyin
```

如果已经有这个文件，在现有的 `patch` → `schema_list` 列表中添加下面一行，保留原来的方案：

```yaml
    - schema: chuiyi_pinyin
```

## 3. 部署并选用

右击托盘图标，选择“重新部署”。完成后按 **Ctrl + `**（Tab 上方的反引号键），选择“吹衣带调拼音 1.0-dev”。

输入 `womf`（我们）、`mama`（妈妈）或 `jlxy`（继续），查看候选。

## 更新或停用

更新时替换上述文件，重新部署。保留个人用户词典和其他配置。

停用时切回原来的方案即可。若要从选单移除，在 `schema_list` 中删除 `chuiyi_pinyin` 这一项，再重新部署。
