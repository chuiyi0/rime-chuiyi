# 验证状态

静态生成结果：415 个音节，2075 条声调映射，554366 条字词读法，增加 142 条重复字轻声别名。继承词库因未映射拼音而排除的行数为 0。

生成器独立断言 27 个重点映射，以及相同字轻声继承、连续重复字、不同字轻声不继承和爸爸/妈妈/妹妹别名存在。validation.json 记录来源哈希、重码清单、字词条数及示例编码。

Windows 当前输入法、Android 实机：尚未测试。远程电脑显示在线但请求未及时响应，未写入已安装输入法。

Rime 引擎测试：Linux librime 1.10.0 隔离部署、实际编译成功，26/26 项候选检查通过。包括常用词、重复字轻声默认码与兼容码、o/ou/er/ri、lv/nv/nve/lve/luo/jue，以及单字不全局增加轻声跨组别名的反向检查。详细结果及输入哈希见 engine-verification.json。

复现引擎验证（Linux，需自行安装 librime 开发包及默认资料）：

```text
python schemes/chuiyi_pinyin/tools/verify_engine.py --library /usr/lib/x86_64-linux-gnu/librime.so.1 --api-header /usr/include/rime_api.h --shared-data /usr/share/rime-data --deployer /usr/bin/rime_deployer
```

稀有拼音通过映射验证，不声称所有稀有读音都有词条或候选。实际候选测试使用现有词库覆盖的汉字。
