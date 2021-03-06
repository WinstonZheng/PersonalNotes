# 进线程管理
## 区别
- 进程，进程是程序执行的过程，是系统资源调度和分配的独立单位，进程拥有独立的堆栈以及内存寻址空间。
- 线程，线程是进程的执行中更小的资源划分单位，通常是CPU调度和分派的基本单位，一个进程包含多个线程，同个进程的线程共享内存寻址空间，共享堆，但是拥有独立的栈。

## 线程
### 线程同步
- 互斥量(mutex)，采用互斥对象机制，只有拥有互斥对象的线程才有访问公共资源的权限。因为互斥对象只有一个，所以可以保证公共资源不会被多个线程同时访问。（只允许一个资源访问的信号量的状态）
- 信号量(sem)，允许同一个时刻多个线程访问统一资源，通过计数器控制同一时刻访问资源的最大线程数。
- 事件（信号），通过通知操作方式保持多线程同步，实现多线程优先级比较。


## 进程
### 进程状态


### 进程间通信
- 管道
    - 无名管道，半双工通信方式，数据只能单向流动，一般只能允许父子（亲缘关系）关系进程间通信；
    - 有名管道，半双工通信方式，可以允许无亲缘关系进行通信；
- 系统IPC
    - 信号量，计数器，控制多个进程对资源访问，通过作为锁机制；
    - 消息队列，消息链表，存在在内核中并由
    - 信号，通知接受进程某个事件发生；
    - 共享内存，映射一段能被多个进程访问的内存。
- SOCKET
    - Unix Socket，利用Socket通信方式（TCP/IP协议栈）使本地进程与进程通信。



# 内存管理



# 信息保护和安全



> 缓冲区溢出：缓冲区溢出，指的是缓冲区中存储的数据超出了缓冲区的大小，覆盖在合法数据区上。
    - 造成程序崩溃，导致服务拒绝；
    - 跳转并执行恶意代码。
    
# Reference
- [操作系统面试题](https://zhuanlan.zhihu.com/p/23755202)
- 《操作系统精髓与设计原理》
