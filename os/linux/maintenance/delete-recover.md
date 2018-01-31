# 误删恢复
## 方案一

```
grep -a -B 50 -A 60 'some string in the file' /dev/sda1 > results.txt
```

## 方案二
ext3grep