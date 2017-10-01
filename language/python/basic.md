# Python 2.7
# Content
* [基础类型](#基础类型)
* [流程控制](#流程控制)
* [标准输入/输出](#standard-io)
    * [输出](#output)
    * [输入](#input)
* [函数](#函数)
    * [空函数](#空函数)
    * [传递参数](#传递参数)
       * [参数类型检查](#参数类型检查)
       * [参数种类](#参数种类)
    * [返回值](#返回值)
* [小技巧](#小技巧)
* [Reference](#reference)

# 基础类型
python是弱类型语言（解释型）。

- String <br>
    utf-8用于传输类型，而unicode用于内存和磁盘存储。
```py
# 分段连接字符串，必须加（），否则出错
# TypeError: bad operand type for unary +: 'str'
message = (
      "From: %s\r\n" % fromaddr
    + "To: %s\r\n" % toaddrs
    + "CC: %s\r\n" % ",".join(cc)
    + "Subject: %s\r\n" % message_subject
    + "\r\n" 
    + msg
)
```


- list和tuple  list是可变数组，而tuple元组，不可变列表。

- dict和set <br>
dict对应map，使用键值存储(key-value)，提供索引（Hash） ，查询速度快 , 耗内存。
```py
# the key is existing or not, if not, the reuslt is false
result = 'winston' in nameList
# use get, if not , the result is None
result = nameList.get('winston')
# delete
nameList.pop('winston')
```
set是一组key，无重复key，存储不可变对象。（重复元素，自动消除）
```py
s = set([1,2,3])
s.add(4)
s.remove(1)
r = set([2,3])
# result is set([2,3])，交集
r & s
# result is s，并集
r | s
```
> attention!
> set和dict中存储的key是不可变对象，例如：字符串和整数，List是可变的。

- 简单数据类型转换 
```py
int('123')
int(12.34)
float('12.34')
str(1.23)
str(100)
//True
bool(1)
//Flase
bool('')
```



# 流程控制

- 判断
```py
if <condition 1>:
    <process 1>
elif <condition 2>:
    <process 2>
else:
    <process 3>
# x 非零数值，非空字符串，非空list等，为True
if x:
    print 'True'
```

- 循环
```
for <value> in <values>
    print value 
while <condition>:
    <process>
```


# Standard IO
## Output
- Print to Screen <br>
```py
# %r is used to debugging , %s and %d is display to user
name = crazybear
age = " %d "
print "Hello", name
print "1 + 1 = %d" % 2
print "Hello %s" % 'crazybear'
print "Hello %s, age %d" % ( name, age % 2  )
# the output is "..."
print "." * 3
# print with formatter
formatter = "%r %r %r %r"
print formatter % (1,2,3,4)
print formatter % ("one","two","three","four")
print formatter % (True, False , False , True)
print formatter % (formatter, formatter, formatter, formatter)
# %r id "raw" format for debugging
print "%r" % '\n'
# print a block, you can use """ or '''
print """
 hahha
 hehhe
"""
```
- A list of all of the escape sequences Python supports.(**转义字符**)

|Escape|What it does.|
|----|----|
|`\\`|Backslash()|
|`\'`|Single quote(')|
|`\"`|Double quote(")|
|`\a`|ASCII Bell(BEL)|
|`\b`|ASCII Backspace (BS)|
|`\f`|ASCII Formfeed (FF)|
|`\n`|ASCII Linefeed (LF)|
|`\N{name}`|Character named name in the Unicode database (Unicode only)|
|`\r ASCII`|Carriage Return (CR)|
|`\t ASCII`|Horizontal Tab (TAB)|
|`\uxxxx`|Character with 16-bit hex value xxxx (Unicode only)|
|`\Uxxxxxxxx`|Character with 32-bit hex value xxxxxxxx (Unicode only)|
|`\v`|ASCII Vertical Tab (VT)|
|`\ooo`|Character with octal value ooo|
|`\xhh`|Character with hex value hh|

## Input
- raw_input and input <br>
input通过raw_input实现（raw_input + eval），input接受合法python表达式（直观字符串需要加“”），raw_input转化为字符串。（一般推荐用raw_input作为交互）
```py
print "How old are you?",
age = raw_input()
// convert the input to an integer 
x = int(raw_input())
```

- argv，命令行参数
```py
# unpack the argv
from sys import argv
def main():
    script,arg1,arg2 = argv
    print "name",script
    print "arg1:",arg1
    print "arg2:",arg2
```
 
# 函数
## 空函数

```py
def nop():
    pass
```

## 传递参数

### 参数类型检查

使用内置函数isinstance检查。

```py
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
```

### 参数种类


- 必选参数
```py
def power(x)
    return  x * x
```

- 默认参数
默认参数降低函数调用难度，默认参数的默认值应用不变对象，可变对象容易造成默认值更改。
```py
def login(name, password = '123')
    print('name', name)
    print('password', password)
# 多次调用add_end()，改变默认值 
def add_end(L=[])
    L.append('END')
    return L
# 改进
def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
```

- 可变参数
可以在参数中传入任意个参数（0个或多个），自动组装成tuple。
```py
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
# 传入list或者tuple作为可变参数
>>> nums = [1,2,3]
>>> calc(*nums)
```

- 关键字参数
可以传入0个或任意个含参数名的参数，自动组装为一个dict。(用于扩展函数功能，记录更多的信息)
```py
def person(name, age, **others)
    print(name, age, others)
>>> others = {'city':'Beijing'}
>>> print('rui',12,others['city'])
>>> print('rui',12,**others)
```

- 命名关键字参数 python3
限制关键字参数名字。
```py
# "*"后面参数视为命名关键字参数
def person(name, age, *, city, job):
    print(name, age, city, job)
# 传入参数名，对应命名关键字参数。已有可变参数，之后命名关键字参数不用带*
# 如果不存在可变参数，则需要*，否则无法区分命名关键字参数和位置参数
def person(name, age, *args, city, job):
    print(name, age, args, city=‘jinhua’, job)
```

> ** 参数组合**
> 参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。
> *args 是可变参数，tuple；**kw是关键字参数，dict。


## 返回值

- 无返回结果 None
- 返回多个值， 返回一个tuple(可以省略括号)

```
import math
def move(x, y, step, angle = 0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny 
```



# 小技巧

- 告诉编辑器，使用utf-8编码
```py
#-*- coding:utf-8 -*-
```

- 查看函数文档
``` py
pydoc raw_input
```

- python代码模板
```py
#!/usr/bin/env python
or
#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
a description for program
"""
__author__="XXX"
    <soruce code>
```




***
# Reference
- Learn Python The Hard Way. 3rd
- [廖雪峰Python2.7教程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014316784721058975e02b46cc45cb836bb0827607738d000)
