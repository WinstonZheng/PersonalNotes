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

