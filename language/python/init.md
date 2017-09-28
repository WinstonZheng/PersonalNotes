# Python 2.7
## Content
* [Type 3](#type)
* [Output](#output)
* [Input](#input)
* [Module](#module)
* [Reference](#reference)

## Type

- 数据类型转换

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




## Output
- Print to Screen

```py
// %r is used to debugging , %s and %d is display to user
name = crazybear
age = " %d "
print "Hello", name
print "1 + 1 = %d" % 2
print "Hello %s" % 'crazybear'
print "Hello %s, age %d" % ( name, age % 2  )
 
// the output is "..."
print "." * 3

// print with formatter
formatter = "%r %r %r %r"
print formatter % (1,2,3,4)
print formatter % ("one","two","three","four")
print formatter % (True, False , False , True)
print formatter % (formatter, formatter, formatter, formatter)

// %r id "raw" format for debugging
print "%r" % '\n'

// print a block, you can use """ or '''
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
- raw_input and input 

input通过raw_input实现（raw_input + eval），input接受合法python表达式（直观字符串需要加“”），raw_input转化为字符串。（一般推荐用raw_input作为交互）

```
print "How old are you?",
age = raw_input()
// convert the input to an integer 
x = int(raw_input())

```

 
## Funxtion
### 空函数

```py
def nop():
    pass
```

### 传递参数

#### 参数类型检查

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

#### 参数种类


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

// 多次调用add_end()，改变默认值 
def add_end(L=[])
    L.append('END')
    return L
// 改进
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
// 传入list或者tuple作为可变参数
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

```
// * 后面参数视为命名关键字参数
def person(name, age, *, city, job):
    print(name, age, city, job)
// 传入参数名，对应命名关键字参数。已有可变参数，之后命名关键字参数不用带*
// 如果不存在可变参数，则需要*，否则无法区分命名关键字参数和位置参数
def person(name, age, *args, city, job):
    print(name, age, args, city=‘jinhua’, job)

```

> ** 参数组合**
> 参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。
> *args 是可变参数，tuple；**kw是关键字参数，dict。


### 返回值

- 无返回结果 None
- 返回多个值， 返回一个tuple(可以省略括号)

```
import math

def move(x, y, step, angle = 0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny 
```


## Module


## little tips

```py
// tell the editor to use the utf-8
#-*- coding:utf-8 -*-

// uset the command to view the command line document
pydoc raw_input

```




***
## Reference
- Learn Python The Hard Way. 3rd
- [廖雪峰Python教程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014316784721058975e02b46cc45cb836bb0827607738d000)
