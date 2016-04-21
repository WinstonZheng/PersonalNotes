[TOC]
# JQuery语法细节

标签（空格分隔）： JQuery

---
## Basic
1. jQuery() <=> $()
2. jQuery读写和处理文档DOM，在文档加载之后进行：
    
    ```
    //正常加载方式：
    $(document).ready(function(){
    //jQuery代码
    });
    
    //JS使用方式(区别在于onload事件后于ready事件发生)：
    window.onload = function(){
        //js代码
        }
    //简化方式：
    $(function(){
        //jQuery
        });
    ```
**核心**：jQuery就是从HTML元素中找到匹配元素并对其进行操作。

### **DOM对象**与**jQuery对象**差别：
> DOM对象：Document Object Model，访问文档节点的内置方法：
    - getElementsByTagName();
    - getElementById();
> jQuery对象：jQuery包装DOM对象后产生的新对象。（本质上是DOM对象的集合体，DOM类数组）
### **DOM对象**与**jQuery对象**互相转化：
+ DOM => jQuery

```
//the first 数组下标
var $li = $("li");
var li = $li[0];
//the second get()方法
var $li = $("li");
var li = $li.get(0);
```
+ jQuery => DOM

```
var li = document.getElementsByTagName("li");
//the first
var $li = $(li[0]);
//the second
var $li2 = $(li);
```
## jQuery构造器
1. jQuery(expression,context);
    expression: ID/DOM元素名/CSS表达式/XPath表达式等；      
    
    ```
    //:first是一个伪类，CSS表达式
    jQuery("div#wrap>p:first").addClass("red");
    ```
2. jQuery(elements);    
    参数表示一个HTML结构字符串。    

    ```
    //将<li></li>转化为DOM对象
    $('ul').append($('<li>new item</li>'));
    ```
3. jQuery(fn);  
    参数表示一个处理函数，$(document).ready() => $(fn);


## jQuery选择器
本质是某种含义的字符串传递给jQuery构造器，返回DOM对象，返回jQuery对象，主要功能是选择和过滤。

