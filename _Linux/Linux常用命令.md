## Linux常用命令

### 计算器

```
bc
	-scale=10	保留10位数
```
----------
### 显示日历

```
cal
	2016	一年的日历
	12 2016	某月的日历
```
----------
### 显示时间

```
date
	+%Y
```
----------
### 列出文件信息

```
ls				显示文件(list)
	-a	显示所有文件
	-l	显示文件详细信息
	-h	将占用的字节人性化显示
	-d	显示目录信息
	-i	显示 inode ID
	-s 	显示大小
	-1 	一行行显示

	--time=atime 	显示访问时间
	--time=ctime 	显示创建时间
	-R 	递归显示
```
----------
### 查看历史命令

```
history
	!numner	执行历史命令
```
----------
### 查看命令简短信息

```
whatis
```
----------
### 生成whatis库

```
makewhatis
```
----------
### 查找命令的目录及帮助文档的目录

```
whereis
	-b 		只显示二进制文件
	-m 		显示帮助文档
```
----------
### 查找命令所在的路径及有无别名

```
which
```
----------
### 查看配置文件简短信息

```
apropos
```
----------
### 查看命令帮助

```
man
	/search
		n/N  查找
		^search  开头
```
----------
### 将缓存中的内容写到磁盘中去

```
sync
```
----------
### 开关机

```
shutdown 
		 -r now		重启	
		 -k			显示通知信息不会真的关机
		 -h 10 		10分钟后关机
		 -h 8:20	到时间自己关机

reboot		重启
		-f	强制重启

poweroff	关机
		-f	强制关机
```
----------
### 运行级别

```
0　关机
1　单用户
2　不带网络的多用户
3　带网络的多用户
4　保留，用户可以自给定义
5　图形界面的多用户
6　重起系统

runlevel  # 显示当前环境级别

init number # 改变当前环境的级别

```
----------
### 图形文本界面互换

```
multi-user.target 		第3运行级
graphical.target 		第5运行级

1，设置开机模式为：命令模式
	systemctl set-default multi-user.target
	ln -sf /lib/systemd/system/multi-user.target /etc/systemd/system/default.target

2，设置开机模式为：图形模式
	systemctl set-default graphical.target
	ln -sf /lib/systemd/system/graphical.target /etc/systemd/system/default.target

startx	# 开启xwindow
```
----------
### 文件类型

```
-	普通文件
d 	文件夹
b 	块设备（U盘）
c 	字符型设备文件（鼠标）
l 	快捷方式（软连接）
```
----------
### 修改权限

```
chmod [{ugoa}{+-=}{rwx}][文件或目录]
	  [rwx=421][文件或目录]

	  -R 	递归修改
```
----------
### 修改文件所有者

```
chown -R root
chown -R root[:.]root /aa 	# 修改文件所有者及所属组

chgrp -R root /aa 			# 修改所属组
```
----------
### 文件访问权限说明

1. 文件夹的 x 代表是否可以进入该文件夹，如果没有 x，即使有w，其他用户也不可操作该文件将夹下的文件
2. 文件夹的 w 代表是否可以操作文件夹中的文件，当文件夹有 w 时，即使其他用户没有读该文件夹中文件的权限，该用户也可以删除文件
3. 文件夹没有 r 时，其他用户可以进入该文件夹但是不能读取该文件夹中的文件，但是可以创建文件，操作文件

----------
### 查看文件类型

```
file filename
```
----------
### 目录结构

```
/bin
/sbin
	相当于win32的作用

/boot
	主要存放启动Linux系统所必需的文件，包括内核文件、启动菜单配置文件等

/dev
	设备文件，字符设备，存储设备

/etc 
	主要存放系统配置文件
	
/lib
	主要存放一些库文件
	
/media 		自动挂载
/mnt 		手动挂载
	在某些Linux的发行版中用来挂载那些USB接口的移动硬盘（U盘）等
	
/opt
	可以理解为安装可选程序的地方。安装源码包

/proc
	内核参数，不占用磁盘大小

/root
	根用户的家目录。里面存放根目录的数据、文件等。
	
/usr
	主要存放安装的软件、系统共用的文件、内核源码等。

/tmp
	临时文件

/var
	缓存，日志，数据库文件
```
----------
### 查看系统信息

```
uname
	-i # 架构
	-r # 内核
	-a # 查看所有

cat /etc/redhat-release # CentOS Linux release 7.1.1503 (Final)

hostnamectl
		status 			查看操作系统信息
		--static		查看静态主机名
		--transient 	查看瞬态主机名
		--pretty 		查看灵活主机名

hostname 	# 主机名
```
----------
### 创建目录

```
mkdir
		-p	递归创建
		-p small/{bug,cat,hadoop}
```
----------
### 复制文件

```
cp	[item] resource target
	-r	复制目录
	-p	保留文件属性
	-u  新文件覆盖旧文件（旧文件不会覆盖新文件）
	-l  生成硬链接
	-f 	强制
	-a = -rfp
	-d 	默认情况下拷贝链接会把原文件拷贝出来，可以加该参数拷贝链接
```
----------
### 创建软硬链接

```
ln 	# 硬链接不能跨分区
	-s	创建软连接
```
----------
### 移动和改名

```
mv
	-i	询问要不要删除（默认）
	-r	递归
	-f	强制
```
----------
### 别名

```
alias ll # 显示别名

alias ll='ls -lh --color=auto' # 修改别名
```
----------
### 显示文件名目录名

```
basename 	# 只显示文件名
dirname 	# 只显示目录名
```
----------
### 浏览小文件信息

```
cat
	-n	显示行号
```
----------
### 反向浏览文件

```
tac
```
----------
### 不算空行显示行号

```
nl
	-d 	# 算空行显示行号
```
----------
### 浏览文件信息

```
more
	(空格)或f	翻页
	(Enter)		换行
	q或Q		退出
```
----------
### 浏览文件信息

```
less
	(空格)或f	翻页
	(Enter)		换行
	q或Q		退出
	上箭头		向上翻一行
	pgup		向上翻一页
	/XXX		搜索
	n			下一个搜索结果
	-N 			显示行号
```
----------
### 显示文件前几行

```
head
	-5	显示前5行
```
----------
### 显示文件后几行

```
tail
	-n	显示后几行
	-f	动态显示文件末尾内容（监视日志）或者 tailf
```
----------
### 查看非文本文件

```
od
	-t c 	# 以ASCII码格式显示输出

strings 	# 显示二进制文本文件
```
----------
### 删除文件

```
rm
	-r	删除目录
	-f	强制删除

rm -rf !(keep1 | keep2) 	# 删除keep1，keep2文件之外的文件
```
----------
### 显示当前目录

```
pwd
```
----------
### 创建文件

```
touch {a,b,c,d}
```
----------
### 权限过滤符

```
umask
	文件权限 = 666 - umask
	目录权限 = 777 - umask
```
----------
### 隐藏属性

```
lsattr		# 列出文件隐藏属性
chattr		# 修改文件隐藏属性
	+a （文件不可写，文件夹只可创建不可删除）
	+i （文件夹中，不可添加也不可删除文件）

SUID  	在命令所有者的位置上出现S代表其他人在执行该命令时具有所有者的权限
		chmod u+s xx
		chmod 4333 xx

SGID 	如果一个文件夹的的所属组中出现了S，代表着之后在该文件夹下创建的文件都将会继承该文件夹的所属组
		chmod g+s xx
		chmod 2333 xx

SBIT 	只出现在文件夹的其他人权限位，意思是除了root和所有者外其他人即使有权限也不能删除
		chmod o+t xx
		chmod 1333 xx
```
----------
### 在字符串中执行命令

```
echo "hostname is `hostname`"		
echo "hostname is $(hostname)"
```
----------
### 快速搜索

```
locate 	# 每天跟新一次数据库，新创建的文件可能找不到
		-i	不区分大小写

updatedb 	# 更新资料库
	/var/lib/mlocate/mlocate.db  	数据库位置
```
----------
### 查找文件

```
find path -option [argu] 		

	-or 			或关联关系
	-name			根据名称查找
	-size +5M		根据大小查找
	-size -5M -size +3M  	查找大于3M小于5M的文件
	-user smallbug	根据所有者查找
	-group			根据所属组查找
	-ctime +1  		创建超过1天的文件
	-cmin +1		创建时间超过一分钟
	-amin			访问时间
	-newer filename 查找比当前文件比较新的文件
	-perm 222			根据权限查找（2 -> o, 22 -> go）
			+222 		ugo只要有一个写权限就行
			-222 		ugo必须都有写权限
```
----------
### 分区介绍

```
1> 
MBR->[分区]->[分区]

MBR：引导程序(446) + 分区表(64) + 结束符(2)

一个分区需要16字节

2> 
[分区]

[block group]
boot sector -> { 
				[super block->文件系统描述信息->块位图->inode位图->inode表->block],
				[super block->文件系统描述信息->块位图->inode位图->inode表->block],
				[super block->文件系统描述信息->块位图->inode位图->inode表->block]
			}

super block : 存储了文件系统非常关键的信息用于向使用者描述当前文件系统的状态，例如block与inode的使用情况（总量和已使用量）、每个inode的大小、文件系统挂载点等等信息

文件系统描述信息 ：记录一个分区中的 block group 信息。

块位图 ：记录block区域中哪些block使用了，哪些没使用。

inode位图：同上

inode表：记录文件存放在哪些block中(128/4只能指向32个block)
	|--→直接区（12）
	|--→间接区（1）
	|--→二间接区（1）
	|--→三间接区（1）

```
----------
### 查看文件在哪些block中

```
filefrag -v cc
```
----------
### 查看分区信息

```
dumpe2fs  /dev/sda3

tune2fs -l /dev/sda5 	# 显示的是上面信息的头部部分
```
----------
### 显示文件夹大小

```
du
	-s 	单层显示
	-h 	人性化显示
```
----------
### 显示已挂载磁盘信息

```
df
	-h  人性化显示
	-T   显示文件类型
```
----------
### 分区操作

```
1>
	fdisk -l            查看分区情况(有多个硬盘的话可以加硬盘名)

2>
	fdisk /dev/sda      给sda分区
3> 
		## m查看帮助
   a   toggle a bootable flag                
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition 	//删除分区
   g   create a new empty GPT partition table
   G   create an IRIX (SGI) partition table
   l   list known partition types 	//列出分区类型
   m   print this menu
   n   add a new partition 	//创建一个新的分区
   o   create a new empty DOS partition table 	
   p   print the partition table 	//显示分区表
   q   quit without saving changes 	//不保存退出
   s   create a new empty Sun disklabel
   t   change a partition's system id 	//修改分区类型
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit 	//保存并推出
   x   extra functionality (experts only)

4>
	partprobe [/dev/sda]    //更新分区表

5> 
	mkfs -t ext3 /dev/sda5    格式化分区(=mkfs.ext3 /dev/sda5)
	mkfs -t ext3 -b 4096 /dev/sda5   //每一个block是4k

6>
	mount /dev/sda5 /mnt   //挂载
	umount /dev/sda5     //卸载

	mount -o remount,ro /mnt  		 //以只读的形式挂载（remount：重新挂载，先卸载再挂载）
	mount -o remount,rw /mnt 		//读写权限
	mount -o remount,noexec /mnt  	//无执行权限
	mount -o loop xx.iso /mnt 		//挂载镜像
	vim /etc/fstab   				//永久挂载
									（/dev/sda5   /home/smallbug/workspace   ext3    defaults   0 0）
									（defaults：默认权限，0：是否要做备份    0：是否用fsck检查）
```
----------
### 检查磁盘

```
fsck -f(强制检查) -C（显示进度）/dev/sda4
```
----------
### 检查坏道

```
badblock  -sv（进度）/dev/sda4
```
----------
### 查看哪个进程占用该磁盘

```
fuser -mv /mnt
```
----------
### 查看交换分区

```
cat /proc/swaps
```
----------
### 将Linux文件格式转换为windows格式

```
unix2dos -n 123 345
```
----------
### 压缩备份

```
1>
gzip 	# 压缩文件为 *.gz
		-d 	# 解压
		gzip -c hosts > hosts.gz 	# 压缩时保留源文件

2> 
zcat 	# 查看gzip压缩过的文件

3> 
gunzip(gzip -d) 	# 解压缩文件

4>
zip 		-r	压缩目录
	解压：unzip FileName.zip
	压缩：zip FileName.zip DirName

5> 
bzip2	压缩文件
		-k	产生压缩文件后保留原文件
		-d  解压
		bzip2 -c hosts > hosts.bz2    缩时保留源文件

bzcat 查看bzip2压缩过的文件

bunzip2	解压缩文件

6> 
tar			打包文件
		-c	打包（-x	解包）
		-v	显示详细信息
		-f	指定文件名
		-z	打包同时压缩（解压缩）（gzip）
		-j	打包同时压缩（解压缩）（bzip2）
		-t  不解档的情况下，查看文件内容
		-C 目录   指定解档目录

tar zcvf mkd.tar.gz ./mkd/

7> 
创建ISO镜像
	mkisofs -o xx.iso file1 file2 file3

cp /dev/cdrom xxx.iso
	直接将光盘中的文件复制成iso镜像

8>
dd if=/dev/sda5 of=test   将sda5分区中的数据备份到test中

dd if=/dev/zero of=file bs=1M count=100 		## 创建100M文件file
```
----------
### vim程序编辑器

```
vi filename(进入)--->命令模式
	 :wq(退出)------>命令模式
						|	 
						|ESC
						|
	 iao------------>插入模式
	 
a	在光标所在字符后插入
A	在光标所在行尾插入
i	在光标所在字符前插入
I	在光标所在行行首插入
o	在光标下插入新行
O	在光标上插入新行

:set nu		设置行号
:set nonu	取消行号

gg			到第一行
G			到最后一行
nG			到第n行
:n			到第n行

$			移至行尾
0			移至行首

x			删除光标所在处字符
nx			删除光标所在处后n个字符
dd			删除光标所在行
ndd			删除n行
dG			删除光标所在行到文件末尾内容
D			删除光标所在处到文件末尾内容
:n1,n2d		删除指定范围的行

yy			复制当前行
nyy			复制当前行以下n行
dd			剪切当前行
ndd			剪切当前行以下n行
p、P		粘贴在当前光标所在行下或行上

r			取代光标所在处字符
R			从光标所在处开始替换字符，按ESC结束
u			取消上一步操作

/string		搜索指定字符串
			搜索时忽略大小写:set ic
n			搜索指定字符串的下一个出现的位置

:%s/old/new/g(不询问)c(询问)		全文替换指定的字符串
:n1,n2s/old/new/g					在一定范围内替换指定字符串

:W					保存修改
:W new_filename		另存为指定文件
:wq					保存修改并退出
ZZ					快捷键，保存修改并退出
:q!					不保存修改退出
:wq!				保存修改并退出（文件所有者及root可以使用）
	 
:r 文件名			将文件中的所有内容导入到该文件中
: !命令				执行命令
:map Ctrl+v Ctrl+()	增加快捷键

:n1,n2s/^/#/g		注释多行

:ab 				打出a换成b
:sp        分屏
ctrl+w     切换
:only      取消分屏

/home/username/.vimrc		普通用户设置vim快捷键
/root/.vimrc				root用户设置vim快捷键

插入列,例如我们在每一行前都插入"() "：
	1.光标定位到要操作的地方。
	2.CTRL+v 进入“可视 块”模式，选取这一列操作多少行。
	3.SHIFT+i(I) 输入要插入的内容。
	4.ESC 按两次，会在每行的选定的区域出现插入的内容。


vim插件：
	1>https://github.com/ma6174/vim
				编写python程序

				自动插入头信息：
				#!/usr/bin/env python
				# coding=utf-8
				输入.或按TAB键会触发代码补全功能
				:w保存代码之后会自动检查代码错误与规范
				按F6可以按pep8格式对代码格式优化
				按F5可以一键执行代码
				多窗口操作

				使用:sp + 文件名可以水平分割窗口
				使用:vs + 文件名可以垂直分割窗口
				使用Ctrl + w可以快速在窗口间切换
				编写markdown文件

				编写markdown文件(*.md)的时候，在normal模式下按 md 即可在当前目录下生成相应的html文件
				生成之后还是在normal模式按fi可以使用firefox打开相应的html文件预览
				当然也可以使用万能的F5键来一键转换并打开预览
				如果打开过程中屏幕出现一些混乱信息，可以按Ctrl + l来恢复
				快速注释

				按\ 可以根据文件类型自动注释
				
	2>https://github.com/amix/vimrc
```
----------
### 用户信息查看

```
/etc/passwd 	# 用户信息存放目录

/etc/shadow 	# 用户密码存放目录

/etc/group 		# 组的存放目录
```
----------
### 统计文件字数行数
```
wc
	-l 	# 查看行数
	-w 	# 查看字数
	-c 	# 统计字节数
```
----------
### UID & passwd

```
1>
uid标志一个用户
每一个UID对应一个用户，root的UID是0，1~499是系统用户UID，500~65535是普通用户

2>
passwd  每一行是6个冒号分成7部分
repository:x:1000:1000:repository:/home/repository:/bin/bash
用户名:密码占位符:UID:GID:注释信息:家目录:shell信息
```
----------
### 用户用户组管理

```
groupadd bob   # 添加一个组
groupdel bob   # 删除一个组

gpasswd -a smallbug root   # 将smallbug添加到root组中
		-d 删除

groups smallbug 		查看smallbug用户的所属组

newgrp root //临时切换默认组(exit可恢复到原状态)


useradd			添加用户
	-D  查看创建用户时的默认值
	-c "注释"
	-s  制指定shell
	-d  家目录
	-g  组（不创建组，只分配到默认组）
	-G  root 除了创建本组外还会将用户添加到root组中
	-u  UID

vim /etc/default/useradd    修改默认值

/sbin/nologin 		只能登陆服务不能登陆主机

usermod -c "修改用户信息" repository

userdel -r 删除用户


usermod 		可用来修改用户帐号的各项设定。
	　-c<备注> 　修改用户帐号的备注文字。 
	　-d登入目录> 　修改用户登入时的目录。 
	　-e<有效期限> 　修改帐号的有效期限。 
	　-f<缓冲天数> 　修改在密码过期后多少天即关闭该帐号。 
	　-g<群组> 　修改用户所属的群组。 
	　-G<群组> 　修改用户所属的附加群组。 
	　-l<帐号名称> 　修改用户帐号名称。 
	　-L 　锁定用户密码，使密码无效。 
	　-s<shell> 　修改用户登入后所使用的shell。 
	　-u<uid> 　修改用户ID。 
	　-U 　解除密码锁定。


查看系统中有哪些用户：cut -d : -f 1 /etc/passwd

查看可以登录系统的用户：cat /etc/passwd | grep -v /sbin/nologin | cut -d : -f 1

查看用户登录历史记录：last

```
----------
### 密码操作

```
password smallbug 		修改smallbug的密码

sudo passwd -S smallbug 	查看smallbug密码的加密方式

passwd -S repositpry   //查看密码信息

passwd -d repository   //清空密码
		-l //锁定账号信息（=usermod -L smallbug）
		-u  //解锁（=usermod -U smallbug）

echo $xx | passwd --stdin tom 		脚本方式修改密码
```
----------
### 查看用户UID，GID，GROUPS

```
$> id tom

uid=1001(tom) gid=1001(tom) groups=1001(tom)

```
----------
### 当前有哪些用户登录

```
who
```
----------
### 查看是否开启信息功能

```
mesg 	# 即使关闭，root发送的信息也可看到

write tom pts/3 		写信息
		你好
```
----------
### 查看当前在线用户

```
w
```
----------
### 查看后台进程

```
jobs
```
----------
### 运行后台进程

```
bg 1
```
----------
### 将进程重新调到前台

```
fg 1
```
----------
### 杀死后台进程号为1的进程

```
kill -9 %1 		

kill -l  查看所有信号

killall -9 java   直接杀死进程
```
----------
### 关闭远程客户端程序依然在运行

```
nohup ping www.baidu.com & 
```
----------
### ps命令

```
ps -l		当前shell运行的程序

ps -aux 	显示所有进程，所有者，详细信息

ps -ex -o comm,%cpu    查看进程名及对应的CPU使用情况
			   %mem   内存使用率
			   pid    显示pid
			   stat    显示进程状态
			   		R 正在运行
			   		Z 僵尸状态
			   		T 停止状态
			   		S 睡眠状态


ps -ex -o comm,%cpu,%mem,pid,stat

```
----------
### 查看某一个PID是多少

```
pidof  bash
```
----------
### 进程查看优先级改变

```
top  动态显示资源使用状态

top -d 1   一秒钟刷新一次状态

优先级=优先系数+nice值（-20~19）（最高~最低）

1> 在top中r修改nice值，改变进程优先级

2> PID to renice [default pid = 25593]

3> Renice PID 23369 to value -12

renice -20 2061   修改PID为2061的进程将其nice值改成-20

nice -n -19  cat  以nice值为-19来运行cat命令

```
----------
### 显示内存及交换分区的使用情况

```
free -h # 人性化显示
```
----------
### 时间查看

```
uptime  # 当前时间，系统运行时间，连接用户，系统负荷
```
----------
### 系统资源状态

```
vmstat 1 3     1s执行一次，执行3次
```
----------
### 查看有哪些端口处于监听状态

```
netstat -ntul 	# n:做反向解析
```
----------
### 显示进程树

```
pstree -u 
```
----------
### 查看系统中的服务

```
ls -al /usr/lib/systemd/system
```
----------
### 编译安装

```
yum install gcc-c++ libstdc++-devel

安装未指定目录默认路径是 /usr/local
./configure --prefix=/opt/XXX   指明安装目录

生成makeFile文件之后 make & make install
```
----------
### rpm & yum

```
1> 
rpm：
	-ivh  i安装 v显示过程  h调用数字签名（--force强制安装）
	-qa   查看当前系统所安装的所有软件包
	-ql   查看软件安装目录
	-qc   查看软件安装配置文件
	-qd   查看帮助文档
	-qi   查看详细信息
	-qf   查看该软件由哪个软件包安装的
	-K    验证rpm包是否是官方原版（rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7）
	-qlp  查看rpm包的安装目录
	-e    卸载软件 （--nodeps  忽略软件包的依赖关系）
	-Uvh  更新软件
	--test                            安装测试，并不实际安装
	--replacepkge                    无论软件包是否已被安装，都强行安装软件包

2>
yum [options] [command] [package ...]

	-h 		帮助
	-y 		当安装过程提示选择全部为"yes"
	-q 		不显示安装的过程

yum install yum-fastestmirror 		自动搜索最快镜像插件

yum install yumex 					安装yum图形窗口插件

yum grouplist 						查看可能批量安装的列表

1 安装
	yum install 全部安装
	yum install package1 安装指定的安装包package1
	yum groupinsall group1 安装程序组group1

2 更新和升级
	yum update 全部更新
	yum update package1 更新指定程序包package1
	yum check-update 检查可更新的程序
	yum upgrade package1 升级指定程序包package1
	yum groupupdate group1 升级程序组group1

3 查找和显示
	yum info package1 显示安装包信息package1
	yum list 显示所有已经安装和可以安装的程序包
	yum list package1\* 显示指定程序包安装情况package1，\*代表后面字符不受限制
	yum search package 查看远程和本地可用的包
	yum groupinfo group1 显示程序组group1信息yum search string 根据关键字string查找安装包

4 删除程序
	yum remove package1 删除程序包package1
		-y 不会询问，直接卸载
		
	yum groupremove group1 删除程序组group1
	yum deplist package1 查看程序package1依赖情况

5 清除缓存
	yum clean packages 清除缓存目录下的软件包
	yum clean headers 清除缓存目录下的 headers
	yum clean oldheaders 清除缓存目录下旧的 headers
	yum clean, yum clean all (= yum clean packages; yum clean oldheaders) 清除缓存目录下的软件包及旧的headers
	
```
----------