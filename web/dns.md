# DNS解析过程



# 多种域名解析方式
- A
- MX
- CNAME
- NS
- TXT

# DNS工具
- nslookup，Windows/linux下，查看域名解析结果。
- dig，linux系统下，查看DNS解析过程。

- DNS缓存
    - ipconfig /flushdns，windows下清除缓存。
    - service nscd restart，清除缓存

> DNS缓存解析结果的位置：1. Local DNS Server; 2. 用户本地机器；
> Java缓存DNS，在JVM中，DNS缓存通过InetAddress类中完成，缓存时间由两个配置项决定：
> 1. networkaddress.cache.ttl;
> 2. networkaddress.cache.negative.ttl;
> 通过修改配置文件，或者加JAVA启动参数方式控制运行。
> InetAddress类解析域名，需使用单例模式，否则每次创建，进行完整域名解析，非常耗时。



# Reference
- 《深入分析Java Web 技术内幕》
