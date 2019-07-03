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
- newWorkStealingPool，JDK1.8，创建一个工作密取的线程池，使用多个队列减少竞争，可以输入并行度，表示积极参与或可用的最大线程数，实际线程数可动态增加和缩小，不保证任务执行顺序。


> Timer负责管理延迟任务和周期任务，基于绝对时间调度，存在缺陷，使用ScheduledThreadPoolExecutor（相对时间）代替。Timer在执行所有定时任务，创建一个线程，当一个任务执行时间过长，会影响其他任务定时的精确性；另一个问题，不会捕获异常，抛出异常后会终止定时线程，导致后面任务无法执行。

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

## Runnable和Callable
Runnable作为一个线程基本执行单位存在缺陷，无法返回线程值，同时无法抛出异常。Callable都能满足，Callable适合延迟计算，获取结果。Executor的任务有四个生命周期，创建、提交、开始、完成。

Executor框架中，允许取消提交当尚未开始的任务（已开始任务，只能中断）。其中，Future类表示任务的生命周期，提供判断任务是否完成或取消，以及获取任务结果和取消任务等功能。Future提供的get()方法，根据不同的任务运行状态，呈现不同的效果。
- 任务完成，get返回或者抛出Exception；
- 任务未完成，阻塞；
- 任务抛出异常，封装为ExecutionException并重新抛出（可以通过getCause，获取原始异常）；
- 任务被取消，抛出CancellationException。

![](/images/java/concureent/future.PNG)

如何获得Future?
- ExecutorServie的submit方法；
- FutureTask。

```java
// 通过适配器模式，将Runnable对象，包装成Callable。
static final class RunnableAdapter<T> implements Callable<T> {
        final Runnable task;
        final T result;
        RunnableAdapter(Runnable task, T result) {
            this.task = task;
            this.result = result;
        }
        public T call() {
            task.run();
            return result;
        }
    }
```

## Future与CompletionService
Future管理一个任务的执行结果，通过get()方式，获取任务结果。当需要管理一系列任务的结果时，Future操作过于繁琐，CompletionService将Executor与BlockingQueue的功能结合，ExecutorCompletionService实现CompletionService，将任务执行委托给Executor。

具体实现，ExecutorCompletionService创建BlockingQueue保存计算结果。计算完成时调用done方法。当提交某个任务时首先包装成一个QueueFuture（FutureTask子类），改写子类done，将结果放入BlockingQueue（将tabke和poll方法委托给了BlockingQueue）

### ExecutorCompletionService

```java
public class ExecutorCompletionService<V> implements CompletionService<V> {
    // 任务运行委托对象
    private final Executor executor;
    private final AbstractExecutorService aes;
    // 完成队列
    private final BlockingQueue<Future<V>> completionQueue;
    // 任务实际包装的对象
    private class QueueingFuture extends FutureTask<Void> {
        QueueingFuture(RunnableFuture<V> task) {
            super(task, null);
            this.task = task;
        }
        protected void done() { completionQueue.add(task); }
        private final Future<V> task;
    }
    // 其中一个构造函数，默认初始化
    public ExecutorCompletionService(Executor executor) {
        if (executor == null)
            throw new NullPointerException();
        this.executor = executor;
        // 将执行器包装成AbstractExecutorService
        this.aes = (executor instanceof AbstractExecutorService) ?
            (AbstractExecutorService) executor : null;
        this.completionQueue = new LinkedBlockingQueue<Future<V>>();
    }
    // 提交执行
    public Future<V> submit(Callable<V> task) {
        if (task == null) throw new NullPointerException();
        RunnableFuture<V> f = newTaskFor(task);
        // 包装成QueueingFuture，重写done，executor运行任务完成后，调用done，写入结果队列
        executor.execute(new QueueingFuture(f));
        return f;
    }
    // 获取结果
    public Future<V> take() throws InterruptedException {
        return completionQueue.take();
    }
    public Future<V> poll() {
        return completionQueue.poll();
    }
}
```


## 注意事项
1. 任务堆积，newFixedThreadPool创建指定数目线程，但是其工作等待的队列时无界的，采用了LinkedBlockingQueue（上线是Integer.MAX_VALUE），如果产生速度大于处理速度，占用大量内存，出现OOM问题（jmap等工具查看大量任务入队）；
2. 避免过度扩展线程，处理大量短时的任务采用缓存的线程池（缓存60s），不能准确预估需要线程数目（缓存线程池默认构建上线Integer.MAX_VALUE），因为缓存线程池采用SynchronousQueue，一般来说
吞吐量比较大；
3. 另外，如果线程数目不断增长（jstack等工作检查），可能出现线程泄露问题，可能处理任务逻辑卡在某个位置，导致工作线程无法释放；
4. 避免死锁；
5. 避免使用ThreadLocal。









