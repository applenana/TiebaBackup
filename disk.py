import os
import tqdm
def execCmd(cmd):
  r = os.popen(cmd)
  text = r.read()
  r.close()
  return text
cmd='df -h'
content=execCmd(cmd)
total=content.split("\n")[10].split()[1]
now=content.split("\n")[10].split()[2]
Left=content.split("\n")[10].split()[3]
percent=content.split("\n")[10].split()[4]
print("<h3 align='center'>"+"服务器硬盘总空间"+total+"</h3>")
print("<h3 align='center'>"+"现在已经使用"+now+"</h3>")
print("<h3 align='center'>"+"仍可用"+Left+"</h3>")
print("<h3 align='center'>"+"文件占用空间"+percent+"</h3>")
print("<h3 align='center'>"+"仍可备份"+str(int(Left.replace("G",""))//2)+"份帖子</h3>")