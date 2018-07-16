# ArrayBlockingQueue
ArrayBlockingQueue主要以循环数组的形式实现了BlockingQueue（FIFO），主要查看take()和put()方法的实现思路，实现采用了生产者和消费者的思想。

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


# LinkedBlockingQueue
LinkedBlockingQueue通过两个锁控制链表。消费者-生产者变种，可以让消费者和生产者同时访问队列，提高吞吐量，当然实现复杂度也上升了。

```java
public class LinkedBlockingQueue<E> extends AbstractQueue<E>
        implements BlockingQueue<E>, java.io.Serializable{
     static class Node<E> {
        E item;
        /**
         * One of:
         * - the real successor Node
         * - this Node, meaning the successor is head.next
         * - null, meaning there is no successor (this is the last node)
         */
        Node<E> next;
        Node(E x) { item = x; }
    }   
    // 头指针，在构造函数中新建，item为null
    transient Node<E> head;
    // 队列尾部
    private transient Node<E> last;
    // 出队锁
    private final ReentrantLock takeLock = new ReentrantLock();
    // 出队条件变量
    private final Condition notEmpty = takeLock.newCondition();
    // 入队锁
    private final ReentrantLock putLock = new ReentrantLock();
    // 入队条件变量
    private final Condition notFull = putLock.newCondition();
    // 由于并发访问，所以需要保持线程安全
    private final AtomicInteger count = new AtomicInteger();
    // 不变性，保持线程安全 
    private final int capacity;
    
    public LinkedBlockingQueue(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException();
        this.capacity = capacity;
        last = head = new Node<E>(null);
    }
}
```

> 没有给LinkedBlockingQueue指定容量大小，其默认值将是Integer.MAX_VALUE，如果存在添加速度大于删除速度时候，有可能会内存溢出。

## 入队
```java
public void put(E e) throws InterruptedException {
        if (e == null) throw new NullPointerException();
        // Note: convention in all put/take/etc is to preset local var
        // holding count negative to indicate failure unless set.
        int c = -1;
        Node<E> node = new Node<E>(e);
        final ReentrantLock putLock = this.putLock;
        // 获取数量
        final AtomicInteger count = this.count;
        putLock.lockInterruptibly();
        try {
            /*
             * Note that count is used in wait guard even though it is
             * not protected by lock. This works because count can
             * only decrease at this point (all other puts are shut
             * out by lock), and we (or some other waiting put) are
             * signalled if it ever changes from capacity. Similarly
             * for all other uses of count in other wait guards.
             * 在这种情况下，count只能减少（不能增加），由于生产者共用一个锁
             */
            while (count.get() == capacity) {
                notFull.await();
            }
            // 将节点加入队列
            enqueue(node);
            // 原子操作，c返回旧值
            c = count.getAndIncrement();
            // 通知其他生产者
            if (c + 1 < capacity)
                notFull.signal();
        } finally {
            putLock.unlock();
        }
        if (c == 0)
            // 通知消费者
            signalNotEmpty();
    }
private void enqueue(Node<E> node) {
        // assert putLock.isHeldByCurrentThread();
        // assert last.next == null;
        last = last.next = node;
    }
// 线程非空，唤醒消费者
private void signalNotEmpty() {
        final ReentrantLock takeLock = this.takeLock;
        takeLock.lock();
        try {
            notEmpty.signal();
        } finally {
            takeLock.unlock();
        }
    }
```

## 出队
```java
// 出队
public E take() throws InterruptedException {
        E x;
        int c = -1;
        final AtomicInteger count = this.count;
        final ReentrantLock takeLock = this.takeLock;
        // 获取消费者的锁
        takeLock.lockInterruptibly();
        try {
            while (count.get() == 0) {
                notEmpty.await();
            }
            x = dequeue();
            c = count.getAndDecrement();
            if (c > 1)
                notEmpty.signal();
        } finally {
            takeLock.unlock();
        }
        if (c == capacity)
            signalNotFull();
        return x;
    }
// 往链表头部加节点
private E dequeue() {
        // assert takeLock.isHeldByCurrentThread();
        // assert head.item == null;
        Node<E> h = head;
        Node<E> first = h.next;
        h.next = h; // help GC
        head = first;
        E x = first.item;
        first.item = null;
        return x;
    }
// 使用条件变量，首先得持有锁
private void signalNotFull() {
        final ReentrantLock putLock = this.putLock;
        putLock.lock();
        try {
            notFull.signal();
        } finally {
            putLock.unlock();
        }
    }
```

## 区别（From Reference）
1.队列大小有所不同，ArrayBlockingQueue是有界的初始化必须指定大小，而LinkedBlockingQueue可以是有界的也可以是无界的(Integer.MAX_VALUE)，对于后者而言，当添加速度大于移除速度时，在无界的情况下，可能会造成内存溢出等问题。
2.数据存储容器不同，ArrayBlockingQueue采用的是数组作为数据存储容器，而LinkedBlockingQueue采用的则是以Node节点作为连接对象的链表。
3.由于ArrayBlockingQueue采用的是数组的存储容器，因此在插入或删除元素时不会产生或销毁任何额外的对象实例，而LinkedBlockingQueue则会生成一个额外的Node对象。这可能在长时间内需要高效并发地处理大批量数据的时，对于GC可能存在较大影响。
4.两者的实现队列添加或移除的锁不一样，ArrayBlockingQueue实现的队列中的锁是没有分离的，即添加操作和移除操作采用的同一个ReenterLock锁，而LinkedBlockingQueue实现的队列中的锁是分离的，其添加采用的是putLock，移除采用的则是takeLock，这样能大大提高队列的吞吐量，也意味着在高并发的情况下生产者和消费者可以并行地操作队列中的数据，以此来提高整个队列的并发性能。

# Reference
- [深入剖析java并发之阻塞队列LinkedBlockingQueue与ArrayBlockingQueue](https://blog.csdn.net/javazejian/article/details/77410889)