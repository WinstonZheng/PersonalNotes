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

## 基本概念
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
// 树节点（红黑树），还是基于上面的Node类
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
HashMap元素插入操作，进行如下几个流程：
1. 如果当前表为空（或者长度为0），则进行resize()初始化扩容；
2. 通过hash函数以及与操作(%)，找到hash位置，如果表的元素为null，直接插入；如果not null，进行3；
3. 判断节点类型是否为TreeNode，是，则调用putTreeVal，在红黑树中插入值；如果不是，则进行4；
4. 节点为链表节点，插入节点，如果链表中存在节点，则替换旧值，并返回旧值（onlyIfAbsent ），如果不存在，进行5；
5. 在链表末尾插入新节点，并判断链表长度是否超过规定值(TREEIFY_THRESHOLD )，如果超过，则转换成红黑树。


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
```

## 链表红黑树转换
TODO： 如何转化的细节

```java
final void treeifyBin(Node<K,V>[] tab, int hash) {
        int n, index; Node<K,V> e;
        // 判断是否数组太小，太小首先扩容
        if (tab == null || (n = tab.length) < MIN_TREEIFY_CAPACITY)
            resize();
        // 将tab中的Node转化为TreeNode
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

扩容是一个相当耗时的操作，因为它需要重新计算这些元素在新的数组中的位置并进行复制处理。因此，我们在用HashMap的时，最好能提前预估下HashMap中元素的个数，这样有助于提高HashMap的性能。

```java

// 以保证返回一个比给定整数大且最接近的2的幂次方的整数。(利用位操作和或操作）,举个例子容易理解。
static final int tableSizeFor(int cap) {
        int n = cap - 1;
        n |= n >>> 1;
        n |= n >>> 2;
        n |= n >>> 4;
        n |= n >>> 8;
        n |= n >>> 16;
        return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
}

/*
* 向map中添加新的key/value时，将会检查是否需要扩容。map存了两个数据：map的size和threshold。
* size表示在map中存的entry的数目。这个值在每次插入和删除时都会更新。
* threshold等于(数组容量 * loadFactor)。在每次扩容后刷新。
*/
final Node<K,V>[] resize() {

        Node<K,V>[] oldTab = table;

        int oldCap = (oldTab == null) ? 0 : oldTab.length;
        // 通过加载因子计算的存储容量上限
        int oldThr = threshold;
        int newCap, newThr = 0;

        // 扩容
        // 原数组长度大于最大容量(1073741824) 则将threshold设为Integer.MAX_VALUE=2147483647
        if (oldCap > 0) {
            // 达到最大值
            if (oldCap >= MAXIMUM_CAPACITY) {
                threshold = Integer.MAX_VALUE;
                return oldTab;
            }
            // 如果未达到最大值，则扩展两倍。
            else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                     oldCap >= DEFAULT_INITIAL_CAPACITY)
                // 如果原来的thredshold大于0则将容量设为原来的thredshold
                // 在第一次带参数初始化时候会有这种情况（see带参的初始化函数）
                newThr = oldThr << 1; // double threshold
        }
        else if (oldThr > 0) // initial capacity was placed in threshold，构造器传入threshold
            newCap = oldThr;
        else {               // zero initial threshold signifies using defaults 构造器为空
            newCap = DEFAULT_INITIAL_CAPACITY;
            newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
        }


        if (newThr == 0) {
            //如果新的容量等于0
            float ft = (float)newCap * loadFactor;
            newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                      (int)ft : Integer.MAX_VALUE);
        }

        threshold = newThr;
        @SuppressWarnings({"rawtypes","unchecked"})
            Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
        
        table = newTab;
        // 将旧的值插入到扩容的新数组中。
        if (oldTab != null) {
            for (int j = 0; j < oldCap; ++j) {
                Node<K,V> e;

                if ((e = oldTab[j]) != null) {
                    // 垃圾回收
                    oldTab[j] = null;
                    if (e.next == null)
                        // 重新计算位置
                        newTab[e.hash & (newCap - 1)] = e;
                    else if (e instanceof TreeNode)
                        // 当后接的红黑树时
                        ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                    else { // preserve order
                        // 进行链表复制
                        // 没有重新计算元素在数组中的位置
                        // 而是采用了原始位置加原数组长度的方法计算得到位置
		        //命名lo和hi，就是将新table分为了两部分，原先大小的部分（lo）和新扩容大小的部分（hi）。
                        // 原先大小
                        Node<K,V> loHead = null, loTail = null;
                        // 扩容后大小
                        Node<K,V> hiHead = null, hiTail = null;
                        Node<K,V> next;
                        do {
                            // 链表下一个节点
                            next = e.next;
                            // 说明e的哈希位置没有超出老的链表范围
                            // 计算元素的在数组中的位置是否需要移动，确定当前节点时放在lo还是hi中。可进行数学推导。详见参考5
                            if ((e.hash & oldCap) == 0) {
                                if (loTail == null)
                                    loHead = e;
                                else
                                    loTail.next = e;
                                loTail = e;
                            }
                            else {
                                // 说明，e的哈希位置超出老的范围，
                                // 当扩容时，位置会发生变化，也就会生成新的链表。
                                if (hiTail == null)
                                    hiHead = e;
                                else
                                    hiTail.next = e;
                                hiTail = e;
                            }
                        } while ((e = next) != null);
                        if (loTail != null) {
                            loTail.next = null;
                            newTab[j] = loHead;
                        }
                        if (hiTail != null) {
                            hiTail.next = null;
                            newTab[j + oldCap] = hiHead;
                        }
                    }
                }
            }
        }
        return newTab;
}
```

> HashMap为什么树化？
> 本质上是个安全问题，如果一个对象发生hash冲突，都被放置在同一个桶里面，则会形成一个链表，严重影响存储性能。而在现实世界中，构造hash冲突的数据并不复杂，恶意代码利用大量hash冲突数据访问服务端，构成hash碰撞拒绝服务攻击。


## 其他操作
1. 注意containsKey方法和containsValue方法。前者直接可以通过key的哈希值将搜索范围定位到指定索引对应的链表，而后者要对哈希数组的每个链表进行搜索。
2. HashMap中则通过h&(length-1)的方法来代替取模，同样实现了均匀的散列，但效率要高很多，这也是HashMap对Hashtable的一个改进。
3. 为什么哈希表的容量一定要是2的整数次幂

    首先，length为2的整数次幂的话，h&(length-1)就相当于对length取模，这样便保证了散列的均匀，同时也提升了效率；其次，length为2的整数次幂的话，为偶数，这样length-1为奇数，奇数的最后一位是1，这样便保证了h & (length-1)的最后一位可能为0，也可能为1（这取决于h的值），即与后的结果可能为偶数，也可能为奇数，这样便可以保证散列的均匀性，而如果length为奇数的话，很明显length-1为偶数，它的最后一位是0，这样h & (length-1)的最后一位肯定为0，即只能为偶数，这样任何hash值都只会被散列到数组的偶数下标位置上，这便浪费了近一半的空间，因此，length取2的整数次幂，是为了使不同hash值发生碰撞的概率较小，这样就能使元素在哈希表中均匀地散列。



## 线程安全

### HashTable

Hashtable同样是基于哈希表实现的，同样每个元素是一个key-value对，其内部也是通过单链表解决冲突问题，容量不足（超过了阀值）时，同样会自动增长。（将核心操作方法加上了sychronized，线程安全）

Hashtable也是JDK1.0引入的类，是线程安全的，能用于多线程环境中。

Hashtable同样实现了Serializable接口，它支持序列化，实现了Cloneable接口，能被克隆。

```java
public class Hashtable<K,V>  
    extends Dictionary<K,V>  
    implements Map<K,V>, Cloneable, java.io.Serializable { 
    
}
```
1. Hashtable使用链表解决冲突，但是并不会转化为红黑树；
2. Hashtable计算hash值，直接用key的hashCode()，而HashMap重新计算了key的hash值，Hashtable在求hash值对应的位置索引时，用取模运算，而HashMap在求位置索引时，则用与运算，且这里一般先用hash&0x7FFFFFFF后，再对length取模，&0x7FFFFFFF的目的是为了将负的hash值转化为正值，因为hash值有可能为负数，而&0x7FFFFFFF后，只有符号外改变，而后面的位都不变；
3. HashTable在不指定容量的情况下的默认容量为11，而HashMap为16，Hashtable不要求底层数组的容量一定要为2的整数次幂，而HashMap则要求一定为2的整数次幂。
4. Hashtable中key和value都不允许为null，而HashMap中key和value都允许为null（key只能有一个为null，而value则可以有多个为null）。但是如果在Hashtable中有类似put(null,null)的操作，编译同样可以通过，因为key和value都是Object类型，但运行时会抛出NullPointerException异常，这是JDK的规范规定的。

总体来说HashTable和HashMap的实现思路上差别不大，但是，可以看到HashMap进行了很多优化（用与操作、链表转树），所以单线程操作下现在很少用HashTable，多用HashMap。此外，多线程底下的ConcurrentHashMap效率也高于HashTabel。





# Reference
- [How does a HashMap work in JAVA](http://coding-geek.com/how-does-a-hashmap-work-in-java/)
- [jdk源码中hashmap的hash方法原理是什么](https://www.zhihu.com/question/20733617/answer/111577937)
- [HashMap中tableSizeFor的一个精巧的算法](https://blog.csdn.net/dagelailege/article/details/52972970)
- [Java 1.8中HashMap的resize()方法扩容部分的理解](https://blog.csdn.net/u013494765/article/details/77837338)
- [jdk1.8 HashMap put时确定元素位置的方法与扩容拷贝元素确定位置的方式冲突？](https://www.zhihu.com/question/44460053)
- [哈希表](http://www.cnblogs.com/jiewei915/archive/2010/08/09/1796042.html)





