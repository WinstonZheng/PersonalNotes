# 一次HTTP请求过程
1. 用户输入URL到浏览器中；
2. DNS服务器将域名解析成IP；
    - 首先查看浏览器自身的缓存；
    - 查找操作系统的DNS缓存；
    - 查找配置的DNS服务器（UDP的53端口），迭代DNS解析请求（[详见DNS解析](/web/basic/dns.md)或[恩恩先生的博客](https://www.cnblogs.com/engeng/articles/5959335.html))；
3. 浏览器访问服务器IP，发送HTTP请求；
> TCP/IP通信协议栈往下是**逐步封装**，往上是**分用**；
> 请求通过arp协议获取mac地址（网关），通过ip协议路由到目标服务器IP；

4. 由传输层建立TCP连接，三次握手；
> SYN + SYN && ACK + ACK
> 首先，进行握手，原因是确保双方可以用TCP通信，
> 此外，进行三次握手，是因为TCP是全双工的管道，两边通信都需要通过序列号保持包顺序，SYN就是为了传递初始的序列号，同时，第二次发送SYN携带ACK确认，所以，节省一次确认的发送。

5. 建立连接后，将应用层协议包HTTP协议（HTTP请求，GET/POST）包装切分后（报文段），通过TCP协议传输；
> 途中可能存在负载均衡器转发，服务器中的文件可能存在分布式缓存系统、文件、数据库中。

6. 服务器将HTTP请求的资源（HTML文件）返回，最后返回HTTP响应，成功返回200状态码（其他情况返回其他的状态码）；
> 服务器提供给用户资源有不同方式，一般有两种：
> 1. tomcat + jsp ，服务器渲染方式。tomcat是servlet容器，提供网页的动态资源，将数据库中数据取出填入到jsp页面中，最后生成html文件返回前端；
> 2. ajax + nginx + tomcat + rest , 前后端分离的方式，nginx可以通过url映射将静态资源的申请和动态资源的申请进行分离，静态资源可以放置在CDN中；动态资源通过ajax异步访问，nginx会将请求映射到tomcat容器（通过rest api的方式访问，利用json格式简化数据传输）。

8. 浏览器渲染HTML文件，将页面展示给用户。
> 浏览器解析html页面，
> 遇到js/css/image等静态资源时，向服务器端去请求下载（多线程下载，每个浏览器的线程数不一样），根据keep-alive特性了，建立一次HTTP连接，可以请求多个资源
> [前端必读](https://kb.cnblogs.com/page/129756/)
9. 一次HTTP请求响应之后，断开TCP连接，四次挥手。
> 

# HTTP 结构

- HTTP Header

- HTTP Body



# Reference 
- [一次完整的HTTP请求过程](https://www.cnblogs.com/engeng/articles/5959335.html)
- 《深入分析 Java Web技术内幕》