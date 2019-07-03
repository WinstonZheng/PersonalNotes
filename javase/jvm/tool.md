# 性能监控与故障处理工具
**SunJDK的工具包**
a. jps：虚拟机进程状况工具，可以查询虚拟机进程的LVMID（对本地虚拟机进程而言，与本地进程ID一致）；
b. jstat：用于监控虚拟机运行状态信息的工具（本地/远程，类装载、内存、垃圾收集、JIT编译等），远程查询；
c. jinfo：实时查看和调整虚拟机参数；
d. jmap：用于生成堆转储快照（一般称为heapdump或dump文件），还可查询finalize执行队列、Java堆和永久代（JDK1.7后不存在了）详细信息；
e. jhat：虚拟机堆转储快照分析工具，与jmap搭配使用，分析dump文件，内置微型HTTP/HTML服务器，通过浏览器查看；
f. jstack：堆栈跟踪工具，用于生成当前时刻线程快照（一般称为threaddump或者javacore文件），主要目的在于定位线程出现长时间停顿原因。
g. HSDIS是SUN官方推荐HotSpot虚拟机JIT编译代码的反汇编插件（将本地代码还原成汇编，加注释）。
h. JDK可视化工具，JConsole和VisualVM。
