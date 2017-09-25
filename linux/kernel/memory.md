# Basic
## 内存对齐
默认gcc编译器编译struct结构体存在内存对齐现象。
```
struct A{
    int a;
    char b;
}
printf("%d", sizeof(A));
// output is 8 bytes
```

1. 单结构体控制；
2. 某一个段源程序控制；
3. 

## 