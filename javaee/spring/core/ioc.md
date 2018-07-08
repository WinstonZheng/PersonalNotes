# Spring IOC
# 基本概念
控制反转，将对类的创建、依赖关系（类在运行过程中，如何获得所需依赖对象的引用）的管理，交由框架管理。

Spring中依赖注入的三种方法：
1. 接口注入(Type1 IoC);
2. setter注入(Type2 IoC);
3. 构造器注入(Type3 IoC);

类之间依赖关系维护，并不是固化在类中，而是通过配置文件（注解）的方式进行维护。当修改类的依赖关系时，无须修改和编译Java源码，直接修改文件。

# 设计与实现
## IoC容器实现假想
IoC容器用于管理Bean的创建，依赖的注入（Bean之间关系）。首先，需要一个Map<String, Object>形式的存储Bean，然后，能够扫描包，顺序发现注册的Bean，由于Bean的注册有先后的关系，所以，可以通过维护一个链表的方式去管理，通过反射机制创建实例，并加入到Map中，最后，在需要注入的例子中，将Object传入。

从上面看来，Bean应该是无状态的，加入维护某种状态，其改变时未知的。总结一下，IOC容器，需要维护如下内容：
- 对象实例
- 对象之间的依赖关系


## IOC容器
主要用于管理对象依赖关系，对象依赖注入。这些对象也有一定的特点：
1. 与系统运行状态没有很强关联；
2. 业务逻辑（处理数据），不常变化，常以单件起作用；
3. 不涉及数据和状态共享问题。

### 设计
BeanFactory是所有IOC容器的基础，具备基础的获取Bean、Bean类型和别名等信息的功能。其他的IOC容器类，是基于BeanFactory基础上扩展不同的方法。主要有两条设计路径：
1. BeanFactory -> HierarchicalBeanFactory -> ConfigurableBeanFactory
2. BeanFactory -> ListableBeanFactory -> ApplicationContext -> WebApplicationContext/ConfigurableApplicationContext.

- BeanFactory

BeanFactory接口定义了getBean方法，通过Bean的名字、类型（prototype和singleton），以及指定构造器参数方式，获取Bean。BeanFactory设计原理： Resource -> BeanDefinition（管理依赖关系） -> BeanFactory

```java
// 1 创建IOC配置文件，包含BeanDefinition需要的Bean依赖关系定义
// 2 创建BeanFactory IOC容器；
// 3 载入一个BeanDefinition读取器，这里使用XmlBeanDefinitionReader，读取XML配置文件(通过回调配置给BeanFactory)；
// 4 读取资源文件，载入和注册Bean。
ClassPathResource res = new ClassPathResource('beans.xml')
DefaultListableBeanFactory factory = new DefaultListableBeanFactory();
XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(factory);
reader.loadBeanDefinitions(res);
```

> BeanFactory and ApplicationContext的区别？
BeanFactory是单纯的IOC容器，负责管理Bean的依赖（依赖关系、依赖注入），而ApplicationContext是在BeanFactory的基础上扩展了许多额外的功能，例如：Bean依赖关系的资源定位、加载(DefaultResourceLoader)等。

- ApplicationContext

ApplicationContext在BeanFactory基础上添加许多附加功能：
1. 支持不同的信息源（MessageSource接口，支持国际化）；
2. 访问资源（ResourceLoader and Resource支持）；
3. 支持应用事件，继承接口ApplicationEventPublisher；
...

这些附加事件，使得Application更加面向框架，一般在开发应用时使用ApplicationContext作为Ioc容器基本形式。

### 初始化
IOC容器的初始化主要分为三个阶段：
1. 定位，指如何找到定义了BeanDefiniton内容的资源，主要通过Resource类定位，例如：文件系统资源采用FileSystemResource;类路径资源采用ClassPathResource等。
2. 加载，前一步已经能定位到资源，加载指的就是将Bean的依赖关系，通过磁盘、web等多种来源读入到内存中，并创建BeanDefinition类。此种方式可以通过AbstarctBeanDefinitionReade系类实现。
3. 注册，将BeanDefinition关系注册到BeanFactory IOC容器中，通过调用BeanDefinitionRegistry接口实现（BeanDefinition在IOC容器中主要通过HashMap形式管理）

- 总结一下<br>
首先，在ApplicationContext接口的具体实现类中调用refresh()方法启动初始化。refresh()启动过程，会初始化创建一个BeanFactory。然后将创建的BeanFactory和IOC容器本身作为资源加载器（ResourceLoader）传入到BeanDefinitionReader实现类中。BeanDefinitionReader通过资源加载器定位到资源创建Resource，然后将Resource资源解析读入，形成Document（以XML为例），然后利用DocumentBeanDefinitionReader类按照Spring的xml配置规则，创建BeanDefinitionHolder，最后，获取BeanFactory，并将BeanDefinition放置到其中（以Map的形式）。
















