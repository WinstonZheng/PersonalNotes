# Logging
日志模块。


## 初始化
创建日志对象，注意，同样的name，返回同样的实例对象。


```
import logging
logging.debug('Debugging information')
logging.info('Informational message')
logging.warning('Warning:config file %s not found', 'server.conf')
logging.error('Error occurred')
logging.critical('Critical error -- shutting down')
```