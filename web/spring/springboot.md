# 基础
## Spring Boot简介
Spring Boot简化了Spring的配置，无XML配置。提供了其他的一系列功能（例如：内嵌的servers，security,metrics,health checks, externalized configuration），SpringBoot是伴随着Spring4.0诞生的。
### Spring Boot优缺点
- 优点：
    - Spring Boot简化编码，包括引入依赖、注入一个Bean；
    - Spring Boot简化配置，
    > xml config -> java config
    > setBean(Bean bean) -> @Autowire
    > *.propterties / *.xml -> application.yml
    - Spring Boot使部署变简单，不需要部署应用服务器。（Embedded HTPP Container）
    - Spring Boot使监控变简单，Spring actuator，以REST方式，获取进程运行期性能参数。
- 缺点：
    - 入门级微框架，对微服务支持有限。

## Spring Boot注解相关

- @SpringBootApplication作用    
1. @Configuration
2. @EnableAutoConfiguration
3. @EnableWebMvc
4. @ComponentScan 当前包下查找。<br>
[更多细节](http://spring.io/guides/gs/spring-boot/)

@EnableAutoConfiguration 将当前包作为"search package"。

```
@EnableAutoConfiguration

    - @AutoConfigurationPackage
    - @Import
```

## SpringBoot配置

```
// application.properties
// Spring Boot static content
spring.mvc.static-path-pattern=/public/**
spring.mvc.view.prefix= /public/html
spring.mvc.view.suffix= .html

//Spring Boot test
@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
```


# 原理
## @Configuration
本质上是一个@Component，@Configuration类通过AnnotationConfigApplicationContext或者其web-capable variant AnnotationConfigWebApplicationContext。





# 实践

### Spring Boot配置文件获取自定义配置
你能通过properties files, YAML files，environment variables and command-line arguments扩展配置。属性值的导入：
1. @Value annotation;
2. Environment abstraction;
3. @ConfigurationProperties绑定到结构化的对象；

- @Value    
通过在@Configuration注解类上配置@PropertySource获取application.properties文件，才能使用@Value，如果不配置，不能使用。这是使用Spring的PropertySourcesPlaceholderConfigurer，用XML配置是<context:property-placeholder>。   

- @ImportResource   
通过此注解，加载Spring的XML配置文件。

Spring Boot uses a very particular PropertySource order that is designed to allow sensible overriding of values.

[Spring boot 参考文件说明](http://docs.spring.io/spring-boot/docs/1.4.4.RELEASE/reference/htmlsingle/#boot-features-sql/)
