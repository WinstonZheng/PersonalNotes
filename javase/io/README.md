# IO
JavaIO的基础框架，从读写来源主要分为对磁盘的读写（File）、对网络的读写（Socket/Datagram）。此外，根据读写方式分，可以分为传统的基于流的阻塞式IO，非阻塞的NIO，以及JDK1.7的AIO。

- 面向流的 I/O 一次处理一个字节数据：一个输入流产生一个字节数据，一个输出流消费一个字节数据。为流式数据创建过滤器非常容易，链接几个过滤器，以便每个过滤器只负责复杂处理机制的一部分。不利的一面是，面向流的 I/O 通常相- 当慢。
- 面向块的 I/O 一次处理一个数据块，按块处理数据比按流处理数据要快得多。但是面向块的 I/O 缺少一些面向流的 I/O 所具有的优雅性和简单性。

> I/O 包和 NIO 已经很好地集成了，java.io.* 已经以 NIO 为基础重新实现了，所以现在它可以利用 NIO 的一些特性。例如，java.io.* 包中的一些类包含以块的形式读写数据的方法，这使得即使在面向流的系统中，处理速度也会更快。

## File
以File类为核心，通过FileInputStream/FileOutputStream，以及FileReader/FileWriter进行读写。主要负责对磁盘中文件的操作。

## Socket/Datagram
- InetAddress，用于表示网络上的硬件资源，即 IP 地址；
- URL，统一资源定位符；
- Socket，使用 TCP 协议实现网络通信；
    - ServerSocket：服务器端类
    - Socket：客户端类
    - 服务器和客户端通过 InputStream 和 OutputStream 进行输入输出。
- Datagram，使用 UDP 协议实现网络通信。





# Blocking IO
传统的阻塞式IO是基于流的方式实现，整个框架的设计思路是通过装饰器模式构建。根据不同的数据来源（File or Socket），通过包装不同的InputStream（最常用的应该是BufferedInputStream）提供不同的能力。在JDK1.4之前，用Java编写网络请求，都是建立一个ServerSocket，然后，客户端建立Socket时就会询问是否有线程可以处理，如果没有，要么等待，要么被拒绝。即：一个连接，要求Server对应一个处理线程。

# NIO
新的输入/输出 (NIO) 库是在 JDK 1.4 中引入的。NIO 弥补了原来的 I/O 的不足，提供了高速的、面向块的 I/O。
这套API由三个主要的部分组成：缓冲区（Buffers）、通道（Channels）和非阻塞I/O的核心类组成。在理解NIO的时候，需要区分，说的是New I/O还是非阻塞IO,New I/O是Java的包，NIO是非阻塞IO概念。这里讲的是后面一种。

NIO本身是基于事件驱动思想来完成的，其主要想解决的是BIO的大并发问题： 在使用同步I/O的网络应用中，如果要同时处理多个客户端请求，或是在客户端要同时和多个服务器进行通讯，就必须使用多线程来处理。也就是说，将每一个客户端请求分配给一个线程来单独处理。这样做虽然可以达到我们的要求，但同时又会带来另外一个问题。由于每创建一个线程，就要为这个线程分配一定的内存空间（也叫工作存储器），而且操作系统本身也对线程的总数有一定的限制。如果客户端的请求过多，服务端程序可能会因为不堪重负而拒绝客户端的请求，甚至服务器可能会因此而瘫痪。

NIO基于Reactor，当socket有流可读或可写入socket时，操作系统会相应的通知引用程序进行处理，应用再将流读取到缓冲区或写入操作系统。 
也就是说，这个时候，已经不是一个连接就要对应一个处理线程了，而是有效的请求，对应一个线程，当连接没有数据时，是没有工作线程来处理的。

# AIO
与NIO不同，操作系统负责处理内核区/用户区的内存数据迁移和真正的IO操作，应用程序只须直接调用API的read或write方法即可。这两种方法均为异步的，对于读操作而言，当有流可读取时，操作系统会将可读的流传入read方法的缓冲区，并通知应用程序；对于写操作而言，当操作系统将write方法传递的流写入完毕时，操作系统主动通知应用程序。 
即可以理解为，read/write方法都是异步的，完成后会主动调用回调函数。 
在JDK1.7中，这部分内容被称作NIO.2，主要在java.nio.channels包下增加了下面四个异步通道：
- AsynchronousSocketChannel
- AsynchronousServerSocketChannel
- AsynchronousFileChannel
- AsynchronousDatagramChannel
其中的read/write方法，会返回一个带回调函数的对象，当执行完读取/写入操作后，直接调用回调函数。

# Reference
- [](https://blog.csdn.net/u013851082/article/details/53942947)