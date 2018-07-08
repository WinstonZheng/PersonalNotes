# 依赖注入DI
## 基础装配Bean
三种主要装配机制：
1. 在XML中进行显式配置；
2. 在Java中进行显式配置；
3. 隐式的bean发现机制和自动装配；

按照Spring创建Bean方式有分为两类：
- Application Context;
    - Java配置加载Spring应用 AnnotationConfigApplicationContext
    - Java配置加载Spring Web应用 AnnotationConfigWebApplicationContext   
    - 类路径下xml配置 ClassPathXmlApplicationContext   
    - 文件系统下xml配置 FileSystemXmlapplicationcontext
    - web应用下xml配置 XmlWebApplicationContext
- Bean工厂;

### 隐式bean发现机制和自动装配
1.组件扫描(conponent scanning);


- 组件类 <br>
表明**组件类**，Spring会自动生成bean。

```
@Component
```

Spring会给组件类生成的Bean配置ID，默认为类名（首字母小写）。
可以自定义。

```
@Component("lonelyHeartsClub")
public class SgtPeppers implements CompactDisc{...}
```

注：@Named可以作为替代方案，有细微差别。

- 组件扫描 <br>

**组件的扫描**默认是不启动的，需要显示配置。
标注某个类，无其他配置，会默认扫描这个包以及这个包下的子包。

```
@ComponentScan
```

参数可以设置组件扫描基础包（类型不安全的）。
通过basePackageClasses设置组建类，将这些类所在包作为基础包。

```
//表明这是一个配置类，描述Spring应用上下文中如何创建Bean的细节。
@Configuration
@ComponentScan("sound")
public class CDPlayerConfig{}
//其他方式
@ComponentScan(basePackages="sound")
@ComponentScan(basePackages={"gaga","hehe"})
@ComponentScan(basePackageClasses={CDPlayer.class,DVDPlayer.class})
```

2.自动装配(autowiring);
通过构造器、Setter方法以及其他方法。Spring都尝试满足参数上声明的依赖。

```
@Component
public class CDPlayer implements MediaPlayer{
    private CompactDisc cd;
    
    @Autowired
    public CDPlayer(CompactDisc cd){
        this.cd = cd;
    }
    //如果 cd为null，则不报错。
    @Autowired(required = false)
    public void setCompactDisc(CompactDisc cd){
        this.cd = cd;
    }
    @Autowired
    public void insertDisc(CompactDisc cd){
        this.cd = cd;
    }
}
```

注：可以用@Inject替代，有细微差别。




