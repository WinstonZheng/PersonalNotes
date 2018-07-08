# FileSystemXmlApplicationContext
前面已经提到过IOC容器中BeanFactory和ApplicationContext的区别，两者一个是纯IOC容器，另一个是ApplicationContext是附加许多其他功能。在此，基于FileSystemXmlApplicationContext来分析IOC容器的主要功能，包括IOC容器的初始化、依赖注入两个部分。

## 初始化
IOC容器的初始化分为三步骤：
1. 定位，不同的形式的资源通过不同形式的Resource表示。通过ApplicationContext实现的接口ResourceLoader实现资源的加载；
2. 加载，找到了配置文件的位置，通过BeanDefinitionReader系列模块可以将文件中Bean的相关定义读取出来，通过BeanDefinitionHolder类保存下来；
3. 注册，最后，将BeanDefinitionHolder中的信息注册到BeanFactory真正的IOC容器中，通过一个Map形式的数据结构保存。


![](/images/javaee/applicationcontext.PNG)

从上图可以看出FileSystemXmlApplicationContext的继承体系。ApplicationContext的继承体系主要采用了模板设计模式，refresh()作为启动ApplicationContext的入口点。
- 其中AbstractApplicationContext实现了refresh方法，提供ApplicationContext的实际实现，然后，开始创建BeanFactory，通过obtainFreshBeanFactory方法。<br>
```java
public void refresh() throws BeansException, IllegalStateException {
    synchronized (this.startupShutdownMonitor) {
    // Prepare this context for refreshing.
   prepareRefresh();
   // Tell the subclass to refresh the internal bean factory.
   ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();
   ....
   }
}
protected ConfigurableListableBeanFactory obtainFreshBeanFactory() {
    // 抽象方法，由子类实现
    refreshBeanFactory();
    ConfigurableListableBeanFactory beanFactory = getBeanFactory();
    if (logger.isDebugEnabled()) {
    	logger.debug("Bean factory for " + getDisplayName() + ": " + beanFactory);
    }
     return beanFactory;
}
```

- 在AbstractRefreshableApplicationContext类中实现了refreshBeanFactory方法，新建了一个BeanFactory，并通过线程安全的方式赋值给本类的属性。其中，loadBeanDefinition为抽象方法，由子类实现。从方法名可以看出，此方法的主要作用是从不同的目标加载BeanDefinition，所以派生出了两个子类AbstractXmlApplicationContext和AbstractRefreshableWebApplicationContext。
```java
protected final void refreshBeanFactory() throws BeansException {
    if (hasBeanFactory()) {
    	// 如果存在BeanFactory，则销毁并关闭
    	destroyBeans();
    	closeBeanFactory();
    }
    try {
    	DefaultListableBeanFactory beanFactory = createBeanFactory();
    	beanFactory.setSerializationId(getId());
    	customizeBeanFactory(beanFactory);
    	//由子类实现具体的方法，不同子类在此方法中调用不同的BeanDefinitionReader
    	loadBeanDefinitions(beanFactory);
    	synchronized (this.beanFactoryMonitor) {
    		this.beanFactory = beanFactory;
    	}
    }
    catch (IOException ex) {
    	throw new ApplicationContextException("I/O error parsing bean definition source for " + getDisplayName(), ex);
    }
}
```

- 主要将注意力集中在AbstractXmlApplicationContext中，从类名可知，从xml配置文件中读取BeanDefinition，那么来看loadBeanDefinition方法，可知是通过XmlBeanDefinitionReader类将配置文件中配置读出并加载到BeanFactory中。
```java
// AbstractXmlApplicationContext
protected void loadBeanDefinitions(DefaultListableBeanFactory beanFactory) throws BeansException, IOException {
		// 传入BeanFactory，用于注册BeanDefinition
		XmlBeanDefinitionReader beanDefinitionReader = new XmlBeanDefinitionReader(beanFactory);

		// Configure the bean definition reader with this context's
		// resource loading environment.
		beanDefinitionReader.setEnvironment(this.getEnvironment());
		// 在beanDefinitionReader中，AbstractXmlApplicationContext是起ResourceLoader的作用
		beanDefinitionReader.setResourceLoader(this);
		beanDefinitionReader.setEntityResolver(new ResourceEntityResolver(this));

		// Allow a subclass to provide custom initialization of the reader,
		// then proceed with actually loading the bean definitions.
		initBeanDefinitionReader(beanDefinitionReader);
		loadBeanDefinitions(beanDefinitionReader);
}
```
从下图可以看出BeanDefinitionReader提供了多种格式配置文件的读写（获取文件的输出流）。

![](/images/javaee/beandefinitionreader.PNG)

- 查看



### 定位
