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
// AbstractApplicationContext
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
// AbstractRefreshableApplicationContext
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

// 从该方法中可以看出，IOC容器是如何进行定位
protected void loadBeanDefinitions(XmlBeanDefinitionReader reader) throws BeansException, IOException {
		Resource[] configResources = getConfigResources();
		if (configResources != null) {
			reader.loadBeanDefinitions(configResources);
		}
		String[] configLocations = getConfigLocations();
		if (configLocations != null) {
			reader.loadBeanDefinitions(configLocations);
		}
}
```
从下图可以看出BeanDefinitionReader提供了多种格式配置文件的读写（获取文件的输出流）。

![](/images/javaee/beandefinitionreader.PNG)

从下图可以看出，Resource资源接口的结构。

![](/images/javaee/resource.PNG)

### 定位
承接上一项，资源是如何定位的，通过AbstractXmlApplicationContext的loadBeanDefinitions方法中获取到资源，包装成Resouce[]或者String[]形式。所以，由此可得派生出的FileSystemXmlApplicationContext和ClassPathXmlApplicationContext由于不同的资源定位方式划分。(以FileSystemXmlApplicationContext为例，getConfigResources就为空)

- 追踪getConfigLocations()，AbstarctRefreshableConfigApplicationContext中实现，顾名思义，此类主要负责获取配置文件路径获取。

```java
//AbstarctRefreshableConfigApplicationContext
protected String[] getConfigLocations() {
		return (this.configLocations != null ? this.configLocations : getDefaultConfigLocations());
	}
	
// AbstractBeanDefinitionReader
public int loadBeanDefinitions(String... locations) throws BeanDefinitionStoreException {
		Assert.notNull(locations, "Location array must not be null");
		int counter = 0;
		for (String location : locations) {
			counter += loadBeanDefinitions(location);
		}
		return counter;
}
public int loadBeanDefinitions(String location, @Nullable Set<Resource> actualResources) throws BeanDefinitionStoreException {
		// 通过ResourceLoader加载资源
		ResourceLoader resourceLoader = getResourceLoader();
		if (resourceLoader == null) {
			throw new BeanDefinitionStoreException(
					"Cannot import bean definitions from location [" + location + "]: no ResourceLoader available");
		}

		// Ant style path patterns.
		if (resourceLoader instanceof ResourcePatternResolver) {
			// Resource pattern matching available.
			try {
				// 采用getResources方法获取资源
				Resource[] resources = ((ResourcePatternResolver) resourceLoader).getResources(location);
				int loadCount = loadBeanDefinitions(resources);
				....
		}
		else {
			// Can only load single resources by absolute URL.
			Resource resource = resourceLoader.getResource(location);
			int loadCount = loadBeanDefinitions(resource);
			....
}

```

- getResources是ResourceLoader接口的方法，而ApplicationContext是扩展了DefaultResourceLoader，所以说在XmlBeanDefinitionReader中，IOC容器主要作为资源加载器使用。

```java
// DefaultResourceLoader
public Resource getResource(String location) {
		Assert.notNull(location, "Location must not be null");

		for (ProtocolResolver protocolResolver : this.protocolResolvers) {
			Resource resource = protocolResolver.resolve(location, this);
			if (resource != null) {
				return resource;
			}
		}

		if (location.startsWith("/")) {
			// 实际调用方法
			return getResourceByPath(location);
		}
		else if (location.startsWith(CLASSPATH_URL_PREFIX)) {
			return new ClassPathResource(location.substring(CLASSPATH_URL_PREFIX.length()), getClassLoader());
		}
		else {
			try {
				// Try to parse the location as a URL...
				URL url = new URL(location);
				return (ResourceUtils.isFileURL(url) ? new FileUrlResource(url) : new UrlResource(url));
			}
			catch (MalformedURLException ex) {
				// No URL -> resolve as resource path.
				return getResourceByPath(location);
			}
		}
	}
// FileSystemXmlApplicationContext，最终在getResource中调用的方法
protected Resource getResourceByPath(String path) {
		if (path.startsWith("/")) {
			path = path.substring(1);
		}
		return new FileSystemResource(path);
	}
```

### 加载
回到AbstractBeanDefinitionReader,目前有了Resource表示的资源，需要开始对其中的BeanDefinition进行加载操作，也就是AbstractBeanDefinitionReader中loadBeanDefinitions(Resource resource)方法，此方法也采用模板设计模式，通过子类XmlBeanDefinitionReader读取

```java
//真正加载BeanDefinition的地方
protected int doLoadBeanDefinitions(InputSource inputSource, Resource resource)
			throws BeanDefinitionStoreException {
		try {
			// 首先将Resource转为Document
			Document doc = doLoadDocument(inputSource, resource);
			return registerBeanDefinitions(doc, resource);
		}
		....
}

public int registerBeanDefinitions(Document doc, Resource resource) throws BeanDefinitionStoreException {
		// 将Document转化为BeanDefinition
		BeanDefinitionDocumentReader documentReader = createBeanDefinitionDocumentReader();
		int countBefore = getRegistry().getBeanDefinitionCount();
		documentReader.registerBeanDefinitions(doc, createReaderContext(resource));
		return getRegistry().getBeanDefinitionCount() - countBefore;
}
```

> 具体的加载规则在BeanDefinitionDocumentReader

### 注册

```java
//DefaultBeanDefinitionDocumentReader
protected void processBeanDefinition(Element ele, BeanDefinitionParserDelegate delegate) {
		BeanDefinitionHolder bdHolder = delegate.parseBeanDefinitionElement(ele);
		if (bdHolder != null) {
			bdHolder = delegate.decorateBeanDefinitionIfRequired(ele, bdHolder);
			try {
				// Register the final decorated instance.
				// 注册得到的BeanDefinition
				BeanDefinitionReaderUtils.registerBeanDefinition(bdHolder, getReaderContext().getRegistry());
			}
			catch (BeanDefinitionStoreException ex) {
				getReaderContext().error("Failed to register bean definition with name '" +
						bdHolder.getBeanName() + "'", ele, ex);
			}
			// Send registration event.
			getReaderContext().fireComponentRegistered(new BeanComponentDefinition(bdHolder));
		}
	}
//BeanDefinitionReaderUtils
public static void registerBeanDefinition(
			BeanDefinitionHolder definitionHolder, BeanDefinitionRegistry registry)
			throws BeanDefinitionStoreException {

		// Register bean definition under primary name.
		String beanName = definitionHolder.getBeanName();
		registry.registerBeanDefinition(beanName, definitionHolder.getBeanDefinition());

		// Register aliases for bean name, if any.
		String[] aliases = definitionHolder.getAliases();
		if (aliases != null) {
			for (String alias : aliases) {
				registry.registerAlias(beanName, alias);
			}
		}
}
//DefaultListableBeanFactory
public void registerBeanDefinition(String beanName, BeanDefinition beanDefinition)
			throws BeanDefinitionStoreException {

		Assert.hasText(beanName, "Bean name must not be empty");
		Assert.notNull(beanDefinition, "BeanDefinition must not be null");

		if (beanDefinition instanceof AbstractBeanDefinition) {
			try {
				((AbstractBeanDefinition) beanDefinition).validate();
			}
			catch (BeanDefinitionValidationException ex) {
				throw new BeanDefinitionStoreException(beanDefinition.getResourceDescription(), beanName,
						"Validation of bean definition failed", ex);
			}
		}

		BeanDefinition oldBeanDefinition;

		oldBeanDefinition = this.beanDefinitionMap.get(beanName);
		if (oldBeanDefinition != null) {
			if (!isAllowBeanDefinitionOverriding()) {
				throw new BeanDefinitionStoreException(beanDefinition.getResourceDescription(), beanName,
						"Cannot register bean definition [" + beanDefinition + "] for bean '" + beanName +
						"': There is already [" + oldBeanDefinition + "] bound.");
			}
			else if (oldBeanDefinition.getRole() < beanDefinition.getRole()) {
				// e.g. was ROLE_APPLICATION, now overriding with ROLE_SUPPORT or ROLE_INFRASTRUCTURE
				if (this.logger.isWarnEnabled()) {
					this.logger.warn("Overriding user-defined bean definition for bean '" + beanName +
							"' with a framework-generated bean definition: replacing [" +
							oldBeanDefinition + "] with [" + beanDefinition + "]");
				}
			}
			else if (!beanDefinition.equals(oldBeanDefinition)) {
				if (this.logger.isInfoEnabled()) {
					this.logger.info("Overriding bean definition for bean '" + beanName +
							"' with a different definition: replacing [" + oldBeanDefinition +
							"] with [" + beanDefinition + "]");
				}
			}
			else {
				if (this.logger.isDebugEnabled()) {
					this.logger.debug("Overriding bean definition for bean '" + beanName +
							"' with an equivalent definition: replacing [" + oldBeanDefinition +
							"] with [" + beanDefinition + "]");
				}
			}
			// 将BeanDefinition放置到Map中
			this.beanDefinitionMap.put(beanName, beanDefinition);
		}
		else {
			if (hasBeanCreationStarted()) {
				// Cannot modify startup-time collection elements anymore (for stable iteration)
				synchronized (this.beanDefinitionMap) {
					this.beanDefinitionMap.put(beanName, beanDefinition);
					List<String> updatedDefinitions = new ArrayList<>(this.beanDefinitionNames.size() + 1);
					updatedDefinitions.addAll(this.beanDefinitionNames);
					updatedDefinitions.add(beanName);
					this.beanDefinitionNames = updatedDefinitions;
					if (this.manualSingletonNames.contains(beanName)) {
						Set<String> updatedSingletons = new LinkedHashSet<>(this.manualSingletonNames);
						updatedSingletons.remove(beanName);
						this.manualSingletonNames = updatedSingletons;
					}
				}
			}
			else {
				// Still in startup registration phase
				this.beanDefinitionMap.put(beanName, beanDefinition);
				this.beanDefinitionNames.add(beanName);
				this.manualSingletonNames.remove(beanName);
			}
			this.frozenBeanDefinitionNames = null;
		}

		if (oldBeanDefinition != null || containsSingleton(beanName)) {
			resetBeanDefinition(beanName);
		}
	}


```




