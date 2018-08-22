# ConcurrentHashMap

## Java1.7
ConcurrentHashMap 是一个 Segment 数组，Segment 通过继承 ReentrantLock 来进行加锁，所以每次需要加锁的操作锁住的是一个 segment，这样只要保证每个 Segment 是线程安全的，也就实现了全局的线程安全（也就意味着当前只有一个线程在修改操作）。
```java
// 注意，ConcurrentHashMap的相关操作都是在Segment中实现
static final class HashEntry<K,V> {
        final int hash;
        final K key;
        volatile V value;
        volatile HashEntry<K,V> next;

        HashEntry(int hash, K key, V value, HashEntry<K,V> next) {
            this.hash = hash;
            this.key = key;
            this.value = value;
            this.next = next;
        }
        ......
}
// 添加/更新操作
final V put(K key, int hash, V value, boolean onlyIfAbsent) {
            // 在往该 segment 写入前，需要先获取该 segment 的独占锁
            // 先看主流程，后面还会具体介绍这部分内容
            HashEntry<K,V> node = tryLock() ? null :
                scanAndLockForPut(key, hash, value);
            V oldValue;
            try {
                // 这个是 segment 内部的数组
                HashEntry<K,V>[] tab = table;
                // 再利用 hash 值，求应该放置的数组下标
                //
                int index = (tab.length - 1) & hash;
                // first 是数组该位置处的链表的表头
                HashEntry<K,V> first = entryAt(tab, index);
                // 下面这串 for 循环虽然很长，不过也很好理解，
                // 想想该位置没有任何元素和已经存在一个链表这两种情况
                for (HashEntry<K,V> e = first;;) {
                    if (e != null) {
                        K k;
                        if ((k = e.key) == key ||
                            (e.hash == hash && key.equals(k))) {
                            oldValue = e.value;
                            if (!onlyIfAbsent) {
                                // 覆盖旧值
                                e.value = value;
                                ++modCount;
                            }
                            break;
                        }
                        // 继续往下走
                        e = e.next;
                    }
                    else {
                        // node 到底是不是 null，这个要看获取锁的过程，不过和这里都没有关系。
                        // 如果不为 null，那就直接将它设置为链表表头；如果是null，初始化并设置为链表表头。
                        if (node != null)
                            node.setNext(first);
                        else
                            node = new HashEntry<K,V>(hash, key, value, first);
                        int c = count + 1;
                        // 超过了阈值，扩容
                        if (c > threshold && tab.length < MAXIMUM_CAPACITY)
                            rehash(node);
                        else
                            // 在index索引处放置node节点
                            setEntryAt(tab, index, node);
                        ++modCount;
                        count = c;
                        oldValue = null;
                        break;
                    }
                }
            } finally {
                unlock();
            }
            return oldValue;
        }
```

读的操作未加锁，由于修改和删除操作都是在单一线程中操作，而查看HashEntry类，定义的属性key和hash是不可变的，而next和value都是volatile，符合volatile的操作场景，一个线程修改，其他线程读取操作。


## Java1.8
由于在1.8中HashMap做了一个优化，本来hash表解决冲突时采用链表的方式，1.8做的优化是当链表过长时，采用红黑树的方法将链表进行修改。

```java
/** Implementation for put and putIfAbsent */
    final V putVal(K key, V value, boolean onlyIfAbsent) {
        // 不能放置空指针的键和值
        if (key == null || value == null) throw new NullPointerException();
        int hash = spread(key.hashCode());
        int binCount = 0;
        for (Node<K,V>[] tab = table;;) {
            Node<K,V> f;
            int n, i, fh;
            if (tab == null || (n = tab.length) == 0)
                // 新建一个数组，新建前首先通过CAS操作将sizeCtl置为-1，保证可以被访问
                tab = initTable();
            // 获取Node数组在索引值的位置，CAS操作，保证获取的是主存的最新值
            else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
                // 如果数组该位置为空，
                //    用一次 CAS 操作将这个新值放入其中即可，这个 put 操作差不多就结束了，可以拉到最后面了
                //    如果 CAS 失败，那就是有并发操作，进到下一个循环就好了
                if (casTabAt(tab, i, null,
                             new Node<K,V>(hash, key, value, null)))
                    break;                   // no lock when adding to empty bin
            }
            // 获取节点的状态
            else if ((fh = f.hash) == MOVED)
                tab = helpTransfer(tab, f);
            else {
                V oldVal = null;
                // 对Node节点加对象锁
                synchronized (f) {
                    // 获取数组中Node的位置
                    if (tabAt(tab, i) == f) {
                        if (fh >= 0) {
                            binCount = 1;
                            for (Node<K,V> e = f;; ++binCount) {
                                K ek;
                                // 如果发现了"相等"的 key，判断是否要进行值覆盖，然后也就可以 break 了
                                if (e.hash == hash &&
                                    ((ek = e.key) == key ||
                                     (ek != null && key.equals(ek)))) {
                                    oldVal = e.val;
                                    if (!onlyIfAbsent)
                                        e.val = value;
                                    break;
                                }
                                // 到了链表的最末端，将这个新值放到链表的最后面
                                Node<K,V> pred = e;
                                if ((e = e.next) == null) {
                                    pred.next = new Node<K,V>(hash, key,
                                                              value, null);
                                    break;
                                }
                            }
                        }
                        else if (f instanceof TreeBin) {
                            Node<K,V> p;
                            binCount = 2;
                            // 插入节点到红黑树中
                            if ((p = ((TreeBin<K,V>)f).putTreeVal(hash, key,
                                                           value)) != null) {
                                oldVal = p.val;
                                if (!onlyIfAbsent)
                                    p.val = value;
                            }
                        }
                    }
                }
                // 链表的值大于链表长度限定值，则变成红黑树，这个不在同步块内部
                if (binCount != 0) {
                    if (binCount >= TREEIFY_THRESHOLD)
                        // 这个方法和 HashMap 中稍微有一点点不同，那就是它不是一定会进行红黑树转换，
                        // 如果当前数组的长度小于 64，那么会选择进行数组扩容，而不是转换为红黑树
                        //    具体源码我们就不看了，扩容部分后面说
                        treeifyBin(tab, i);
                    if (oldVal != null)
                        return oldVal;
                    break;
                }
            }
        }
        addCount(1L, binCount);
        return null;
    }
```







# Reference
- [Java7/8 中的 HashMap 和 ConcurrentHashMap 全解析](http://www.importnew.com/28263.html)