
# Docker java client
> 正常的Docker server与**Docker client**的链接方式是：Unix sockets

> Docker server与**Docker java client**的默认链接方式是UNIX
  sockets。Docker-java client 默认使用TCP/IP技术链接Docker            server，确保Docker server正在监听TCP的port。  
默认的配置文件在 /etc/default/docker    
需要在配置文件中添加如下：

```
DOCKER_OPTS="-H tcp://127.0.0.1:2375 -H unix:///var/run/docker.sock"
```
> 此外，你可以强制docker-java使用UNIX socket:

```
unix:///var/run/docker.sock
```


