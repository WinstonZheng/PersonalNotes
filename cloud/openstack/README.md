# OpenStack
## Horizon组件
主要为OpenStack提供可视化界面管理。管理的内容主要是虚拟的资源，针对计算（虚拟机）、网络（路由器、子网IP等）、存储（卷、对象存储），支持增加、删除、修改和监控的功能，此外，还包括虚拟机迁移、资源权限等功能。
> 笔者主要使用的是Newton版本，OpenStack半年开发一个新版本，迭代较快，不同的版本之间的问题存在着一些兼容性（依赖包版本）的问题。

- [Horizon组件安装](/cloud/openstack/horizon/install.md)
- [Horizon源码追踪](/cloud/openstack/horizon/src-tracking.md)

## KeyStone组件
KeyStone组件的主要作用是负责客户端对OpenStack中不同组件的访问权限的管理。

- [keystone基础概念](/cloud/openstack/keystone/basic-concept.md)