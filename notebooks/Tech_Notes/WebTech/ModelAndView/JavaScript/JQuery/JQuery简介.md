jQuery 是一个 JavaScript 函数库。   
jQuery 库包含以下特性：
- HTML 元素选取
- HTML 元素操作
- CSS 操作
- HTML 事件函数
- JavaScript 特效和动画
- HTML DOM 遍历和修改
- AJAX
- Utilities

### JQuery语法

使用各种选择器来选择HTML元素。
```
//隐藏当前的 HTML 元素。
$(this).hide()    

//隐藏 id="test" 的元素。
$("#this").hide() 

//隐藏所有 <p> 元素。
$("p").hide()

//隐藏所有 class="test" 的元素。
$(".test").hide()
```
> 基础语法：
    $(selector).action()
    >> - 美元符号定义 jQuery
    >> - 选择符（selector）“查询”和“查找” HTML 元素
    >> - jQuery 的 action() 执行对元素的操作       

> 文档就绪函数：防止文档在完全加载前运行jQuery代码，可能失败。

```
$(document).ready(function(){

--- jQuery functions go here ----

});
```
