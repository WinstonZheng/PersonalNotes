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

### BeanFactory
BeanFactory接口定义了getBean方法，通过Bean的名字、类型（prototype和singleton），以及指定构造器参数方式，获取Bean。

- BeanFactory设计原理： Resource -> BeanDefinition（管理依赖关系） -> BeanFactory

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




















