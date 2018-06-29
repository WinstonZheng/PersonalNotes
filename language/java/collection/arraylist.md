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



# 基础操作
注意，每次操作都会修改modCount，modCount记录集合的变化次数，迭代器通过modCount判断在迭代过程中是否有修改，如果有，则会抛出异常。

## 增加
添加时，首先判断数组是否为空，空则初始化为10个对象大小数组，此外，如果数组已满，则扩展为目前数组长度的1.5倍大小的新对象数组。（如果数组长度过大，超出int值，则会变成负数，抛出OutOfMemoryError）
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
```
public E set(int index, E element) {
        rangeCheck(index);

        E oldValue = elementData(index);
        elementData[index] = element;
        return oldValue;
    }
```
## subList
subList方法，返回一个SubList对象，属于ArrayList的内部类，记录边界值，引用的对象数组还是父类的对象数组。
