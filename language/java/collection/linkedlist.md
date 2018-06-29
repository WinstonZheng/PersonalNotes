# LinkedList
LinkedList底层采用双向链表的方式实现，链表的节点是存储两个引用，指向前节点的引用和指向后节点的引用。

```java
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
LinkedList包含两个分别指向首尾的指针，初始化时都为空。

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
删除

## 更新

## 查找





