# JVM

## Paralle Scavenge
新生代，复制算法，多线程收集器。与之前区别在于关注可控制的吞吐量，吞吐量 = 运行用户时间 / (运行用户代码时间 + 垃圾收集时间)，此外，提供GC自适应调节策略（GC Ergonomics，-XX:+UseAdaptiveSizePolicy）。配置如下两个优化目标：
    - 可以控制最大垃圾收集停顿时间 -XX:MaxGCPauseMills（减少参数，是以频繁垃圾收集为代价）；
    - 设置吞吐量大小-XX:GCTimeRatio（0-100, etc.  19 -> (1 / (1 + 19), 5%)，99 -> (1 / (1 + 99), 1%)）

## Serial Old收集器
Serial收集器的老年代版本，单线程收集器，在Client模式（管理虚拟内存较少）下虚拟机使用。
Server模式下，
    - JDK1.5以及之前的版本中，与Parallel Scavenge收集器搭配使用；
    - CMS收集器的后备预案，在并发收集发生Concurrent Mode Failure时使用。
    
## Parallel Old收集器
Parallel Scavenge收集器的老年代版本，使用多线程和“标记-整理”算法。（from JDK 1.6，注重吞吐量和CPU资源敏感场合）

## CMS收集器
基于“标记-清除”算法，注重最短回收停顿时间，重视服务响应速度。称之为并发低停顿收集器。
    - 初始标记，Stop The World，标记直接关联到的对象，单线程。
    - 并发标记，GC Root Tracing，与用户线程一起工作。
    - 重新标记，修正并发标记期，因用户程序继续运作而导致标记产生变动的那一部分对象的标记记录（也会停顿，时间比初始标记稍长，比并发标记短）。
    - 并发清除，与用户线程一起工作。<br>
缺点：
    - 不利于CPU资源敏感，与用户线程并发执行，导致占用用户资源，当CPU数量不足4个尤为明显。（默认启动回收线程数：CPU数量 + 3 / 4）;
    - 无法处理浮动垃圾（Floating Garbage），在标记之后，产生新的垃圾，可能导致“Concurrent Mode Failure”，引起Full GC。此外，在运行中，保留部分内存空间给用户线程使用，（JDK 1.6 92%），当老年代增长过快，导致预留内存不足，出现“Concurrent Mode Failure”，启动后备方案：Serial Old收集器。（预留内存通过-XX:CMSInitiatingOccupancyFraction设置，触发百分比）
    - “标记-清除”算法，导致内存碎片过多，无法分配大对象，于是，提供一个碎片整理功能，-XX:+UseCMSCompactAtFullCollection（默认开启），同样，导致回收时间变长。此外，提供一个-XX:CMSFullGCsBeforeCompaction，设置执行多少次不压缩Full GC后，进行一次带压缩的。
    
    
    
## G1收集器
面向服务端应用的垃圾收集器，关注点也是降低停顿时间。G1收集器划分内存模型方式：将JAVA划分为多个大小相等的区域（Region)，追踪每个Region中垃圾堆积的价值（回收空间大小和回收所需时间的经验值），维护一个优先级列表，每次根据允许的时间值，回收价值最大的Region（在有限时间内，提高效率）。<br>
这里存在一个问题，就是如果不同Region之间存在互相引用，如何Tracing是否对象可清理。如何解决？通过RemeberSet方式，每次对Reference写操作，产生一个Write Barrier暂时中断写操作，检查Reference引用对象是否在不同的Region（或者老年代引用新生代），如果是，则通过CardTable把相关应用信息记录到被应用对象Region的RemeberSet中。（通过遍历RemeberSet，就可以不用全堆扫描）    
    
- 初始标记(Initial Marking)
标记直接关联对象，修改TAMS(Next Top at Mark Start)的值，让下一阶段直接在Region中执行，此阶段需要Stop The World。

- 并发标记(Concurrnet Marking)
从GC Root开始进行可达性分析，找出存活对象，耗时长，可与用户线程并发执行。

- 最终标记(Final Marking)
修正在并发标记期间因用户程序继续运作而产生变化的标记记录，将这段时间的对象变化记录在Remebered Set Logs，然后将Remebered Set Logs的数据合并到Remebered Set中。此阶段停顿线程（也可并发执行）。

- 筛选回收(Live Data Counting and Evacuation)
对各个Region回收价值和成本进行排序，根据用户期望的停顿时间执行回收计划。需要停顿，也可并发执行，但是只回收一部分Region，时间是可控的，停顿大幅提高效率。

特点：
- 并行与并发，并行可以充分利用多个CPU优势，采用多线程标记，缩短Stop the World时间；并发可以让Java用户线程同时进行；
- 分代收集，采用不同方式处理新对象和老对象；
- 空间整合，从整体看是“标记-整理”的算法，从局部（两个Region之间）基于“复制”的算法，
- 可预测停顿*，G1跟踪各个Region里面的垃圾堆积价值大小（回收空间大小/所需时间的经验值），后台维护一个优先级列表，每次根据允许时间，优先回收价值最大的Region。

## 内存分配回收规则
	Client模式，默认是Serial/Serial Old收集器。
1. 对象优先在新生代Eden分配，
当没有足够空间，虚拟机将发起一次MinorGC。当Minor GC结束，会将Eden中分配的对象移动到Survivor中，而Survivor大小不足以存储存在对象，则直接移入老年代；

2. 大对象（需要大量连续内存空间的对象），直接进入老年代；
-XX：PretenureSizeThreshold=3145728，令大于这个值直接在老年代分配（避免大量内存拷贝）。此参数只对Serial和ParNew两款收集器有效（Parallell Scavenge无效）

3. 长期存活对象进入老年代；
如何判断对象进入新生代还是老年代？一个对象，拥有一个对象年龄（Age）计数器，在Eden出生并经过第一次Minor GC后，仍然存活并被survivor容纳，则对象年龄记为1，每经历一次Minor GC，年龄加1。当年龄增加到一定值（默认值为15），进入老年代。通过-XX:MaxTenuringThreshold设置，晋升老年代年龄阈值。

4. 动态对象年龄判定；	
如果Survivor空间中相同年龄对象的大小总和大于Survivor空间的一半，年龄大于或等于该年龄的对象可以直接进入老年代（无需满足MaxTenuringThreshold设置）。

5. 空间分配担保；
在发生MinorGC时，虚拟机检测之前每次晋升到老年代的平均大小（经验值）是否大于老年代的剩余空间大小，如果大于，则改为直接进行一次Full GC。如果小于，则查看HandlerPromotionFailure设置是否允许担保失败；如果允许，那只会进行Minor GC，如果不允许，则进行一次Full GC。（如果这次晋升的对象很大，超出老年代容纳范围，会产生HandlePromotionFailure失败，发生Full GC）
> 注：JDK6 Update 24之后，HandlePromotionFailure参数不在影响虚拟机空间担保策略，规则变为，只要老年代的连续空间大于新生代对象总大小或者历次晋升的平均大小就会进行MinorGC，否则进行FullGC。

    
> Minor GC和 Full GC的区别：
> 新生代GC(Minor GC)：指发生在新生代的垃圾收集动作，发生频繁，收集速度快；
> 老年代GC(Major GC/Full GC)：老年代垃圾收集，不同的垃圾收集器实现不同（一般之前有一次MinorGC，也可能不存在），Major GC速度一般比Minor GC慢十倍以上。

    
    
    
    
    

