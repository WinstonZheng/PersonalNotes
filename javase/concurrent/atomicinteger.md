# AtomicInteger
对int的封装，提供原子性访问和更新操作，原子性的操作基于CAS（compare-and-swap）技术。

## CAS
CAS操作从表面上来看叫做比较并替换，是CPU新增的一条原子指令，能保证这两步操作的原子性。CAS指令的使用，则是通过记录一个原始值，并进行一系列操作，然后调用CAS指令，成功则操作成功；失败，则采用一些补偿操作，例如：重试。

## Unsafe
Java底层使用Unsafe类提供CAS操作，Unsafe类在sun.misc包下，不属于Java标准。Unsafe采用了单例模式，只有主类加载器加载的类才能使用。(只有加载器为Null的类)

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