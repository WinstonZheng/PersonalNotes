# Hadoop
# Hadoop1.x

# Hadoop2.x

NodeManager是YARN中单个节点的代理，它须要与应用程序的ApplicationMaster和集群管理者ResourceManager交互;它从ApplicationMaster上接收有关Container的命令并执行(比方启动、停止Contaner);向ResourceManager汇报各个Container执行状态和节点健康状况，并领取有关Container的命令（比方清理Container）。





# Reference

[Hadoop - YARN NodeManager 剖析](https://www.cnblogs.com/yangykaifa/p/7015598.html)