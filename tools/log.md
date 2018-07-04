# SLF4J
SLF4J是一个独立于其他日志系统的抽象层，提供统一的日子编程接口，可以与多个日志实现结合。
## SLF4J与Log4J,logback和java.util.Logging
- 提供占位符"{}"的语法，place holder；<br>
    降低代码连接次数，根据生产级别，日志。
- 延迟字符串建立，不建立不需要的日志级别的字符串，减少堆内存消耗。

# log4j
## 配置
1. Loggers，设置信息输出级别；
2. Appender，设置日志输出的地方（文件、控制台等）：
    1. Layouts，定制格式化输出日志；

## log4j与log4j2

- log4j2
    - 性能更好；
    - API分离，log4j-api日志接口层与log4j-core日志接口实现层分离；
    - log4j2支持json文件配置，不支持properties文件 <br>
    ...

# logback
logback分为三个模块：logback-core，logback-classic，logback-access。



# Reference 
[Log4j1 升级 Log4j2 实战](http://www.importnew.com/25729.html)
[Log4J日志配置详解](https://www.cnblogs.com/ITtangtang/p/3926665.html)