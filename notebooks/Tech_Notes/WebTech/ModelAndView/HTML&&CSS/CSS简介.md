[TOC]

# CSS简介
> CSS（Cascading Style Sheets）指层叠样式表。 > CSS文件存储在.css文件中。

多重样式将层叠为一个：  
层叠次序（1->4，优先级由低到高）：  
1. 浏览器缺省设置
2. 外部样式表
3. 内部样式表（位于 <head> 标签内部）
4. 内联样式（在 HTML 元素内部）    
（所以说，在HTML元素中定义的样式，优先级最高）

# CSS语法
## 基础语法
> CSS由两个部分组成：
> 1. 选择器：通常是你需要改变样式的HTML元素；
> 2. 一条或者多条的声明：每条声明由一个属性和一个值组成；
```
selector{declaration1;declaration2;...declarationN}
```
属性(property)是你希望设置的样式属性（style attribute）。
```
selector{property:value}
```
> CSS对大小写不敏感，与HTML相关联的Class和id名称是大小写敏感的。

## 高级语法

> 选择器分组:    
将HTML中多种多种元素，设置在同一个组，能设置统一的属性。
```
h1,h2,h3,h4,h5,h6 {
 color:green;
}
```
> 继承
  子元素会继承父元素的属性，而有些浏览器不支持这种属性，所以可以用组选择器的方式。

## 选择器
### 派生选择器
> 根据文档的上下文关系来确定某个标签样式。
```
li strong {
    font-style: italic;
    font-weight: normal;
  }
```
(后代选择器、子元素选择器、相邻兄弟选择器)

### id选择器
> 利用id，设置某个元素的属性。
```
#red {color:red;}
#green {color:green;}
```
## 类选择器
> 书写的顺序不同，产生的效果也不同。
```
//某些类为fancy的元素所包含的表格单元格，采取当前属性。
.fancy td {
	color: #f60;
	background: #666;
	}
//类为fancy的表格单元格，采取当前属性。
td.fancy {
	color: #f60;
	background: #666;
	}
```
## 属性选择器
> IE7和IE8支持属性选择器，IE6以及更低版本中，不支持属性选择。
```
[title]
{
color:red;
}
//title="W3School
[title=W3School]
{
border:5px solid blue;
}
```
- [attribute]
- [attribute=value]
- [attribute~=value]
- [attribute|=value]
- [attribute^=value]
- [attribute$=value]
- [attribute*=value]
[CSS属性选择器参考手册](http://www.w3school.com.cn/css/css_syntax_attribute_selector.asp)

## 如何插入样式表
1. 外部样式表：
```
<head>
<link rel="stylesheet" type="text/css" href="mystyle.css" />
</head>
```
(不要添加任何没有意义的空格)
2. 内部样式表：
在文档头部定义：
```
<head>
<style type="text/css">
  hr {color: sienna;}
  p {margin-left: 20px;}
  body {background-image: url("images/back40.gif");}
</style>
</head>
```
3. 内联样式表：
将表现和内容混杂在一起。
```
<p style="color: sienna; margin-left: 20px">
This is a paragraph
</p>
```
4. 多重样式：
如果某些属性在不同的样式表中被同样的选择器定义，那么属性值将从更具体的样式表中被继承过来。

