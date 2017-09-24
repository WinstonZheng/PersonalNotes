# Python2.7
## Output
- print to Screen

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

```
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




## little tips

```py
# tell the editor to use the utf-8
#-*- coding:utf-8 -*-
```



