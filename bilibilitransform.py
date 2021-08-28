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
