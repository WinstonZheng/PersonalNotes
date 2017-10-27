# 简介
内容分布网络(Content Delivery Network)。
CDN = 镜像(Mirror) + 缓存(Cache) + 整体负载均衡(GSLB)。
## 目标
- 可扩展性（Scalability)，性能可扩展。
- 安全性(Security)。
- 可靠性、响应和执行(Reliability、Responsiveness和Performance)。
## 请求过程
![](/images/web/dns.PNG)
以下是简化过程：
    1. 用户通过HTTP请求访问静态资源；
    2. 浏览器根据URL发送DNS域名解析请求，到LDNS；
    3. LDNS经过迭代式解析通过CNAME解析到另一个域名（域名指向CDN全局中DNS负载均衡服务器）；
    4. 由负载均衡服务器（GTM）分配CDN节点，将节点IP返回用户。 

# 负载均衡
通过负载均衡，解决单点失效问题，提高可扩展性（解决网络拥塞），提高资源响应效率。
- 链路负载均衡，DNS解析，
- 集群负载均衡
    - 硬件负载均衡：F5，效率高，费用高。
    - 软件负载均衡：成本低，效率低，结构复杂。
- 操作系统负载均衡

# CDN动态加速
CDN动态加速技术，CDN的DNS解析中通过动态链路探测寻找回源最好途径，然后通过DNS调度将所有请求调度到选定的这条路径上回源。

# Reference
- 《深入分析Java Web 技术内幕》
