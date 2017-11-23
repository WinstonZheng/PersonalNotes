# Horizon源码追踪详解
由于技术选型问题，所以研究了一下Horizon源码。针对源码简单做一个分析。通过源码追踪的方式，解析Horizon的实现原理。而，horizon是一个MVC架构的网站，采用python的Django框架支持。
> 有兴趣可以看一下最近写的安装horizon的文档。[click here](/virtualization/openstack/horizon/install.md)

## Horizon目录结构
Horizon这套面板设计分为三层：Dashboard -> PanelGroup -> Panel。首先，说一下本文主要涉及的Horizon的目录结构：<br>
- doc horizon文档；
- horizon 提供horizon模板组件，针对其他的Django框架可以复用；
- openstack_dashboard 
    - api 提供访问OpenStack的Client支持
    - dashboards 是根据需求组装的模板（admin/identity/project/settings）

## 模块追踪
   那么horizon是如何进行加载控件的？首先，我们应该找到入口，那么，如何去找到horizon的入口呢？既然，之前提了horizon是一个MVC架构的网站，采用了Django框架支持。那么，找到网站的url方法映射是一种很好的入口。<br>
我们来看看openstack_dashboard下的目录结构：
- openstack_dashboard 基于Django开发网站
    - templates 视图模板(html等)
    - setting.py 网站配置文件
    - views.py 视图渲染
    - urls.py 视图映射 <br>

熟悉Django架构网站的人（由于python优良的可读性，不熟悉也可以很容易理解）知道，urls.py文件就是我们需要找的。之后，我们通过代码追踪与注释的方式，从前往后逐步深入Horizon。

### /openstack_dashboard/urls.py
分析urls.py文件。
```py
# urlpatterns是一个list，url方法的第一个参数是正则表达式匹配的url，第二个参数
# 是对应的处理方法，而include()是导入其他urls属性或者urls.py文件。
# 选择第三个匹配空字符的url，映射到horizon.urls，找到目录horizon.__init__.py文件
import horizon
urlpatterns = [
    url(r'^$', views.splash, name='splash'),
    url(r'^api/', include(rest.urls)),
    url(r'', include(horizon.urls)),
]
```

 ### /horizon/__init__.py
 由urls.py中import可知，url映射到了horizon模块。
 ```py
 # 从如下代码可以看出，导出了horizon/base.py下的Horizon模块，并调用了其中的_lazy_urls方法。
 try:
    from horizon.base import Dashboard  # noqa
    from horizon.base import Horizon  # noqa
    from horizon.base import Panel  # noqa
    from horizon.base import PanelGroup  # noqa
 
 if Horizon:
    register = Horizon.register
    unregister = Horizon.unregister
    get_absolute_url = Horizon.get_absolute_url
    get_user_home = Horizon.get_user_home
    get_dashboard = Horizon.get_dashboard
    get_default_dashboard = Horizon.get_default_dashboard
    get_dashboards = Horizon.get_dashboards
    urls = Horizon._lazy_urls
 ```
 
 ### /horizon/base.py
 base.py文件是核心文件，为horizon组件提供了三层页面模板组织。





# 总结