# Java 反射

# 注解
> 基本原则：注解不能影响程序代码的执行，无论增加、删除 Annotation，代码都始终如一的执行。

Annotation（注解）就是Java提供了一种元程序中的元素关联任何信息和着任何元数据（metadata）的途径和方法。Annotation（注解）是JDK5.0以后版本引入。注解有多种用途：<br>
- 生成说明文档；
- 跟踪代码的依赖性；
- 执行基本编译时检查 <br>
...

## 元注解


- @Target <br>
说明对象修饰的范围，包、类、接口、枚举类型等。

- @Retention <br>
定义Annotation被保留时间长短，SOURCE/CLASS/RUNTIME，在什么时期被保留；注解与类处理是分离的。

- @Documented <br>
用于描述其它类型的annotation应该被作为被标注的程序成员的公共API，因此可以被例如javadoc此类的工具文档化。

- @Inherited <br>
是一个标记注解，表示标注这个注解的类的之类也继承这个注解。

## 注解语法特性
- @interface标识注解，自动继承java.lang.annotation.Annotation接口。
- 定义注解，不能继承其他的注解或接口。
- 注解中的每一个方法，声明一个配置参数：
    - 方法名称 -> 参数名称，方法修饰只有两种选择：public/默认(default)；
    - 方法返回类型 -> 参数类型
    - default -> 参数默认值
- 注解元素必须有确定的值，通过默认值/使用时指定，非基本元素不可为null。
> 只声明一个参数，最好用"value"，后加小括号。

**实例：**<br>
```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface MyElement {
    String value() default "";
}
```

# 注解处理器
读取注解的方法和工作。Java在java.lang.reflect包下新增的AnnotatedElement接口，表示可接受注解的元素。接口有如下实现类：
- Class: 类定义；
- Constructor：构造器定义
- Field：类的成员变量定义
- Method：类的方法定义
- Package：类的包定义


# Reference 
- [深入理解Java：注解（Annotation）基本概念](http://www.cnblogs.com/peida/archive/2013/04/23/3036035.html)
- [lombok 注解简化编程](https://projectlombok.org/)

