# Java IO
## 基本架构
根据IO的传输的方式和数据格式分组（基本位于java.io下）：
1. 基于字节的I/O接口：InputStream和OutputStream；
2. 基于字符的I/O接口：Writer和Reader；
3. 基于磁盘的操作I/O接口：File；
4. 基于网络操作的I/O接口：Socket；
> 1/2 主要数据格式，2/4主要传输方式

## 基于字节的I/O操作接口
- InputStream类层次结构：<br>
![](/images/java/javaio/javaio-inputstream.PNG)

- OutputStream类层次结构：<br>
![](/images/java/javaio/javaio-outputstream.PNG)

## 基于字符的I/O操作接口
磁盘存储和网络传输都是以字节为基础，字节转换为字符，需要通过编码转换。
- Writer类层次结构<br>
![](/images/java/javaio/javaio-writer.PNG)

- Reader类层次结构<br>
![](/images/java/javaio/javaio-reader.PNG)

- 字节与字符转化主要通过StreamDecoder与StreamEncoder实现：<br>
![](/images/java/javaio/javaio-encoder.PNG)<br>
![](/images/java/javaio/javaio-encoder.PNG)

## 磁盘I/O
文件访问方式分类如下：
- 标准访问文件方式，基础的磁盘数据读写，从用户空间到内核缓存，然后从内核缓存到磁盘。<br>
![](/images/java/javaio/javaio-standio.PNG)

- 直接I/O方式，在之前基础上，提高传输效率，通过直接访问磁盘数据（不经过内核缓冲区）的方式，是一种直接I/O的方式（应用于数据库管理系统，缺点：应用程序缓存直接访问磁盘，效率低下）<br>
![](/images/java/javaio/javaio-directio.PNG)

- 同步访问文件方式，写入与读取都是同步阻塞的，性能较差。<br>
![](/images/java/javaio/javaio-syn.PNG)

- 异步访问文件方式，发送磁盘读写请求，然后，处理其他事务，提高程序效率。<br>
![](/images/java/javaio/javaio-asyn.PNG)

- 内存映射方式，将操作系统内存某一块区域与磁盘文件关联，访问此段内存转化为访问文件，减少内核空间缓存到用户空间缓存数据复制操作。<br>
![](/images/java/javaio/javaio-mmap.PNG)

### Java访问磁盘
File类，表示虚拟文件对象（可能是文件或目录），当读写文件（创建FileInputStream类）时，检验文件是否存在。而，FileInputStream对象，创建FileDescriptor对象，这是一个存在文件的真正代表。
> FileDescriptor.getFD()，获取文件操作符；
> FileDescriptor.sync()，强制将数据刷到物理磁盘；

![](/images/java/javaio/javaio-hdjava.PNG)

### Java序列化
将对象转化成一个二进制表示的字节数组，持久化。java序列化

## 网络I/O
### TCP状态转化
![](/images/java/javaio/javaio-tcpstatus.PNG) <br>
1. CLOSED: 起始点，在超时或者连接关闭时进入状态；
2. LISTEN: Server端在等待连接时状态，Server端调用Socket、bind、listen函数，应用程序被动打开。（等待客户端连接）
3. SYN-SENT：客户端发起连接，发送SYN给服务器端。如果服务器不能连接，则直接进入CLOSED状态；
4. SYN-RCVD：与3对应，服务端接受客户端SYN请求，服务器端由LISTEN状态进入SYN-RCVD状态。同时服务端回应一个ACK，发送一个SYN给客户端；另一种情况，客户端在发起SYN同时接受到服务器端的SYN请求，客户端会由SYN-SENT转换到SYN-RCVD状态。
5. ESTABLISHED：服务端与客户端在完成3次握手后进入状态，说明已经可以开始传输数据。
6. FIN-WAIT-1：主动关闭一方，由状态5进入此状态。具体动作是发送FIN给对方。
7. FIN-WAIT-2：主动关闭一方，接收到对方的FIN ACK，进入此状态。由此不能发送数据，但是能接受数据。
8. CLOSE-WAIT：接收到FIN以后，被动关闭的一方进入此状态，接受FIN，发送ACK。
9. LAST-ACK：被动关闭一方，发起关闭请求，又状态8进入此状态。具体动作，发送FIN给对方，同时接收ACK进入CLOSED状态。
10. CLOSING：两边同时发起关闭请求时，会由FIN-WAIT-1进入此状态。具体动作是接收到FIN请求，同时响应一个ACK。
11. TIME-WAIT：三种方式转化为此状态：
    1. FIN-WAIT-2 -> TIME-WAIT，正常关闭，主动关闭方进入状态。
    2. CLOSING -> TIME-WAIT，同时关闭。
    3. FIN-WAIT-1 -> TIME-WAIT，同时接收到FIN和ACK。
    
> 影响网络传输因素：
> 1. 网络带宽；
> 2. 传输距离；
> 3. TCP拥塞控制。

### Java Socket
Socket <-> ServerSocket
InputStream/OutputStream <-> InputStream/OutputStream


## NIO
### BIO挑战
阻塞式IO，使线程失去CPU使用权，影响线程执行性能。此外，针对高并发长连接的情况，开销很大。

### 工作机制（网络）
NIO通过Channel、Buffer和Selector，能够更细致控制IO过程。<br>
![](/images/java/javaio/javaio-nio.PNG)

- 基于NIO的Socket请求处理过程 <br>
![](/images/java/javaio/javaio-niosocket.PNG)


### Buffer
Buffer用于缓存数据。
- capacity，缓冲区数组总长度。
- position，下一个操作的数据元素的位置。
- limit，缓冲区数组中不可操作的下一个元素的位置，limit <= capacity
- mark, 用于记录当前position的前一个位置或者默认是0.

![](/images/java/javaio/javaio-buffer1.PNG)

写入数据之后：<br>
![](/images/java/javaio/javaio-buffer2.PNG)

调用byteBuffer.flip()后，<br>
![](/images/java/javaio/javaio-buffer3.PNG)

调用mark()方式，记录当前position前一个位置，当调用reset时，position将恢复mark记录下来的值。

Channel获取I/O数据需要经过操作系统Socket缓冲区，再将数据复制到Buffer中，较为耗费性能。Buffer提供一种操作操作系统缓冲区的方式，ByteBuffer.allocateDirector(size)，返回DirectByteBuffer与底层存储关联的缓冲区，通过Native代码操作非JVM堆内存空间。每次创建或者释放时候调用一次System.gc()。
> 注意，使用DirectByteBuffer时，可能引起JVM内存泄漏。

![](/images/java/javaio/javaio-bytebuffer.PNG)

### NIO的磁盘访问方式
NIO针对传统的文件访问方式提供了优化，NIO的两种优化方法如下：
1. FileChannel.transferTo、FileChannel.transferFrom;<br>
FileChannel.transfreXXX与传统访问文件方式减少了数据从内核到用户空间复制，数据直接在内核空间中移动。(类似于Linux中sendfile系统调用),比较如下：<br>
![](/images/java/javaio/javaio-nio-tradition.PNG)<br>
优化之后：<br>
![](/images/java/javaio/javaio-nio-filechannel.PNG)

2. FileChannel.map <br>
FileChannel.map将文件按照一定大小映射为内存区域，当程序访问此内存区域，将直接操作文件。（这种方式节省了内核空间向用户空间复制损耗）

## 设计模式
- 适配器模式，将一个类接口变换为系统所能接受的另一种接口，换言之，将一个接口适配另一个接口。<br>
  例如：InputStreamReader和OutputStreamWriter，继承了Reader和Writer接口，创建时传入InputStream和OutputStream。（InputStreamReader通过StreamDecoder间接持有）<br>
  ![](/images/java/javaio/javaio-adapter.PNG)

- 装饰器模式，针对接口，动态给对象添加额外职责，从增加功能的角度来说，比继承中的子类更加灵活。（装饰模式，是继承关系的替代方案）<br>
  例如：FilterInputStream和BufferedInputStream对于InputStream。<br>
  ![](/images/java/javaio/javaio-decorater.PNG)

> 装饰器与适配器模式都有一个别名就是包装模式(Wrapper)，区别在于，适配器模式是将一个接口转变为另一个接口，装饰器模式目的是增强（改变）原有对象的处理方法。
