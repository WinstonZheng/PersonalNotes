

# SpringMvc基础知识
---
## 初始化
SpringMVC处理流程：
1. 请求离开浏览器后，包含URL和表单数据。
2. 通过DispatcherServlet这个前端控制器Servlet，将不同的请求转发给SpringMVC控制器。
3. 通过控制器接受和处理数据，返回model（模型）打包和一个逻辑视图名(view)给DispatcherServlet。
4. DispatcherServlet使用视图解析器(view resolver)将逻辑视图名匹配一个特定的视图实现。
5. DispacherServlet交付模型数据，请求任务完成。视图将使用模型数据渲染输出，这个输出会通过响应对象传递给客户端。

### 配置DispatcherServlet
AbstractAnnotationConfigDispatcherServletInitializer

@EnableWebMvc 启用SpringMVC,配置视图解析器和静态资源处理

### 常用注解
- @Controller
- @RequestMapping
- @ResponseBody
- @RequestBody
- @PathVariable
- @RestController

### 基本配置
定制一个配置类WebMvcConfigurerAdapter类（并在此类上使用@EnableWebMvc）。    
配置内容：
> 静态资源映射

> 拦截器配置

> @ControllerAdvice

> 其他配置

## 页面解析渲染

## 页面之间跳转
Spring MVC默认采用转发来定位视图，如果要重定向：
1.  使用RedirectView
2.  redirect:前缀，这种方式可以有效防止重复提交。
## 接受请求输入（页面 -> 控制器）
### 传参方式
1. 获取路径传参数：
```
@PathVarible
```

2. 获取form表单中Get方式传递的参数：
用注解@RequestParam绑定请求参数
```java
@RequestParam(value="a", required=false)
```

3. 获取form表单中Post方式传递的参数：
```java
@ModelAttribute
HttpServletRequest
```

4. HttpServletRequest
```java
@RequestMapping(method = RequestMethod.GET) 
public String get(HttpServletRequest request, HttpServletResponse response) { 
   System.out.println(request.getParameter("a")); 
    return "helloWorld"; 
}
```

### 检验表单
## Controller层向页面传参
1. 使用ModelAndView对象
```java
@RequestMapping("/login.do")  
public ModelAndView  login(String name,String pass){  
    User user = userService.login(name,pwd);  
    Map<String,Object> data = new HashMap<String,Object>();  
    data.put("user",user);  
    return new ModelAndView("success",data);  
} 
```

2. ModelMap
ModelMap数据会利用HttpServletRequest的Attribute传值到页面中：
```java
    @RequestMapping("/login.do")  
    public　String login(String name,String pass ,ModelMap model){  
        User user  = userService.login(name,pwd);  
        model.addAttribute("user",user);  
        model.put("name",name);  
        return "success";  
    }  
```

3. @ModelAttribute
 在Controller方法的参数部分或Bean属性方法上使用@ModelAttribute数据会利用HttpServletRequest的Attribute传值到页面中：
```java
    @RequestMapping("/login.do")  
    public String login(@ModelAttribute("user") User user){  
        //TODO  
       return "success";  
    }  
      
    @ModelAttribute("name")  
    public String getName(){  
        return name;  
    }  
```
4. Session存储：
可以利用HttpServletRequest的getSession()方法
```java
    @RequestMapping("/login.do")  
    public String login(String name,String pwd  
                                ModelMap model,HttpServletRequest request){  
         User user = serService.login(name,pwd);  
         HttpSession session = request.getSession();  
         session.setAttribute("user",user);  
         model.addAttribute("user",user);  
         return "success";  
    }  
```

## SpringMvc 结合 ajax
Spring解析视图时，涉及两个接口：ViewResolver 和 View；
1. ViewResolver：提供 view name 和 实际 view的映射；
2. View：getContentType 和 render ，解析请求中的参数并把这个请求处理成某一种 View；

使用方法：
使用@ResponseBody来标注ajax对应的Controller层方法，方法的return值返回在响应实体中。
返回页面调用ajax中success标注的回调方法。
也可能调用error标注的回调方法，调用情况：Reuqest请求出错（返回的字符串不符合编码方式）

## filter/listener/interceptor
### filter
filter是一个可以复用的代码片段，可以用来转换HTTP请求、响应和头信息。Filter不像Servlet，它不能产生一个请求或者响应，它只是修改对某一资源的请求，或者修改从某一的响应。

### listener
监听器，从字面上可以看出listener主要用来监听只用。通过listener可以监听web服务器中某一个执行动作，并根据其要求作出相应的响应。通俗的语言说就是在application，session，request三个对象创建消亡或者往其中添加修改删除属性时自动执行代码的功能组件。

### interceptor
是在面向切面编程的，就是在你的service或者一个方法，前调用一个方法，或者在方法后调用一个方法，比如动态代理就是拦截器的简单实现，在你调用方法前打印出字符串（或者做其它业务逻辑的操作），也可以在你调用方法后打印出字符串，甚至在你抛出异常的时候做业务逻辑的操作。

http://www.concretepage.com/spring/spring-mvc/spring-handlerinterceptor-annotation-example-webmvcconfigureradapter

## 其他问题
1.  [@PathVariable出现点号"."时导致路径参数截断获取不全的解决办法](http://www.bubuko.com/infodetail-834323.html)
    在参数后面多加一个字段。


# SpringMVC详解
MVC框架解决问题：
1. 将Web页面的请求传给服务器；
2. 根据不同的请求处理不同的逻辑单元；
3. 返回处理结果数据并跳转到响应的页面；

applicationContext.xml Spring配置文件。Spring的核心是配置文件，通过关键配置contextConfigLocation将Web与Spring的配置文件相结合。

## 页面技术
### @ModelAttribute
此注解标识的参数，在@RequestMapping标注的方法前，将其加入到映射表中。使得，在方法中，能够被访问。<br>
![](/images/web/springmvc-modeltorequest.png) <br>
如上图所示，先ModelAttribute先放到model中，然后，放到HttpServletRequest中。     
为什么不将参数直接添加到Request的对象中，而是添加到Model中，满足MVC框架需求：   
It should be as view-agnostic as possible, which means we’d like to be able to incorporate view technologies not bound to the HttpServletRequest as well.

### @SessionAttribute   
Session中存储的属性，将会放置到HttpServletRequest和HttpSession中。

## 异常处理
- Spring支持将自定义Exception映射到对应的状态码；
```java
// 加入Controller抛出此异常，自动映射到404响应；
@ResponseStatus( value = HttpStatus.NOT_FOUND,
                reason = "Student Not Found")
public class StudentNotFoundException extends RuntimeException{
}
```

- 将Controller层中异常处理路径分离出来，简化Controller方法（易理解和测试）
```java
//该方法位于Controller层中
@ExceptionHandler(StudentNotFoundException.class)
public String handleStudentNotFound(){
    return "error/not_found";
}
```

- @ControllerAdvice, 拦截所有controller中的异常。



# SpringMVC源码解析
SpringMVC中Controller是单例的。





