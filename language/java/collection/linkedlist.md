# LinkedList
LinkedList底层采用双向链表的方式实现，链表的节点是存储两个引用，指向前节点的引用和指向后节点的引用。
LinkedList是基于链表实现的，所以增删效率高，查找效率低。
```java
// AbstractSequentialList表示元素顺序访问
// Deque表示队列两边都能进出数据（扩展了Queue接口）
public class LinkedList<E>
    extends AbstractSequentialList<E>
    implements List<E>, Deque<E>, Cloneable, java.io.Serializable
    {
        // 头结点
        transient Node<E> first;
        transient Node<E> last;
         // 节点
        private static class Node<E> {
            E item;
            Node<E> next;
            Node<E> prev;
    
            Node(Node<E> prev, E element, Node<E> next) {
                this.item = element;
                this.next = next;
                this.prev = prev;
            }
        }
    }
```
LinkedList是基于双向循环链表（从源码中可以很容易看出）实现的，除了可以当做链表来操作外，它还可以当做栈、队列和双端队列来使用。

LinkedList同样是非线程安全的，只在单线程下适合使用。

LinkedList实现了Serializable接口，因此它支持序列化，能够通过序列化传输，实现了Cloneable接口，能被克隆。


# 操作
LinkedList包含两个分别指向首尾的指针，初始化时都为空，LinkedList支持item值为空的节点。

## 增加
初始化时，首尾的引用指向的都是新添加的节点。

```java
void linkLast(E e) {
        final Node<E> l = last;
        final Node<E> newNode = new Node<>(l, e, null);
        last = newNode;
        if (l == null)
            first = newNode;
        else
            l.next = newNode;
        size++;
        modCount++;
    }
```

## 删除
删除操作从首节点开始往后遍历。

```java
public boolean remove(Object o) {
        if (o == null) {
            for (Node<E> x = first; x != null; x = x.next) {
                if (x.item == null) {
                    unlink(x);
                    return true;
                }
            }
        } else {
            for (Node<E> x = first; x != null; x = x.next) {
                if (o.equals(x.item)) {
                    unlink(x);
                    return true;
                }
            }
        }
        return false;
    }
```

## 更新
根据index值替换对应的node节点的item值，并返回旧值。

## 查找
链表通过node函数获取对应的索引值的引用。(查找操作与ArrayList类似，分为null和非null情况，遍历数组)
```java
/**
     * Returns the (non-null) Node at the specified element index.
     * 判断离链表首位近，还是离链表末尾近
     */
Node<E> node(int index) {
        // assert isElementIndex(index);

        if (index < (size >> 1)) {
            Node<E> x = first;
            for (int i = 0; i < index; i++)
                x = x.next;
            return x;
        } else {
            Node<E> x = last;
            for (int i = size - 1; i > index; i--)
                x = x.prev;
            return x;
        }
    }
```

## Queue and Stack
LinkedList支持栈和队列的操作。



