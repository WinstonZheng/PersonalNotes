# java集合框架

![](/images/java/collection/java-colletions.jpg)

从上图中可以看出，集合类主要分为两大类：Collection和Map。

抽象类AbstractCollection、AbstractList和AbstractSet分别实现了Collection、List和Set接口，这就是在Java集合框架中用的很多的[适配器设计模式](/methods/design-patterns/adapter.md)，用这些抽象类去实现接口，在抽象类中实现接口中的若干或全部方法，这样下面的一些类只需直接继承该抽象类，并实现自己需要的方法即可，而不用实现接口中的全部抽象方法。

## Collection
Collection是List、Set等集合高度抽象出来的接口，它包含了这些集合的基本操作，它主要又分为两大部分：List和Set。

### List
List接口通常表示一个列表（数组、队列、链表、栈等），其中的元素可以重复，常用实现类为ArrayList和LinkedList，另外还有不常用的Vector。另外，LinkedList还是实现了Queue接口，因此也可以作为队列使用。

### Set
Set接口通常表示一个集合，其中的元素不允许重复（通过hashcode和equals函数保证），常用实现类有HashSet和TreeSet，HashSet是通过Map中的HashMap实现的，而TreeSet是通过Map中的TreeMap实现的。另外，TreeSet还实现了SortedSet接口，因此是有序的集合（集合中的元素要实现Comparable接口，并覆写Compartor函数才行）。

### Queue
Queue是队列的实现思想，主要的扩展分为两部分BlockingQueue和Deque。BlockingQueue，主要提供put()和take()方法，实现阻塞的元素获取和添加，在concurrent子包中，常用于多线程并发场景；Deque实现双端队列的操作，能从两边获取、加入元素。

## Map
Map是一个映射接口，其中的每个元素都是一个key-value键值对，同样抽象类AbstractMap通过适配器模式实现了Map接口中的大部分函数，TreeMap、HashMap、WeakHashMap等实现类都通过继承AbstractMap来实现，另外，不常用的HashTable直接实现了Map接口，它和Vector都是JDK1.0就引入的集合类。

## Iterator
 Iterator是遍历集合的迭代器（不能遍历Map，只用来遍历Collection），Collection的实现类都实现了iterator()函数，它返回一个Iterator对象，用来遍历集合，ListIterator则专门用来遍历List。而Enumeration则是JDK1.0时引入的，作用与Iterator相同，但它的功能比Iterator要少，它只能再Hashtable、Vector和Stack中使用。
 
 ## Arrays and Collections
  Arrays和Collections是用来操作数组、集合的两个工具类，例如在ArrayList和Vector中大量调用了Arrays.Copyof()方法，而Collections中有很多静态方法可以返回各集合类的synchronized版本，即线程安全的版本，当然了，如果要用线程安全的结合类，首选Concurrent并发包下的对应的集合类。

此外，提供了如下几种方法：
- 排序操作（基于JDK1.7的DualPivotQuicksort），以及并发排序（JDK1.8）操作；
- 二分查找；
- 批量赋值；
- copyOf（ArrayList的添加删除操作的底层依赖）；
等等


# Reference
- [Java集合框架](https://blog.csdn.net/ns_code/article/details/35564663)