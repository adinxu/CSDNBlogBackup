# -*- coding: utf-8 -*-

import re#正则表达式操作
import os#多种操作系统接口
import sys#系统相关的参数和函数
import chilkat

#报文头字符串
head_string="""
<html>
<head>
  <title>Evernote Export</title>
  <basefont face="微软雅黑" size="2" />
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
  <meta name="exporter-version" content="Evernote Windows/276127; Windows/6.3.9600;"/>
  <style>
    body, td {
      font-family: 微软雅黑;
      font-size: 10pt;
    }
  </style>
</head>
<body>
"""
#报文尾字符串
tail_string="""
</body>
</html>
"""

iter_count=0

#爬取文章列表
def extractBlogLists(user_name='m0_37565736',loop_times=1000):
    url="http://blog.csdn.net/{0}/".format(user_name)
    print("the user blog base url is {}".format(url))
    spider=chilkat.CkSpider()
    spider.Initialize(url)
    pattern=user_name+'/article/details'#具体文章路径的匹配模式
    file_path='URLList-'+user_name+'.txt'
    f=open(file_path,'w')
    url_count=0
    for i in range(0,loop_times):
        success = spider.CrawlNext()
        if (success == True):
            url=spider.lastUrl()
            m=re.search(pattern,url)
            if not m:
                continue#必须是指定用户的文章才保存链接
            url_count+=1
            print(url_count)
            print(url)
            title=spider.lastHtmlTitle().split(' -')[0]
            #Todo:可以加入去除用户名的处理
            #标题中有特殊符号时的处理
            specialpatt=r'[_\/:*?"<>|\n]'
            n=re.search(specialpatt,title)
            if n:
                print("old title is {0}".format(title))
                title=re.sub(specialpatt,'-',title)
                print("new title is {0}".format(title))
            f.write(url+","+title+'\n')
            #Print(The HTML META title)
            #print(spider.lastHtmlTitle().decode('gbk'))
        else:
            #Did we get an error or are there no more URLs to crawl?
            if (spider.get_NumUnspidered() == 0):
                print("No more URLs to spider")
            else:
                print(spider.lastErrorText())
        #Sleep 1 second before spidering the next URL.
        spider.SleepMs(1000)
    f.close()
    #对生产的文件进行备份
    open('URLList-'+user_name+'-backup.txt', "w").write(open(file_path, "r").read())

#下载所有文章
def downloadBlogLists(user_name='m0_37565736'):
    global iter_count
    mht = chilkat.CkMht()
    success = mht.UnlockComponent("Anything for 30-day trial")
    if (success != True):
        print((mht.lastErrorText()))
        sys.exit()

    file_path='URLList-'+user_name+'.txt'
    f=open(file_path,'r')
    fout=open('Error.txt','w')
    
    for line in f.readlines():
        m=re.search('(http.+[0-9]{7,}),(.+)',line)#文章链接最后必定为9位数字
        url=m.group(1)
        title=m.group(2)
        mht_doc = mht.getMHT(url)
        if (mht_doc == None ):
            print((mht.lastErrorText()))
            sys.exit()
            
        if not os.path.exists('CSDN-'+user_name):
            os.mkdir('CSDN-'+user_name)
        #Now extract the HTML and embedded objects:
        unpack_dir = "./CSDN-"+user_name+'/'
        html_filename = title+".html"
        parts_subdir = title
        success = mht.UnpackMHTString(mht_doc,unpack_dir,html_filename,parts_subdir)
        if (success != True):
            print(mht.lastErrorText())
            fout.write(line)
        else:
            print("Successfully Downloaded "+title)
    f.close()
    fout.close()
    if iter_count>=5:
        print("Some Blogs May Not Be Downloaded Successfully, Pleace Make Sure By Checking Error.txt And Index.html.")
        #移除本次结果，将上次结果作为本次处理的数据
        os.remove(file_path)
        os.rename('URLList-'+user_name+'-backup.txt',file_path)
    if iter_count<10 and os.path.getsize('Error.txt')>0:
        iter_count+=1
        print("进行第 "+str(iter_count)+" 次迭代下载")
        os.remove(file_path)
        os.rename('Error.txt',file_path)
        downloadBlogLists(user_name)

#生成索引页面
def generateIndex(user_name='m0_37565736'):
    file_path='URLList-'+user_name+'.txt'
    f=open(file_path,'r')
    #此处需指定编码方式，否则乱码
    fout=open('./CSDN-'+user_name+'/Index.html','w',encoding="utf-8")
    fout.write(head_string)
    fout.write("""<h2>"""+user_name+"的博客"+"""</h2>\n""")
    fout.write("""<ol>\n""")
    for line in f.readlines():
        m=re.search('(http.+[0-9]{7,}),(.+)',line)
        title=m.group(2)
        print(title)
        fout.write("""<li><a href=\""""+title+".html"+"""\">"""+title+"""</a></li>\n""")
    fout.write("""</ol>""")
    fout.write(tail_string)
    f.close()
    fout.close()


if __name__=='__main__':
    print("Please Input The Username Of Your CSDN Blog")
    user_name=input()
    if not user_name:
        user_name = "m0_37565736"
    print("Start Extracting  Blog List...")
    extractBlogLists(user_name)
    print("Start Downloading Blog List...")
    downloadBlogLists(user_name)
    print("Start Generating Index.html...")
    generateIndex(user_name)
    print("Done")
