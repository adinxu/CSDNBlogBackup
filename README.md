## <span style="color:green;">写在前面@adinxu</span>
<span style="color:green;">我本来是想要把csdn博客迁移到github page上，网站啥的都搞好了，但是把文章挪过来却是个麻烦事。  
在github上搜索发现了这个项目，下载下来，当时安装chilkat库时好像就因为site-packet结果报错，折腾了一会。后来安装好也没正常运行。我看见了下上次commit时间是2016年了，今天花了点时间看了看python，之前没学过，看的也头晕眼花，用惯了c语言的我，一边看，一边经常在说：还能这样？看完之后先用2to3把文件转了，因为我用的python3，而很明显，原来是Python2的。然后只有一个编码问题需要解决就ok了。虽然这个脚本可以完美运行了，但还是不是我想要的。我想要的是提取出markdown文件，方便修改，而且需要取出创建日期，用以给markdown文件命名，因为这是github page对post的要求。其他的元数据里的分类和tag就不说了。不过好歹是把文章全都下下来了，虽然全部都是html格式的。等我再找找吧。  
ps:CSDNBlogBackup.py.bak是原始文件的备份，也就是python2的脚本，而CSDNBlogBackup.py是python3脚本，方便直接比较查看修改内容。
</span>

# Python实现CSDN博客的完美备份

## 出发点

之所以造这个轮子无非是现有的轮子不好使，CSDN官网是推出的博客备份在系统中读不到博客数据，打开后还会闪退，其他人写的工具，要么是收费，要么只是对网页的下载，不能完整的下载网页中嵌入的图片等各种资源。

于是自己花几个小时写了这个工具，其特点是可以做到CSDN博客的完美备份，下载整个网页，包括网页中的图片，css，js等，可以做到博客的完整备份。


## 功能

1 CSDN博客的完美备份；

2 下载整个博客网页，包括图片，css，js等各种资源；

3 生成Index.html方便对本地博客的浏览；

4 完全免费，开源。


## 效果截图

利用整个脚本已经把自己的博客做了完整备份，一些截图如下：


这是下载完成后文件夹里的部分内容，所有网页对应的图片等资源都放到了同名文件夹中。

<img src="https://github.com/lanbing510/CSDNBlogBackup/blob/master/screenshots/downloaded.jpg" width="100%" height="100%">


这是Inde下.html索引文件：

<img src="https://github.com/lanbing510/CSDNBlogBackup/blob/master/screenshots/index.png" width="100%" height="100%">


这是部分博客内容的展示，其对图片和公式都能非常好的支持，即便公式是用mathjax写的（因为下载了网页需要的所有资源，包括js）。

<img src="https://github.com/lanbing510/CSDNBlogBackup/blob/master/screenshots/blog.png" width="100%" height="100%">



## 运行环境

1 python；

2 python的chilkat库。

## 使用说明

使用时直接双击CSDNBlogBackup.py，输入你要备份的CSDN的用户名，等待下载完成即可。

## 注

可以自己各种DIY做各种其他博客的备份。Enjoy It!

