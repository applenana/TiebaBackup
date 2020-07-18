
Server = True
#是否为服务器定时运行模式

import argparse
import urllib
from addcss import add_css
import hashlib
import time
import datetime
import const
import os
import shutil
import requests
import html
import sys
import traceback
import subprocess
import timeit
import re
from tqdm import tqdm
from download import DownloadPool
from avalon import Avalon
from time import sleep
class RetryError(Exception):pass
class RetryExhausted(RetryError):pass
class RetryCheckFailed(RetryError):pass
class UserCancelled(Exception):pass
class TiebaApiError(Exception):pass
class UndifiedMsgType(TiebaApiError):pass
class RequestError(TiebaApiError):
    def __init__(self, data):
        self.data = data

start_time=timeit.default_timer()


AudioCount = None
IsCreate = None
FileHandle = None
Progress = None
VideoCount = None
ImageCount = None
Pool = None
IsDownload = None
FFmpeg = None


const.PageUrl    = "http://c.tieba.baidu.com/c/f/pb/page"
const.FloorUrl   = "http://c.tieba.baidu.com/c/f/pb/floor"
const.EmotionUrl = "http://tieba.baidu.com/tb/editor/images/client/"
const.AliUrl     = "https://tieba.baidu.com/tb/editor/images/ali/"
const.VoiceUrl   = "http://c.tieba.baidu.com/c/p/voice?play_from=pb_voice_play&voice_md5="
const.SignKey    = "tiebaclient!!!"
# const.IS_WIN=(os.name=="nt")

DirName_New=""
OverWriteMode = 0
PreList = list()
PreDirList = list()
CopyDir = ""
Copy = False
Delay = False
Delay_time = ""
Delay_times = ""


exe_mode = False
if ('.exe' in sys.argv[0]):
    add_css()
    exe_mode = True
    Avalon.info("正在以exe模式运行")


if (Server):
    pid = 6684644957#6477171863#4016579360
    #6477171863
    #帖子链接/id
    lz = False
    #是否只看楼主
    comment = True
    #是否包含评论
    DirName = "ppp"
    #输出文件夹路径,为空则默认为(\"吧名\\标题\)
    OutPutFileName = "index"
    #输出文件名,方便网站部署,为空则默认为帖子pid
    OutputHTML = True
    #是否输出html,否则输出markdown
    OverWriteMode = 3
    #存在同名文件处理方式:0-交互 1-跳过 2-覆盖 3-备份已有文件夹
    PreSet = True
    #批量模式
    PreList = [5851299305,5872001700,5889692007,5936021703,6004314276,6063623782,6106125852,6189777120,6459597519,4728539641,5562942226,6125418712,6112840112,5799820184,6280965487,6008600754,5568121591,6158733858,3975950695,6440383436,6477171863,2836629615,4982493094,3582502925,6558868080,6208573077,6477771371,6487985238,6509368661,6513673233,6521363329,6531580993,6486873926,6508222706,6546604005,6545078814,6235349098,6546496899,6543073883,6468607665,6478694107]
    #批量模式下帖子链接/pid
    PreDirList = ["4016579360","4731835105","6187040784","5851299305","5872001700","5889692007","5936021703","6004314276","6063623782","6106125852","6189777120","6459597519","4728539641","5562942226","6125418712","6112840112","5799820184"]
    #批量模式下保存文件夹名,与上面pid对应
    PreDirDirect = True
    #批量模式下是否直接使用特殊名称作为保存文件夹名,开启后忽略上一项,开启后请更改下一项模式
    PreDirDirectMode = 0
    #直接使用特殊名称作为保存文件夹名设置: 0-帖子id 1-吧名\\标题\
    Delay = True
    #是否在启用下载延迟,以对抗百度限制,批量模式下建议开启
    Delay_time = 60
    #延迟时长,以秒为单位,建议60左右
    Delay_times = 2
    #间隔n个帖子延迟一次,建议为2或2以上
    Copy = False
    #是否对备份完成的帖子复制到部署文件夹,批量模式下不可用
    CopyDir = ""
    #对备份完成的帖子复制到部署文件夹的路径
    Auto_Clean = True
    #是否自动删除备份文件夹
    Auto_Clean_time = 2
    #自动删除几天前的备份文件夹
    #TODO:自动删除
    Work_path = ""
    #"C:\\Users\\28448\\Administrator\\Git\\TiebaBackup-complete\\td23"
    #设置工作目录,即备份文件储存目录
    Avalon.info("正在以Server模式运行 " + str(datetime.datetime.now()))
    if(PreDirDirect):
        if(PreDirDirectMode !=0 and PreDirDirectMode !=1):
            Avalon.error("文件夹名直出模式错误!请更正!")
            exit()
        PreDirList = []
        if(PreDirDirectMode == 0):
            for i in PreList:
                PreDirList.append(str(i))
        elif(PreDirDirectMode == 1):
            for i in PreList:
                PreDirList.append("")
    PreList.append(0)
    PreDirList.append("0")
else:
    Avalon.info("正在以交互模式运行 " + str(datetime.datetime.now()))



if not (Server):
    try:
        Work_path = Avalon.gets("请输入工作目录(备份文件父目录),为空或错误则为当前目录:")
    except KeyboardInterrupt:
        Avalon.error("Control-C,exiting",front="\n")
        if (exe_mode):
            input("按回车键退出...")
        sys.exit()
if(Server):
    if(Auto_Clean):
        Avalon.info("自动清理已开启,将会自动删除" + str(Auto_Clean_time) + "天前的备份文件")

not_work_path = False
exe_path = os.getcwd()
    
if (os.path.exists(Work_path)):
    try:
        os.chdir(Work_path)
        Avalon.info("当前工作目录为" + os.getcwd())
    except KeyboardInterrupt:
        ForceStop()
        Avalon.error("Control-C,exiting",front="\n")
        sys.exit()
    except UserCancelled:
        Avalon.warning("用户取消")
    except Exception as err:
        ForceStop()
        Avalon.error("发生异常:\n"+traceback.format_exc() + str(datetime.datetime.now()),front="\n")
        sys.exit()
else:
    Avalon.warning("指定工作目录不存在!请检查!当前工作目录为" + os.getcwd())
    not_work_path = True



#TODO:将其更换为第三方库实现

'''if (len(sys.argv) > 1):
    if (sys.argv[1] == "--lz-T"):
        lz = True
        Avalon.info("从传入参数获取新的只看楼主模式:True")
    elif (sys.argv[1] == "--lz-F"):
        lz = False
        Avalon.info("从传入参数获取新的只看楼主模式:False")
    if (len(sys.argv) > 3):
        if (sys.argv[2] == "--DirName"):
            DirName = sys.argv[3]
            Avalon.info("从传入参数获取输出文件夹路径:"+DirName)
'''


Html_Header =(
'''<!doctype html>
<html lang="zh-cn">
<head>
<link rel="stylesheet" type="text/css" href="main.css">
</head>
<body>
<div id="write">
'''
)
#Html文件头

if (Server and PreSet):
    #DirName = ""
    Avalon.info("正在以批量模式运行,任务列表: [" + (','.join('%s' %id for id in PreList)) + "]")
    if (not PreDirDirect):
        Avalon.info("正在以批量模式运行,目录列表: [" + (','.join('%s' %dn for dn in PreDirList)) + "]")
    else:
        Avalon.info("正在以批量模式运行,目录为各帖子名称")

if (Delay and PreSet):
    Avalon.info("每下载 "+ str(Delay_times) + " 个帖子,将会等待 " + str(Delay_time) + " 秒")


def DelOlds(MaxDays):
    DirList = os.listdir(os.getcwd())
    BeenDelList = list()
    for i in DirList:
        OldDir = re.search(r'(([0]\d{0}[1-9]\d{0})|[1]\d{0}[0-2]\d{0})-(([0-2]\d{0}[0-9]\d{0})|([3]\d{0}[0-1]\d{0}))', i)
        if OldDir:
            #print (i)
            OldDate = str(datetime.datetime.now().year) + "-" + i
            #print(datetime.strptime(i, '%Y-%m-%d'))
            DiffTime = datetime.datetime.now() - datetime.datetime.strptime(OldDate, '%Y-%m-%d')
            DiffTime = str(DiffTime)
            #print(DiffTime)
            DiffDay = re.findall(r'[0-9]\d{0,1} day', DiffTime)
            if(DiffDay):
                DiffDay = DiffDay[0][:-4]
            else: DiffDay = 0
            #print(DiffDay)
            if (int(DiffDay) >= MaxDays):
                shutil.rmtree(i)
                BeenDelList.append(i)
    return BeenDelList

def MakeDir(dirname):
    global IsCreate
    if (dirname in IsCreate):
        return
    if (os.path.isdir(dirname)):
        pass
    elif (os.path.exists(dirname)):
        raise OSError("%s is a file"%dirname)
    else:
        os.makedirs(dirname)
    IsCreate.add(dirname)

def Init(pid,overwrite):
    global FileHandle,Progress,AudioCount,VideoCount,ImageCount,Pool,IsDownload,DirName,IsCreate,OutputHTML,FFmpeg,OutPutFileName,DirName_New
    IsDownload=set()
    IsCreate=set()
    AudioCount=VideoCount=ImageCount=0
    if (os.path.isdir(DirName)):
        Avalon.warning("\"%s\"已存在"%DirName)
        if (overwrite==1):
            Avalon.warning("跳过%d"%pid)
        elif (overwrite==2):
            Avalon.warning("默认覆盖\"%s\""%DirName)
        elif (overwrite==3):
            if (len(DirName) > 30):
                DirName_New = DirName[:-11]
            else:
                DirName_New = DirName
            if (Server):
                Avalon.info("已将已存在文件夹备份至" + (datetime.datetime.now().strftime('%m-%d'))+ "/" +DirName_New + " " + (datetime.datetime.now()-datetime.timedelta(hours=12)).strftime('%H-%M'))
                shutil.move(DirName,(datetime.datetime.now().strftime('%m-%d'))+ "/" +DirName_New + " " + (datetime.datetime.now()-datetime.timedelta(hours=12)).strftime('%H-%M'))
            if not (Server):
                Avalon.info("已将已存在文件夹备份至" + (datetime.datetime.now().strftime('%m-%d'))+ "/" +DirName_New + " " + datetime.datetime.now().strftime('%H-%M'))
                shutil.move(DirName,(datetime.datetime.now().strftime('%m-%d'))+ "/" +DirName_New + " " + datetime.datetime.now().strftime('%H-%M'))
            os.makedirs(DirName)
        elif (not Avalon.ask("是否覆盖?",False)):
            raise UserCancelled("...")
    elif (os.path.exists(DirName)):
        raise OSError("存在同名文件")
    else:
        os.makedirs(DirName)
    if (OutputHTML):
        FileHandle=open("%s/%s.html"%(DirName,OutPutFileName),"w+",encoding="utf-8")
        Write(Html_Header)
        Write("<title>%s</title>\n"%(title_name))
        if (exe_mode):
            if (not_work_path):
                shutil.copy("main.css",DirName+"/")
            elif not (not_work_path):
                shutil.copy(exe_path + "/main.css",DirName+"/")
        else:
            shutil.copy(sys.path[0] + "/main.css",DirName+"/")
    else:
        FileHandle=open("%s/%s.md"%(DirName,OutPutFileName),"w+",encoding="utf-8")
    try:
        subprocess.Popen("ffmpeg",stdout=subprocess.DEVNULL,\
            stderr=subprocess.DEVNULL).wait()
        FFmpeg=1
    except FileNotFoundError:
        Avalon.warning("未找到ffmpeg,语音将不会被转为mp3")
        FFmpeg=0
    Pool=DownloadPool(DirName+"/","file")
    Progress=tqdm(unit="floor")

def ConvertAudio():
    global AudioCount,DirName,FFmpeg
    if ((not FFmpeg) or (not AudioCount)):
        return
    for i in tqdm(range(1,AudioCount+1),unit="audio",ascii=True):
        if (FFmpeg):
            prefix="%s/audios/%d"%(DirName,i)
            subprocess.Popen(["ffmpeg","-i","%s.amr"%prefix,\
                "%s.mp3"%prefix,"-y"],stdout=subprocess.DEVNULL,\
                stderr=subprocess.DEVNULL).wait()
            os.remove("%s.amr"%prefix)
    
def Done():
    global OutputHTML
    if (OutputHTML):
        Write('</div></body></html>')
    FileHandle.close()
    Progress.set_description("正在等待下载线程响应...")
    Pool.Stop()
    Progress.close()

def ForceStop():
    if ("FileHandle" in globals().keys()):
        try:
            FileHandle.close()
        except:
            pass
    if ("Pool" in globals().keys()):
        try:
            Pool.ImgProc.close()
        except:
            pass
    if ("Progress" in globals().keys()):
        try:
            Progress.close()
        except:
            pass

def CallFunc(func=None,args=None,kwargs=None):
    if (not (func is None)):
        if (args is None):
            if (kwargs is None):
                return func()
            else:
                return func(**kwargs)
        else:
            if (kwargs is None):
                return func(*args)
            else:
                return func(*args,**kwargs)

# times == -1 ---> forever
def Retry(func,args=None,kwargs=None,cfunc=None,ffunc=None,fargs=None,fkwargs=None,times=3,sleep=1):
    fg=0
    while (times):
        try:
            resp=CallFunc(func,args,kwargs)
        except Exception as err:
            CallFunc(ffunc,fargs,fkwargs)
            times=max(-1,times-1)
            time.sleep(sleep)
        else:
            if (CallFunc(cfunc,(resp,)) in [None,True]):
                return resp
            times=max(-1,times-1)
            fg=1
    if (fg):
        raise RetryCheckFailed(func.__qualname__,args,cfunc.__qualname__,resp)
    else:
        raise RetryExhausted(func.__qualname__,args,cfunc.__qualname__) from err

def Write(content):
    FileHandle.write(content)

def SignRequest(data):
    s = ""
    keys = sorted(data.keys())
    for i in keys:
        s += i + "=" + data[i]
    sign = hashlib.md5((s + const.SignKey).encode("utf-8")).hexdigest().upper()
    data.update({"sign": str(sign)})
    return data

def TiebaRequest(url,data,first=False):
    JsonRetry = 0
    while(JsonRetry=<5):
        try:
            if (first):
                req=Retry(requests.post,args=(url,),kwargs={"data":SignRequest(data)},cfunc=(lambda x: x.status_code==200),ffunc=print,fargs=("连接失败,正在重试...\n",),times=10)
            else:
                req=Retry(requests.post,args=(url,),kwargs={"data":SignRequest(data)},cfunc=(lambda x: x.status_code==200),ffunc=Progress.set_description,fargs=("连接失败,正在重试...",),times=10)
            req.encoding='utf-8'
            ret=req.json()# JSON错误的源头
            break
        except:
            Avalon.warning("遇到一次JSON错误,正在重试")
            JsonRetry+=1
            continue
    #print(ret)
    if (int(ret["error_code"])!=0):
        raise RequestError({"code":int(ret["error_code"]),"msg":str(ret["error_msg"])})
    return ret

def ReqContent(pid,fid,lz):
    if (~fid):
        return TiebaRequest(const.PageUrl,{"kz":str(pid),"pid":str(fid),"lz":str(int(lz)),"_client_version":"9.9.8.32"})
    else:
        return TiebaRequest(const.PageUrl,{"kz":str(pid),"lz":str(int(lz)),"_client_version":"9.9.8.32"})

def ReqComment(pid,fid,pn):
    return TiebaRequest(const.FloorUrl,{"kz":str(pid),"pid":str(fid),"pn":str(pn),"_client_version":"9.9.8.32"})

def FormatTime(t):
    return time.strftime("%Y-%m-%d %H:%M",time.localtime(int(t)))

def ProcessText(text,in_comment):
    global OutputHTML
    if (OutputHTML):
        if (in_comment):
            return html.escape(text)
        else:
            return html.escape(text).replace("\n","<br />")
    else:
        if (in_comment):
            return html.escape(text)
        else:
            return html.escape(text).replace("\\","\\\\").replace("\n","  \n").replace("*","\\*")\
                .replace("-","\\-").replace("_","\\_").replace("(","\\(").replace(")","\\)")\
                .replace("#","\\#").replace("`","\\`").replace("~","\\~").replace("[","\\[")\
                .replace("]","\\]").replace("!","\\!").replace(".","\\.").replace("+","\\+")

def ProcessUrl(url,text):
    return '<a href="%s">%s</a>'%(url,text)

def ProcessImg(url):
    global ImageCount,DirName
    if (url[0:2]=="//"):
        url="http:"+url
    MakeDir(DirName+"/images")
    ImageCount+=1
    name="images/%d.%s"%(ImageCount,url.split("?")[0].split(".")[-1])
    Pool.Download(url,name)
    return '\n<div><img src="%s" /></div>\n'%name

def ProcessVideo(url,cover):
    global VideoCount,DirName,OutputHTML
    MakeDir(DirName+"/videos")
    VideoCount+=1
    vname="videos/%d.%s"%(VideoCount,url.split(".")[-1])
    cname="videos/%d_cover.%s"%(VideoCount,cover.split(".")[-1])
    Pool.Download(url,vname)
    Pool.Download(cover,cname)
    if (OutputHTML):
        return '\n<video src="%s" poster="%s" controls />\n'%(vname,cname)
    else:
        return '\n<a href="%s"><img src="%s" title="点击查看视频"></a>\n'%(vname,cname)

def ProcessAudio(md5):
    global AudioCount,DirName,OutputHTML,FFmpeg
    MakeDir(DirName+"/audios")
    AudioCount+=1
    Pool.Download(const.VoiceUrl+md5,"audios/%d.amr"%AudioCount)
    if (OutputHTML and FFmpeg):
        return '<audio src="audios/%d.mp3" controls />'%AudioCount
    elif (FFmpeg):
        return '<a href="audios/%d.mp3">语音</a>\n'%AudioCount
    else:
        return '<a href="audios/%d.amr">语音</a>\n'%AudioCount

def ProcessEmotion(floor,name,text):
    global DirName,IsDownload
    MakeDir(DirName+"/images")
    lname=len(name)
    if (name=="image_emoticon"):
        name+="1"
        lname+=1
    url=""
    if (lname>=3 and name[0:3]=="ali"):
        url="%s%s.gif"%(const.AliUrl,name)
        name+=".gif"
    elif (lname>=14 and name[0:14]=="image_emoticon"):
        url="%s%s.png"%(const.EmotionUrl,name)
        name+=".png"
    #TODO适配表情,暂时不实现
    #elif (lname<=10 and name[0])
    else:
        Avalon.warning("第%s楼出现未知表情:%s\n"%(floor,name),front="\n\n")
        return ''
    if (not name in IsDownload):
        IsDownload.add(name)
        Pool.Download(url,"images/%s"%name)
    return '<img src="images/%s" alt="%s" title="%s" />'%(name,text,text)

def ProcessContent(floor,data,in_comment):
    content=""
    for s in data:
        #TODO:断点续传
        if (str(s["type"])=="0"):
            content+=ProcessText(s["text"],in_comment)
        elif (str(s["type"])=="1"):
            content+=ProcessUrl(s["link"],s["text"])
        elif (str(s["type"])=="2"):
            content+=ProcessEmotion(floor,s["text"],s["c"])
        elif (str(s["type"])=="3"):
            try:
                content+=ProcessImg(s["origin_src"])
            except:
                content+="无法获取该图片,已自动跳过!" + str(s)
                Avalon.warning("第 %s 楼: 出现不支持的图片: \n%s\n"%(floor,str(s)),front="\n")
        elif (str(s["type"])=="4"):
            content+=ProcessText(s["text"],in_comment)
        elif (str(s["type"])=="5"):
            try:
                content+=ProcessVideo(s["link"],s["src"])
            except:
                content+="无法获取该视频,已自动跳过!" + str(s)
                Avalon.warning("第 %s 楼: 出现不支持的视频: \n%s\n"%(floor,str(s)),front="\n")
        elif (str(s["type"])=="9"):
            content+=ProcessText(s["text"],in_comment)
        elif (str(s["type"])=="10"):
            content+=ProcessAudio(s["voice_md5"])
        elif (str(s["type"])=="11"):
            content+=ProcessImg(s["static"])
        elif (str(s["type"])=="20"):
            content+=ProcessImg(s["src"])
        else:
            Avalon.warning("第 %s 楼: 请求数据错误: \n%s\n"%(floor,str(s)),front="\n")
            # raise UndifiedMsgType("content data wrong: \n%s\n"%str(s))
    return content

def ProcessFloor(floor,author,t,content):
    global OutputHTML
    if (OutputHTML):
        return '<hr />\n<div>%s</div><br />\n<div class="author">\
            %s楼 | %s | %s</div>\n'%(content,floor,author,FormatTime(t))
    else:
        return '<hr />\n\n%s\n<div align="right" style="font-size:12px;color:#CCC;">\
            %s楼 | %s | %s</div>\n'%(content,floor,author,FormatTime(t))

def ProcessComment(author,t,content):
        return '%s | %s:<blockquote>%s</blockquote>'%(FormatTime(t),author,content)

def GetComment(floor,pid,fid):
    global OutputHTML
    if (OutputHTML):
        Write('<pre>')
    else:
        Write('<pre style="background-color: #f6f8fa;border-radius: 3px;\
            font-size: 85%;line-height: 1.45;overflow: auto;padding: 16px;">')
    pn=1
    while (1):
        data=ReqComment(pid,fid,pn)
        data=data["subpost_list"]
        if (len(data)==0):
            break
        for comment in data:
            Write(ProcessComment(comment["author"]["name_show"],comment["time"],ProcessContent(floor,comment["content"],1)))
        pn+=1
    Write('</pre>')

def ProcessUserList(data):
    userlist={}
    for user in data:
        userlist[user["id"]]={"id":user["portrait"].split("?")[0],"name":user["name_show"]}
    return userlist

def GetTitle(pid):
    data=TiebaRequest(const.PageUrl,{"kz":str(pid),"_client_version":"9.9.8.32"},True)
    return {"post":data["post_list"][0]["title"],"forum":data["forum"]["name"]}


def GetPost(pid,lz,comment):
    lastfid=-1
    while (1):
        data=ReqContent(pid,lastfid,lz)
        # print(data)
        userlist=ProcessUserList(data["user_list"])
        for floor in data["post_list"]:
            if (int(floor["id"])==lastfid):
                continue
            fnum=floor["floor"]
            #print ("\n\n"+fnum)
            Progress.update(1)
            Progress.set_description("正在读取第 %s 楼"%fnum)
            fid=int(floor["id"])
            Write(ProcessFloor(fnum,userlist[floor["author_id"]]["name"],floor["time"],ProcessContent(fnum,floor["content"],0)))
            if (int(floor["sub_post_number"])==0):
                continue
            if (comment):
                GetComment(fnum,pid,floor["id"])
        if (lastfid==fid):
            break
        #print(fid,lastfid)
        lastfid=fid

if not (Server):
    while (1):
        try:
            if (Avalon.ask("批量模式?",False)):
                if(Avalon.ask("开启延迟?",True)):
                    Delay = True
                    while(1):
                        try:
                            Delay_time = (Avalon.gets("请输入延迟时长(以秒为单位,留空默认为60s):"))
                            if (Delay_time == ""):
                                Delay_time = "60"
                            Delay_time = int(float(Delay_time))
                            if (Delay_time == 0):
                                Avalon.warning("时长不能为0!")
                                continue
                            break
                        except Exception:
                            Avalon.warning("格式错误,请重新输入!")
                            continue
                        except KeyboardInterrupt:
                            ForceStop()
                            Avalon.error("Control-C,exiting",front="\n")
                            if (exe_mode):
                                input("按回车键退出...")
                            sys.exit()
                    while(1):
                        try:
                            Delay_times = (Avalon.gets("请输入延迟间隔(即每下载n个帖子执行一次延迟,留空默认为2):"))
                            if (Delay_times == ""):
                                Delay_times = "2"
                            Delay_times = int(float(Delay_times))
                            if (Delay_times == 0):
                                Avalon.warning("间隔不能为0!")
                                continue
                            break
                        except Exception:
                            Avalon.warning("格式错误,请重新输入!")
                            continue
                        except KeyboardInterrupt:
                            ForceStop()
                            Avalon.error("Control-C,exiting",front="\n")
                            if (exe_mode):
                                input("按回车键退出...")
                            sys.exit()
                    Avalon.info("每下载 "+ str(Delay_times) + " 个帖子,将会等待 " + str(Delay_time) + " 秒")
                PreList = list()
                PreSet=True
                lz=Avalon.ask("只看楼主?",False)
                comment=(Avalon.ask("包括评论?",True))
                OutPutFileName=(Avalon.gets("输出文件名(为空则为帖子id):"))
                OutputHTML=Avalon.ask("输出HTML(否则表示输出Makrdown)?:",True)
                while(1):
                    try:
                        OverWriteMode=(Avalon.gets("存在同名文件夹时操作? 0-交互 1-跳过 2-覆盖 3-备份 请输入(0/1/2/3) 为空则默认为3:"))
                        if (OverWriteMode == ""):
                            OverWriteMode = "3"
                        OverWriteMode = int(OverWriteMode)
                        if (OverWriteMode != 0 and OverWriteMode != 1 and OverWriteMode != 2 and OverWriteMode != 3):
                            Avalon.warning("请输入0/1/2/3")
                            continue
                        else:
                            break
                    except:
                        pass
                Avalon.info("信息确认: 选定:%s && %s评论 , 目录:\"吧名\\标题\" , 文件名:\"%s%s\" , 文件夹冲突处理模式:%d"%(("楼主" if lz else "全部"),("全" if comment else "无"),OutPutFileName,(".html" if OutputHTML else ".md"),OverWriteMode))
                if (not Avalon.ask("确认无误?",True)):
                    Avalon.warning("请重新输入")
                else:
                    break
            else:
                PreSet=False
                break
        except KeyboardInterrupt:
            ForceStop()
            Avalon.error("Control-C,exiting",front="\n")
            if (exe_mode):
                input("按回车键退出...")
            sys.exit()

if (not Server and PreSet):
    #TODO:逗号分隔批量输入
    while(1):
        try:
            pid_input=int((Avalon.gets("请输入帖子链接或id(输入0结束输入):").split('/'))[-1].split('?')[0])
            PreList.append(pid_input)
            if (pid_input == 0):
                PreDirList.append("0")
                break
        except Exception:
            Avalon.warning("未找到正确的id")
            continue
        except KeyboardInterrupt:
            ForceStop()
            Avalon.error("Control-C,exiting",front="\n")
            if (exe_mode):
                input("按回车键退出...")
            sys.exit()
        PreDir_input=(str(Avalon.gets("输入保存目录(空则表示使用\"吧名\\标题\"):")))
        PreDir_input=re.sub(r'(/|\\|\?|\||\*|\:|\"|\<|\>|\.)','',PreDir_input)
        PreDirList.append(PreDir_input)




if (not Server and PreSet):
    DirName = ""
    #OutPutFileName = str("")
    Avalon.info("正在以批量模式运行,任务列表: [" + (','.join('%s' %id for id in PreList)) + "]")

n = -1
Error = False
Run_times = 0
Run_times_all = 0

while (1):
    n = n+1
    try:
        if (PreSet):
            pid = PreList[n]
            DirName = PreDirList[n]
        if not (Server or PreSet):
            try:
                pid=int((Avalon.gets("请输入帖子链接或id(输入0退出):").split('/'))[-1].split('?')[0])
            except Exception:
                Avalon.warning("未找到正确的id")
                continue
        if (pid==0):
            if (PreSet):
                end_time=timeit.default_timer()
                Avalon.info('\n运行用时: %s\n'%(str(datetime.timedelta(seconds=(end_time-start_time)))))
            if (exe_mode):
                input("按回车键退出...")
            sys.exit()
        if (PreSet and Delay):
            if (Run_times == Delay_times):
                Avalon.info("下载帖子数已达到 "+ str(Run_times_all) +" 个,冷却 " + str(Delay_time) + " 秒中...")
                Run_times = 0
                for i in tqdm(range(Delay_time),ncols = 60,desc = "冷却中"):
                    sleep(1)
        Run_times = Run_times + 1
        Run_times_all = Run_times_all + 1
        if (PreSet):  
            Avalon.info("进度: %d/%d | id: %d"%(Run_times_all,len(PreList),pid))
        title=GetTitle(pid)
        title["forum"]=re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_",title["forum"])
        title["post"]=re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_",title["post"])
        if not (Server or PreSet):
            lz=Avalon.ask("只看楼主?",False)
            comment=(Avalon.ask("包括评论?",True))
            DirName=Avalon.gets("文件夹名(空则表示使用\"吧名\\标题\"):")
            OutPutFileName=Avalon.gets("输出文件名(为空则为帖子id):")
            OutputHTML=Avalon.ask("输出HTML(否则表示输出Makrdown)?:",True)
            while(1):
                try:
                    OverWriteMode=(Avalon.gets("存在同名文件夹时操作? 0-交互 1-跳过 2-覆盖 3-备份 请输入(0/1/2/3) 为空则默认为3:"))
                    if (OverWriteMode == ""):
                        OverWriteMode = "3"
                    OverWriteMode = int(OverWriteMode)
                    if (OverWriteMode != 0 and OverWriteMode != 1 and OverWriteMode != 2 and OverWriteMode != 3):
                        Avalon.warning("请输入0/1/2/3")
                        continue
                    else:
                        break
                except:
                    pass
        title_name=re.sub(r'(/|\\|\?|\||\*|\:|\"|\<|\>|\.)','',title["post"])
        title_name = title_name.rstrip()
        if (len(DirName)==0):
            Avalon.info("帖子标题: " + title_name)
            DirName= (title["forum"]+"\\"+title_name)[0:40]
        if (len(OutPutFileName)==0):
            OutPutFileName = str(pid)
        Avalon.info("信息确认: id:%d , 选定:%s && %s评论 , 目录:\"%s\" , 文件名:\"%s%s\" , 文件夹冲突处理模式:%d"%(pid,("楼主" if lz else "全部"),("全" if comment else "无"),DirName,OutPutFileName,(".html" if OutputHTML else ".md"),OverWriteMode))
        Init(pid,OverWriteMode)
        GetPost(pid,lz,comment)
        Done()
        ConvertAudio()
    except KeyboardInterrupt:
        ForceStop()
        Avalon.error("Control-C,exiting",front="\n")
        if (exe_mode):
            input("按回车键退出...")
        sys.exit()
    except UserCancelled:
        Avalon.warning("用户取消")
    except RequestError as err:
        err=err.data
        Avalon.error("百度贴吧API返回错误,代码:%d\n描述:%s \n"%(err["code"],err["msg"]) + str(datetime.datetime.now()),front="\n\n")
        Error = True
    except Exception as err:
        ForceStop()
        Avalon.error("发生异常:\n" + traceback.format_exc() + str(datetime.datetime.now()),front="\n\n")
        if (exe_mode):
            input("按回车键退出...")
        sys.exit()
    else:
        Avalon.info("%d 已完成"%pid)
        if not (PreSet):
            end_time=timeit.default_timer()
            Avalon.info('\n运行用时: %s \n'%(str(datetime.timedelta(seconds=(end_time-start_time)))))
    if not (PreSet):
        break

if (not Error and Copy):
    try:
        copy_start_time=timeit.default_timer()
        Avalon.info("正在将" + DirName + "复制到" + CopyDir)
        try:
            shutil.rmtree(CopyDir)
        except:
            pass
        shutil.copytree(DirName,CopyDir)
        Avalon.info("已经将" + DirName + "复制到" + CopyDir)
        copy_end_time=timeit.default_timer()
        Avalon.info('复制用时: %s'%(str(datetime.timedelta(seconds=(copy_end_time-copy_start_time)))))
    except KeyboardInterrupt:
        ForceStop()
        Avalon.error("Control-C,exiting",front="\n")
        if (exe_mode):
            input("按回车键退出...")
        sys.exit()
    except UserCancelled:
        Avalon.warning("用户取消")
    except Exception as err:
        ForceStop()
        Avalon.error("发生异常:\n"+traceback.format_exc() + str(datetime.datetime.now()),front="\n\n")
        if (exe_mode):
            input("按回车键退出...")
        sys.exit()
elif (Error):
    Avalon.error("由于发生异常错误,本次部署取消")

if (Server):
    if (Auto_Clean and not Error):
        try:
            Avalon.info("正在清除以下目录:")
            Avalon.info(DelOlds(Auto_Clean_time))
            Avalon.info("以上目录已清除!")
        except:
            Avalon.error("未知错误,自动删除失败!")
    elif (Error):
        Avalon.error("由于发生异常错误,本次清理取消")

if (exe_mode):
    input("按回车键退出...")