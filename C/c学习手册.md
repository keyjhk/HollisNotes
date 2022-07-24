[TOC]
# 基本结构

```c++
#include <cstdio>
#include <iostream>

using namespace std;

int main(){ //main 表示程序入口 固定名字
    //do 
    // cstio 包含了scanf printf 两个输入输出函数
    // iostream 包含了 cin cout两个输入输出函数
    return 0; //正常返回值
}
```



# 变量

## 命名规范

* 以字母、下划线开头，不允许以数字开头(但允许非开头的地方使用数字)，区分大小写
* 不允许与标识符冲突，如`for`、`while`

## 整型

* int：4字节，范围为$[-2^{31},2^{31}=2,147,483,648]$ ， 

* long long：long long int的缩写，8字节。大致范围 $[-9*10^{18}-9*10^{18}]$。

  ```c++
  //long long 变量的初始化要在后面加上LL
  long long a=1e10;
  long long b=10000000000ll;
  ```

  

* unsigned：对于整型数据，都可以在前面加上`unsigned`表示无符号，取消负数范围，正数范围扩扩大一倍

```c
//整型的输入输出格式符号
scanf("%lld",&n);  //longlong

scanf("%d",&n);  //int 

printf("%d");
```

## 浮点

* float：32位存储，只能存储6~7为有效数字
* double：64位存储，有效精度为15~16位，推荐使用double存储浮点型数据

```c
//浮点的输入输出格式符号
scanf("%f",&n);  //float

scanf("%lf",&n);  //double

printf("%f") 

```

## 数组

### 一维数组

创建数组

```cpp
// 数组类型 数组名[数组大小]
// 数组大小必须是常量（包括const），不允许是变量
int a[10];
```

数组的初始化

```cpp
int a[10]={0}; //全部初始化为0
int a[10]={}; //全部初始化为0 

int a[10]={1,2,3}; //部分赋值，后面部分的值视编译器而异

//字符数组的初始化 
char str[10]={'h','e','l','l','o'};
char str1[10]="hello";
```

### 二维数组

二维数组的初始化和一维数组基本一样

```cpp
int a[5][6]; //初始化5*6大小的数组

//二维数组的初始化
int b[2][3]={{1,2},{0}};
```

### memset

memset可以对数组的每一个元素进行赋值，但推荐只赋值成0、-1，因为这两者的补码分别为全0、全1，而memset是按字节初始化的。

memset的语法格式

```cpp
#include <cstring> //memset需要用到这个头文件

//memset(数组名,赋值,sizeof(数组名))
int main(){
	int a[10];
	memset(a,-1,sizeof(a));
	for(int i=0;i<10;i++)
		printf("%d\n",a[i] );
}
```



## 字符和字符串

* 字符：char，用单引号包裹

* 字符串：c语言没有专门的字符串类型，但是可以用字符数组代替。字符串始终以空0`\0`结尾，实际开辟的数组长度要不字符串大1。

  ```cpp
  char name[]="jianghuikai"; //仅可在初始化时赋值
  printf("%s",name);
  
  // 使用strcpy 间接赋值
  # include <cstring>
  strcpy(name,"hollis");
  ```



printf格式控制

| 变量类型  | 格式控制符 |
| --------- | ---------- |
| int       | `%d`       |
| long long | `%lld`     |
| float     | `.mf`      |
| double    | `lf`       |
| char      | `%c`       |



## 类型转换

各个类型之间可以强制性转换`(变量类型)变量` 

```c++
int a=100;
float b=(float)a;
```

## 符号变量和const常量

符号变量

```c
//#define 符号 变量值;任何语句或者片段
#define pi 3.14 
#define add(a,b) ((a)+(b))

```

const 常量 ，一旦定义不允许修改

```cpp
const double pi=3.14;
printf("%lf",pi*2);
```

## 运算符

### 算术运算

```c
/*
+ - * / 分贝对应加减乘除
	/ 当double 与 int 相除时，最后的结果默认会转为int 
% 取余
++ 自增
	i++ 先返回i再自增
	++i 先自增i再返回
-- 自减
	与自增同理
*/
```

### 关系运算

```cpp
/*
> >= < <= 字面意思
== 等于比较
!= 不等于判断
*/
```

### 逻辑运算

```cpp
/*
&& 与 and
|| 或 or
! 非 not
*/
```

### 条件运算

c语言唯一的三目运算，`(a?b:c)`，当a为真的时候，执行b，反之执行c 

### 位运算符

```cpp
/*
<< 左移
>> 右移
& 按位与
| 按位或
^ 按位非
~ 按位异或
*/
```

### 赋值运算

`=`，可以结合其余的算术操作，如`+=` 

## typedef

给一个复杂的结构体另起别名

```cpp
//typedef 类型名 新名字;
typedef long long LL;
```

# 流程控制

## if

 ```c
//如果不加大括号，则执行if下的第一句

//多分支，else if 可以翻译为“又如果”
if (条件A)
	{...}
else if (条件B)
	{...}
else if (条件C)
	{...}
else
	{...}
 ```

## switch

```c
switch（表达式）
{
case 常量表达式1:
   //do case 子模块不用加{} 
   break; //结束当前的case子句
case 常量表达式2:
    ...
    break;
default :
    //

}
```

## while

```c
//while循环

while(条件A)
{
	//do something
}


//do while循环循环无论如何会先执行循环体一次

do
{
    //do something
}
while (条件A)
```

## for

```c++
//在C语言中，不允许在for循环中定义变量，如`for(int i=0;i<100;i++)`而在C++这是允许的 

for(i=0;i<100;i++)
{
	printf(i);
    //break;
    //continue;
}
```



## 输入输出

### scanf printf

```c++
//scanf 以回车结束输入 
scanf('格式控制符',&变量名); //非数组变量
scanf('格式控制符',数组变量名); //数组变量

printf('%d',a)
```

**scanf从输入流中取数据，捕获到合适的字符赋值给足够的变量，然后结束执行，否则阻塞等待。**对于非`%c`字符，scanf会忽略所有空白符，包括回车、换行、制表符等。对于`%c`字符，则总是将输入流中的第一个字符返回。

```c++
// 分作4行输入4个整数

int a,b,c,d;
scanf("%d%d%d%d",&a,&b,&c,&d); //1\n2\n3\n4 ，理解scanf的原理
printf("%d %d %d %d",a,b,c,d)
```







* `getchar`：获取一个字符，`a=getchar()`，也可以单独使用用来吸收空格
* `putchar`：`putchar(变量名)`，打印字符变量
* `gets`： `gets(数组名)`，获取字符串到数组，以空格、回车结束
* `puts`：`puts(数组名)`，将字符串输出到屏幕
* `sscanf`： `sscanf(字符串,格式控制符，变量)`，理解为string+scanf，将字符串变量以格式控制符的要求写入到变量

### getchar putcahar

* getchar：获取单个字符
* putchar：输出单个字符

### cin cout

```c++
#include <iostream>;
using namespace std;

int a,b;

//cin 会剥离输入中的空格
cin>>a >>b ; //把输入流移进变量
cout<<a << b<<endl ; //endl表示回车
```



# 函数

## 声明

c语言不允许函数嵌套定义 。

```cpp
//返回类型 函数名(变量类型 参数1,...)
void Myfunction(int a,double c){
    //do 
}

// 形式参数是个数组
// 二维数组的第2维要写出
void func(int a[],int b[][5]);
    
//形式参数引用变量
void func(int &x);
```



## 参数

* 实参和形参： **除了数组（指针）是地址传递以外**，其余变量类型均是值传递，在函数中的修改不会影响其原有的值。

* 引用：在函数声明时，变量类型后或者变量名前加上`&`表示引用，**相当于地址传递**。如`void Myfunction(int &a)`。习惯上，将`&`放在变量名前（指针的`*`则放在变量名后面）

  * `&`在**非函数声明场合则表示取变量地址**



## 数学函数

 需要包含头文件`#include <cmath>`

* 绝对值： `fabs(double x)`，对doule类型取绝对值
* 取整： `floor(double x)`，向下取整；`ceil(double x)`，向上取整；
* 四舍五入：`round(double x)`，四舍五入取浮点数，返回类型为double，要进行取整int()
* 幂次：`pow(double r,double p)`，计算r^p
* 平方根：`sqrt(double x)`，返回算术平方根
* 对数：`log(double x)`，计算以 **自然对数e**为底的对数，使用换底公式
* 三角函数：`sin/cos/tan/asin/acos/atan`

## 指针
指针，**存放变量地址**的一种变量类型，本质是` unsigned int`类型。



声明时，**`*`号作为变量类型的一部分，**放在类型后或者变量名前都是可以的，**习惯放在变量类型后**。如果一行有多个变量，**`*`只会和第一个变量结合。**

```cpp
int* p; //定义一个int类型的指针
int *p1,*p2,*p3; //多个变量要在每个变量前加上*
```


在非声明场合，`*指针名`表示引用指针，获得指针所指地址的变量。

指针支持加减运算，如`p+i`表示指针向后偏移i个单位地址，**单位取决于指针的类型**。如`int *a`，每次偏移的单位是一个int，4字节。自减同理。

对于数组， 数组名就是指针地址，即`&a[0]==a`。

```cpp
int a[10]={0};
for(int i=0;i<10;i++){ 
    printf("%d\n", *(a+i)); //引用
}
```




| 符号 | 作用                                   |
| ---- | -------------------------------------- |
| &    | 取地址，&变量名                        |
| &    | 引用，在函数声明时，`变量类型 &变量名` |
| \*   | 引用，\*指针变量                       |
| \*   | 表示该变量是指针，`变量类型 *变量名`   |

## 传值传址

传值、传址，发生在函数调用，实参赋值给形参的一种方法。

* 传值：实参拷贝一份内存副本，赋值给形参。**函数内部对形参的修改对实参无效。**
* 传址：实参的地址拷贝给形参，两个参数指向同一处内存。**函数内部对形参的修改会同步到实参。**

c中，除了传数组默认是传址外，其余变量类型都是传值。**要想实现传址，可以借助**：

1. 指针
2. [引用](##引用)

```cpp
//交换两个变量
void swap(double* a,double* b){
	double tmp;
	tmp=*a;*a=*b;*b=tmp;
}

int main(){
	double a=1,b=2;
	swap(&a,&b);
	printf("a:%.2lf, b:%.2lf",a,b );
}
```

## 引用

引用，是c++的语法，**对变量另取别名，传递过程中，不产生副本**，函数中，**对引用变量的操作就是对原变量的操作。**

创建引用，只需要在函数声明时，在变量类型后加上`&`即可。

```cpp
//void func(变量类型& 变量名);

// 借助引用实现交换两个数
void swap(double& a,double& b){
	double tmp;
	tmp=a;a=b;b=tmp;
}

int main(){
	double a=1,b=2;
	swap(a,b);
	printf("a:%.2lf, b:%.2lf",a,b );
}
```

# 结构体

struct，将不同的数据类型、函数封装到一起的数据结构。

## 创建

结构体创建

```cpp
struct name{
    //一些基本的数据结构 
}
```



一个学生信息的结构体示例

```cpp
struct studentInfo
{
	int id;
	char gender; 
	char name[20];
	char major[20];

	studentInfo* next; // 指向下一个同学
} Alice,Bob,stu[1000]; //同时创建变量 

```



使用`stuct.name`来访问结构体的元素。当成员变量是指针时，使用`struct.pointer->name`来获取指针指向结构体的变量。

```cpp
struct studentInfo
{
	char gender; 
	char name[20];

	studentInfo* next; // 指向下一个同学
} Alice,Bob,stu[1000],*p;


int main(){
	strcpy(Alice.name,"Alice");
	strcpy(Bob.name,"Bob");

	Alice.next=&Bob; //指向bob

	printf("alice's name :%s\nnext's name:%s\n",Alice.name,Alice.next->name );
	
}
```



## 初始化

结构体默认存在一个构造函数（但不可见），与结构体的同名，用来初始化结构体变量，正是因为它的存在，才允许我们直接为结构体的变量赋值。

当然，我们也可以自定义构造函数，要求：**“与结构体同名，但无需声明返回类型“**。

构造函数的初始化参数个数、类型不同，即被认为是不同的构造函数。可以实现多个构造函数来应对不同的使用场景。

```cpp
struct node{
    int x,y;
    node(){};  //无任何参数的构造
    node(int _x,int _y){}; //带有坐标点的构造
}
```



一个二维坐标点初始化的例子

```cpp
#include <cstdio>
#include <iostream>
#include <cstring>
using namespace std;

 struct Point
{	
	int x,y;

	Point(){} //无任何参数下的构造

	Point(int _x,int _y){x=_x;y=_y;} //带参数的构造

};


int main(){
	Point pt[10];
	int num=0;
	for(int i=1;i<=3;i++){
		for(int j=1;j<=3;j++){
			pt[num++]=Point(i,j);
		}
	}
	
	for(int i=0;i<num;i++){
		printf("%d , %d\n",pt[i].x,pt[i].y );
	}
	
}
```

# 补充

## 浮点数比较

由于计算机采用有限的二进制编码，因此浮点数在计算机中的存储并不总是精确的，例如，3.14在实际存储过程中，可能变为`3.14000001`。这种情况需要引入一个极小数eps来使逻辑判断`==`、`!=`正常运作。

```cpp
#include <cstdio>
#include <cmath>

const double eps=1e-8;
const double pi=acos(-1);

// [b-eps,b+eps] 这段范围都看做是b
#define Equ(a,b) ( (fabs( (a)-(b) ))<(eps) )  
#define More(a,b) ( ((a)-(b))>(eps)   // a>b+eps
#define Less(a,b) ( ((a)-(b))<(-eps) ) // a<b-eps
#define MoreEqu(a,b) ( ((a)-(b))>(-eps))  //a>b-eps
#define LessEqu(a,b) ( ((a)-(b))<(eps) )  //a<b+eps

int main(){
	double db1=4*asin(sqrt(2)/2);
	double db2=3*asin(sqrt(3)/2);

	printf("db1==db2:%d\n",db1==db2 ); //0
	printf("use Equ\n" );
	if(Equ(db1,db2)) {
		printf("true"); //返回true
	}
	else{
		printf("false" );
	}
}

```

## 黑盒测试

### 单点测试

单点测试，**程序只需要按照正常的逻辑执行一次即可**。程序的写法是一次性写法，只要能够完整处理一组输入数据。

### 多点测试

与单点测试相比，多点测试要求程序能一次运行所有数据**。因此，程序的核心代码应当被一个循环包裹。**同时，多点测试的一些变量如sum、ctr等，应该在每次循环时重置为初始状态。

### 输入数据

* while eof类型

  题目没有明确给定输入的结束条件，就是默认读取到文件末尾。利用`scanf`的返回值来判断，当达到文件末尾时，`scanf`无法捕获足够数量的变量，会返回-1，C中用`EOF`来代表这个-1。

  ```cpp
  while (scanf("%d",&n) !=EOF ){
      // do
  }
  ```

  当在命令行里执行时，scanf是不会遇到EOF的。可以手动输入`ctrl+Z`来发送eof。

* while break类型

  是`while eof`的延伸，以一种特殊的数据格式来表示输入结束。

  ```cpp
  while (scanf("%d",&n) !=EOF ){
      if(a==0 && b==0) break; //结束条件
  }
  ```

* while(T--) 类型

  题目明确告诉了数据有多少组

  ```cpp
  while(T--){
      //do
  }
  ```

### 输出格式

* 正常的连续输出，每行一组数据

* 每组数据之间添加额外的空行

  ```cpp
  while (scanf("%d",&n) !=EOF )
  {   
      printf("正常数据\n");
      printf("\n");
  }
  ```

* 每组数据之间添加额外的空行 ，但是最后一组数据无空行（题目一般会明确有几行数据）

  ```cpp
  //判断是否是最后一组即可
  while (T-- )
  {   
      printf("正常数据\n");
      if(T>0){}
      	printf("\n");
  }
  ```

  