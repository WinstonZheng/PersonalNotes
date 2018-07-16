# ThreadPoolExecutor
是Java线程池的核心实现类。
- 用Worker类包装实际运行的线程，每一个Worker扩展了AQS类，实现简单的加锁/解锁功能；此外，通过ThreadFactory创建一个工作线程，默认是通过Executors.DefaultThreadFactory创建（工厂模式，主要作用，设置线程名等）。实现Runnable接口，真正任务运行依赖于外部类的runWorker方法。
- 通过一个HashSet用于记录工作的线程，此外，通过一个ReentrantLock的mainLock锁控制HashSet同步访问（线程的修改）。mainlock包含一个条件变量，用来等待线程池结束（awaitTermination）；
- 通过一个BlockingQueue阻塞队列管理等待运行的任务，每次有新任务进来，同时创建线程失败，则会加入到队列中（offer()方法）；
- ThreadPoolExecutor的状态通过一个AtomicInteger控制，包含两种信息，一种，前三位表示线程池状态，第二种，后29位表示线程池当前运行的线程数（可能与实际运行的线程数不符）；

## 构造
```java
public class ThreadPoolExecutor extends AbstractExecutorService {
    // 目前显示的运行线程数量（可能与真正运行的线程数量不符）
    private final AtomicInteger ctl = new AtomicInteger(ctlOf(RUNNING, 0));
    private static final int COUNT_BITS = Integer.SIZE - 3;
    private static final int CAPACITY   = (1 << COUNT_BITS) - 1;
    
    // runState is stored in the high-order bits
    // 111 运行状态，接受新任务，处理工作队列任务
    private static final int RUNNING    = -1 << COUNT_BITS;
    // 000 不接受新任务，但可以处理队列任务
    private static final int SHUTDOWN   =  0 << COUNT_BITS;
    // 001 不接受新任务，不运行队列任务，而且中断正在运行的任务
    private static final int STOP       =  1 << COUNT_BITS;
    // 010 所有任务已经结束，运行任务数量为0
    private static final int TIDYING    =  2 << COUNT_BITS;
    // 011 结束完成
    private static final int TERMINATED =  3 << COUNT_BITS;
    // 阻塞的等待工作队列
    private final BlockingQueue<Runnable> workQueue;
    // 存储工作线程
    private final HashSet<Worker> workers = new HashSet<Worker>();
    // 用于同步访问HashSet
    private final ReentrantLock mainLock = new ReentrantLock();
    private final Condition termination = mainLock.newCondition();
}
```

