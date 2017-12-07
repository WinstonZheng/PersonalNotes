# 概述
## 优点
rest风格后端，
- 可以用于网站的前后端分离，前后端进行分工，然后，
- 具备良好的可扩展性；
- 可以为多客户端提供接口访问；

## 特性
- 资源（Resource）
- 资源的表述（Representation）
- 状态转移（State Transfer）
- 统一接口（Uniform Interface）
- 超文本驱动（Hypertext Driven）

# 分层处理
- controller层，负责检验页面传参，以及返回成功或错误提示信息；
- service层，负责正常事件流和异常事件流，将相关信息返回controller层中。


# 安全验证
## 方式一（Session）
通过传统的Session + Cookie的方式，但是不适用于多平台（移动APP不支持）。

## 方式二（类Session）
1. 用户输入用户名和密码；
2. 浏览器，将密码进行对称加密，

需要分以下几步完成：
1. 用户登录认证，给用户返回token（服务端存储用户授权信息）；
2. 拦截请求，检查请求是否符合要求。


rest风格网站需要提供针对api的权限验证功能。
- Http Basic Authentication
- 类cookie-session
- OAuth 2.0

# 异常处理
通过切面统一处理异常，返回页面Response信息。

# 分页
包装一个page类，将特定的分页信息传递到页面。
