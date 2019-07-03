# JVM内存管理
## JVM运行时数据区
 JVM运行时的数据区域，可以理解为Java程序在运行时，数据存放的位置。主要分为7个部分（理论模型）：
 
 1. 程序计数器，保存当前程序执行的内存地址（字节码的行号）。用于分支、循环、跳转、异常处理和线程恢复等基础功能；
 2. Java虚拟机栈，线程私有，一个栈包含多个栈帧(Flames)，进入一个方法新建一个栈帧，栈帧包含局部变量表（存储变量值，引用变量记录指向堆的地址）、操作数栈（用于存储操作数，中间结果）、动态链接（运行时多态）、方法出口等信息；
 3. 本地方法栈（native），由本地代码实现，类似于栈；
 4. 直接内存，NIO调用Native函数库直接分配堆外内存，通过DirectByteBuffer对象作为这块内存的引用进行操作。（提高性能避免Java堆和Native堆来回复制数据）。
 5. Java堆，线程共享，存储从类中新建的实例对象，垃圾收集器管理的主要区域；
 6. 方法区，各线程共享区域，存储如下内容：
  - 类加载器引用(classLoader)；
  - 运行时常量池：所有常量、字段引用、方法引用、属性
  - 字段数据：每个方法的名字、类型(如类的全路径名、类型或接口) 、修饰符（如public、abstract、final）、属性
  - 方法数据：每个方法的名字、返回类型、参数类型(按顺序)、修饰符、属性
  - 方法代码：每个方法的字节码、操作数栈大小、局部变量大小、局部变量表、异常表和每个异常处理的开始位置、结束位置、代码处理在程序计数器中的偏移地址、被捕获的异常类的常量池索引

### 方法区实现(HotSpot)
方法区的实现在1.8之前称为永久代。永久代的垃圾收集是和老年代(old generation)捆绑在一起的，因此无论谁满了，都会触发永久代和老年代的垃圾收集。

 JDK1.7，存储在永久代中部分转移到Heap或Native Heap中。
- 字符串常量池从Perm区移到Java的Heap区域（同时，字符串常量池能够存储字符对象的引用）。
- 符号引用被移到了native heap；
- 字面量(interned strings)被移到了java heap；
- 类静态变量(class statics)被移到了java heap；
 
JDK1.8，内存模型变化，移除了Perm区，使用本地内存来存储类元数据信息并称之为：元空间（Metaspace）（注意：字符串常量池还是在Heap区域），元空间所在位置是本地内存区域。


如何判断使用jdk1.6/jdk 1.7/jdk1.8

```java
// jdk1.6 OutOfMemoryError: PermGen space
// jdk1.7 OutOfMemoryError: Java heap space
// jdk1.8 OutOfMemoryError: Java heap space /Unrecognized VM option 'MaxPermGen=8m'
public class StringOomMock { 
  static String base = “string”; 
  public static void main(String[] args) { 
    List list = new ArrayList(); 
    for (int i=0;i< Integer.MAX_VALUE;i++){ 
      String str = base + base; 
      base = str; 
      list.add(str.intern()); 
    } 
  } 
} 
```

### Metaspace
随着JDK8的到来，JVM不再有PermGen。但类的元数据信息（metadata）还在，只不过不再是存储在连续的堆空间上，而是移动到叫做“Metaspace”的本地内存（Native memory）中。

```
// 初始空间大小，达到该值就会触发垃圾收集进行类型卸载，同时GC会对该值进行调整：如果释放了大量的空间，就适当降低该值；如果释放了很少的空间，那么在不超过MaxMetaspaceSize时，适当提高该值。 
-XX:MetaspaceSize
// 最大空间，默认是没有限制的
-XX:MaxMetaspaceSize
// 在GC之后，最小的Metaspace剩余空间容量的百分比，减少为分配空间所导致的垃圾收集 
-XX:MinMetaspaceFreeRatio
// 在GC之后，最大的Metaspace剩余空间容量的百分比，减少为释放空间所导致的垃圾收集
　-XX:MaxMetaspaceFreeRatio
```

  此外，在HotSpot中的每个垃圾收集器需要专门的代码来处理存储在PermGen中的类的元数据信息。从PermGen分离类的元数据信息到Metaspace,由于Metaspace的分配具有和Java Heap相同的地址空间，因此Metaspace和Java Heap可以无缝的管理，而且简化了Full GC的过程，以至将来可以并行的对元数据信息进行垃圾收集，而没有GC暂停。

- [元空间](https://blog.csdn.net/zhushuai1221/article/details/52122880)

永久代的缺点：
1. 大小是在启动时固定好的，很难进行调优。-XX:MaxPermSize，设置成多少好呢？随着加载类的增多，类回收效率低，容易造成OOM。

Metaspace好处：
1. 将类信息放在本地内存管理，内存没有限制，可以动态增减；
2. 可以在GC不进行暂停的情况下并发地释放类数据；
3. 简化了Full GC，每个垃圾回收器原先有专门的元数据迭代器，Metaspace的内存有专门的Metaspace VM回收。



## 对象生命周期
- new对象； 
- 检查常量区（不存在，则执行类加载），获取类符号引用 ；
- 类加载完成，分配内存：

  单线程内存分配：
  1. 指针碰撞(Bump the Pointer)，用过内存在一边，没用过的在另外一边，内存规整（需要垃圾收集器带由压缩整理功能，Serial、ParNew等带Compact过程的收集器）；
  2. 空闲列表(Free List)，记录空闲内存的列表，内存不规整（CMS，Mark-Sweep）。
  
  多线程内存分配：
  1. CAS + 失败重试，保证更新操作的原子性；
  PS: CAS（compare and swap），乐观锁，比较和替换。CAS(V,E,N)，V表示要更新的变量，E表示预期的值，N表示新值。只有当V的值等于E时，才会将V的值修改为N。如果V的值不等于E，说明已经被其他线程修改了，当前线程可以放弃此操作，也可以再次尝试次操作直至修改成功。
  2. 本地线程分配缓冲（Thread Local Allocation Buffer, TLAB)，预先分配一小块内存，只有当TLAB耗尽时，才使用CAS操作分配内存，-XX:+/-UseTLAB参数。（jdk5及以后的版本默认是启用TLAB的）
 
- 分配完成后，内存空间初始化零值（TLAB，可以再划分时初始化），这样可以不用初始化就使用变量；
- 设置对象头( Object Header）；
- 执行<init>方法；

> 注意：对象的分配可能在栈中，也可能在TLAB中。

- 实例对象内存分配完成之后，进行访问（同时，需要访问类对象）：
  1. 句柄: 
  在堆中单独划分出一块内存作为句柄池，句柄池中包含对对象实例数据的指针和对象类型数据的指针。
  优点：不用修改；缺点：多一次跳转，耗时。
  2. 直接指针（Sun HotSpot）: 
  直接指向对象实例数据，对象实例数据中包含对象类型的指针。
  优点：速度快，节省时间开销；缺点：改动频繁。

- 通过可达性分析分析（GC Root）对象是否可达，然后，通过二次标记方法标记对象是否需要被回收；
- 通过不同的垃圾收集器，将标记为垃圾的对象进行回收。
  - 标记-清除（Mark-Sweep）；
  - 标记-整理；
  - 复制；
  - 分代回收。


### 对象内存布局（HotSpot）
对象内存结构分为三个部分：1. 对象头( Object Header )、2. 实例数据( Instance Data )、3. 对齐填充( Padding )。

#### 对象头
对象头包含两部分信息：

1. 自身的运行时数据：
    1. 哈希码；
    2. GC分代年龄；
    3. 锁状态标志；
    4. 线程持有的锁；
    5. 偏向线程ID；
    6. 偏向时间戳等。
    官方：Mark Word，非固定的存储结构。如果对象是数组，需要有一块存储数组长度的信息。
2. 类型指针。（是否存在，具体看实现）

#### 实例数据
数据存储，受虚拟机分配策略参数和字段定义顺序影响。默认分配策略：

1. longs/doubles;
2. ints;
3. shorts/chars;
4. bytes/booleans;
5. oops(Ordinary Object Pointers)。
  
#### 对齐填充
Hotspot VM要求对象起始地址是8字节的整数倍。
  
# Reference
- [Java常见面试题——栈分配与TLAB](https://www.2cto.com/kf/201709/675347.html)
  
  
  
  
