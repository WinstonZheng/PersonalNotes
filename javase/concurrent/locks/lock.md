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


# ReetrantLock





# Reference
- [剖析基于并发AQS的重入锁(ReetrantLock)及其Condition实现原理](https://blog.csdn.net/javazejian/article/details/75043422)
