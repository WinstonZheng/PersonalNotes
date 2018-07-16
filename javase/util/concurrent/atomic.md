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

```java
//下面是sun.misc.Unsafe.java类源码
package sun.misc;
import java.lang.reflect.Field;
/***
 * This class should provide access to low-level operations and its
 * use should be limited to trusted code.  Fields can be accessed using
 * memory addresses, with undefined behaviour occurring if invalid memory
 * addresses are given.
 * 这个类提供了一个更底层的操作并且应该在受信任的代码中使用。可以通过内存地址
 * 存取fields,如果给出的内存地址是无效的那么会有一个不确定的运行表现。
 * 
 * @author Tom Tromey (tromey@redhat.com)
 * @author Andrew John Hughes (gnu_andrew@member.fsf.org)
 */
public class Unsafe
{
  // Singleton class.
  private static Unsafe unsafe = new Unsafe();
  /***
   * Private default constructor to prevent creation of an arbitrary
   * number of instances.
   * 使用私有默认构造器防止创建多个实例
   */
  private Unsafe()
  {
  }
  /***
   * Retrieve the singleton instance of <code>Unsafe</code>.  The calling
   * method should guard this instance from untrusted code, as it provides
   * access to low-level operations such as direct memory access.
   * 获取<code>Unsafe</code>的单例,这个方法调用应该防止在不可信的代码中实例，
   * 因为unsafe类提供了一个低级别的操作，例如直接内存存取。
   * 
   * @throws SecurityException if a security manager exists and prevents
   *                           access to the system properties.
   *                           如果安全管理器不存在或者禁止访问系统属性
   */
  public static Unsafe getUnsafe()
  {
    SecurityManager sm = System.getSecurityManager();
    if (sm != null)
      sm.checkPropertiesAccess();
    return unsafe;
  }
  
  /***
   * Returns the memory address offset of the given static field.
   * The offset is merely used as a means to access a particular field
   * in the other methods of this class.  The value is unique to the given
   * field and the same value should be returned on each subsequent call.
   * 返回指定静态field的内存地址偏移量,在这个类的其他方法中这个值只是被用作一个访问
   * 特定field的一个方式。这个值对于 给定的field是唯一的，并且后续对该方法的调用都应该
   * 返回相同的值。
   *
   * @param field the field whose offset should be returned.
   *              需要返回偏移量的field
   * @return the offset of the given field.
   *         指定field的偏移量
   */
  public native long objectFieldOffset(Field field);
  /***
   * Compares the value of the integer field at the specified offset
   * in the supplied object with the given expected value, and updates
   * it if they match.  The operation of this method should be atomic,
   * thus providing an uninterruptible way of updating an integer field.
   * 在obj的offset位置比较integer field和期望的值，如果相同则更新。这个方法
   * 的操作应该是原子的，因此提供了一种不可中断的方式更新integer field。
   * 
   * @param obj the object containing the field to modify.
   *            包含要修改field的对象
   * @param offset the offset of the integer field within <code>obj</code>.
   *               <code>obj</code>中整型field的偏移量
   * @param expect the expected value of the field.
   *               希望field中存在的值
   * @param update the new value of the field if it equals <code>expect</code>.
   *           如果期望值expect与field的当前值相同，设置filed的值为这个新值
   * @return true if the field was changed.
   *                             如果field的值被更改
   */
  public native boolean compareAndSwapInt(Object obj, long offset,
                                          int expect, int update);
  /***
   * Compares the value of the long field at the specified offset
   * in the supplied object with the given expected value, and updates
   * it if they match.  The operation of this method should be atomic,
   * thus providing an uninterruptible way of updating a long field.
   * 在obj的offset位置比较long field和期望的值，如果相同则更新。这个方法
   * 的操作应该是原子的，因此提供了一种不可中断的方式更新long field。
   * 
   * @param obj the object containing the field to modify.
   *              包含要修改field的对象 
   * @param offset the offset of the long field within <code>obj</code>.
   *               <code>obj</code>中long型field的偏移量
   * @param expect the expected value of the field.
   *               希望field中存在的值
   * @param update the new value of the field if it equals <code>expect</code>.
   *               如果期望值expect与field的当前值相同，设置filed的值为这个新值
   * @return true if the field was changed.
   *              如果field的值被更改
   */
  public native boolean compareAndSwapLong(Object obj, long offset,
                                           long expect, long update);
  /***
   * Compares the value of the object field at the specified offset
   * in the supplied object with the given expected value, and updates
   * it if they match.  The operation of this method should be atomic,
   * thus providing an uninterruptible way of updating an object field.
   * 在obj的offset位置比较object field和期望的值，如果相同则更新。这个方法
   * 的操作应该是原子的，因此提供了一种不可中断的方式更新object field。
   * 
   * @param obj the object containing the field to modify.
   *    包含要修改field的对象 
   * @param offset the offset of the object field within <code>obj</code>.
   *         <code>obj</code>中object型field的偏移量
   * @param expect the expected value of the field.
   *               希望field中存在的值
   * @param update the new value of the field if it equals <code>expect</code>.
   *               如果期望值expect与field的当前值相同，设置filed的值为这个新值
   * @return true if the field was changed.
   *              如果field的值被更改
   */
  public native boolean compareAndSwapObject(Object obj, long offset,
                                             Object expect, Object update);
  /***
   * Sets the value of the integer field at the specified offset in the
   * supplied object to the given value.  This is an ordered or lazy
   * version of <code>putIntVolatile(Object,long,int)</code>, which
   * doesn't guarantee the immediate visibility of the change to other
   * threads.  It is only really useful where the integer field is
   * <code>volatile</code>, and is thus expected to change unexpectedly.
   * 设置obj对象中offset偏移地址对应的整型field的值为指定值。这是一个有序或者
   * 有延迟的<code>putIntVolatile</cdoe>方法，并且不保证值的改变被其他线程立
   * 即看到。只有在field被<code>volatile</code>修饰并且期望被意外修改的时候
   * 使用才有用。
   * 
   * @param obj the object containing the field to modify.
   *    包含需要修改field的对象
   * @param offset the offset of the integer field within <code>obj</code>.
   *       <code>obj</code>中整型field的偏移量
   * @param value the new value of the field.
   *      field将被设置的新值
   * @see #putIntVolatile(Object,long,int)
   */
  public native void putOrderedInt(Object obj, long offset, int value);
  /***
   * Sets the value of the long field at the specified offset in the
   * supplied object to the given value.  This is an ordered or lazy
   * version of <code>putLongVolatile(Object,long,long)</code>, which
   * doesn't guarantee the immediate visibility of the change to other
   * threads.  It is only really useful where the long field is
   * <code>volatile</code>, and is thus expected to change unexpectedly.
   * 设置obj对象中offset偏移地址对应的long型field的值为指定值。这是一个有序或者
   * 有延迟的<code>putLongVolatile</cdoe>方法，并且不保证值的改变被其他线程立
   * 即看到。只有在field被<code>volatile</code>修饰并且期望被意外修改的时候
   * 使用才有用。
   * 
   * @param obj the object containing the field to modify.
   *    包含需要修改field的对象
   * @param offset the offset of the long field within <code>obj</code>.
   *       <code>obj</code>中long型field的偏移量
   * @param value the new value of the field.
   *      field将被设置的新值
   * @see #putLongVolatile(Object,long,long)
   */
  public native void putOrderedLong(Object obj, long offset, long value);
  /***
   * Sets the value of the object field at the specified offset in the
   * supplied object to the given value.  This is an ordered or lazy
   * version of <code>putObjectVolatile(Object,long,Object)</code>, which
   * doesn't guarantee the immediate visibility of the change to other
   * threads.  It is only really useful where the object field is
   * <code>volatile</code>, and is thus expected to change unexpectedly.
   * 设置obj对象中offset偏移地址对应的object型field的值为指定值。这是一个有序或者
   * 有延迟的<code>putObjectVolatile</cdoe>方法，并且不保证值的改变被其他线程立
   * 即看到。只有在field被<code>volatile</code>修饰并且期望被意外修改的时候
   * 使用才有用。
   *
   * @param obj the object containing the field to modify.
   *    包含需要修改field的对象
   * @param offset the offset of the object field within <code>obj</code>.
   *       <code>obj</code>中long型field的偏移量
   * @param value the new value of the field.
   *      field将被设置的新值
   */
  public native void putOrderedObject(Object obj, long offset, Object value);
  /***
   * Sets the value of the integer field at the specified offset in the
   * supplied object to the given value, with volatile store semantics.
   * 设置obj对象中offset偏移地址对应的整型field的值为指定值。支持volatile store语义
   * 
   * @param obj the object containing the field to modify.
   *    包含需要修改field的对象
   * @param offset the offset of the integer field within <code>obj</code>.
   *       <code>obj</code>中整型field的偏移量
   * @param value the new value of the field.
   *       field将被设置的新值
   */
  public native void putIntVolatile(Object obj, long offset, int value);
  /***
   * Retrieves the value of the integer field at the specified offset in the
   * supplied object with volatile load semantics.
   * 获取obj对象中offset偏移地址对应的整型field的值,支持volatile load语义。
   * 
   * @param obj the object containing the field to read.
   *    包含需要去读取的field的对象
   * @param offset the offset of the integer field within <code>obj</code>.
   *       <code>obj</code>中整型field的偏移量
   */
  public native int getIntVolatile(Object obj, long offset);
  /***
   * Sets the value of the long field at the specified offset in the
   * supplied object to the given value, with volatile store semantics.
   * 设置obj对象中offset偏移地址对应的long型field的值为指定值。支持volatile store语义
   *
   * @param obj the object containing the field to modify.
   *            包含需要修改field的对象
   * @param offset the offset of the long field within <code>obj</code>.
   *               <code>obj</code>中long型field的偏移量
   * @param value the new value of the field.
   *              field将被设置的新值
   * @see #putLong(Object,long,long)
   */
  public native void putLongVolatile(Object obj, long offset, long value);
  /***
   * Sets the value of the long field at the specified offset in the
   * supplied object to the given value.
   * 设置obj对象中offset偏移地址对应的long型field的值为指定值。
   * 
   * @param obj the object containing the field to modify.
   *     包含需要修改field的对象
   * @param offset the offset of the long field within <code>obj</code>.
   *     <code>obj</code>中long型field的偏移量
   * @param value the new value of the field.
   *     field将被设置的新值
   * @see #putLongVolatile(Object,long,long)
   */
  public native void putLong(Object obj, long offset, long value);
  /***
   * Retrieves the value of the long field at the specified offset in the
   * supplied object with volatile load semantics.
   * 获取obj对象中offset偏移地址对应的long型field的值,支持volatile load语义。
   * 
   * @param obj the object containing the field to read.
   *    包含需要去读取的field的对象
   * @param offset the offset of the long field within <code>obj</code>.
   *       <code>obj</code>中long型field的偏移量
   * @see #getLong(Object,long)
   */
  public native long getLongVolatile(Object obj, long offset);
  /***
   * Retrieves the value of the long field at the specified offset in the
   * supplied object.
   * 获取obj对象中offset偏移地址对应的long型field的值
   * 
   * @param obj the object containing the field to read.
   *    包含需要去读取的field的对象
   * @param offset the offset of the long field within <code>obj</code>.
   *       <code>obj</code>中long型field的偏移量
   * @see #getLongVolatile(Object,long)
   */
  public native long getLong(Object obj, long offset);
  /***
   * Sets the value of the object field at the specified offset in the
   * supplied object to the given value, with volatile store semantics.
   * 设置obj对象中offset偏移地址对应的object型field的值为指定值。支持volatile store语义
   * 
   * @param obj the object containing the field to modify.
   *    包含需要修改field的对象
   * @param offset the offset of the object field within <code>obj</code>.
   *     <code>obj</code>中object型field的偏移量
   * @param value the new value of the field.
   *       field将被设置的新值
   * @see #putObject(Object,long,Object)
   */
  public native void putObjectVolatile(Object obj, long offset, Object value);
  /***
   * Sets the value of the object field at the specified offset in the
   * supplied object to the given value.
   * 设置obj对象中offset偏移地址对应的object型field的值为指定值。
   * 
   * @param obj the object containing the field to modify.
   *    包含需要修改field的对象
   * @param offset the offset of the object field within <code>obj</code>.
   *     <code>obj</code>中object型field的偏移量
   * @param value the new value of the field.
   *       field将被设置的新值
   * @see #putObjectVolatile(Object,long,Object)
   */
  public native void putObject(Object obj, long offset, Object value);
  /***
   * Retrieves the value of the object field at the specified offset in the
   * supplied object with volatile load semantics.
   * 获取obj对象中offset偏移地址对应的object型field的值,支持volatile load语义。
   * 
   * @param obj the object containing the field to read.
   *    包含需要去读取的field的对象
   * @param offset the offset of the object field within <code>obj</code>.
   *       <code>obj</code>中object型field的偏移量
   */
  public native Object getObjectVolatile(Object obj, long offset);
  /***
   * Returns the offset of the first element for a given array class.
   * To access elements of the array class, this value may be used along with
   * with that returned by 
   * <a href="#arrayIndexScale"><code>arrayIndexScale</code></a>,
   * if non-zero.
   * 获取给定数组中第一个元素的偏移地址。
   * 为了存取数组中的元素，这个偏移地址与<a href="#arrayIndexScale"><code>arrayIndexScale
   * </code></a>方法的非0返回值一起被使用。
   * @param arrayClass the class for which the first element's address should
   *                   be obtained.
   *                   第一个元素地址被获取的class
   * @return the offset of the first element of the array class.
   *    数组第一个元素 的偏移地址
   * @see arrayIndexScale(Class)
   */
  public native int arrayBaseOffset(Class arrayClass);
  /***
   * Returns the scale factor used for addressing elements of the supplied
   * array class.  Where a suitable scale factor can not be returned (e.g.
   * for primitive types), zero should be returned.  The returned value
   * can be used with 
   * <a href="#arrayBaseOffset"><code>arrayBaseOffset</code></a>
   * to access elements of the class.
   * 获取用户给定数组寻址的换算因子.一个合适的换算因子不能返回的时候(例如：基本类型),
   * 返回0.这个返回值能够与<a href="#arrayBaseOffset"><code>arrayBaseOffset</code>
   * </a>一起使用去存取这个数组class中的元素
   * 
   * @param arrayClass the class whose scale factor should be returned.
   * @return the scale factor, or zero if not supported for this array class.
   */
  public native int arrayIndexScale(Class arrayClass);
  
  /***
   * Releases the block on a thread created by 
   * <a href="#park"><code>park</code></a>.  This method can also be used
   * to terminate a blockage caused by a prior call to <code>park</code>.
   * This operation is unsafe, as the thread must be guaranteed to be
   * live.  This is true of Java, but not native code.
   * 释放被<a href="#park"><code>park</code></a>创建的在一个线程上的阻塞.这个
   * 方法也可以被使用来终止一个先前调用<code>park</code>导致的阻塞.
   * 这个操作操作时不安全的,因此线程必须保证是活的.这是java代码不是native代码。
   * @param thread the thread to unblock.
   *           要解除阻塞的线程
   */
  public native void unpark(Thread thread);
  /***
   * Blocks the thread until a matching 
   * <a href="#unpark"><code>unpark</code></a> occurs, the thread is
   * interrupted or the optional timeout expires.  If an <code>unpark</code>
   * call has already occurred, this also counts.  A timeout value of zero
   * is defined as no timeout.  When <code>isAbsolute</code> is
   * <code>true</code>, the timeout is in milliseconds relative to the
   * epoch.  Otherwise, the value is the number of nanoseconds which must
   * occur before timeout.  This call may also return spuriously (i.e.
   * for no apparent reason).
   * 阻塞一个线程直到<a href="#unpark"><code>unpark</code></a>出现、线程
   * 被中断或者timeout时间到期。如果一个<code>unpark</code>调用已经出现了，
   * 这里只计数。timeout为0表示永不过期.当<code>isAbsolute</code>为true时，
   * timeout是相对于新纪元之后的毫秒。否则这个值就是超时前的纳秒数。这个方法执行时
   * 也可能不合理地返回(没有具体原因)
   * 
   * @param isAbsolute true if the timeout is specified in milliseconds from
   *                   the epoch.
   *                   如果为true timeout的值是一个相对于新纪元之后的毫秒数
   * @param time either the number of nanoseconds to wait, or a time in
   *             milliseconds from the epoch to wait for.
   *             可以是一个要等待的纳秒数，或者是一个相对于新纪元之后的毫秒数直到
   *             到达这个时间点
   */
  public native void park(boolean isAbsolute, long time);
}
```


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
- [Java中Unsafe类详解](http://blog.csdn.net/zgmzyr/article/details/8902683)







