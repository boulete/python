# Python批量合并移动端下载B站视频[安卓]
从移动端哔哩哔哩上下载的视频格式为音视频分割格式：  
即为**video.m4s**的视频流和**audio.m4s**的音频流。另外在其上一级文件夹还有用于存放**视频标题**等信息的**JSON**文件。剪辑软件可以将它们合并起来，但当有一定数量的时候可以考虑用程序来执行。  

## 一、整体思路  
使用**ffmpeg**工具进行合并，**Python**编程，运用**Python**的**ffmpy**、**glob**、**json**库进行批量作业。  
  
## 二、步骤
### 1、安装相关工具和环境
#### 1.1 安装 Python
官网下载链接：[Python 3.9.6](https://www.python.org/downloads/release/python-396/)  
要求配置**环境变量**
#### 1.2 下载安装 ffmpeg 工具
下载安装**ffmpeg**，要求配置**环境变量**。  
链接：[ffmpeg | 百度云盘](https://pan.baidu.com/s/1Z2wtfaCSe8zcX70YapdQ1Q)  
提取码：**boul** 
#### 1.3 安装Python第三方库
```
pip install json
pip install ffmpy
```
### 2、分析学习
#### 2.1 下载内容主要构成  
安卓端下载的视频一般存放在如下目录：  
```
Android/data/tv.danmaku.bili/download
```
**entry.json**用于存放标题等信息，**video.m4s**用于存放视频流，**audio.m4s**用于存放音频流。（其他的用不上） 
  
**下载目录**
> 文件夹
>> 文件夹
>>> + entry.json
>>> + 80[文件夹]
>>>> + video.m4s
>>>> + audio.m4s
  
#### 2.2 使用ffmpeg工具
**主要指令**  
```
ffmpeg -i video.m4s -i audio.m4s -vcodec copy -acodec copy output.mp4
```
随便找一个80文件夹试试吧：  
![image](http://boulete.xyz/templateimg/img1.png)  
在该目录下打开 **cmd** ，输入上述指令，成功得到一个将视频流和音频流合并起来的一个 **output.mp4** ，终于可以正常打开一个文件播放视频与音频。

#### 2.3 使用Python的ffmpy库
删除上面生成的**output.mp4**，我们使用Python的ffmpy库来生成一个。  

在上面的80目录下新建一个**transform.py文件**。  
输入：
```
from ffmpy import FFmpeg

def transform(v,a,o):
    ff = FFmpeg(inputs={v:None,a:None},
                outputs={o:'-vcodec copy -acodec copy'})
    # 查看生成的代码
    print(ff.cmd)
    # 执行代码
    ff.run()

# 以下部分确认transform函数可以正常运行后删除
v = 'video.m4s'
a = 'audio.m4s'
o = 'output.mp4'
transform(v,a,o)
```
在这里我们建立了一个**transform**函数来引导，对其输入视频流参数**v**，音频流参数**a**，输出文件名参数**o**，引入三个参数来生成一个新的视频文件。
|参数|内容|数据类型|
|:-:|:-:|:-:|
|v|视频流|字符串|
|a|音频流|字符串|
|o|输出文件名|字符串|
执行，同样能够正常输出一个**output.mp4文件**。

**FFmpeg**为**ffmpy**库所带的类，实例化用来生成实际运行的代码，调用**ffmpeg**工具的。

**FFmpeg**实例化的对象具有**cmd**参数和**run**方法，有**cmd**参数可以用来查看其生成的实际运行的代码，**run**方法则用来执行。  

至此我们实现了使**用Python代码**实现调用**ffmpeg工具**的目的。删除函数部分之外参数赋值和调用函数的代码，保存，后面可以用。

#### 2.4 使用Python的json库
在**80文件夹**的上一级文件夹（有**entry.json**文件的那个)中打开**cmd**，进入**Python环境**。  
  
输入如下代码：
```
>>> from json import load
>>> f = open('entry.json','r',encoding='utf8')
>>> data = load(f)
```
调用：
```
>>> data['title']
'该视频的标题'
>>> 
```
#### 2.5 使用Python的glob库
**glob**库是Python自带的文件操作库，接下来我们用它来批量获取文件路径。  
在**下载目录**下新建一个**control.py文件**。  
输入：
```
from glob import glob

paths1 = glob(f'./*/*/entry.json')
paths2 = glob(f'./*/*/80/')
print(paths1,paths2)
```
如此一来，就可以得到所有我们想要的文件路径了，剩下就是结合上面学到的知识将它们结合起来。
### 3、知识结合，最终代码
```
from glob import glob
from ffmpy import FFmpeg
from json import load

# 转换合并函数
def transform(v,a,o):
    ff = FFmpeg(inputs={v:None,a:None},outputs={o:'-vcodec copy -acodec copy'})
    print(ff.cmd)
    ff.run()
    
# 解析json文件，获取标题，将其返回
def get_title(path):
    f = open(path,'r',encoding='utf8')
    data = load(f)
    return data['title']
    
# 获取路径集
paths1 = glob(f'./*/*/entry.json')
paths2 = glob(f'./*/*/80/')

# 遍历路径集，执行函数
for i in range(len(paths1)):
    # 原始数据视频流路径
    v = paths2[i] + 'video.m4s'
    # 原始数据音频流路径
    a = paths2[i] + 'audio.m4s'
    # 输出路径（带标题）
    o = get_title(paths1[i]) + '.mp4'
    # 执行合并函数
    transform(v,a,o)

```
执行代码，自动合并视频流和音频流，生成新的MP4文件。  

生成完毕后，记得将下载的视频文件夹都删除。
