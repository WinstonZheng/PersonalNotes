# 基础概念
- Domain <br>
    Domain是最高层的概念，包含多个Projects/Users/Groups/Roles，方便用户管理云平台。
- Tenant/Project <br>
    在Keystone V3版本，将Tenant改称为Project，并在其上添加Domain概念。其中，Project或者Tenant指的是一组资源的集合。
- Groups/Users <br>
    属于某一个Project（或多个Project），Group是一组Users集合，通过赋予Group的Role，方便统一赋予Users权限。Users指的是一切使用OpenStack服务的对象。
- Role <br>
    角色，用于分配操作权限，通过赋予用户权限，可以指定用户操作权限。
- Token <br>
    指的是一串比特值或者字符串，用来作为访问资源的记号。Token 中含有可访问资源的范围和有效时间。
- Endpoint <br>
    这是Keystone的服务注册功能，服务访问端口（暴露端口），分为public（全局访问）、private（局域网访问）、admin（在常规访问中分离）。




# Reference
- [OpenStack Keystone V3 简介](https://www.ibm.com/developerworks/cn/cloud/library/1506_yuwz_keystonev3/index.html)
