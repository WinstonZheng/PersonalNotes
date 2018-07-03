# TreeMap
TreeMap实现红黑树，其保证在log(n)时间内实现Map的containsKey，get，put和remove操作。

1、TreeMap是根据key进行排序的，它的排序和定位需要依赖比较器或覆写Comparable接口，也因此不需要key覆写hashCode方法和equals方法，就可以排除掉重复的key，而HashMap的key则需要通过覆写hashCode方法和equals方法来确保没有重复的key。
2、TreeMap的查询、插入、删除效率均没有HashMap高，一般只有要对key排序时才使用TreeMap。
3、TreeMap的key不能为null，而HashMap的key可以为null。

```java
// key都必须实现Comparable接口，实现compareTo方法，或者使用比较器comparator的compare方法比较
// SortedMap，表示一个有序Key组成的map，当Map以Collection方式遍历时，按照key排序返回；
// NavigableMap，扩展SortedMap，能够通过升序和降序的方式访问Map。
// TreeMap时基于NavigableMap接口的红黑树实现。
public class  TreeMap<K,V>
    extends AbstractMap<K,V>
    implements NavigableMap<K,V>, Cloneable, java.io.Serializable{
    // 基础结构
    private transient Entry<K,V> root;
    /**
     * The number of entries in the tree
     */
    private transient int size = 0;
    
    // Red-black mechanics
    private static final boolean RED   = false;
    private static final boolean BLACK = true;
    
    static final class Entry<K,V> implements Map.Entry<K,V> {
        // 键
        K key;
        // 值
        V value;
        // 左子树
        Entry<K,V> left;
        // 右子树
        Entry<K,V> right;
        // 指向父节点
        Entry<K,V> parent;
        // 着色
        boolean color = BLACK;
        ...
    }
    
    
}
```


> NavigableMap
> 扩展SortedMap，具有了为给定搜索目标报告最接近匹配项的导航方法。方法 lower、floor、ceiling 和 higher 分别返回小于、小于等于、大于等于、大于给定元素的元素，如果不存在这样的元素，则返回 null。 类似地，方法 lowerKey、floorKey、ceilingKey 和 higherKey 只返回关联的键。所有这些方法是为查找条目而不是遍历条目而设计的。

## 基础概念
树相关知识详见[数据结构-树相关知识](/methods/datastructure/tree)
- 二叉树 
- 二叉排序（搜索）树，
- AVL树
- 红黑树


# 基本操作
## 查找操作

```java
final Entry<K,V> getEntry(Object key) {
    // Offload comparator-based version for sake of performance
    // 比较器存在，则用比较器查找
    if (comparator != null)
        return getEntryUsingComparator(key);
    if (key == null)
        throw new NullPointerException();
    @SuppressWarnings("unchecked")
    Comparable<? super K> k = (Comparable<? super K>) key;
    Entry<K,V> p = root;
    while (p != null) {
        int cmp = k.compareTo(p.key);
        if (cmp < 0)
            p = p.left;
        else if (cmp > 0)
            p = p.right;
        else
            return p;
    }
    return null;
}
```

## 插入操作
```java
// 插入K-V数据，如果key存在，则更新value
public V put(K key, V value) {
    // 根节点
    Entry<K,V> t = root;
    if (t == null) {
        // 如果树为空，作为根节点，默认是黑色
        compare(key, key); // type (and possibly null) check

        root = new Entry<>(key, value, null);
        size = 1;
        modCount++;
        return null;
    }
    int cmp;
    Entry<K,V> parent;
    // split comparator and comparable paths
    Comparator<? super K> cpr = comparator;
    if (cpr != null) {
        do {
            parent = t;
            cmp = cpr.compare(key, t.key);
            if (cmp < 0)
                t = t.left;
            else if (cmp > 0)
                t = t.right;
            else
                return t.setValue(value);
        } while (t != null);
    }
    else {
        if (key == null)
            throw new NullPointerException();
            @SuppressWarnings("unchecked")
            Comparable<? super K> k = (Comparable<? super K>) key;
        do {
            parent = t;
            cmp = k.compareTo(t.key);
            if (cmp < 0)
                t = t.left;
            else if (cmp > 0)
                t = t.right;
            else
                return t.setValue(value);
        } while (t != null);
    }
    Entry<K,V> e = new Entry<>(key, value, parent);
    // 查找到根节点
    if (cmp < 0)
        parent.left = e;
    else
        parent.right = e;
    // 上滤，节点已经插入
    fixAfterInsertion(e);
    size++;
    modCount++;
    return null;
}
```

## 删除操作

```java
private void deleteEntry(Entry<K,V> p) {
    modCount++;
    size--;
    // If strictly internal, copy successor's element to p and then make p
    // point to successor. 指向后继节点，由于左右都不为空，则取的是右子树的最大值
    if (p.left != null && p.right != null) {
        Entry<K,V> s = successor(p);
        p.key = s.key;
        p.value = s.value;
        p = s;
    } // p has 2 children

    // Start fix up at replacement node, if it exists.
    // p要不只有一颗子树，要不就是叶子节点；
    Entry<K,V> replacement = (p.left != null ? p.left : p.right);

    if (replacement != null) {
        // Link replacement to parent
        // p只有一颗子树，直接用子树的根节点替换目标节点
        replacement.parent = p.parent;
        if (p.parent == null)
            root = replacement;
        else if (p == p.parent.left)
            p.parent.left  = replacement;
        else
            p.parent.right = replacement;

        // Null out links so they are OK to use by fixAfterDeletion.
        p.left = p.right = p.parent = null;

        // Fix replacement
        if (p.color == BLACK)
            // 如果颜色为黑色，则需要修复
            fixAfterDeletion(replacement);
    } else if (p.parent == null) { // return if we are the only node.
        root = null;
    } else { //  No children. Use self as phantom replacement and unlink.
        // p是叶子节点
        if (p.color == BLACK)
            fixAfterDeletion(p);

        if (p.parent != null) {
            if (p == p.parent.left)
                p.parent.left = null;
            else if (p == p.parent.right)
                p.parent.right = null;
            p.parent = null;
        }
    }
}
```


## 颜色调整
上滤操作，具体见源码，这里就不贴出来。












