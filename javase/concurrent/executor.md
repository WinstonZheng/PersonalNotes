# Executor
Executor框架主要用来管理任务执行调度，同时可以给任务执行提供监控、调优、记录日志、错误报告等多种功能。使用Executor提交任务，比单纯使用Thread.start()来启动任务更加灵活，优势如下：
1. 将任务的提交与运行解耦，通过配置Executor的实现，可以实现任务不同的执行策略，应对不同的资源情况与任务执行需求；
2. Executor实现还提供了对生命周期的支持，以及统计信息的收集、应用程序管理机制和性能监控等机制；

Executor的实现是基于生产者-消费者模式，提交任务的操作相当于生产者（生产待完成工作单元），执行任务的线程相当于消费者（执行完这些工作单元）。

## 执行策略
将任务的执行与提交解耦，有利于修改执行策略，以满足不同的执行要求：
1. 在什么（What)线程中执行；
2. 任务按照什么(What)顺序执行（FIFO/LIFO/优先级）；
3. 有多少个（How Many）任务能并发执行；
4. 在队列中有多少个（How Many）任务在等待执行；
5. 如果系统过载，需要拒绝任务，应选择哪一个（Which）？另外，如何（How）通知应用程序有任务被拒绝？
6. 在执行一个任务之前或之后，应该进行哪些（What）动作？

> 最佳的执行策略取决于可用资源和对服务质量的需求。

## 线程池
Executors的静态工厂方法创建一个线程池。
- newFixedThreadPool，创建一个固定长度的线程池，每当提交一个任务就创建一个线程，直到达到线程池的最大数量，线程池规模保持不变（当线程出现Exception结束，补充一个新线程）；
- newCachedThreadPool，创建一个可缓存的线程池，如果线程池的当前规模超过了处理需求时，那么将回收空闲的线程，当需求增加，增加新线程，线程池规模无限制；
- newSingleThreadExecutor，单线程的Executor，创建单个工作者线程执行任务，如果这个线程异常结束，创建另一个线程替代（根据队列不同顺序串行执行）。
- newScheduledThreadPool，创建固定长度线程池，以延迟或定时的方式来执行任务，类似于Timer。

## 生命周期
ExecutorService扩展了Executor的接口提供了Executor中线程的生命周期管理功能，具体代码如下：
```java
public interface ExecutorService extends Executor {
    
    // 平滑关闭，停止接受新任务，等待已提交任务执行（包括还未开始执行的任务）。
    void shutdown();
    // 立即关闭，尝试取消所有运行任务，并不再启动队列中尚未开始的任务
    List<Runnable> shutdownNow();
    // 阻塞等待，shutdown之后任务停止（或者超时，或者被中断，看那个先发生）
    boolean awaitTermination(long timeout, TimeUnit unit)
        throws InterruptedException;
    boolean isShutdown();
    // 需要调用shutdown，才能线程true    
    boolean isTerminated(); 
}
```