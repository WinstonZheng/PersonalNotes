
`[TOC]`

## Docker中的一些操作说明：
1. docker attach命令是连接上container中正在运行的进程， 可以使用：  
   + CTRL+C , 退出当前进程，并发送一个SIGKILL信号结束container；
   + CTRL+P CTRL+Q ,退出进程，但不结束container中的进程。