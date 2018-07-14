# 线程
线程是比进程跟轻量级的调度执行单位，主流操作系统提供线程实现，

## 基础操作
### 创建
有两种：
- Thread类；
- Runnable接口；

Thread本身是实现了Runnable接口的类。我们知道“一个类只能有一个父类，但是却能实现多个接口”，因此Runnable具有更好的扩展性。此外，Runnable还可以用于“资源的共享”。即，多个线程都是基于某一个Runnable对象建立的，它们会共享Runnable对象上的资源。通常，建议通过“Runnable”实现多线程！

> start与run的区别：
- start() : 作用是启动一个新线程，新线程会执行相应的run()方法，start()不能被重复调用；（判断当前线程状态，不为NEW，则抛出IllegalThreadStateException）
- run()  : run()就和普通的成员方法一样，可以被重复调用，单独调用run()的话，会在当前线程中执行run()，而并不会启动新线程。

```java
// 线程的创建会调用Thread的init方法
public Thread() {
        init(null, null, "Thread-" + nextThreadNum(), 0);
}
    
private void init(ThreadGroup g, Runnable target, String name,
                      long stackSize, AccessControlContext acc,
                      boolean inheritThreadLocals) {
        if (name == null) {
            throw new NullPointerException("name cannot be null");
        }
        // 设置名称 
        this.name = name;
        // 设置父线程
        Thread parent = currentThread();
        // 设置安全组
        SecurityManager security = System.getSecurityManager();
        if (g == null) {
            /* Determine if it's an applet or not */
            /* If there is a security manager, ask the security manager
               what to do. */
            if (security != null) {
                g = security.getThreadGroup();
            }
            /* If the security doesn't have a strong opinion of the matter
               use the parent thread group. */
            if (g == null) {
                g = parent.getThreadGroup();
            }
        }
        /* checkAccess regardless of whether or not threadgroup is
           explicitly passed in. */
        g.checkAccess();
        /*
         * Do we have the required permissions?
         */
        if (security != null) {
            if (isCCLOverridden(getClass())) {
                security.checkPermission(SUBCLASS_IMPLEMENTATION_PERMISSION);
            }
        }
        g.addUnstarted();
        this.group = g;
        this.daemon = parent.isDaemon();
        // 继承父线程的优先级
        this.priority = parent.getPriority();
        if (security == null || isCCLOverridden(parent.getClass()))
            this.contextClassLoader = parent.getContextClassLoader();
        else
            this.contextClassLoader = parent.contextClassLoader;
        this.inheritedAccessControlContext =
                acc != null ? acc : AccessController.getContext();
        this.target = target;
        setPriority(priority);
        if (inheritThreadLocals && parent.inheritableThreadLocals != null)
            this.inheritableThreadLocals =
                ThreadLocal.createInheritedMap(parent.inheritableThreadLocals);
        /* Stash the specified stack size in case the VM cares */
        this.stackSize = stackSize;

        /* Set thread ID */
        tid = nextThreadID();
    }
```

### 线程优先级
java 中的线程优先级的范围是1～10，默认的优先级是5。“高优先级线程”会优先于“低优先级线程”执行。也就是说，cpu尽量将执行资源让给优先级比较高的线程。优先级具有继承性，A线程启动B线程，则B线程的优先级与A一样。

### 守护线程
守护进程(daemon thread)，t.setDaemon(true)，唯一用途为其他线程提供服务（建议不要访问固有资源，如：文件、数据库等），当只剩下守护进程，程序终止。

JVM停止条件：
- 调用了exit()方法，并且exit()有权限被正常执行；
- JVM中只存在“守护线程”，方法返回。

### 异常处理
未捕获异常处理器，实现Thread.UncaughtExceptionHandler接口，可以在执行前为当前线程注册处理器，如果未注册，线程处理器默认为线程组。

### 线程停止
- 采用interrupted()会消除线程中断状态；采用isInterrupted()不会消除线程中断；
- 线程抛出异常，也会清理异常状态；
- **stop方法**停止线程，线程所包含的对象锁立即被释放，容易导致对象处于不一致的状态。（例如：在转账过程中，钱转出去时，中断线程，钱并没有转到另一个账户中）而从另一个角度，interrupt()方法将线程停顿的位置交给线程自身控制，防止出现不一致的情况。（stop会抛出java.lang.ThreadDeath异常）
- **suspend方法**挂起线程，并不会丢弃锁，而当调用suspend方法的线程需要被suspend方法挂起线程持有的锁时，会发生死锁（suspend需要resume才能继续执行）。

### yield()/wait()/sleep()
1. wait()是让线程由“运行状态”进入到“等待状态”，会线程释放所持有对象的同步锁；
2. yield()是让线程由“运行状态”进入到“就绪状态”，不会释放锁；
3. sleep() 的作用是让当前线程休眠，即当前线程会从“运行状态”进入到“休眠状态”，不会释放锁。

### getId()/currentThread()
- getId()，获得唯一的标识；
- currentThread()，返回当前线程的对象；


## 线程间通信
### wait/notify
wait()和notify()都是Object的方法，通过本地方法实现。在使用中，都需要在同步块中使用，也就是当前线程需要持有该对象锁，否则抛出异常IllegalMonitorStateException。
- 针对当前锁对象调用wait()方法，线程进入当前对象锁的等待队列，可设置超时时间；
- 调用notify()可以唤醒一个线程，但是不会释放锁，需要运行完同步快；
- 同理，notifyAll()可以唤醒所有线程，竞争锁。

> 线程释放锁三种可能：
1. 执行完同步代码块；
2. 遇到异常终止；
3. wait()。

### 生产者/消费者
基本的使用思路使用同一个对象进行信息交互，使用同一个锁进行同步。

```java
// 基础接口
public interface ShareObject {
    void produce(Object value);
    Object consumer();
}
// 基础实现类，目前采用栈方式通信
public class ShareBase implements ShareObject{

    private LinkedList<Object> list = new LinkedList();
    private final Integer Upper = 1;

    public synchronized void produce(Object value) {
        try {
            String name = Thread.currentThread().getName();
            while(Upper == list.size()){
                System.out.println("Producer:: " + name + " is waitting.");
                this.wait();
            }
            list.push(value);
            System.out.println("Producer:: " + name + " produce one.");
            // 注意，这里采用notify会产生死锁问题
            this.notifyAll();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    
    public synchronized Object consumer() {
        Object result = null;
        try {
            String name = Thread.currentThread().getName();
            while(0 == list.size()){
                System.out.println("Cosumer:: " + name + " is waitting.");
                this.wait();
            }
            System.out.println("Cosumer:: " + name + " consume one.");
            result = list.pop();
            this.notifyAll();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return result;
    }
}
// 线程类
public class Producer implements Runnable {

    private ShareObject share;
    public Producer(ShareObject share){
        this.share = share;
    }
    public void run() {
        Object produce = new Object();
        while (true){
            share.produce(produce);
        }
    }
}

public class Consumer implements Runnable {

    private ShareObject share;

    public Consumer(ShareObject lock){
        this.share = lock;
    }
    public void run() {
        while (true){
            share.consumer();
        }
    }
}
```
> 



### join
### ThreadLocal


## JVM实现
- 内核线程实现；<br>
    在支持多线程内核中，采用用户空间轻量级进程和内核空间线程1：1的映射关系实现；
    - 优+点：实现简单，调度灵活；
    - 缺点：线程的创建、销毁及同步，需要系统调用，用户和内核空间切换，消耗性能和内核资源；
    
- 用户线程实现；<br>
    用户线程的建立、同步、销毁和调度完全在用户态中实现，无需内核，实现方式一对多，1：N。
    - 优点：性能好；
    - 缺点：实现复杂。
    
- 用户线程加轻量级进程混合实现；<br>
    使用内核线程与用户线程结合，用户线程创建、切换、析构等操作廉价，支持大规模用户线程并发。通过操作系统提供的轻量级进程连接用户线程与内核线程，用户线程的系统调用通过轻量级进程实现，线程调度功能及处理器映射（访问），N:M。


### Java线程实现
JDK1.2以前，基于称为"Green Threads"的用户线程实现；在JDK1.2中，线程模型替换为基于操作系统的原生线程模型实现。具体的虚拟机线程模型实现，根据不同的操作系统底层与不同的虚拟机JDK有关。其中，对于Sun JDK其Windows版与Linux版都是使用一对一线程模型实现的，一条JAVA线程映射到一条轻量级进程中。而在Solaris平台中，平台支持一对一及多对多，提供两个平台专有虚拟机参数：-XX:+UseLWPSynchronization（默认）和-XX:+UseBoundThreads指明使用哪一种线程模型。

> 注意：从上面实现来看，Java的线程实现要不采用内核线程实现，要不采用混合实现，但是两种都有一个特点，如果线程状态变化，都是通过操作系统的系统调度实现，也就意味着加锁阻塞是一种非常耗时的操作。


## Java线程调度
### 调度分类
主要分为协同式调度（Cooperative Threads-Scheduling）和抢占式调度（Preemptive Threads-Scheduling）。
- 协同式调度，线程执行时间由线程本身控制，线程的调度由线程本身执行完成后通知调度器调度。（不稳定，如果线程一直阻塞，出现饿死的情况）
- 抢占式调度，由系统分配执行时间，线程切换由系统控制。

Java中采用抢占式调度，可以通过Thread.yield()出让执行时间，还可以通过设置优先级可能改变线程调度先后顺序（由于10个优先级和底层系统线程优先级数量不一致，可能造成多对一的情况）。

### 线程状态转换
线程主要分为五中状态：
- 新建，New，Thread创建，但并未执行；
- 运行，Runnable，Thread.start()之后，可能执行，可能就绪（时间片，抢占式调度）；
- 无限期等待，Waiting，Object.wait()/Thread.join()/LockSupport.park()方法或者是等待java.util.concurrent库中的Lock或Condition，没有设置超时时间；
- 限期等待，TimeWaiting，Thread.sleep()/Object.wait(timeout)/Thread.join(timeout)/LockSupport.parkNanos()/LockSupport.parkUntil()方法，超时等待；
- 阻塞，Blocked，阻塞状态等待一个排他锁，正在等待一个monitor lock来进入synchronized块/方法，或者是在调用wait方法后重入synchronized块/方法。等待监视锁，这个时候线程被操作系统挂起。当进入synchronized块/方法或者在调用wait()被唤醒/超时之后重新进入synchronized块/方法，锁被其它线程占有，这个时候被操作系统挂起，状态为阻塞状态。阻塞状态的线程，即使调用interrupt()方法也不会改变其状态，会抛出InterruptException。
- 结束，Terminated，run方法结束/发生未捕获异常。




# Reference
- 《深入理解Java虚拟机》





