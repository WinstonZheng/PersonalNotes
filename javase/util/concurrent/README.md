# 基础
在访问共享可变状态时需要进行的管理。

## 线程安全
当多个线程访问一个对象时，如果不用考虑这些线程运行时环境下的调度与交替运行，也不需要进行额外同步，或者在调用方法进行任何其他的协调工作，调用这个对象的行为可以获得正确的结果，那这个对象就是线程安全的。简单来说，当多个线程访问某个类时，这个类能表现出正确的行为。

> 无状态的类一定时线程安全的，无状态指的就是不包含任何类属性或者实例属性的引用。

### 类构造器
1. 在构造函数一开始，this就是可用的；
2. 构造函数和普通函数一样，并不是默认被synchronized 的，有可能出现同步问题；
3. 如果构造函数中访问静态变量的话，必须同步这个静态变量，否则一定会出问题；
4. 构造函数访问成员变量不会出现问题；
5. this溢出。

## 关键区/临界区
会被多线程访问的代码区域。

临界区指的是一个访问共用资源（例如：共用设备或是共用存储器）的程序片段。

## 竞态条件/竞争条件
当某个值计算的正确性取决于多个线程的交替执行时序时，那么就会发生竞态条件。常见的竞态条件如下：
- 先检查后执行；（基于一种可能失效的观察结果来做出判断或者执行某个计算）
- 读取-修改-写入；

## 原子性操作
两个操作A和B，如果从执行A的线程来看，当另一个线程执行B时，要不将B全部执行完，要么完全不执行B，那么A和B对彼此来说时原子的。（操作是不可中断的）

## 类状态
一般指的是类的属性，会在类方法中被修改。

要保持类状态的一致性，需要在原子操作中更新所有相关的状态变量。（类状态的线程安全，建立在与属性关联的不变性条件不被破坏基础上）



## 良好实践
- 给线程起个有意义的名字，这样可以方便找 Bug。

- 缩小同步范围，例如对于 synchronized，应该尽量使用同步块而不是同步方法。

- 多用同步类少用 wait() 和 notify()。首先，CountDownLatch, Semaphore, CyclicBarrier 和 Exchanger 这些同步类简化了编码操作，而用 wait() 和 notify() 很难实现对复杂控制流的控制。其次，这些类是由最好的企业编写和维护，在后续的 JDK 中它们还会不断优化和完善，使用这些更高等级的同步工具你的程序可以不费吹灰之力获得优化。

- 多用并发集合少用同步集合。并发集合比同步集合的可扩展性更好，例如应该使用 ConcurrentHashMap 而不是 Hashtable。

- 使用本地变量和不可变类来保证线程安全。

- 使用线程池而不是直接创建 Thread 对象，这是因为创建线程代价很高，线程池可以有效地利用有限的线程来启动任务。

- 使用 BlockingQueue 实现生产者消费者问题。







# Reference
- 《Java并发编程实战》
- [Interview-Notebook Java 并发](https://github.com/CyC2018/Interview-Notebook/blob/master/notes/Java%20%E5%B9%B6%E5%8F%91.md)
