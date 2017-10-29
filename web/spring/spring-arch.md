# Spring架构
- Spring 3 架构图

![](/images/web/spring3-ar.PNG)

- Spring 4 架构图

![](/images/web/spring4-ar.PNG)

从Spring3和Spring4的架构图中，可以看出，Spring3到4最大的变化是添加两个新功能模块：
1. spring-websocket：为web应用提供的高效通信工具，web通信长连接；
2. spring-messaging：用于构建基于消息的应用程序；

以下分析Spring的模块的对应不同依赖包：

## Core Container
1. spring-core：依赖注入IoC与DI的最基本实现
2. spring-beans：Bean工厂与bean的装配
3. spring-context：spring的context上下文即IoC容器
4. spring-expression：spring表达式语言
> Spring Core依赖于common-logging，或者提供自定义日志实现，或者加common-logging依赖包，否则，编译出错。

```
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>3.2.17.RELEASE</version>
    <exclusions>
        <exclusion>
            <groupId>commons-logging</groupId>
            <artifactId>commons-logging</artifactId>
        </exclusion>
    </exclusions>
</dependency>
``` 
## aop
    1. spring-aop：面向切面编程
    2. spring-aspects：集成AspectJ
    3. spring-instrument：提供一些类级的工具支持和ClassLoader级的实现，用于服务器
    4. spring-instrument-tomcat：针对tomcat的instrument实现

## data access
    1. spring-jdbc：jdbc的支持
    2. spring-tx：事务控制
    3. spring-orm：对象关系映射，集成orm框架
    4. spring-oxm：对象xml映射
    5. spring-jms：java消息服务

## web 
    1. spring-web：基础web功能，如文件上传
    2. spring-webmvc：mvc实现
    3. spring-webmvc-portlet：基于portlet的mvc实现
    4. spring-struts：与struts的集成，不推荐，spring4不再提供

## test

    1. spring-test：spring测试，提供junit与mock测试功能
    2. spring-context-support：spring额外支持包，比如邮件服务、视图解析等

> Spring配置复杂的一方面在于，配置的依赖包种类繁多，从底层到上层支持，所以，列出不同模块依赖包的作用，有助于理解引用不同依赖的作用。

# Spring Boot Starter关系
> 参考 spring-boot 1.4.3.RELEASE
 
![](/images/web/spring-boot-starter.png)

图中主要展示了spring-boot-starter和spring-boot-starter-web的依赖关系图，图中展示的主要是必须的依赖包（还包含一些可选的依赖包）。


