#python爬取QQ音乐(网易云需要API,我还没爬过)某个歌手的全部专辑歌曲歌词并生成词云图片
> 背景:最近因为想做一个py项目,由于非常喜欢周杰伦的歌,了解到python适合做词云,从而产生了用py生成歌手所有专辑的歌中的歌词的词云.

#程序功能
- 获取某个歌手的QQ音乐的专辑歌曲歌词(除了周杰伦以外,其他歌手的歌曲歌词等可自行爬取)
- 生成歌词云图片

#工作原理
    1. F12找到数据接口,调用并且用正则获取json格式的数据.
	2. 获取本地的所有歌词,清洗干净那些特殊字符,然后用jieba分词,最后通过WordCloud输出.
	3. 最终在本地生成相应词云
#运行:
配好环境,修改好路径以后,运行wordc.py文件即可,词云图片保存在pictures文件夹下,可以自己修改文件夹路径.

效果图

项目图:
![image](https://github.com/29DCH/Word_Cloud/blob/master/pictures/jaychou/3.png)

专辑:
![image](https://github.com/29DCH/Word_Cloud/blob/master/pictures/jaychou/1.png)

歌词:
![image](https://github.com/29DCH/Word_Cloud/blob/master/pictures/jaychou/2.png)
![image](https://github.com/29DCH/Word_Cloud/blob/master/pictures/jaychou/4.png)

jaychou歌词词云:
![image](https://github.com/29DCH/Word_Cloud/blob/master/pictures/jaychou/jaychou.jpg)


加背景的词云:
![image](https://github.com/29DCH/Word_Cloud/blob/master/pictures/jaychou/test.jpg)
