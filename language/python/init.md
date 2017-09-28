# Python2.7
## Content
* [OutPut](#output)
* [Input](#input)
* [Module](#module)
* [Reference](#reference)

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
- 


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

