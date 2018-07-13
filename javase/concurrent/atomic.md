# Basic
## CAS
CAS操作从表面上来看叫做比较并替换，是CPU新增的一条原子指令，能保证这两步操作的原子性。CAS指令的使用，则是通过记录一个原始值，并进行一系列操作，然后调用CAS指令，成功则操作成功；失败，则采用一些补偿操作，例如：重试。
## ABA问题
当一个线程a采用CAS操作，在获取旧值A之后修改的期间，有线程b将这个值先修改成了B，又有一个线程c将其修改成了A，那么此时线程a采用CAS操作，将认为值并没有被修改过。
> 如何解决此问题？ 基于维护版本的思想，AtomicStampedReference原子类是一个带有时间戳的对象引用，在每次修改后，AtomicStampedReference不仅会设置新值而且还会记录更改的时间。每次CAS操作就是更新对象引用（时间戳 + 新值）。

# Unsafe
Atomic类型的数据底层使用Unsafe类提供CAS操作，Unsafe类在sun.misc包下，不属于Java标准。Unsafe采用了单例模式，只有Bootstrap类加载器加载的类才能使用。(只有加载器为Null的类)

```java
public static Unsafe getUnsafe() {
        Class var0 = Reflection.getCallerClass();
        if (!VM.isSystemDomainLoader(var0.getClassLoader())) {
            throw new SecurityException("Unsafe");
        } else {
            return theUnsafe;
        }
    }

 public static boolean isSystemDomainLoader(ClassLoader var0) {
        return var0 == null;
    }
```

## 主要功能
Unsafe的实现都是标注native方法。

- 内存管理，通过类似C语言指针的操作内存，注意Unsafe类中的所有方法都是native修饰的，也就是说Unsafe类中的方法都直接调用操作系统底层资源执行相应任务；
- 数组操作；
- CAS操作相关，CPU直接支持的指令。（JDK1.8新增，根据内存偏移量对于字段，获取值）；
- 线程挂起和恢复（park和unpark）；
- 内存屏障，JDK1.8
- 其他操作（加锁、加载类）




# AtomicInteger
对int的封装，提供原子性访问和更新操作，原子性的操作基于CAS（compare-and-swap）技术。

## 基本操作
通过Unsafe类获取实例对象的内存偏移量（针对AtomicInteger是类变量的地址），然后修改内存值，提供原子性操作。（类new实例的时候（主动首次使用）才会触发类的初始化操作）

```
static {
        try {
            valueOffset = unsafe.objectFieldOffset
                (AtomicInteger.class.getDeclaredField("value"));
        } catch (Exception ex) { throw new Error(ex); }
}

// JDK 1.8源码，自增操作
public final int getAndAddInt(Object o, long offset, int delta) {
        int v;
        do {
            v = getIntVolatile(o, offset);
        } while (!compareAndSwapInt(o, offset, v, v + delta));
        return v;
}
// JDK 1.7源码，自增操作
public final int incrementAndGet() {
    for (;;) {
        int current = get();
        int next = current + 1;
        if (compareAndSet(current, next))
            return next;
    }
}

```

# AtomicReference

实现原理是一样的，通过CAS操作，原子更新引用。

```java
public class AtomicReference<V> implements java.io.Serializable {
    
    private static final long valueOffset;
    static {
        try {
            valueOffset = unsafe.objectFieldOffset
                (AtomicReference.class.getDeclaredField("value"));
        } catch (Exception ex) { throw new Error(ex); }
    }
    //内部变量value，Unsafe类通过valueOffset内存偏移量即可获取该变量
    private volatile V value;
    
    //CAS方法，间接调用unsafe.compareAndSwapObject(),它是一个
    //实现了CAS操作的native方法
    public final boolean compareAndSet(V expect, V update) {
            return unsafe.compareAndSwapObject(this, valueOffset, expect, update);
    }



}
```

# AtomicIntegerFieldUpdater
可以将原先不是线程安全的属性转变为线程安全的属性操作。



# Reference
- [Java并发编程-无锁CAS与Unsafe类及其并发包Atomic](https://blog.csdn.net/javazejian/article/details/72772470)








