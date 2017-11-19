# Java 反射

# 元注解
- @Target <br>
说明对象修饰的范围，包、类、接口、枚举类型等。

- @Retention <br>
定义Annotation被保留时间长短，SOURCE/CLASS/RUNTIME，在什么时期被保留；注解与类处理是分离的。

- @Documented <br>
用于描述其它类型的annotation应该被作为被标注的程序成员的公共API，因此可以被例如javadoc此类的工具文档化。

- @Inherited <br>
是一个标记注解，表示标注这个注解的类的之类也继承这个注解。