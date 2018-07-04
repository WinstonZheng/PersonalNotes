# LinkedHashMap
LinkedHashMap由于继承自HashMap，因此它具有HashMap的所有特性，同样允许key和value为null。


```java
public class LinkedHashMap<K,V>
    extends HashMap<K,V>
    implements Map<K,V>{
    
    /**
     * The head (eldest) of the doubly linked list.
     */
    transient LinkedHashMap.Entry<K,V> head;

    /**
     * The tail (youngest) of the doubly linked list.
     */
    transient LinkedHashMap.Entry<K,V> tail;        
    
    /**
     * The iteration ordering method for this linked hash map: <tt>true</tt>
     * for access-order, <tt>false</tt> for insertion-order.
     * 默认是false
     * @serial
     */
    final boolean accessOrder;
    
    // Entry作为中介，也可以转化为HashMap.TreeNode 
    static class Entry<K,V> extends HashMap.Node<K,V> {
        Entry<K,V> before, after;
        Entry(int hash, K key, V value, Node<K,V> next) {
            super(hash, key, value, next);
        }
    }
 
     
    Node<K,V> newNode(int hash, K key, V value, Node<K,V> e) {
        LinkedHashMap.Entry<K,V> p =
            new LinkedHashMap.Entry<K,V>(hash, key, value, e);
        linkNodeLast(p);
        return p;
    }
                   
}
```

LinkedHashMap内部维护了一个双向链表，按照插入的顺序，将HashMap中的节点放置在链表尾部。如果accessOrder为True时，在链表被访问时，会将被访问的对象放置在双向链表的尾部。

HashMap.TreeNode扩展了LinkedHashMap.Entry，可以在链表中支持普通node和treenode两种类型。




# 基本操作

## 插入操作
LinkedHashMap通过重写newNode和newTreeNode，实现双向链表的插入操作(HashMap的putVal()方法会调用newNode创建节点)。

```java
Node<K,V> newNode(int hash, K key, V value, Node<K,V> e) {
        LinkedHashMap.Entry<K,V> p =
            new LinkedHashMap.Entry<K,V>(hash, key, value, e);
        linkNodeLast(p);
        return p;
}

TreeNode<K,V> newTreeNode(int hash, K key, V value, Node<K,V> next) {
        TreeNode<K,V> p = new TreeNode<K,V>(hash, key, value, next);
        linkNodeLast(p);
        return p;
}

```
## 查找操作
HashMap提供了afterNodeAccess方法，支持在accessOrder为true时，能够每次访问节点之后，将节点放置在双向链表的尾部。

```java
void afterNodeAccess(Node<K,V> e) { // move node to last
        LinkedHashMap.Entry<K,V> last;
        if (accessOrder && (last = tail) != e) {
            LinkedHashMap.Entry<K,V> p =
                (LinkedHashMap.Entry<K,V>)e, b = p.before, a = p.after;
            p.after = null;
            if (b == null)
                head = a;
            else
                b.after = a;
            if (a != null)
                a.before = b;
            else
                last = b;

            if (last == null)
                head = p;
            else {
                p.before = last;
                last.after = p;
            }
            tail = p;
            ++modCount;
        }
}
```

## 删除操作

```java
// 在链表中删除
void afterNodeRemoval(Node<K,V> e) { // unlink
        LinkedHashMap.Entry<K,V> p =
            (LinkedHashMap.Entry<K,V>)e,
                b = p.before,
                a = p.after;
        p.before = p.after = null;
        if (b == null)
            head = a;
        else
            b.after = a;
        if (a == null)
            tail = b;
        else
            a.before = b;
}
```

## LRU
LinkedHashMap是如何实现LRU的（缓存）。

首先，当accessOrder为true时，才会开启按访问顺序排序的模式，才能用来实现LRU算法。

无论是put方法还是get方法，都会导致目标Entry成为最近访问的Entry，因此便把该Entry加入到了双向链表的末尾。

这样便把最近使用了的Entry放入到了双向链表的后面，多次操作后，双向链表前面的Entry便是最近没有使用的，这样当节点个数满的时候，删除的最前面的Entry(head后面的那个Entry)便是最近最少使用的Entry。


















