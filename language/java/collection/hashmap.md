# HashMap
HashMap是最常用的Map类型（K-V形式）实现，基本的实现原理是通过哈希表的方式存储数据。

具体流程如下，当往 HashMap 中 put 元素的时候，先根据 key 的 hashCode 重新计算 hash 值，根据 hash 值再通过高位运算和取模运算得到这个元素在数组中的位置（即下标），如果数组该位置上已经存放有其他元素了，那么在这个位置上的元素将以链表的形式存放，新加入的放在链尾，如果该链表超出8个的话，就转换成红黑树。如果数组该位置上没有元素，就直接将该元素放到此数组中的该位置上。


```java
public class HashMap<K,V> extends AbstractMap<K,V>
    implements Map<K,V>, Cloneable, Serializable {
    
}
```

HashMap是非线程安全的，只是用于单线程环境下，多线程环境下可以采用concurrent并发包下的concurrentHashMap。

HashMap 实现了Serializable接口，因此它支持序列化，实现了Cloneable接口，能被克隆。

HashMap的key能为null，value也能为null。

## Basic
哈希表比较关键的两个点：
1. hash function;
2. 解决冲突的方法。

哈希表的查询效率高（理想无冲突下，O（1）），

> 装填因子：表中元素个数和表大小的比。


# 基本操作

## 默认配置

```java
// 默认初始值
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4;
// 默认最大值
static final int MAXIMUM_CAPACITY = 1 << 30;
// 默认记载因子
static final float DEFAULT_LOAD_FACTOR = 0.75f;
// 转化因子，超过该值，则将链表转化为红黑树。
static final int TREEIFY_THRESHOLD = 8;
// 在一次resize中，将树还原成链表的最大值，当树中元素小于该值，还原成链表。
static final int UNTREEIFY_THRESHOLD = 6;
// 当链表转树时，要求的数组存储的最小大小。如果，不满足，则首先选择resize，而不是转成红黑树。
static final int MIN_TREEIFY_CAPACITY = 64;
// 链表节点数据结构
static class Node<K,V> implements Map.Entry<K,V> {
        final int hash;
        final K key;
        V value;
        Node<K,V> next;
        ...
}
// 树节点（红黑树）
static final class TreeNode<K,V> extends LinkedHashMap.Entry<K,V> {
        TreeNode<K,V> parent;  // red-black tree links
        TreeNode<K,V> left;
        TreeNode<K,V> right;
        TreeNode<K,V> prev;    // needed to unlink next upon deletion
        boolean red;
        ...
}




```

## hash function（hash函数）

key.hashCode()函数调用的时key键值类型自带的哈希函数，返回`int`类型的散列表。散列表范围很大，但用之前还要先做对数组的长度取模运算，得到余数才能用来访问数组下标。

这解释了hashmap为什么要将数组长度取2的整次幂。因为数组长度减1正好相当于一个低位掩码。将散列值的高位全部归零，只保留低位值，用来做数组下标访问。

```java

// p = tab[i = (n - 1) & hash
// 插入时与数组长度做并运算保留低位信息，在putval方法里(高效取模)。
static final int hash(Object key) {
        int h;
        // 将32位整型的前16位与后16位异或
        // 扰动函数，自己的高半区和低半区做异或，为了混合原始
        // 哈希值的高位和低位，以此来加大低位的随机性。而且混合后的低位掺杂了高位的部分特征，
        // 这样高位的信息也变相保留了下来。
        return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}

```

## 插入

```java
public V put(K key, V value) {
        return putVal(hash(key), key, value, false, true);
}

final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
                   boolean evict) {
        // p指向的是hash后表中的节点
        Node<K,V>[] tab; 
        Node<K,V> p; 
        int n, i;
        // 如果当前表为空, 则创建一个新表（通过resize()）
        if ((tab = table) == null || (n = tab.length) == 0)
            n = (tab = resize()).length;
        // 如果hash到的位置为空，则插入。
        if ((p = tab[i = (n - 1) & hash]) == null)
            tab[i] = newNode(hash, key, value, null);
        else {//当前的hash表位置已经有值存在，p指向表中值，产生冲突。
            //如果当前值在链表/数组中存在，则将赋值给e。
            Node<K,V> e; 
            K k;
            // 如果两个值相等，则将p赋值给e
            if (p.hash == hash &&
                ((k = p.key) == key || (key != null && key.equals(k))))
                e = p;
            // 如果p是树节点
            else if (p instanceof TreeNode)
                e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
            // p是链表节点
            else {
                for (int binCount = 0; ; ++binCount) {
                    // 插入链表
                    if ((e = p.next) == null) {
                        p.next = newNode(hash, key, value, null);
                        // 一个位置的链表长度超过8个，则将链表组成红黑树。
                        // 如果链表过短，则先扩展链表。
                        if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                            treeifyBin(tab, hash);
                        break;
                    }
                    if (e.hash == hash &&
                        ((k = e.key) == key || (key != null && key.equals(k))))
                        break;
                    p = e;
                }
            }

            if (e != null) { // existing mapping for key
                V oldValue = e.value;
                if (!onlyIfAbsent || oldValue == null)
                    e.value = value;
                // 用于LinkedHashMap调整
                afterNodeAccess(e);
                return oldValue;
            }
        }
        ++modCount;
        // HashMap的阈值，用于判断是否需要调整HashMap的容量（threshold = 容量*加载因子）
        if (++size > threshold)
            resize();

        // 用于LinkedHashMap调整，HashMap中并没有实现
        afterNodeInsertion(evict);
        return null;
}

final void treeifyBin(Node<K,V>[] tab, int hash) {
        int n, index; Node<K,V> e;
        if (tab == null || (n = tab.length) < MIN_TREEIFY_CAPACITY)
            resize();
        else if ((e = tab[index = (n - 1) & hash]) != null) {
            TreeNode<K,V> hd = null, tl = null;
            do {
                TreeNode<K,V> p = replacementTreeNode(e, null);
                if (tl == null)
                    hd = p;
                else {
                    p.prev = tl;
                    tl.next = p;
                }
                tl = p;
            } while ((e = e.next) != null);
            if ((tab[index] = hd) != null)
                hd.treeify(tab);
        }
}


```

## 容量及扩容










# Reference
- [How does a HashMap work in JAVA](http://coding-geek.com/how-does-a-hashmap-work-in-java/)
- [jdk源码中hashmap的hash方法原理是什么](https://www.zhihu.com/question/20733617/answer/111577937)
- [HashMap中tableSizeFor的一个精巧的算法](https://blog.csdn.net/dagelailege/article/details/52972970)
- [Java 1.8中HashMap的resize()方法扩容部分的理解](https://blog.csdn.net/u013494765/article/details/77837338)
- [jdk1.8 HashMap put时确定元素位置的方法与扩容拷贝元素确定位置的方式冲突？](https://www.zhihu.com/question/44460053)
- [哈希表](http://www.cnblogs.com/jiewei915/archive/2010/08/09/1796042.html)





