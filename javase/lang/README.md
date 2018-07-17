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

## float和dobule
1.1 字面量属于 double 类型，不能直接将 1.1 直接赋值给 float 变量，因为这是向下转型。Java 不能隐式执行向下转型，因为这会使得精度降低。
```java
// float f = 1.1;
float f = 1.1f;
short s1 = 1;
// s1 = s1 + 1; no 结果是int
// += 可以隐式转换
s1 += 1;
```

> 因为字面量 1 是 int 类型，它比 short 类型精度要高，因此不能隐式地将 int 类型下转型为 short 类型。

## Switch
- 从 Java 7 开始，可以在 switch 条件判断语句中使用 String 对象;
- switch 不支持 long，是因为 switch 的设计初衷是为那些只需要对少数的几个值进行等值判断，如果值过于复杂，那么还是用 if 比较合适。

# String
String是final修饰的不可变对象（不可继承），内部持有final修饰的字符数组，String不可变好处：
- 缓存hash值，一次计算；
- String Pool，如果已经创建过的String，直接从字符串常量池中获取（堆），如果值经常变化，则无法使用字符串常量池；
- 天生具备线程安全性；

## StringBuffer与StringBuilder
- String 不可变，因此是线程安全的
- StringBuilder 不是线程安全的
- StringBuffer 是线程安全的，内部使用 synchronized 来同步

## String pool
可以使用String.intern()将字符串加入到字符串常量池中（java1.7以前不建议这么做，因为字符串常量池在永久代，容易造成OutOfMemory。

# 参数传递
Java中参数传递是值传递，对象传递是将对象的地址作为值传入到方法中。而传递对象的引用指向是不会被方法改变的，而引用指向的内容是会被方法改变的。（最简单的验证内容，在方法中交换参数引用，方法外不会受影响）



