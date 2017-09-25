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
// output is 256
// 表示机器为
// 不管大端/小端机器，数组低位是在低字节/高位在高字节
// 注意：字节内部不分大小端读取，字节之间分大小端读取顺序
void main() {
    g.b[1] = 1;
    g.b[0] = 0;
    g.b[2] = 0;
    g.b[3] = 0;
    printf("%d,%d\n",sizeof(A), g.a);
}
```


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
## 