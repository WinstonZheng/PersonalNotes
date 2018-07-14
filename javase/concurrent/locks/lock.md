# Lock接口
提供如下方法：
1. lock()，加锁；
2. unlock()，解锁；
3. void lockInterruptibly() throws InterruptedException，可中断取锁；
4. boolean tryLock()，尝试非阻塞取锁；
5. boolean tryLock(long time, TimeUnit unit) throws InterruptedException，非阻塞取锁，限定一段时间内取锁；
6. Condition newCondition()，获取等待通知组件，通过组件使用wait()。

# AQS并发框架



# ReetrantLock





# Reference
- [剖析基于并发AQS的重入锁(ReetrantLock)及其Condition实现原理](https://blog.csdn.net/javazejian/article/details/75043422)
