* [概述](#概述)
* [第一步 初始化环境](#第一步-初始化环境)
* [第二步 安装horizon依赖包](#第二步-安装horizon依赖包)
* [第三步 配置local_settings文件](#第三步-配置local_settings文件)
* [第四步 翻译](#第四步-翻译)
* [第五步 静态资源设置](#第五步-静态资源设置)
* [第六步 Session存储](#第六步-session存储)
* [第七步 部署Apache2服务器](#第七步-部署apache2服务器)
	* [Runserver](#runserver)
	* [Apache2](#apache2)
* [**Bug记录**](#bug记录)
	* [import base模块出错](#import-base模块出错)
	* [secret_key_stone权限问题](#secret_key_stone权限问题)
	* [nova_client找不到security_group](#nova_client找不到security_group)
	* [静态资源打包出错](#静态资源打包出错)
* [Reference](#reference)

# 概述
Horizon是OpenStack中提供可视化管理（Dashboard）的组件，使用的Python的Web开发框架Django开发，使得Horizon本身代码结构较为简单，但是，内部数据流比较复杂。<br>
本文主要目的是记录如何去远程部署一个Horizon组件（Horizon后台通过OpenStack提供的不同的Client访问服务接口），有助于之后考虑在Horizon上进行二次开发。
> 注意：本文实测的版本是 horizon-newton版本，其他版本可能存在不同问题，仅供参考。此外，服务器使用的是Ubuntu14.04。

# 第一步 初始化环境

-  安装Linux环境 <br>
```py
# 注意pip最好用最新的版本，旧版不支持python约束文件参数
# 参照官网升级https://pip.pypa.io/en/stable/installing/
sudo apt-get install git python-pip
sudo pip install python-dev
# 构建python虚拟运行环境
sudo pip install virutalenv
```

- 下载源码 <br>
```py
# 首先拉下Horizon的代码
git clone https://git.openstack.org/openstack/horizon
# 因为，实验环境是Newton版本，所以，需要将版本回退，查看版本号
git tag
# 回退任意版本的commit
git revert <commit>
```

# 第二步 安装horizon依赖包
这一步是主要出问题的一步，因为在newton版本下，目录提供requirement.txt是版本是有问题的，直接通过pip工具下载，运行会报错，至于问题在什么地方，请继续往下看。<br>
此外，最新的文档中提供用tox工具的安装，配置虚拟环境，非常简单，但是，运行newton版本时候还是出错，这里暂时不深究这个。而，在newton版本下的tools目录下，提供了install_venv.py的脚本工具安装，同样非常方便，但是，本人尝试过，直接运行同样存在依赖包版本的问题。<br>
其实，看一下脚本，究其根本而言，原理都是配置一个python虚拟环境，然后在虚拟环境中安装依赖包，配置运行环境变量，然后运行网站。所以，本文就从基础一步一步配置，让读者了解清楚原理。

- 安装虚拟运行环境
```
cd horizon/
virtualenv .venv
soucre .venv/bin/activate
# 安装需要的依赖包
pip install -Ur test-requirements.txt && pip install -Ur requirements.txt
# 检查约束，openstack提供对于newton版本的依赖约束
# https://github.com/openstack/requirements/blob/stable/newton/upper-constraints.txt
pip install -c <constraints-file>
```


# 第三步 配置local_settings文件
```
//从模板创建配置文件。
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py
```

修改配置文件的如下属性：
- DEBUG = False/True（日志输出水平）
- ALLOWED_HOSTS = ['*',]（限制远端访问）
- OPENSTACK_HOST = "xxx.xxx.xxx.xxx"（访问OPENSTAKC服务的IP地址）

# 第四步 翻译
如果需要中文支持，那么需要通过gettext工具提供编译不同语言支持。
```py
sudo apt-get install gettext
./manage.py compilemessages
```


# 第五步 静态资源设置
需要事先在local_setting.py文件中设置COMPRESS_OFFLINE = True。
```
./manage.py collectstatic
./manage.py compress
```

# 第六步 Session存储
Horizon使用Django's session framework控制会话数据。可以通过多种方式后端提供支持。通过在local_setting.py文件中，对SESSION_ENGINE设置。

1. Memcached.
2. Database.
3. Cached Database 

如果实验环境，可以进行简单配置，使用本地内存：
```
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.locmem.LocMemCache',
    },
}
```

> 具体可参考 [Openstack Manul install](https://docs.openstack.org/horizon/latest/install/from-source.html)

# 第七步 部署Apache2服务器
可以通过两种方式运行Horizon组件：
1. 通过Django的manage.py工具；
2. 直接运行Apache2服务器。

## Runserver
正常的Django，可以通过manage.py这个工具包运行网站。
```
./manage.py runserver <ip>:<port>
```

## Apache2
- 安装依赖包 <br>
```
sudo apt-get install apache2 libapache2-mod-wsgi
```
- 生成一个WSGI文件 <br>
``` 
./manage.py make_web_conf --wsgi
```
- 在apache2服务器下配置horizon网站
```
 ./manage.py make_web_conf --apache > /etc/apache2/sites-available/horizon.conf
```
- 配置apache2服务器监听端口。（apache 配置监听对应自定义端口 ports.conf）
- 运行apache2服务器
```
sudo a2ensite horizon
sudo service apache2 restart
```

> 此处只是简单提供一个部署步骤，更多配置参考Reference。

# **Bug记录**
## import base模块出错
- 出错 <br>
```
Mon Nov 13 08:11:22.273662 2017] [:error] [pid 39513:tid 139788644116224] [remote 192.168.0.199:61715]   File "/home/XXX/workspace/python/horizon-newton/openstack_dashboard/api/__init__.py", line 34, in <module>
[Mon Nov 13 08:11:22.273672 2017] [:error] [pid 39513:tid 139788644116224] [remote 192.168.0.199:61715]     from openstack_dashboard.base import *
[Mon Nov 13 08:11:22.273695 2017] [:error] [pid 39513:tid 139788644116224] [remote 192.168.0.199:61715] ImportError: No module named base
```
- 解决方案 <br>
```
# 修改源码 openstack_dashboard/api/__init__.py
# before，记得将ALL变量也注释掉
from openstack_dashboard.api import base
from openstack_dashboard.api import ceilometer
from openstack_dashboard.api import cinder
from openstack_dashboard.api import fwaas
from openstack_dashboard.api import glance
from openstack_dashboard.api import heat
from openstack_dashboard.api import keystone
from openstack_dashboard.api import lbaas
from openstack_dashboard.api import network
from openstack_dashboard.api import neutron
from openstack_dashboard.api import nova
from openstack_dashboard.api import swift
from openstack_dashboard.api import vpn
# after
import base
from openstack_dashboard.api.ceilometer import *
from openstack_dashboard.api.cinder import *
from openstack_dashboard.api.fwaas import *
from openstack_dashboard.api.glance import *
from openstack_dashboard.api.heat import *
from openstack_dashboard.api.keystone import *
from openstack_dashboard.api.lbaas import *
from openstack_dashboard.api.network import *
from openstack_dashboard.api.neutron import *
from openstack_dashboard.api.nova import *
from openstack_dashboard.api.swift import *
from openstack_dashboard.api.vpn import *
```
## secret_key_stone权限问题
运行网站的用户需要对于.secret_key_store文件拥有写的权限。
- 出错 <br>
```
IOError: [Errno 13] Permission denied: '/home/winston/workspace/python/horizon-newton/openstack_dashboard/local/.secret_key_store'
```
- 解决方案：修改.secret_key_store权限。

## nova_client找不到security_group
- 出错 <br>
```
[Mon Nov 13 08:15:02.238413 2017] [:error] [pid 40074:tid 139788761728768] [remote 192.168.0.199:62739]     from openstack_dashboard.api import rest
[Mon Nov 13 08:15:02.238418 2017] [:error] [pid 40074:tid 139788761728768] [remote 192.168.0.199:62739]   File "/home/winston/workspace/python/horizon-newton/openstack_dashboard/api/__init__.py", line 36, in <module>
[Mon Nov 13 08:15:02.238427 2017] [:error] [pid 40074:tid 139788761728768] [remote 192.168.0.199:62739]     from openstack_dashboard.api.cinder import *
[Mon Nov 13 08:15:02.238431 2017] [:error] [pid 40074:tid 139788761728768] [remote 192.168.0.199:62739]   File "/home/winston/workspace/python/horizon-newton/openstack_dashboard/api/cinder.py", line 38, in <module>
[Mon Nov 13 08:15:02.238439 2017] [:error] [pid 40074:tid 139788761728768] [remote 192.168.0.199:62739]     from openstack_dashboard.api import nova
[Mon Nov 13 08:15:02.238444 2017] [:error] [pid 40074:tid 139788761728768] [remote 192.168.0.199:62739]   File "/home/winston/workspace/python/horizon-newton/openstack_dashboard/api/nova.py", line 34, in <module>
[Mon Nov 13 08:15:02.238452 2017] [:error] [pid 40074:tid 139788761728768] [remote 192.168.0.199:62739]     from novaclient.v2 import security_group_rules as nova_rules
[Mon Nov 13 08:15:02.238470 2017] [:error] [pid 40074:tid 139788761728768] [remote 192.168.0.199:62739] ImportError: cannot import name security_group_rules
```

- 解决方案：将nova-client版本改为2.29.0（可能其他版本支持，但是，方便起见，将其回退到最早的版本），要求的最低版本，最新版本将security_group_rules给弃用了。

## 静态资源打包出错
- 出错 <br>
```
CommandError: An error occurred during rendering /home/winston/workspace/python/horizon-newton/openstack_dashboard/templates/_stylesheets.html: Couldn't find anything to import: /horizon/lib/roboto_fontface/css/roboto-fontface.scss
Extensions: <NamespaceAdapterExtension>, <DjangoExtension>, <CompassExtension>
Search path:
on line 16 of themes/material/bootstrap/_styles.scss
imported from line 16 of themes/material/_styles.scss
imported from line 1 of u'string:c61b5d22d54bf56c:\n    // My Themes\n@import "/themes/material/variables";\n\n// Horizon\n@import "/dashboard/scss/horizon'
```

- 解决方案 <br>
```
sudo pip install -U "XStatic-roboto-fontface===0.4.3.2"
# output
Installing collected packages: XStatic-roboto-fontface
  Found existing installation: XStatic-roboto-fontface 0.5.0.0
    Uninstalling XStatic-roboto-fontface-0.5.0.0:
      Successfully uninstalled XStatic-roboto-fontface-0.5.0.0
Successfully installed XStatic-roboto-fontface-0.4.3.2
```

# Reference
- [Openstack Manul install](https://docs.openstack.org/horizon/latest/install/from-source.html)
- [Horizon Is Easy, Horizon Is Complex](http://blog.csdn.net/lixinhu0104/article/details/51860767)