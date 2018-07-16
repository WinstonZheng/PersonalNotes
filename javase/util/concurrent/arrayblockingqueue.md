# ArrayBlockingQueue
ArrayBlockingQueue主要以循环数组的形式实现了BlockingQueue，主要查看take()和put()方法的实现思路，实现采用了生产者和消费者的思想。

```java
// 初始化
public class ArrayBlockingQueue<E> extends AbstractQueue<E>
        implements BlockingQueue<E>, java.io.Serializable{
        // 大小不可变
        final Object[] items;
        // 访问时都会加锁，提供线程安全
        final ReentrantLock lock;
        // 获取时，等待的信号 
        private final Condition notEmpty;
        // 添加时，等待的信号
        private final Condition notFull;
        // 队列的起始端        
        int takeIndex;
        // 队列的末端
        int putIndex;
}
```


## 入队

```java
public void put(E e) throws InterruptedException {
        checkNotNull(e);
        final ReentrantLock lock = this.lock;
        // 加锁
        lock.lockInterruptibly();
        try {
            // 当队列满时，则生产者等待
            while (count == items.length)
                notFull.await();
            enqueue(e);
        } finally {
            lock.unlock();
        }
    }
private void enqueue(E x) {
        // assert lock.getHoldCount() == 1;
        // assert items[putIndex] == null;
        final Object[] items = this.items;
        items[putIndex] = x;
        // 如果达到数组的末尾，跳到数组的开始
        if (++putIndex == items.length)
            putIndex = 0;
        count++;
        // 唤醒消费者线程
        notEmpty.signal();
}
```


## 出队
```java
// 删除
public E take() throws InterruptedException {
        final ReentrantLock lock = this.lock;
        // 加锁保平安
        lock.lockInterruptibly();
        try {
            // 当队列为空，则消费者等待；
            while (count == 0)
                notEmpty.await();
            // 出队
            return dequeue();
        } finally {
            lock.unlock();
        }
    }
// 将队列元素清空
private E dequeue() {
        // assert lock.getHoldCount() == 1;
        // assert items[takeIndex] != null;
        final Object[] items = this.items;
        @SuppressWarnings("unchecked")
        E x = (E) items[takeIndex];
        // 垃圾回收
        items[takeIndex] = null;
        // 取下一个位置，如果获取的索引值达到了数组末尾，则回到数组开头
        if (++takeIndex == items.length)
            takeIndex = 0;
        count--;
        if (itrs != null)
            // 更新现有的迭代器
            itrs.elementDequeued();
        // 唤醒生产者线程
        notFull.signal();
        return x;
    }


```