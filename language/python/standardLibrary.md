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

- 创建Handler对象 <br>
    handler 控制输出方式，控制日志等级。


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