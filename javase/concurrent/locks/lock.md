# Lock接口
提供如下方法：
1. lock()，加锁；
2. unlock()，解锁；
3. void lockInterruptibly() throws InterruptedException，可中断取锁；
4. boolean tryLock()，尝试非阻塞取锁；
5. boolean tryLock(long time, TimeUnit unit) throws InterruptedException，非阻塞取锁，限定一段时间内取锁；
6. Condition newCondition()，获取等待通知组件，通过组件使用wait()。

# AQS并发框架
AQS的实现，采用了模板方法设计模式，主要维护了同步队列和条件队列，提供了维护队列（插入节点、删除节点）的基本操作，队列中的节点是线程对象的包装。

> AQS的底层通过volatile提供可见性，通过Unsafe的CAS基础操作提供原子性，实现在多线程情况下，状态转变、队列插入和删除等操作，保证线程的安全性。

## 同步队列

```java
// 通过此函数，查看是否能够获取锁，如果不能，则通过addWaiter加入队列。tryAcquire通过子类实现（通过CAS指令修改状态值，模拟竞争锁操作），实现功能判断是否能获得锁。
public final void acquire(int arg) {
        if (!tryAcquire(arg) &&
                // 同步队列入队(CAS入队)
                // acquireQueued通过一个自旋过程，一般是头节点的后一个节点在不断尝试获取同步状态，
                // 其他节点使用Unsafe进入阻塞状态（一般修改节点状态、加入节点等操作都是CAS乐观锁）
            acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
            selfInterrupt();
}
// 加入队列
private Node addWaiter(Node mode) {
        Node node = new Node(Thread.currentThread(), mode);
        // Try the fast path of enq; backup to full enq on failure
        // 如果是第一个节点，则为空（从尾部插入）
        Node pred = tail;
        if (pred != null) {
            node.prev = pred;
            // CAS替换节点，插入尾部
            if (compareAndSetTail(pred, node)) {
                pred.next = node;
                return node;
            }
        }
        //如果第一次加入或者CAS操作没有成功执行enq入队操作，enq通过死循环初始化或者将线程加入队列
        enq(node);
        return node;
}
// 解锁
public final boolean release(int arg) {
        //尝试释放锁，子类实现
        if (tryRelease(arg)) {
            Node h = head;
            if (h != null && h.waitStatus != 0)
                //唤醒后继结点的线程（头节点后一个还存活的节点）
                // Unsafe.unpark
                unparkSuccessor(h);
            return true;
        }
        return false;
    }
```

## 等待队列（Condition）
- Condition是等待队列（FIFO），通过AQS中的ConditionObject实现，队列的节点形式也是Node，但是之后一个指向后来节点的指针（nextWaiter），等待队列中节点的状态只有两种Cancelled和Condition。

- 一个Lock对象可以对应多个等待队列，但是只有一个同步队列，当等待队列中的节点被唤醒时，会将等待队列中的节点放置到同步队列中。

- 由于Condition的操作对象一定时当前持有锁的线程，所以对等待队列的操作时单线程的，不需要CAS做同步。

- 独占模式下有等待队列，共享模式下不存在（signal如果不是独占模式，会抛出异常）。

# ReetrantLock（独占模式）
通过Sync类提供了可重入锁，而通过NonfairSync和FairSync实现了非公平锁和公平锁。
```java
// Sync 
// 一 是尝试再次获取同步状态，如果获取成功则将当前线程设置为OwnerThread，
// 否则失败，二是判断当前线程current是否为OwnerThread，
// 如果是则属于重入锁，state自增1，并获取锁成功，返回true，
// 反之失败，返回false，也就是tryAcquire(arg)执行失败，返回false。
final boolean nonfairTryAcquire(int acquires) {
            final Thread current = Thread.currentThread();
            int c = getState();
            //判断同步状态是否为0，并尝试再次获取同步状态
            if (c == 0) {
                if (compareAndSetState(0, acquires)) {
                    setExclusiveOwnerThread(current);
                    return true;
                }
            }
            //如果当前线程已获取锁，属于重入锁，再次获取锁后将status值加1
            else if (current == getExclusiveOwnerThread()) {
                int nextc = c + acquires;
                if (nextc < 0) // overflow
                    throw new Error("Maximum lock count exceeded");
                //设置当前同步状态，当前只有一个线程持有锁，因为不会发生线程安全问题，可以直接执行 setState(nextc);
                setState(nextc);
                return true;
            }
            return false;
}
// Sync，尝试释放锁
protected final boolean tryRelease(int releases) {
            int c = getState() - releases;
            if (Thread.currentThread() != getExclusiveOwnerThread())
                throw new IllegalMonitorStateException();
            boolean free = false;
            if (c == 0) {
                free = true;
                setExclusiveOwnerThread(null);
            }
            setState(c);
            return free;
        }
// NonfairSync
protected final boolean tryAcquire(int acquires) {
            return nonfairTryAcquire(acquires);
}
// FairSync，与非公平锁区别在于，当竞争锁的时候，先判断队列中是否存在节点，如果存在，则先取队列中的。
protected final boolean tryAcquire(int acquires) {
        final Thread current = Thread.currentThread();
        int c = getState();
        if (c == 0) {
            if (!hasQueuedPredecessors() &&
                compareAndSetState(0, acquires)) {
                setExclusiveOwnerThread(current);
                return true;
            }
        }
        else if (current == getExclusiveOwnerThread()) {
            int nextc = c + acquires;
            if (nextc < 0)
                throw new Error("Maximum lock count exceeded");
            setState(nextc);
            return true;
        }
        return false;
}

```











# Reference
- [剖析基于并发AQS的重入锁(ReetrantLock)及其Condition实现原理](https://blog.csdn.net/javazejian/article/details/75043422)
