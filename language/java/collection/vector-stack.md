# Vector
Vector也是基于数组实现的，是一个动态数组，其容量能自动增长。

Vector是JDK1.0引入了，它的很多实现方法都加入了同步语句，因此是线程安全的（其实也只是相对安全，有些时候还是要加入同步语句来保证线程的安全），可以用于多线程环境。

Vector没有实现Serializable接口，因此它不支持序列化，实现了Cloneable接口，能被克隆，实现了RandomAccess接口，支持快速随机访问。

```
public class Vector<E>
    extends AbstractList<E>
    implements List<E>, RandomAccess, Cloneable, java.io.Serializable
    {
        // 初始的大小为10
    }
```

# 操作
1. 注意扩充容量的方法ensureCapacityHelper。与ArrayList相同，Vector在每次增加元素（可能是1个，也可能是一组）时，都要调用该方法来确保足够的容量。当容量不足以容纳当前的元素个数时，就先看构造方法中传入的容量增长量参数CapacityIncrement是否为0，如果不为0，就设置新的容量为就容量加上容量增长量，如果为0，就设置新的容量为旧的容量的2倍，如果设置后的新容量还不够，则直接新容量设置为传入的参数（也就是所需的容量），而后同样用Arrays.copyof()方法将元素拷贝到新的数组。

2. Vector可以看做是ArrayList的同步实现，操作添加了sychronized同步语句；

3. Vector可以存储NULL; 


# Stack
Stack是扩展了Vector接口，实现了Stack的push和pop操作。