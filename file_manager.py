# -*- coding: utf-8 -*-
"""
这个py文件是用来修改文件夹名称的，帮助人们阅读服务器的文件
包含功能：
修改文件结构
从日期-具体日期&帖子
改变为更加人性化的
日期-具体日期-作者-帖子文件结构

H1：最上级文件夹名称
H2:下一层
H3:以此类推
……

在ser.py运行后运行
与ser.py无直接关联

！！！！！！！！
可能会导致：
服务器备份文件倍增
备份文件名显示不全
工作流被打断

未经测试请勿直接用于生产
！！！！！！！

!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!WARNING!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!

警告：
本程序调用了拥有外部安装包的模块pdfkit
在不同环境调用时候的方法并不一致
请自行百度修改
该程序中使用的环境为ubuntu
所以不需要配置文件
windows需要输如配置文件地址

"""

import os
import shutil 
import datetime
from bs4 import BeautifulSoup
from collections import Counter
import pdfkit

#！给文件权限，方便一会备份

os.system("chmod 777 /www/wwwroot/story.applenana.top/* -R ")

def mkdir(path):
    # 引入模块
    import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        os.makedirs(path) 
 
        #print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print (path+' 目录已存在')
        return False
    
class TZ:pass

f=open("pids.tmp","r+",encoding=("utf-8"))
pids=eval(f.read())
f.close()

F1=[]
for H1 in os.listdir():
    if "." not in H1:
        try:
            int(H1)
        except:pass
        else:
            F1.append(H1)
#获取了刚刚备份好的文件夹

mkdir("backup/"+str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day))
now="backup/"+str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().hour)+"时"+str(datetime.datetime.now().minute)+"分"
mkdir(now)
mkdir(now+'/按作者查看')
mkdir(now+'/按帖子名直接查看')
mkdir(now+"/备份下载[pdf]")

for H1 in F1:
    f=open("./"+H1+"/index.html","r+",encoding=("utf-8"))
    con=f.read()
    f.close()
    con=con.replace("</head>",'''</head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />''')
    f=open("./"+H1+"/index.html","w+",encoding=("utf-8"))
    f.write(con)
    f.close()
    options = {"enable-local-file-access": None}
    pdfkit.from_file("./"+H1+"/index.html","./"+H1+"/"+H1+".pdf",options=options)
#备份下载——转换成pdf

#新建一个author的列表，并创建对应文件夹
author=[]
for H1 in F1:
    file=open("./"+H1+"/index.html",encoding=("utf-8"))
    soup=BeautifulSoup(file,'lxml')   
    if str(soup.find_all("div",id="write")[0].find_all("div",attrs={"class": "author"})[0]).replace('<div class="author">            1楼 | ',"").split()[0] not in str(author):
        author.append(str(soup.find_all("div",id="write")[0].find_all("div",attrs={"class": "author"})[0]).replace('<div class="author">            1楼 | ',"").split()[0])
for name in author:
    mkdir(now+"/按作者查看/"+name+"/")

for H1 in F1:
    file=open("./"+H1+"/index.html",encoding=("utf-8"))
    soup=BeautifulSoup(file,'lxml')  
    tz=TZ()
    tz.title=str(soup.title).replace("<title>","").replace("</title>","")
    #print(tz.title)
    
    tz.author=str(soup.find_all("div",id="write")[0].find_all("div",attrs={"class": "author"})[0]).replace('<div class="author">            1楼 | ',"").split()[0]
    #print(tz.author)    
    
    mkdir(now+"/按作者查看/"+tz.author+"/"+tz.title)
    mkdir(now+"/按帖子名直接查看/"+tz.title)
    
    #复制备份的pdf到对应文件夹中
    shutil.copyfile("./"+H1+"/"+H1+".pdf","./"+now+"/备份下载[pdf]/"+tz.title+".pdf")
    
    
    for file in os.listdir("./"+H1):
        if "." in file:
            shutil.copyfile("./"+H1+"/"+file, "./"+now+"/按帖子名直接查看/"+tz.title+"/"+file)
            shutil.copyfile("./"+H1+"/"+file, "./"+now+"/按作者查看/"+tz.author+"/"+tz.title+"/"+file)
        else:
            mkdir("./"+now+"/按作者查看/"+tz.author+"/"+tz.title+"/"+file)
            mkdir(now+"/按帖子名直接查看/"+tz.title+"/"+file)
            for IN in os.listdir("./"+H1+"/"+file):
                shutil.copyfile("./"+H1+"/"+file+"/"+IN, "./"+now+"/按帖子名直接查看/"+tz.title+"/"+file+"/"+IN)
                shutil.copyfile("./"+H1+"/"+file+"/"+IN, "./"+now+"/按作者查看/"+tz.author+"/"+tz.title+"/"+file+"/"+IN)
    
    

'''
就在刚刚，我们把所有的文件已经按照文件格式重新排列
接下来就是把过于远久的帖子给删除
remove_day就是过多少天后删除
在后面会简写成RD

通过比对最近两次备份的差异，即可知道哪些帖子被删了
但这也就意味着，我们不能胡乱减少帖子备份列表
否则就会被误判成被删除
 
同时，对于已经被删除帖子
我们会把它复制到被删除文件夹中

我们会遍历寻找被删帖子最新的一次备份，并举家复制搬迁
'''
    
mkdir("./backup/被删除帖子")
mkdir("./Last")
Last=os.listdir("./Last")
Now=F1
More=Counter(Last)
Less=Counter(Now)
Different=list((More-Less).elements())
print("检测到本次备份相比上一次有缺失文件"+'\n'+"为"+str(Different))
print('将会不会删除缺失文件')

if "lost.tz" not in os.listdir("./"):
    f=open("./lost.tz","w",encoding=("utf-8"))
    f.close()
f=open("./lost.tz","r+",encoding=("utf-8"))
readlist=f.readlines()
f.close()
for need in Different:
    if need not in readlist:
        f=open("./lost.tz","a+",encoding=("utf-8"))
        f.write(need+"\n")
        f.close()
        print("已将"+need+"添加入lost.tz")
        f=open("./Last/"+need+"/index.html",encoding=("utf-8"))
        soup=BeautifulSoup(f,'lxml')  
        tz=TZ()
        tz.title=str(soup.title).replace("<title>","").replace("</title>","")
        #print(tz.title)
        f.close()
        
        tz.author=str(soup.find_all("div",id="write")[0].find_all("div",attrs={"class": "author"})[0]).replace('<div class="author">            1楼 | ',"").split()[0]
        #print(tz.author)  
        mkdir("./backup/被删除帖子/按作者查看")
        mkdir("./backup/被删除帖子/按作者查看/"+tz.author)
        mkdir("./backup/被删除帖子/按名字查看")
        mkdir("./backup/被删除帖子/备份下载[pdf]")
        
        shutil.copyfile("./Last/"+need+"/"+need+".pdf","./backup/被删除帖子/备份下载[pdf]/"+tz.title+".pdf")
        shutil.copytree("./Last/"+need,"./backup/被删除帖子/按作者查看/"+tz.author+"/"+tz.title)
        shutil.copytree("./Last/"+need, "./backup/被删除帖子/按名字查看/"+tz.title)

shutil.rmtree("./Last")        
'''
就在刚刚
我们把被删除帖子移动到了“被删除帖子”文件夹中
并且对它更名
删除了上一次的Last文件夹
接下来
并且重新生成这一次Last文件夹
最后检测日期，并删除过期文件夹！
完成！
'''

    
#处理以后归档为Last    
for H1 in F1:
    file=open("./"+H1+"/index.html",encoding=("utf-8"))
    soup=BeautifulSoup(file,'lxml')  
    tz=TZ()
    tz.title=str(soup.title).replace("<title>","").replace("</title>","")
    #print(tz.title)
    
    tz.author=str(soup.find_all("div",id="write")[0].find_all("div",attrs={"class": "author"})[0]).replace('<div class="author">            1楼 | ',"").split()[0]
    #print(tz.author)    
    
    mkdir("./Last")
    
    for file in os.listdir("./"+H1):
        if "." in file:
            mkdir("./Last/"+H1)
            shutil.copyfile("./"+H1+"/"+file, "./Last/"+H1+"/"+file)
        else:
            mkdir("./Last/"+H1+"/"+file)
            for IN in os.listdir("./"+H1+"/"+file):
                shutil.copyfile("./"+H1+"/"+file+"/"+IN, "./Last/"+H1+"/"+file+"/"+IN)
                
    shutil.copyfile("./"+H1+"/"+H1+".pdf", "./Last/"+H1+"/"+H1+".pdf")
    
    shutil.rmtree("./"+H1)        

