# 吹衣输入法 · 12 套 Trime 皮肤

这是 **同文输入法 Trime 3.3.12** 的皮肤集合，配套吹衣带调拼音等方案。
十二套主题基于原有吹衣小米风键盘布局生成。键位、上滑、长按、分词及数字键盘均保留；新增的是色彩主题与候选区的宽松排版。

## 目录结构

```text
themes/trime/
├── light/                   # 浅色 · 5 套
│   ├── cy_01_cloud-white.trime.yaml    云瓷白
│   ├── cy_02_glacier-blue.trime.yaml   冰川蓝
│   ├── cy_03_cream-apricot.trime.yaml  奶杏
│   ├── cy_04_mint-tea.trime.yaml       薄荷茶
│   └── cy_09_paper-white.trime.yaml    清纸白
├── dark/                    # 深色 · 3 套
│   ├── cy_05_graphite.trime.yaml       石墨灰
│   ├── cy_06_deep-sea.trime.yaml       深海蓝
│   └── cy_08_obsidian.trime.yaml       黑曜夜
├── color/                   # 彩色 · 3 套
│   ├── cy_07_sakura.trime.yaml         樱花糖
│   ├── cy_10_dusk-purple.trime.yaml    暮光紫
│   └── cy_11_amber-paper.trime.yaml    琥珀纸
├── texture/                 # 通透风格 · 1 套
│   └── cy_12_mist-glass.trime.yaml     雾玻璃
├── showcase/
│   └── index.html           # 纯 HTML/CSS/JS，手机离线预览
├── manifest.json            # 12 套元数据
└── README.md                # 本文
```

> **说明**：「雾玻璃」是色彩、轮廓和轻柔层次的拟玻璃效果，并非 Android 真正实时背景模糊。

## 手机安装与选用

1. 将所需 `*.trime.yaml` 放进同文的 **shared / 共享主题目录**。该目录为扁平结构，不按 GitHub 的分类子文件夹存放。
2. 打开同文输入法，使用 **键盘样式** 菜单选择「吹衣 · 编号 主题名」。
3. 根据同文版本和配置，必要时在主界面点击 **部署**，以应用新皮肤。
4. 用相同的输入内容测试键位、上滑、长按、候选栏、数字键、符号键；出现问题可切回旧皮肤。

本次在 Redmi K70 上已直接安装的目录：

```text
/sdcard/Android/data/com.osfans.trime/files/shared/
```

手机离线预览文件：

```text
/sdcard/Download/Chuiyi_12_Themes.html
```

通过文件管理器打开该 HTML（使用浏览器）可先比较 12 套设计；也可用 GitHub 文件列表下载预览页。

## 排版统一规则

- 候选词字体：19。
- 候选词横向留白 `candidate_padding: 16`。
- 候选高度 `candidate_view_height: 42`。
- 按键宽松间距 `horizontal_gap: 6`、`vertical_gap: 11`。
- 数字布局：四行五列，键高 36，保留返回、删除与空格。
- **每行最多几个候选**由同文应用设置决定；`candidate_padding` 只影响候选视觉间距。
- 用户词库、编码文件和已启用方案均不在本皮肤项目中修改。

## 更新与校验

- 本仓库皮肤与手机上正在使用的皮肤分开命名，不覆盖原始主题。
- 主题更新后，要核对同文部署后的 build 文件，而不能仅凭 shared 源文件判断是否生效。
- 如遇间距、颜色未变化，可切换皮肤并重新部署，检查 build 中实际参数。
- 本次仅验证了主题 YAML 从原皮肤生成、保留键盘定义、ADB 传输与手机文件存在；**尚未逐套完成屏幕显示及手势操作验收**。

## 版权

源皮肤基于同文输入法及其 GPL-3.0 预设主题改编。保留原文件署名和许可要求；相关引用资源与字体仍受其原始许可约束。

## 配色专用版本：保持键盘不变

12 套主题**只允许更换配色及主题名称**。按键大小、按键数量、分词键、上滑与长按、数字键盘、候选间距、键盘总体高度均来自统一的 `base/chuiyi_layout_reference.trime.yaml`。

可在仓库根目录运行：

```bash
python themes/trime/tools/validate_palette_only.py
```

校验会逐套比对除主题名称与默认配色之外的全部 YAML 文本；如果任何主题意外改变了布局或按键定义，就会失败。

注意：网页版 `showcase/index.html` 的早期示意图用了不同的 CSS 尺寸，现在已按模板的键高 36、横向间距 6、行距 11、候选字体 19、候选高度 42 和底部留白 39 修正。不过 HTML 仍是视觉模拟，不是 Trime 的原生渲染器。实际机型的字体度量、屏幕缩放和应用设置可能产生细微差别。

## 2026-11-08 空输入工具栏与编辑键盘

12 套主题及 base 参考模板已统一加入 Trime 3.3.12 `tool_bar` 配置：

- 未输入编码时显示：菜单、编辑、剪贴板、表情、设置（具体顺序按同文从右向左的按钮布局）；输入编码时按 Trime 自身逻辑切换为候选栏。
- 编辑入口使用独立的 `editor` 键盘，支持全选、剪切、复制、粘贴、光标移动、删除和返回原键盘。
- 仍然保留原 `qwerty`、数字键盘、键高、间距、上滑、长按、候选间距及底部留白；颜色仅取当前主题的配色。
- 部署前先备份手机原皮肤。复制所需 `.trime.yaml` 到同文 shared 目录，选用该皮肤后按需重新部署。
- 安卓 `wxm` 等三码不出候选的问题不属于皮肤修复：另有 [安卓专用可选补丁](../../schemes/chuiyi_pinyin/android/README.md)，只安装在手机，不影响 Windows。
- 已做 12/12 套主题与 base 非配色内容一致性检查。**尚未在手机上完成工具栏按钮和三码候选的实机验收**。
