## 依赖

## 依赖范围

maven包编译项目代码时需要使用多种classpath。依赖范围用于控制依赖与classpath（编译classpath、测试classpath、运行classpath）关系，分类如下：

* compile，默认，对于编译、测试、运行三种classpath都有效；
* test，测试classpath；
* provided，对于编译和测试classpath有效，在运行时，不需要此依赖（servlet-api）；
* runtime，对于测试和运行classpath有效（JDBC），第三方驱动；
* system，与provided范围一致，但是，通过systemPath制定依赖文件（可移植性差）。
* import\(Maven &gt;= 2.0.9\)，不会对三种classpath产生实际影响。

## 依赖传递

依赖具备传递性，将依赖的包中需要的依赖传递到当前项目中。

## 依赖调解

传递依赖路径上如果存在相同的包，maven有两个处理原则：

* 第一原则，首先解析路径短的依赖；
* 第二原则（Maven &gt;= 2.0.9），按照依赖声明顺序，先声明的先解析。



# 



