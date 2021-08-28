from glob import glob
from json import load
from ffmpy import FFmpeg

def output(name,v,a):
    ff = FFmpeg(inputs={v:None,a:None},
    	outputs={name +'.mp4':'-vcodec copy -acodec copy'})
    print(ff.cmd)
    ff.run()
path1s = glob(f'./*/*/entry.json')
path2s = glob(f'./*/*/80/')

for i in range(0,len(path1s)):
    f = open(path1s[i],'r',encoding='utf8')
    name = load(f)['title']
    print(name)
    v = path2s[i] + 'video.m4s'
    a = path2s[i] + 'audio.m4s'
    print(v)
    print(a)
    output(name,v,a)

