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
    // 创建工作线程
    private volatile ThreadFactory threadFactory;
    // 调用shutdown或shutdownNow后，新任务会交给handler处理
    private volatile RejectedExecutionHandler handler;
    // 空闲线程等待任务时间（数量超出corePoolSize，或者allowCoreThreadTimeOut为True）
    private volatile long keepAliveTime;
    // 默认false，核心线程保持，即使空闲；如果是true，核心线程使用上一个时间，等待（超时退出）
    private volatile boolean allowCoreThreadTimeOut;
    // 设定保持活跃状态线程的数量，不允许超时，除非上一个变量设置成true
    private volatile int corePoolSize;
    // 最大限制
    private volatile int maximumPoolSize;
}
```

## 运行三步骤
```java
public void execute(Runnable command) {
        if (command == null)
            throw new NullPointerException();
        /*
         * Proceed in 3 steps:
         *
         * 1. 当小于corePoolSize数目时，尝试通过addWorker方法创建线程，并将输入的command
         * 作为其首个任务，addworker会自动检测运行状态和工作数目，如果创建失败，则返回false
         *
         * 2. 如果线程创建失败，则尝试加入等待队列中，当等待队列添加成功之后，
         * 需要二次检查是否应该添加线程（因为，可能存在线程死亡），或者可能线程池
         * shut doen，如果发现线程池不运行，则从等待队列中删除，调用reject拒绝任务。
         * 或者，如果无线程执行，则启动一个新线程。
         *
         * 3. 如果我们既不能启动线程，又不能加入队列，则说明线程池处于关闭阶段，拒绝任务。
         */
        // 获取目前记录的运行线程数量
        int c = ctl.get();
        // 如果比设定小
        if (workerCountOf(c) < corePoolSize) {
            // 新建线程
            if (addWorker(command, true))
                return;
            c = ctl.get();
        }
        // 如果创建线程（Worker）失败，加入队列
        if (isRunning(c) && workQueue.offer(command)) {
            int recheck = ctl.get();
            // 再次检查，
            if (! isRunning(recheck) && remove(command))
                reject(command);
            else if (workerCountOf(recheck) == 0)
                addWorker(null, false);
        }
        // 创建线程失败，添加工作队列失败，再次创建线程，如果失败，则说明处于shutdown状态，拒绝任务
        else if (!addWorker(command, false))
            reject(command);
    }
```

## 添加工作线程

```java
private boolean addWorker(Runnable firstTask, boolean core) {
        retry:
        for (;;) {
            // 目前运行的线程数
            int c = ctl.get();
            // 获取运行时状态
            int rs = runStateOf(c);

            // Check if queue empty only if necessary.
            // 如果线程池状态处于运行
            // 并且firstTask不为空
            // 工作队列不是空的
            if (rs >= SHUTDOWN &&
                ! (rs == SHUTDOWN &&
                   firstTask == null &&
                   ! workQueue.isEmpty()))
                return false;

            for (;;) {
                int wc = workerCountOf(c);
                // 超出限定
                if (wc >= CAPACITY ||
                        // 根据core，判断以那个为上界
                    wc >= (core ? corePoolSize : maximumPoolSize))
                    return false;
                // 增加线程数量
                if (compareAndIncrementWorkerCount(c))
                    break retry;
                // 内循环，线程数量变化，失败重试；外循环，线程池状态变化，失败重试。
                c = ctl.get();  // Re-read ctl
                if (runStateOf(c) != rs)
                    continue retry;
                // else CAS failed due to workerCount change; retry inner loop
            }
        }

        boolean workerStarted = false;
        boolean workerAdded = false;
        Worker w = null;
        try {
            // 允许创建线程，不允许的要不在循环重试，要不返回false退出
            w = new Worker(firstTask);
            final Thread t = w.thread;
            if (t != null) {
                final ReentrantLock mainLock = this.mainLock;
                mainLock.lock();
                try {
                    // Recheck while holding lock.
                    // Back out on ThreadFactory failure or if
                    // shut down before lock acquired.
                    int rs = runStateOf(ctl.get());
                    // 再次检查状态是否正常
                    if (rs < SHUTDOWN ||
                        (rs == SHUTDOWN && firstTask == null)) {
                        // 线程如果是正在运行的，不能用来启动任务
                        if (t.isAlive()) // precheck that t is startable
                            throw new IllegalThreadStateException();
                        workers.add(w);
                        int s = workers.size();
                        // 记录最大的线程池数量
                        if (s > largestPoolSize)
                            largestPoolSize = s;
                        workerAdded = true;
                    }
                } finally {
                    mainLock.unlock();
                }
                if (workerAdded) {
                    t.start();
                    workerStarted = true;
                }
            }
        } finally {
            if (! workerStarted)
                addWorkerFailed(w);
        }
        return workerStarted;
    }

private final class Worker
        extends AbstractQueuedSynchronizer
        implements Runnable
{
        final Thread thread;
        Runnable firstTask;
        Worker(Runnable firstTask) {
            setState(-1); // inhibit interrupts until runWorker
            this.firstTask = firstTask;
            // 通过默认的线程工厂创建线程
            this.thread = getThreadFactory().newThread(this);
        }
        // 实际运行的任务
        public void run() {
            runWorker(this);
        }
}
```
首先判断线程池是否处于正常运行状态以及参数是否正确，检验之后，通过CAS操作增加线程计数器（通过重复运行进行补偿）。如果，线程池状态变化，则重新大循环，检验连接池状态；如果，线程池状态不变，则进行小循环仿佛尝试。

成功增加计数器之后，新建Work对象，获取锁对象，将Worker对象添加到HashSet中，添加成功之后，启动线程，如果启动失败则返回false。



