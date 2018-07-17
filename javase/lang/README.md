# 基本类型
java中基本类型对象都包含缓冲区，其中Integer通过数组的方式存储了默认-127到128的数字对象，其valueOf方法就是首先查找缓冲区中是否存在，如果不存在，则新建对象（可以通过JVM参数修改缓冲区大小）。
- jdk1.5引入了自动装箱和拆箱的功能，在Integer和int之间操作，具体例子如下：
```java
// Integer.valueOf
Integer i = 10;
// Integer.intValue
int j = i++;
```

- 由于在int和Integer使用时，Integer作为一个对象，会包含对象头（Mark Word，Hash值，GC年龄，锁等信息）和实例数据，所以占内存较大，建议使用int。

- Integer时不可变对象，value是final修饰，但是不是线程安全的。