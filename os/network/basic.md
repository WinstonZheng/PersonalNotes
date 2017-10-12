# 网络分层
目前针对操作系统网络模型分为两类，一种是OSI七层模型；另一种是TCP/IP四层模型。
- 网络七层模型<br>
	- 应用层(Application)	 
	- 表示层(Presentation)	 
	- 会话层(Session)	 
	- 传输层(Transport)	 
	- 网络层(Network)	路由器
	- 数据链路层(Data Link)	交换机
	- 物理层(Physical)	网卡、集线器（Hub
- tcp/ip 四层模型
![](/images/network/tcp_ip_layers.PNG)

# TCP_IP 四层模型
- 应用层
应用层提供应用程序处理业务逻辑，如：HTTP、DNS和FTP等协议，而常见功能有文件传输、名称查询和网络管理等。
应用层程序工作在用户空间。

- 传输层
传输层用于提供端到端的传输（逻辑链路），主要协议包括TCP、UDP和SCTP（与网络层逐跳的方式不同）。负责的主要功能包括数据的收发、链路的超时重传等。
	- TCP(Transmission Control Protocol)协议，提供可靠、面向连接和基于流(stream，无边界限制)的服务，TCP实现全双工通道、可靠连接、数据分片、超时重连、拥塞控制、紧急传输等多种功能。同时，在连接过程中，内核维护连接状态、读写缓冲区、定时器等内核数据（耗费资源）。
	- UDP(User Datagram Protocol)协议，提供不可靠、无连接、基于数据报的服务。UDP不存在重传机制，损失之后发送端并不清楚，由上层协议控制超时重传机制，而过长的UDP数据报会引起IP分片（TCP本身存在划分，尽量避免分片）。相比较基于流的数据，数据报需要接收端一次将数据全部读出，否则数据截断。

- 网络层
实现数据包的选路和转发。网络层协议也是面向无连接、不可靠的协议。
	- 核心协议是IP（Internet Protocol）协议，通过IP协议，能够在广域网中定位一台主机，并通过查询路由表和路由算法的应用转发到目标主机。所以，IP协议的核心在于IP地址和路由，两个方面。
	- ICMP（Internet Control Message Protocol，因特网控制协议报文)，ICMP实现网络检查功能，包括差错报文、重定向报文，用于检测网络连接（通过IP协议定位发送，CRC）。

- 数据链路层
实现网络接口驱动程序，为上层提供统一接口（与底层最接近的一层）。主要协议为ARP和RARP协议。
	- ARP(Address Resolve Protocol)，IP转化为MAC地址。
	- RARP(Reverse Address Resolve Protocol)，无盘操作系统用MAC地址查询IP。

# 封装

# 分用