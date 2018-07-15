# 线程安全集合
1. java.util.concurrent包，映射表、有序集和队列：ConcurrentHashMap、ConcurrentSkipListMap、ConcurrentsSkipListSet、ConcurrentLinkedQueue
2. 写数组拷贝：CopyOnWirteArrayList和CopyOnWriteArraySet(适合进行迭代的线程数超过修改线程数，构造的迭代器指向旧数组)
3. 较早的线程安全集合：Vector/Hashtable已被弃用。现在可以采用Collections.synchronizedList/Collections.synchronizedMap等，但是多次操作还是需要使用synchronized进行同步。
4. Callable与Future
	- Callable类似于Runnable，但是有返回值，可以通过Future获得（Future接口通过get方法（可以设置超时时间）获取线程执行结果，可被中断）。
	- FutureTask包装器，可以结合Callable和Future接口。

