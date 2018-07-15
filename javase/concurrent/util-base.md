# 基础构建模块
1. java.util.concurrent包，映射表、有序集和队列：
    - ConcurrentHashMap（Map）；
    - ConcurrentSkipListMap（SortedMap）；
    - ConcurrentsSkipListSet（SortedSet）；
    - ConcurrentLinkedQueue（Queue,PriorityQueue）;
    - BlockingQueue（Queue，去掉List的随机访问，实现高效并发）；
2. List对应写时拷贝：CopyOnWirteArrayList（List）和CopyOnWriteArraySet（Set）(适合进行迭代的线程数超过修改线程数，构造的迭代器指向旧数组);
3. 较早的线程安全集合：Vector/Hashtable已被弃用。现在可以采用Collections.synchronizedList/Collections.synchronizedMap等，但是多次操作还是需要使用synchronized进行同步。

## ConcurrentHashMap
通过分段锁（Lock Striping）的方式控制并发，其返回的迭代器具备弱一致性，容忍并发修改，不会抛出ConcurrentModificationException（不会对迭代过程加锁）。同时提供了一些CAS操作：
- putIfAbsent(K key, V value)
- remove(K key, V value)
- replace(K key, V oldValue, V newValue)

## CopyOnWriteArrayList
写时复制实现，当写如时，发布一个新的容器副本，所以，迭代能保持不变性。适用于多读少写的操作。

## 阻塞队列
BlockingQueue拥有多种实现：
- LinkedBlockingQueue和ArrayBlockingQueue时FIFO队列，类似于LinkedList和ArrayList；
- PriorityBlockingQueue是按优先级排序的队列；
- SynchronousQueue，不具备维护存储空间的功能，维护一组线程，将生成的对象直接发布到线程，不会经过出队和入队操作（如果没有线程就绪，则会阻塞，适用于多个消费者）。

> 在构建高可靠的应用程序时，有界队列时一种强大的资源管理工具：它们能抑制并防止产生过多的工作项，使应用程序在负荷过载的情况下变得健壮。

### 实现
ArrayBlockingQueue通过一个ReentrantLock来同时控制添加线程与移除线程的并非访问，这点与LinkedBlockingQueue区别很大，而对于notEmpty条件对象则是用于存放等待或唤醒调用take方法的线程，告诉他们队列已有元素，可以执行获取操作。同理notFull条件对象是用于等待或唤醒调用put方法的线程，告诉它们，队列未满，可以执行添加元素的操作。

### 串行队列封闭
消费者和生产者的设计模式，能够将一个可变对象，从一个线程安全封闭地传递到另外一个线程，促进了串行封闭。对象池采用了串行线程封闭的技术，在客户端代码中不发布对象引用（或者之后不使用），同时将对象交给线程池管理。而如何安全传递对象池的所有权，可以利用阻塞队列、ConcurrentMap的原子方法remove或者AtomicReference的原子方法compareAndSet可以用于完成这项工作。

### 双端队列于工作密取
Java6新加了两种容器类型，Deque和BlockingDeque，分别对Queue和BlockingQueue进行了扩展，具体实现ArrayDeque和LinkedBlockingDeque。

双端队列适合工作密取模式，即每个消费者有一个工作队列，当一个消费者完成了自身的工作，可以从其他消费者的队列中获取任务执行。此种模式，比传统的消费者、生产者模式更具可伸缩性，工作者线程不会在单个共享队列上发生竞争。此种模式可以应用在消费者端和生产者端。

## 闭锁
闭锁是一种同步工具类，可以延迟线程的进度直到达到终止的状态。闭锁相当于一扇门：在闭锁达到结束状态之前，这扇门一直是关的，并且没有任何线程能够通过，当到达结束状态时，这扇门会打开允许所有线程通过。当闭锁达到结束状态，这扇门会永远保持打开的状态。

- **倒计时门栓（CountDownLatch）**，让一个线程集等待直到计数变为0，一次性（计数值为1的门栓，实现只能通过一次的门）。

```java
// 维护了一个计数器 cnt，每次调用 countDown() 方法会让计数器的值减 1，减到 0 的时候，那些因为调用 await() 方法而在等待的线程就会被唤醒。
public class CountdownLatchExample {
    public static void main(String[] args) throws InterruptedException {
        final int totalThread = 10;
        CountDownLatch countDownLatch = new CountDownLatch(totalThread);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalThread; i++) {
            executorService.execute(() -> {
                System.out.print("run..");
                countDownLatch.countDown();
            });
        }
        countDownLatch.await();
        System.out.println("end");
        executorService.shutdown();
    }
}
```

## 障栅（栅栏）
CyclicBarrier ，实现一个集结点，所有线程执行到集结点，障栅取消，可重复使用。用来控制多个线程互相等待，只有当多个线程都到达时，这些线程才会继续执行。和 CountdownLatch 相似，都是通过维护计数器来实现的。但是它的计数器是递增的，每次执行 await() 方法之后，计数器会加 1，直到计数器的值和设置的值相等，等待的所有线程才会继续执行。和 CountdownLatch 的另一个区别是，CyclicBarrier 的计数器可以循环使用，所以它才叫做循环屏障。

```java
public class CyclicBarrierExample {
    public static void main(String[] args) throws InterruptedException {
        final int totalThread = 10;
        CyclicBarrier cyclicBarrier = new CyclicBarrier(totalThread);
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < totalThread; i++) {
            executorService.execute(() -> {
                System.out.print("before..");
                try {
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
                System.out.print("after..");
            });
        }
        executorService.shutdown();
    }
}
```

另一种形式的障栅Exchanger，一种两方（Two-Party）栅栏。（可用于缓冲区的互换）


## 信号量
以共享锁的方式，支持指定数量的线程共享资源。可用于实现有界阻塞容器，例如：数据库连接池。

## FutureTask
FutureTask表示的计算是通过Callable实现的，相当于一种可生成结果的Runnable。可以处于三种状态：等待运行（wait to run）、正在运行（Running）和运行完成（Completed）。执行完成表示所有可能的结束方式，包括正常结束、由于取消而结束和异常结束。FutureTask的get方法确保了不同状态下的不同返回。<br>
Callable有返回值，返回值通过 Future 进行封装。FutureTask 实现了 RunnableFuture 接口，该接口继承自 Runnable 和 Future 接口，这使得 FutureTask 既可以当做一个任务执行，也可以有返回值。<br>
FutureTask 可用于异步获取执行结果或取消执行任务的场景。当一个计算任务需要执行很长时间，那么就可以用 FutureTask 来封装这个任务，主线程在完成自己的任务之后再去获取结果。

```java
public class FutureTask<V> implements RunnableFuture<V>
public interface RunnableFuture<V> extends Runnable, Future<V>
public class FutureTaskExample {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        FutureTask<Integer> futureTask = new FutureTask<Integer>(new Callable<Integer>() {
            @Override
            public Integer call() throws Exception {
                int result = 0;
                for (int i = 0; i < 100; i++) {
                    Thread.sleep(10);
                    result += i;
                }
                return result;
            }
        });

        Thread computeThread = new Thread(futureTask);
        computeThread.start();

        Thread otherThread = new Thread(() -> {
            System.out.println("other task is running...");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        otherThread.start();
        System.out.println(futureTask.get());
    }
}

```

## ForkJoin
主要用于并行计算中，和 MapReduce 原理类似，都是把大的计算任务拆分成多个小任务并行计算。



# Reference
- 《Java并发编程实战》
- [github Interview-Notebook](https://github.com/CyC2018/Interview-Notebook/blob/master/notes/Java%20%E5%B9%B6%E5%8F%91.md#%E5%85%ABjuc---%E5%85%B6%E5%AE%83%E7%BB%84%E4%BB%B6)