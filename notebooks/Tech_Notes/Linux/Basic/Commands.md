

## trace
> 



## curl
> curl是利用URL语法在命令行方式下工作的开源文件传输工具。    
获取页面方式：  

```
curl https://www.baidu.com
```
> 

## nohup
> 

## bg && fg && jobs
- ctrl + z  
  将前台任务放到后台，并暂停。
- &     
  将任务放在后台执行。
- jobs      
  查看当前shell环境后台正在运行或者挂起的任务。
- fg        
  将后台的任务调至前台运行。
- bg        
  将后台一个暂停的任务，变成继续执行（或者放到后台运行）。如果后台有多个job，可以通过jobs查看不同的任务序号，从而使用 bg + job number来运行（不是pid）。   
  终止进程，可以通过kill+ job number / pid。

## kill
kill -SIGKILL pid  用内核终止进程。

## top
> top提供了对系统处理器的实时状态监控。