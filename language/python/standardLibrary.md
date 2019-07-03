# Logging
日志模块。


## 初始化
- 创建日志对象。
```py
# 同样的name，返回同样的实例对象
# 通过name维护父子关系，例如："parent.son"，则获取的son模块就是parent的子模块
# 建议使用__name__变量，因为这是模块的包命名空间
logging.getLogger(name)
```

- 创建Handler对象
    handler 控制输出方式，控制日志等级。handler对象包括StreamHandler、FileHandler和NullHandler等等，提供输出到文件、流等多种输出方式。
    
- Formatter对象
    通过将LogRecord对象转换成一个格式化字符串字符串。
    %(levelno)s: 打印日志级别的数值
    %(levelname)s: 打印日志级别名称
    %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
    %(filename)s: 打印当前执行程序名
    %(funcName)s: 打印日志的当前函数
    %(lineno)d: 打印日志的当前行号
    %(asctime)s: 打印日志的时间
    %(thread)d: 打印线程ID
    %(threadName)s: 打印线程名称
    %(process)d: 打印进程ID
    %(message)s: 打印日志信息

- Filter Objects
    用于过滤特定的信息（TODO:细化）。
    
- LogRecord Objects
    自动被Logger对象创建，包含每一次需要打印输出的信息。

## 日志等级
日志等级表：

|level|Numeric value|
| - | - |
|CRITICAL|50|
|ERROR|40|
|WARNING|30|
|INFO|20|
|DEBUG|10|
|NOTSET|0|

```
import logging
logging.debug('Debugging information')
logging.info('Informational message')
logging.warning('Warning:config file %s not found', 'server.conf')
logging.error('Error occurred')
logging.critical('Critical error -- shutting down')
```