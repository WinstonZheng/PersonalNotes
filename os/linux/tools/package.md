# 简介
常见linux发行版分为两大类：
1. RedHat 系列：Redhat、Centos、Fedora 等
2. Debian 系列：Debian、Ubuntu 等

由这两大类对软件包管理模块进行划分：
1. Dpkg(Debian系): Ubuntu
2. RPM(Red Hat系): CentOS、Fedora

# Debian系列
- 常见的安装包格式 deb 包，安装 deb 包的命令是“dpkg -参数”
- 包管理工具 apt-get
- 支持 tar 包

apt-get建立在dpkg基础上对软件包进行管理，维护软件包的管理数据库。
1. apt会解决模块之间的依赖问题，并咨询软件仓库，但不会安装本地deb文件。
2. dpkg用于安装本地.deb文件，不解决依赖模块的依赖关系，不关系ubuntu软件仓库里面的软件。
3. aptitude，aptitude 与 apt-get一样，是 Debian 及其衍生系统中功能极其强大的包管理工具。与apt-get不同的是，aptitude 在处理依赖问题上更佳一些。举例来说，aptitude 在删除一个包时，会同时删除本身所依赖的包。这样，系统中不会残留无用的包，整个系统更为干净。
> 注：一般情况下，建议用apt-get安装常用软件，维护良好的ubuntu软件仓库。如果apt-get维护的软件源中无法找到满足版本的软件，再考虑用dpkg安装deb包。（不建议apt-get和aptitude互相混用，一般只用一个软件包管理工具，因为两者安装包互相不可见）

# RedHat系列
- 常见安装包格式rpm包，安装rpm包的命令是“rpm -参数”
- 包管理工具yum
- 支持tar包

1. rpm(RedHat Package Manager)，用于redhat系列发行版的包管理工具，不具备处理rpm包间依赖的能力。
2. yum(yellow dog Updater modified)，是一个在Fedora和RedHat以及SUSE中的Shell前端软件包管理器。基於RPM包管理，能够从指定的服务器自动下载RPM包并且安装，可以自动处理依赖性关系，并且一次安装所有依赖的软体包，无须繁琐地一次次下载、安装。



# 推荐
http://blog.csdn.net/buguyiqie/article/details/4948661
> 讲的很详细，apt相关的原理用法等，有兴趣和时间，可以看一下。