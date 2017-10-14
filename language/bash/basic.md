# Content

* [变量](#变量)
	* [简单数学运算](#简单数学运算)
* [if语句](#if语句)
	* [值判断 ](#值判断)
	* [使用语法](#使用语法)

# 变量
$var是${var}的简写。
## 引用
- 弱引用
```shell
# 变量值用单引号，不发生变量替换
>> echo '$var'
$var
```

- 强引用
```
# 变量值用双引号，发生变量替换
>> var=123
>> echo '$var'
123
```


## 简单数学运算
- expr 转义

```
expr 5 \* 2
```
- let "XXXX"

```
var=1
let "var+=1"
```

- $[ xxx ]

- (())

```
var=1
((var+=1))
```

# if语句
## 值判断 
- if + 一条指令   
    if语句根据命令返回的状态码，判断（返回0，执行成功；返回其他，执行失败）。
```
#!/bin/bash
if date
then 
    echo "it worked"
fi
```
- test命令  
    test条件成立，输出状态码0；test条件不成立，输出状态码不为零。
    - 数值比较 -eq | -ge | -gt | -le | -lt | -ne
    - 字符串比较 = | != | < | > | -n | -z，使用转义（否则当成文件名，重定向）。
    - 文件比较 -d / -e / -f / -r / -s / -w / -x / -O / -G / -nt / -ot
    
```
test condition
// normal
if test condition
then 
    commands
fi
// another
if [ condition ]
then
    commands
fi
```

## 使用语法

- if-then-else

```
#!/bin/bash
# testing the else section
if grep $testuser /etc/passwd
then 
    echo THE FILES FOR USER $testuser are:
    ls -a /home/$testuser/.b*
else 
    echo HAHA
fi
```
- 嵌套if

```
if command1
then 
    commands
elif command2
then
    more commands
fi
```

- AND 和 OR

```
#!/bin/bash
if [ -d $HOME ] && [ -w $HOME/testing ]
then 
    echo "The file exists and you can write to it"
else 
    echo "I cannot write to the file"
fi
```

- 双尖括号 (())，复杂数学运算

```
#!/bin/bash

val1=10
if (( $val1 ** 2 > 90 ))
then
    (( val2 = $val1 ** 2 ))
    echo "The square of $val1 is $val2"
fi
```
- 双方括号[[]]，字符串比较的高级特性(模式匹配)

```
#!/bin/bash
if [[ $USER == r*  ]]
then
    echo "Hello $USER"
else
    echo "Sorry. I do not know you"
fi
```
