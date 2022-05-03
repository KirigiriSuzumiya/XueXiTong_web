# XueXiTong
学习通泛雅课程刷课工具。使用selenium+python，破解了最近更新的测试复制乱码。能够自动进行视频播放与章节测试搜题、提交。



**求星~**



## 功能

1. 尔雅通识刷视频。 支持暂停自动继续、屏蔽视频中弹出题目，窗口可最小化

2. 章节测试。 支持破解测试复制乱码问题并使用CodFrm大神的题库（现有的总是最全的）

   

## 鸣谢

1. 测试复制乱码

   解决方法来源：[【新】【非OCR识别】学习通破解章节测试文字乱码思路-油猴中文网 (tampermonkey.net.cn)](https://bbs.tampermonkey.net.cn/thread-2190-1-1.html)

2. 题库

   https://cx.icodef.com/query.html

   使用了CodFrm大神插件中的网页版搜题功能

   [CodFrm/cxmooc-tools: 一个 超星(学习通)/智慧树(知到)/中国大学mooc 学习工具,火狐,谷歌,油猴支持.全自动任务,视频倍速秒过,作业考试题库,验证码自动打码(੧ᐛ੭挂科模式,启动) (github.com)](https://github.com/CodFrm/cxmooc-tools)



## 环境

python3及以上

selenium库

```python
#selenium安装
pip install selenium
```

chromedriver.exe这是谷歌浏览器驱动，我上传的版本是101.0.4951.41。

版本不对的话可以自己去[chromedriver.storage.googleapis.com/index.html](http://chromedriver.storage.googleapis.com/index.html)下个对的

## 使用

XueXiTong_web.py文件头部有三个变量

```python
# 配置所刷课程的url和学习通的用户名密码

url = ''
username = ''
password = ''

# 以下是执行部分
```

1. url

   **旧版** 超星网页网址。建议自己打开课程页面后复制

   示例：

   ![网页捕获_3-5-2022_15181_mooc1.chaoxing.com](新建 文本文档 (2).assets/网页捕获_3-5-2022_15181_mooc1.chaoxing.com.jpeg)

2. username

   你的学习通用户名（手机号）

3. password

   你的学习通密码

**修改完成后直接运行就行，有什么问题看看命令行输出卡在哪里了。**