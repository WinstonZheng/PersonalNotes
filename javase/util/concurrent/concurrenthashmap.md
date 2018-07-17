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









# Reference
- [Java7/8 中的 HashMap 和 ConcurrentHashMap 全解析](http://www.importnew.com/28263.html)