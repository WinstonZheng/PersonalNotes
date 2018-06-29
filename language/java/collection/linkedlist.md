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



## 操作
