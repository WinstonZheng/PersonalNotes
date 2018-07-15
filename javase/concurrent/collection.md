# 线程安全集合
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

### 串行队列封闭
消费者和生产者的设计模式，能够将一个可变对象，从一个线程安全封闭地传递到另外一个线程，促进了串行封闭。对象池采用了串行线程封闭的技术，在客户端代码中不发布对象引用（或者之后不使用），同时将对象交给线程池管理。而如何安全传递对象池的所有权，可以利用阻塞队列、ConcurrentMap的原子方法remove或者AtomicReference的原子方法compareAndSet可以用于完成这项工作。








# Reference
- 《Java并发编程实战》