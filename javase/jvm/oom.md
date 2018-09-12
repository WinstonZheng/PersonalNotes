# 查漏补缺

## Class文件
以Big-Endian方式存储，高位存在地址。
- 魔数，4个字节，标识是否是Class文件（0xCAFEBABE）；
- Class版本号，4个字节（向下兼容）；
- 常量池，表类型数据项目（从1开始）；
    - 字面量，文本字符串、声明为final的常量值等；
    - 符号引用，类和接口全限定名/字段名称和描述符/方法名称和描述符。




# 解决OOM问题

## 内存溢出和内存泄漏
- 内存溢出，指程序在运行过程中无法申请到足够的内存而发生错误。内存溢出通常发生于OLD段或Perm段垃圾回收后，仍然无内存空间容纳新的Java对象的情况。
- 内存泄露，指程序中动态分配内存给一些临时对象，但是对象不会被GC所回收，它始终占用内存。即被分配的对象可达但已无用。

## OOM发生的区域
一般发生OOM的原因发生在如下几种可能：
1. 多线程情况下，虚拟机栈和本地方法栈溢出（单线程，是StackOverFlowError）；
2. 方法区（运行时常量区）发生溢出，由于1.8将方法区移动到本地内存（一般存在频繁类加载和卸载的程序）；
3. 堆区，对象频繁申请和释放的区域。


## 定位OOM问题
### 堆

```java
/* 
 * -Xms20M : 堆的最小值为20m 
 * -Xmx20M : 堆的最大值为20m，最大值和最小值相同，可以避免堆自动扩展 
 * -Xmn10M : 新生代大小为10m 
 * -XX:+PrintGCDetails : 打印辅助信息 
 * -XX:SurvivorRatio=8 : Java 堆中的Eden区与Survivor区的大小比值，设置为8,则两个Survivor区与一个Eden区的比值为2:8,一个Survivor区占整个年轻代的1/10 
 * -XX:+HeapDumpOnOutOfMemoryError : 当出现内存溢出异常时，dump出当前的内存转储快照信息以便后期分析 
 */  
 
   
/** 
 * 如何处理堆内存溢出？ 
 * 通过EMA eclipse memory analyzer 打开堆内存转储文件 
 * 首先分清是内存泄露还是内存溢出 
 * 如果是内存泄露：通过工具查看泄露对象到GC Roots的引用链，然后找出泄露对象是通过怎样的路径与GC roots 相关联并导致垃圾回收器无法自动回收他们的 
 * 如果不存在泄露，也就是说内存中的对象还活着，那就应当检查虚拟机的堆参数 -Xmx -Xms 是否可以适当的调整 
 * 
 */  
```

步骤分析：
1. 查看服务器运行日志以及项目输出的日志，捕捉到内存溢出异常（根据日志定位到抛出信息），通过打印出GC日志，也能定位问题；（或者可以通过jconsole等工具，监控JVM运行情况）
2. 通过手动（jmap工具）/自动（-XX:+HeapDumpOnOutOfMemoryError），获取dump文件；
3. 通过EMA工具分析dump文件，查看占用内存最多的一块区域。EMA支持多种视图：
 - 查看全局内存；
 - 内存泄漏分析；
 - 大对象排序。

> 此种方法，针对大多数的堆内存的OOM，能够解决。

### 线程

另一种可能，是线程启动过多（未关闭线程池），出现如下错误：
```java
java.lang.OutOfMemoryError: unable to create new native thread
	at java.lang.Thread.start0(Native Method)[:1.8.0_121]
	at java.lang.Thread.start(Thread.java:714)[:1.8.0_121]
```
解决方案：
1. 修改代码，采用线程池；
2. 减少分配给Java程序堆的大小（线程占用内存 = 系统内存 - 分配给Java的内存）；
3. 加大物理内存。


### 本地直接内存
发现OOM后Dump文件很小，而程序中使用了NIO（比如使用了Netty这类框架）。


## Jvm调优
- 根据当前的运行的应用程序特点采用不同的GC收集器（批处理 CMS / 用户交互 G1）;
- 




# Reference
- [测试OOM异常](https://blog.csdn.net/evilcry2012/article/details/79050362)
- [MAT使用](https://www.cnblogs.com/larack/p/6071209.html)
