# HashMap
HashMap是最常用的Map类型（K-V形式）实现，基本的实现原理是通过哈希表的方式。


```java
public class HashMap<K,V> extends AbstractMap<K,V>
    implements Map<K,V>, Cloneable, Serializable {
    
}
```

HashMap是非线程安全的，只是用于单线程环境下，多线程环境下可以采用concurrent并发包下的concurrentHashMap。

HashMap 实现了Serializable接口，因此它支持序列化，实现了Cloneable接口，能被克隆。

## Basic
哈希表比较关键的两个点：
1. hash function;
2. 解决冲突的方法。

哈希表的查询效率高（理想无冲突下，O（1）），

> 装填因子：表中元素个数和表大小的比。
