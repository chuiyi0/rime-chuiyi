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
