# Basic
## 内存对齐&大小端
默认gcc编译器编译struct结构体存在内存对齐现象。
```
struct A{
    int a;
    char b;
};
printf("%d", sizeof(A));
// output is 8 bytes
```
union联合类型变量，存在内存重叠。（C语言标准规定 -> 全局变量初始值为0）

```
// 用途：
// 1. 判断大端/小端机
// 2. windows中变色龙类型（通过一个union表示不同数据类型）
// 3. 超级强制类型转换（普通类型转换存在限制，函数指针不能转换为普通指针）
union A {
    unsigned int a;
    unsigned char b[4];
};
// output is 256，256是小端，65536是大端
// 表示机器为
// 不管大端/小端机器，数组低位是在低字节/高位在高字节
// 注意：字节内部不分大小端读取，字节之间分大小端读取顺序，而数组都是高位存在高地址，低位存在低地址。
void main() {
    g.b[1] = 1;
    g.b[0] = 0;
    g.b[2] = 0;
    g.b[3] = 0;
    printf("%d,%d\n",sizeof(A), g.a);
}


```

大端指的是**高尾端**，小端指的是**低尾端**，指的是尾端放在高地址还是低地址。例如：“11223344”（将数据看成字符串），尾端就是“44”，如下图所示，可以看出大端和小端的区别：

![big-little-endian] 

## 内存对齐控制方式

- 单结构体控制；

```
//gcc自带扩展关键字
struct A{
    ...
}__attribute__((packed));
```

- 某一个段源程序控制；

```
//带#字指令指导编译器工作，运行时消除
#pragma pack(n) // n=1,2,4,8
#pragma pack() //取消对齐
```

- 编译时控制（整个程序）；

```
//1字节对齐
-zp1 
//4字节对齐
-zp4
```

# 内存对齐作用
1. 平台原因(移植原因)：不是所有的硬件平台都能访问任意地址上的任意数据的；某些硬件平台只能在某些地址处取某些特定类型的数据，否则抛出硬件异常。
2. 性能原因：经过内存对齐后，CPU的内存访问速度大大提升。
> CPU按块（memory access granularity）读取内存，


 ***
 # Reference
 - http://www.cnblogs.com/wuyuegb2312/archive/2013/06/08/3126510.html
 
[big-little-endian]: /images/big-little.png 




