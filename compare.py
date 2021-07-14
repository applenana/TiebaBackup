# -*- coding: utf-8 -*-
f=open("./tmp.txt","r+",encoding=("utf-8"))
now=f.read().split("?")[0].split("/p/")[1]
f.close()
import os
os.remove("./tmp.txt")
f=open("./tz.txt","r+",encoding=("utf-8"))
All=f.read()
f.close()
if now in All:
    print('<h1 align="center">你提交的帖子已经有人备份了！可以去<a href="http://story.applenana.top">这里</a>查看<h1/>')
else:
    f=open("./tz.txt","a+",encoding=("utf-8"))
    f.write('http://tieba.baidu.com/p/'+now+"\n")
    f.close()
    print('<h1 align="center">提交成功</h1>')
          
