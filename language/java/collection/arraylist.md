# ArrayList
底层数据存储使用对象数组的方式实现。只有在取出数据的时候，进行强制类型转换。数组的查找操作速度快O(1)，而插入和删除的操作很慢，基本涉及到O(n)的时间复杂度。
```java
public class ArrayList<E> extends AbstractList<E>
        implements List<E>, RandomAccess, Cloneable, java.io.Serializable
        {        
                // 基于数组实现，transient关键字，表示修饰对象不能序列化
                transient Object[] elementData;
                // 目前存储在数组中对象的数量
                private int size;
        }
        
```
ArrayList不是线程安全的，只能用在单线程环境下，多线程环境下可以考虑用Collections.synchronizedList(List l)函数返回一个线程安全的ArrayList类，也可以使用concurrent并发包下的CopyOnWriteArrayList类。

ArrayList实现了Serializable接口，因此它支持序列化，能够通过序列化传输，实现了RandomAccess接口，支持快速随机访问，实际上就是通过下标序号进行快速访问，实现了Cloneable接口，能被克隆。


# 基础操作
注意，每次操作都会修改modCount，modCount记录集合的变化次数，迭代器通过modCount判断在迭代过程中是否有修改，如果有，则会抛出异常。

## 增加

```java
public boolean add(E e) {
        ensureCapacityInternal(size + 1);  // Increments modCount!!
        elementData[size++] = e;
        return true;
}

public void add(int index, E element) {
        rangeCheckForAdd(index);

        ensureCapacityInternal(size + 1);  // Increments modCount!!
        System.arraycopy(elementData, index, elementData, index + 1,
                         size - index);
        elementData[index] = element;
        size++;
}
```
添加时，首先判断数组是否为空，空则初始化为10个对象大小数组，此外，注意扩容方法ensureCapacity，ArrayList在每次增加元素（可能是1个，也可能是一组）时，都要调用该方法来确保足够的容量。

当容量不足以容纳当前的元素个数时，调用grow函数，就设置新的容量为旧的容量的1.5倍（向下取整，如果数组长度过大，超出int值，则会变成负数，抛出OutOfMemoryError），而后用Arrays.copyof()方法将元素拷贝到新的数组。

从中可以看出，当容量不够时，每次增加元素，都要将原来的元素拷贝到一个新的数组中，非常耗时，也因此建议在事先能确定元素数量的情况下，才使用ArrayList，否则建议使用LinkedList。

> Arrays.copyof() 和 System.arraycopy()方法
该方法被标记了native，调用了系统的C/C++代码，最终调用了C语言的memmove()函数（建议复制大量数组采用），保证同一个数组内元素的正确复制和移动，比一般的复制方法的实现效率要高很多。

## 删除
通过System.arraycopy方法，进行批量数组移动，然后最后一个值清空（= null）。
支持根据index删除和对象删除。对象删除需要进行查找操作。

## 查找
提供了indexOf和lastIndexOf方法，分别为从头开始和从尾开始遍历，这里注意，遍历区别是否为null。
```java
public boolean contains(Object o) {
        return indexOf(o) >= 0;
    }
```

## 更新
更新，进行替换操作，并返回旧值。
```java
public E set(int index, E element) {
        rangeCheck(index);

        E oldValue = elementData(index);
        elementData[index] = element;
        return oldValue;
    }
```
## subList
subList方法，返回一个SubList对象，属于ArrayList的内部类，记录边界值，引用的对象数组还是父类的对象数组。

## toArray
第一个，Object[] toArray()方法。该方法有可能会抛出java.lang.ClassCastException异常，如果直接用向下转型的方法，将整个ArrayList集合转变为指定类型的Array数组，便会抛出该异常，而如果转化为Array数组时不向下转型，而是将每个元素向下转型，则不会抛出该异常，显然对数组中的元素一个个进行向下转型，效率不高，且不太方便。

第二个，<T> T[] toArray(T[] a)方法。该方法可以直接将ArrayList转换得到的Array进行整体向下转型（转型其实是在该方法的源码中实现的），且从该方法的源码中可以看出，参数a的大小不足时，内部会调用Arrays.copyOf方法，该方法内部创建一个新的数组返回，因此对该方法的常用形式如下：

```java
public static Integer[] vectorToArray2(ArrayList<Integer> v) {  
    Integer[] newText = (Integer[])v.toArray(new Integer[0]);  
    return newText;  
}
```

注意，测试代码如下：
```java
public class Student {
    private String name;
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }     
}

public static void main(String[] args) {
        ArrayList<Student> students = new ArrayList<>();
        students.add(new Student("haha"));
        students.add(new Student("hehe"));
        Student[] stu = students.toArray(new Student[0]);
        stu[0].setName("123");
        System.out.println(students.get(0));
        System.out.println(stu[0]);
}

// result
Student{name='123'}
Student{name='123'}
```
说明，Arrays.copyof生成的数组中的元素指向的相同的对象（可能和native实现方法关联）。






