* [basic-tools](#basic-tools)
* [monitor](#monitor)
    * [sysstat](#sysstat)
* [network](#network)
    * [net-tools](#net-tools)
    * [iproute2](#iproute2)
* [benchmark](#benchmark)






# basic-tools

- lsb_release <br>
查看linux发布版本。

```
// can use in Ubuntu
lsb_release -a
```

# monitor
## sysstat
用于监控系统性能。
- vmstat - 内存，进程和分页等的简要信息。
- iostat - CPU统计信息，设备和分区的输入/输出统计信息。


# network
## net-tools
这类工具原先起源于BSD TCP/IP工具箱，旨在配置老式Linux内核的网络功能。自2001年以后，在Linux社区停止维护。

- ifconfig
- route
- arp
- netstat

## iproute2
net-tools可以通过procfs（/proc）和ioctl系统调用，访问和更改内核网络配置，iproute2则通过网络链路套接字接口与内核进行联系。/proc接口比网络链路接口来得更笨拙。
> 优点
> 1. 性能好；
> 2. 优良的用户设计界面；
> 3. 处于开发维护，适应新式Linux内核。

- ip link
- ip addr
- ss (socket)
- ip neigh
- ip maddr


# benchmark

- stream(memory test)

- iperf(network test)
> 

- iozone(filesystem test)
> iozone is a filesystem benchmark tool. The benchmark testss file I/O benchmark for the following operations:
    Read, write, re-read, re-write, read backwards, read strided, fread, fwrite, random read, pread ,mmap, aio_read, aio_write










