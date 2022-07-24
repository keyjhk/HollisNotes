---
typora-copy-images-to: upload
---



[toc]

# 关于python

[python官方文档](https://docs.python.org/zh-cn/3.6/) 

解释/编译：Python是一门解释型的跨平台语言，速度没有编译型语言快。**但并不完全是解释型语言**，解释器会先编译程序生成pyc文件，下次解释的时候就会快很多。

```python
#py文件编码格式声明：只要符合正则表达式的规则即可，以#开头

#_*_coding:utf-8_*_
#coding=utf-8
```



## pip

pip ：python的包管理工具，**可以用pip --version查看是否安装。**

```shell
pip install -r 文本    #安装指定文本中的包
pip --default-timeout=100 install #更改等待时延
pip install -i  网址    #安装指定网址的包
pip uninstall      #卸载软件包
pip freeze >requirements.txt      #导出系统已安装的包到文本中
pip list     #列出当前系统的安装包
```

本地包的安装：`python setup.py install` 

## python和Microsoft Visual C++

在windows环境下，python需要调用Microsoft Visual C++ compiler编译器，尤其是在安装第三方包时候，会build项目，这时如果没有安装或者安装不协调的c++构建工具就会报错。 

![image-20210124195825720](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/cpython%E4%B8%8Ems%E7%89%88%E6%9C%AC.png)

安装c++ build tool，网上给出了多种方式：

1、直接安装微软的visual studio 2015以及以上版本。

2、不安装vs2015（以上），直接安装相应的build tools。

3、直接安装c++2015 build tool的standlone版本。



# 基础语法

## 用户交互

* 获取输入：`input(提示信息)`，返回一个str字符串。注意，`input`实际是去取最后存入标准输入缓冲的数据，忽略最后的回车。并不是执行input后才能输入，也不是动态获取屏幕的输入。其效果等价于`sys.stdin.readline().strip() `

* 退出程序：exit('提示字符')，退出程序，会打印提示字符在屏幕上。exit的退出值可以用于自动化测试脚本返回不同结果。

```python
#打印进度条
import time as t
for x in range(20):
   t.sleep(0.5)
   print('\r'+'loading:'+'#'*x,end='')	#\r表示回到本行行首，实现覆盖打印
```



## 流程控制

while循环

```python
while True:
    pass
else:	# while循环正常结束，会走到else分支 
    pass
```

for循环
* 循环跳出：`continue;break` 
* 迭代对象：`range()`对象；enumrate对象（穷举）；

```python
#for 简单使用
for i in range(10): 
    pass

for i in range(9,0,-1)	#逆序输出


for i,j  in enumerate(['a','b','c']) #生成 (0,'a'),(1,'b')

# for else
for i in range(10,-1,-3):
    print(i)
else:
    # for循环结束后，会执行此处	
	pass
```



if-elif-else 

```python
#基本使用
if ():
    pass
elif:
    pass
else:
    pass

#三元语法下的if else使用
a=x  if x <y else y 	#若x<y，a=x，否则a=y 

# 多个条件跨行书写
#方法1,用小括号 
if (a and b
    c and d
    e and f):

#方法2   ，用反斜杆
if(a and\
  b)
```

## 运算符

* 四则运算：
* 加法：整数算数相加； 字符串前后相连； 列表前后相连；
  * 除法： /是真正的除法，//称作地板除法，相当于C语言里的int类型数据除法
  * 乘法：整数相乘 ；列表/字符串自身复制
* 幂运算：`a**(b)`，等效于$a^b$ 
* 求余运算：%，另有内置函数`divmod(x,y)`，返回元组`x//Y,x%y`
* 逻辑操作：and/not/or。**逻辑操作不会返回真假(true/false)，会返回为真的对象。**

*  位运算符：&：与运算；|：或运算；^：异或运算；>>n，右移n位；<<n，左移n位 。 

  * `bin(num)`：显示1个数的2进制，省略多余的0（pyhthon中的int没有位数限制），以1开头。但是对于负数，将显示为`-obxx`，前面添加负号，后面为正数，相当于原码形式，非补码形式。

  计算1个数的2进制含有多少个1：计算机以补码形式存储数，当进行与`&`运算时，自动按照补码的形式位扩展（《计算机组成原理》），利用此点，可以快速统计1个数（无论正负）在计算机中的二进制中有多少个1，如`bin(num&0xffff).count('1')` ，就是计算1个64位数有多少个1。



连续操作：**Python支持多个运算符之间的连续操作**，如`dict['func'](x,y,z)`



## 变量

### 变量类型

可以使用`type(obj)`获取数据类型 

* int型：不限位数，自动扩展。可以转换字符串到int，支持空0，如`int('5')==int('0005')`

* float：最对存储17位有效数，超过则丢失精度，会自动使用科学计数法`xe+y`=$x*10^y$ ，+号不允许省略。

* bool：if等语句会自动触发逻辑测试。

  * int：1是True，0是False。python中用关键字`True/False`对其替换。如(3<4)==1将会返回True
  * ==（!=）：判断值相等（不相等）
  * is：判判断两个对象内存地址是否相同（又称完全一样）。单独查看变量地址，可用`id(变量)`查看 
  * 不等式判断：python里，可以像平时书写那样**连写不等式**，如3<x<5，就表示`x>3&&x<5`。

* None对象：None虽然名字叫做None，但是却实际存在，在内存中占据空间，一般用作占位，相当于c语言的null。注意，`None!=False` 

* 进制：

  * `bin(int十进制数)`，返回一个字符串，为2进制下的数
  * `hex(int十进制数)`，返回一个字符串，为16进制下的数。格式控制为`%#x`（#表示显示0x，可省略，下同）
  * `oct(int十进制数)`，返回一个字符串，为8进制下的数。格式控制为`%#o`
  * `int(有效的字符串)`，字符串对应的进制，返回一个10进制整数，格式控制为`%d`

  

### 标签机制


在python中，**变量名只是作为标签贴在变量的实际内存中**，方便识别，类似于c语言中的指针。**对于原地可修改变量**，list、set、dict，**修改变量时就在原内存中直接进行。而对于不可原地修改变量**，tuple、str、int、float等，修改变量时，**python会另外开辟一个内存空间，该标签会重新指向该内存地址**，原内存失去该变量的引用。

在为变量赋值时，如`b=a`，**b实际是拷贝了a的引用，并没有拷贝a数据的副本，b和a实际指向的是同一处内存地址**（其实就是[浅拷贝与深拷贝](##列表)的问题）。所以，应当留心a所指向的变量类型，如果a是内存可变类型，a对内存的修改对b就会可见。

当一个变量的引用计数为0时（没有变量名指向该内存），Python会自动回收该内存。引用计数会在赋值`a=b`、传参`func(a)`（实际上也是赋值）时增加，相应地，会在变量名指向别处、函数退出时较少。

```python
#不可变类型 原地不可修改 地址发生变更
a=10
print("a的地址为",id(a))  #a指定地址1
a=11
print("a的地址为",id(a))  #a指向新的地址2，原地址1失去1个引用

#可变类型 原地可修改 地址不变
n=[1,2,3]
print("n的地址为",id(n))  #n指定地址1
n.append(4)
print("n的地址为",id(n))  #n依旧指向地址1，不变，可以原地修改

n=[4,5,6]  #这是重新赋值，并不是原地修改，n会指向新的地址2,原来的n地址不同 


'''变量赋值'''
#不可变类型的变量赋值
a=1
b=a	#b指向了内存1	b=a=1 #这种写法等价
print(a,b,id(a)==id(b))	#1 1 True
a=2
print(a,b,id(a)==id(b))	#2 1 False

#可变类型的变量赋值
a=[1]
b=a
print(a,b,id(a)==id(b))	#[1] [1] True
a.append(2)
print(a,b,id(a)==id(b))	#[1,2] [1,2] True
```



### 作用域

变量的访问顺序：LEGB

* L=local，表示本地变量，在def函数内部，函数结束后变量就被销毁
* E=enclosure，闭包，多用于[函数式编程](##匿名函数与内置函数)
* G=global，表示全局变量。函数内部可以访问，**但是试图修改原地不可变类型时时，函数会默认创建一个同名的本地变量**
* B=built-in，表示Python的内置变量，如`__main__`，`__filename_`'等



### 变量标识

* global：在def函数内部声明，表示变量为全局变量，可以直接对全局变量进行修改
* nonlocal：在嵌套函数内部，表示变量为上一层函数的变量，可以直接修改

```python
# 全局变量，整型x，原地可变类型类表n
x = 5
n = []


def f1():
    global x # 将允许修改全局x
    x = 10
    n.append(1)


def f2():
    y = 4

    def f3():
        nonlocal y # 将允许修改闭包变量 y
        y = 10

    f3()
    print(y) #10


if __name__ == '__main__':
    f1()
    print(x, n)  # 10,[1]
    f2()  

```



# 序列

## 序列的通用方法

* `len（obj）`：获取序列大小：
* `type(obj)`：获取数据类型
* `sum(obj，[,开始位置])`：序列元素求和
* `max、min`：求最大值、最小值。若是字典，则只对键排序
* `sorted(obj,[key=func,reverse=False])`：返回一个新的序列，默认从小到大升序排列。可以指定`key=func`关键字，自定义排序规则。
  * `functools.cmp_to_key`：python3取消看了python2中sorted函数的cmp关键字参数，使用`key=cmp_to_key(myfunc)`转换到key关键字参数。查看python的文档可知，cmp函数接收`sorted`传入的两个比较对象x、y，函数内定义自己的升降序规则，`return -1 if (x在y前面的条件) else 1`  

```python
"""
A comparison function is any callable that accept two arguments, compares them, and returns a negative number for less-than, zero for equality, or a positive number for greater-than. A key function is a callable that accepts one argument and returns another value to be used as the sort key
"""

from functools import cmp_to_key

def cmp(x,y):
    #绝对值小的在在前面
    return -1 if abs(x)<abs(y) else 1	
sorted(student_tuples,key=cmp_to_key(cmp)) 
```



## 列表

### 常用操作



* 访问：`list[index]`。index为负数时，表示访问倒数第index个数。**列表可以容纳任何类型元素的数据**。

* 创建：使用`[]`、`list(obj)`、列表推导式。

  列表推导式用于快速地生成列表，语法` [元素表达式 if(条件) pass else pass for 变量 in 迭代对象 ]` 

```python
#简单使用
a=[x for x in range(10)]
#2个for循环，外层for-内层for，相当于语句放在了最前面
a=[i*j for i in range(10) for j in range(i)]	
a=[j for x in a for j in x]	#2维列表转1维列表

#只有if时
a=[x for x in range(10) if x%2==0] #将只会筛选偶数

#if-else的三元表达式
a=[x  if x%2==0 else x**2 for x  in range(10)]
```



* 分片：`list[start:end:step]`，步长可省略，**分片所得是一份浅拷贝的副本，只拷贝第一层**。

  列表/元组的边界 

  * 索引时，不能超出列表的上限，否则报错
  * 分片时，**边界值会被自动处理，当超出列表范围时，会被自动缩放到列表的上限**，如一个5个元素的列表，a[-100:100]和a[:]是一样的。分片的起始序号一定小于终止序号，否则返回空的列表，如`a[-1:-4]=[]` 

* 反转：（1）a.reverse()，原地反转（2）`a=a[::-1]` 
* 算术运算：（1）list1+ list2会返回一个临时列表，该列表是两者的集合 (2)，list*次数，返回一个临时列表，该列表是自身复制相应次数后的扩展
* **元素的添加：**
  * `.append(元素)`，在列表尾部添加该元素
  * `.extend(列表)`，在列表之后补上一段列表，使两个列表合二为一
  * `.insert(位置,元素)`，在目标位置上插入元素，插入元素在目标位置之前，即原位置的元素会往后挪动
* 元素的删除：
  * `.remove(元素)`：会删除列表中第一个匹配到的对象
  * `.pop(位置)`：如果位置参数缺省，就会弹出最后一个元素。支持负数索引
  * `del list[位置]` 、`del list[s:e]`：删除对应位置的元素或者分片。注意，`del l[:]`是删除整个列表的内容，l最后成为一个空的列表。`del l`是删除变量l对内存的应用，变量l不复存在



其他函数：

* `.count(元素)`：计算该元素在列表中出现的次数
* `.index(元素)`：返回该元素在搜索范围内第一次出现的位置
* `.sort(func,key,reverse)`：排序，reverse=true时会从打到小排序
* `in/not in `：判断元素是否出现在列表中



### 深浅拷贝

列表属于原地可变类型，在内存中，赋值`l1=l2`、分片拷贝`[:]`还是`ls.copy()`都只能**复制第一层**。如果是列表套列表，里面的那个列表就不会作为副本拷贝（只拷贝了地址）。

```python
b=[[1,2],3]
c=b[:]
c[0].append(10)
print(a) # [[1, 2, 10], 3]
# 还有1种类似的情况 就是列表的*运算
a=[[]*10] # 改动a[0]其他几个也会跟着变 
```



使用`copy`模块进行深拷贝。**浅拷贝的问题存在于原地可变变量，此处只是以列表举例。**

```python
import copy
d=copy.deepcopy(b)
```



## 元组

常用操作：

* 创建：**用","分隔元素。小括号的形式不是必须的**

* 访问：和列表相同，采用中括号[]

* 修改：不允许变量地址发生变化。换言之，原地不可变类型不允许修改，如果中间含有元素是原地可变类型，如列表、字典，他们是可以修改的。

  ```python
  In [1]: a=([1,],2)
  
  In [2]: a[0].append(3)
  
  In [3]: a
  Out[3]: ([1, 3], 2)
  ```

  

## 字符串

### 常用操作

* 创建：双引号、单引号、三引号都可以。其中三引号包裹的字符串为所见即所得。
* 访问：和列表相同，采用中括号[]
* 比较：两个字符串比较为ASCII码逐个字符比较。ex："1.1.9"<"1.1.11"，



原生字符串r：禁止字符串里的转移字符`\`生效，所见即所得。如`r"C:/key/temp"`等效与`"C://key//temp`  



常用函数：**字符串不能原地修改，所以返回的是副本**（区别于列表的返回None）

* `.ascii_letters`：返回一串字符串，字母表的大小写
* `.digits`：返回一串字符串，为0-9数字，
* `.capitalize()`：大写第一个字母，对于不可大写字母，如数字、符号，不会报错，将原样返回
* `.title()`：将每个单词的首字母大写
* `.swapcase()`：将单词中的大小写互换
* `.center(l,char)`：字符串居中，同时使用char填充至l长度 
* `ljust(width,[char=,])、rjust(width,[char=,])`：字符串以指定宽度左对齐、右对齐，多余部分填充char字符，默认为空格。
* `.upper()`、`.lower()`：转换成大写/小写
* `.isupper()`、`.islower()`：是否只包含大小写（允许包含数字）
* `.isalpha()`：是否只包含字母
* `.isalnum()`：是否只含数字和字母
* `isdigit()`：是否是数字 
* `.startswith('str')`、`endswith('str')`：字符是否以str为前缀或后缀
* `.strip(x)`、`.lstrip(x)`、`.rstrip(x)`：左右剥夺x字符，缺省时默认剥夺空格
* `.index(sub)、.rindex(sub)`：分别从左、右开始查询子串位置，返回（从左开始计数的）索引号，若不存在子串，报错。
* `.find(sub,satrt,end)`：查找子串在str里的位置，若无，将会返回-1 
* `.split(分隔符，分隔次数)`：以指定分隔符分割字符串 ，缺省时默认为空格、回车、制表符 
* `'char'.join(iterate)`：其中每个迭代对象**必须为str类型**，否则会报错。可以是一个字符串，如`'-'.join('apple')` 
* `.replace(old,new [,num])`：替换旧的字符串为新的字符串，不超过num次 



其他：

* `eval()`：将用户的输入作为python里的合法语句。但是不安全，容易被注入攻击，如执行`eaval('rm -rf /')` 

****

### 字符串格式化

* 格式化操作符：`"%d %s" % (变量1,变量2)`

  ```python
  #常见格式控制符：
  %d，整数	%o，八进制	%x，十六进制
  %s，字符串
  %c，字符
  
  
  #常见**辅助**格式化操作符：
  -，结果左对齐
  \#，在八进制数前面显示0o，在十六进制数前面显示“0x
  ```
  
  


  * `format()`：官方推荐，灵活多变，一个变量可以使用多次，并且支持索引等操作。

    * 位置顺序填入：`"{0} love {1} ".formate(str1,str2)`，大括号里的数字若缺省，则按顺序依次填入。另外，若想打印`{}`，则需转义，再写一个大括号`{{}}`。

    * 关键字替换：使用用法类似关键字参数，**支持容器索引、类属性调用**等。

      ```python
      #关键字替换 format实例
      name='link'
      names=['jiang','hui']
      print("{name} {names[0]} {names[1]}".format(name=name,names=names)) 
      
      ```

format格式控制符：与`%`的形式相似，但代之 以`:` 

```python
#format 对齐方式，看不等号指向 
{:10d}  #右对齐> (默认, 宽度为10)
{:<10d} #左对齐 (宽度为10)
{:^10d} #中间对齐 (宽度为10)
{:.2f} #保留2位结果的浮点数。
```



字符串的颜色替换：`"\033[显示设置;字体颜色设置;背景颜色设置m 输入的字符串 \033[0m"`  ；（常见字体颜色32绿色31红色），如`"\033[0;31;0m 输入的字符串 \033[0m"` 



### 字符编码

* ord与chr：`ord('str')`：显示字符的ASCII码（ASCII码表中大写字母+32=小写字母）
* `chr(num)`：转换ASCII码到对应的字符

python3中默认编码为unicode，ord支持汉字，chr支持超过255的数。而python2默认编码为ASCII，即ord/chr只支持ASCII码表上的东西。



各类编码：

* unicode：万国码。[unicode与uft8关系详解](https://www.zhihu.com/question/23374078)
* ASCII：1字节，实际用到的只有7位，0-127。
* latin-1：1字节，8位，0-255。
* unicode：4字节。万国码，因为冗余存储，所以有变长码utf-8。
* utf-8：对于简单的ASCII，用1字节存储。对于超出1字节的，用3字节存储。



**计算机对字符串的存储：**按照对应的编码格式，**将字符串存为字节流**，即0101比特流。用文本编辑器打开文件时，文件会自动转码（解码），将二进制字节转为字符串显示。

* 乱码：（1）找不到映射关系。例如，同样地对4个字节解码，GBK以2个字节为单位去映射码表，ASCII以1个字节为单位去映射，映射结果自然不同，甚至出错。（2）在使用二进制模式读取文件时，移动文件指针到不合适的位置并尝试解码，假设有一文本末尾为`芒\n`，占据3+1=4个字节，若`f.seek(-2,1);f.read()`，则汉字的最后1个字节和\n结合，此时解码自然报错。 



**字符编码encode与二进制解码decode：**在**python3**中，字符串str到二进制码bytes是编码`str.encode('编码格式')`，进制码bytes转为字符串str是解码`binary.decode('编码格式')`**。两者是不同类型，不能进行字符串拼接相加，如`'ab'+b'cd'`会报错。** 





## 字典

常用操作：

* 创建：
  * 空字典声明：`a={}`。a[key]=val。如果key不存在就创建，存在就覆盖原有的值。效率较高 
  * `dict()`：使用`dict`实例化
    * `dict( [(,),(,),(,)] )`。列表元素为2元组。dict（）会将每个2元组作为键值对进行创建，如`dict(dict.items())` 
    * `dict(zip(...))`，将zip对象变成字典，和上一种方法类似，只不过上一种用列表包裹形如`(x,y)`的元素，而本方法由zip对象包裹，如`dict(zip(range(4),'ABCD'))` ，将会返回`{0: 'C', 1: 'M', 2: 'E', 3: 'A'}` 
    * `dict()`：创建一个空字典
* 迭代：**默认迭代会对字典的键迭代**，可以使用`dict.keys();dict.values();dict.items()`分别对值/键值对同时进行迭代。在字典迭代时，不允许增删改键值对。

```python
#对键进行迭代，等效于for key in a.keys()
for key in a:
#对值进行迭代
for val in a.values():
#对键值同时进行迭代
for k,v in a.items()
```

* 判断是否存在某个键：`str in/not in dict `

* 快速创建键值对：dic.fromkeys(键列表,值)，其中列表里所有的键都会映射到同一个值上。**如果是列表或者字典，将会指向内存中的同一个列表，而非拷贝**。字典的值可以是一个函数
* 获取字典的键/值/键值对：`dic.keys()`，`dic.values()`，`dic.items()`分别返回键列表，值列表，迭代对象列表
* 安全地访问字典：`dic.get(键)`，当键不存在却试图访问的时候**不会报错**，会返回一个None。
* 清空字典：`dict.clear()`，将字典回收到内存。直接复制空的字典是不能清除内存的，如a=b=dict1，当a={}，a只是指向到了一个新的字典，内存里的字典没有被真正销毁。b依然可以被访问到。`.clear()`方法对原地可修改类型`list、set、dict`均适用。
  
  * clear 与del 区别：clear不会删除变量，只是对变量指向空间内容清楚，变量依旧可以访问。而del 则是删除该变量名（**但内存可能依旧存在**），此后不可以该变量名访问。
* 复制字典：`dic.copy()`，返回字典的副本
* 更新字典：`dic1.update(dict2)`，重复的会覆盖，没有的会创建。原地更改，返回None
* 删除键值对：`del dic[key] ` 或 `dic.pop(key)` 

  



自定义哈希函数实现字符串映射：ELF哈希，字符串作为key 。（[原理解释](https://www.cnblogs.com/eagling/articles/4848249.html)）


```python
MAXSIZE=1000	#哈希表长度自定义为1000
def elf_hash(str_value):
    h = g = 0
    for i in str_value:
        h = (h << 4) + ord(i)
        g = h & 0xf0000000
        if g:
            h ^= g >> 24
        h &= ~g
    return h % MAX_SIZE
```



## 集合

常用操作：

* 创建：set()。Python2中，a={}表示集合，Python3中，a={}表示空字典，要声明集合为set({})。
* 访问：集合是无序的，不能用索引进行访问。但可以进行迭代，使用`in`运算符。
* 集合的运算(**返回新的集合，原集合不受影响**)：
  * 交：set1.intersection(set2)==set1&set2，取两个集合的交集。
  * 并：set1.union(set2)==set1|set2，取两个集合的并集
  * 差：set1.difference(set2)==set1-set2，取两个集合的差集。差集即是A有B没有的元素。
* 元素的增加/删除：`set.add(val)`，`set.update(set)`；`set.remove()`
* 不可变集合/禁锢集合：`set=fonzenset(set)`

# 文件存储

## 文件对象

`open(文件路径,mode='r',encoding=None)`，返回文件对象 

* `f=open(文件路径,打开模式)`，使用这个方法创建的文件对象，务必记得要和close匹配。

* with语句：with会自动帮你关闭文件。在Python2.7以后支持with后面打开多个文件对象。

  ```python
  with open('文件路径','r') as f1:
      pass
  ```
  
  
  
  若是一个对象实现了上下文管理器，就可以使用with优雅地开关。
  
  ```python
  #上下文管理器方法1： 实现enter和exit魔法方法
  class MyFile:	#with语句调用时
      def __enter__(self):
  		return self.file	#返回IO对象
      def __exit__(self):	#with离开时
          f.close()	#关闭文件
  
  ```



文件对象的操作方法：

* `f.read([n])`：以字符为单位读取**n个字符**，如果缺省，则读取全文为一个字符串，带换行符。注意，**是字符，而不是字节**，汉字被当做1个字符，`\r\n`也被当做1个字符。
* `f.readline(n)`：移动指针，每次读取一行（的n个**字符**），效果等同于遍历`f.readlines() `。
* `f.readlines()`：按行读取并生成列表，一次性读取文本到内存，**当文件过大时，会大量耗费内存资源，不推荐使用。**
* `for each in f`：逐行迭代文本
* `f.seek(off,from=0)`：文件指针从from处偏移off个字节。**from=0表示文本头部，1表示文本尾部，2表示当前位置**。此参数默认值为0。
* `f.tell()`：文件指针，以字符为单位，返回自己所处的位置。
* `f.writelines(list[])`：将列表写入文本，列表的每个元素都要求字符串形式，换行符需要自己添加。即它的效果等同于`f.write(''.join(list))`
* `f.write(str)`：写入str对象到文本 （不会创建空格）

****

文本IO应用 

删除/修改文本中的某一行：（1）小文件读写：将文本先`readlines`以列表的形式读取到内存，再进行ls.pop(指定行)，用writelines写回文本即可。（2）大文件读写：由于readlines需要全部读取然后放到内存中，小文件则有余，大文件则时间耗费巨大。推荐的做法就是打开**两个文件**，一个是原来的文本(r)，一个是新创建的文件(w)，逐行迭代（readline），自己计数，判断是否是指定行，是进行相应的操作，否则逐行写入新文件。

```python
with open(path,'r') as f1,open(path,'r+') as f2:	#原地修改
    pass
with open(path,'r') as f1,open(path1,'w') as f2:	#一个读，一个写
```



## 打开模式

**默认以文本模式打开，以系统编码格式解码**（`sys.getdefaultencoding()`查看系统默认编码）。若其后追加`b`，表示以二进制模式打开文件，例如图片文件；

* `a `，append，追加写入，**文件指针会指向文件末尾**，如果要读取，要重新定位指针`f.seek(0)`，否则读取为空，但是写入时，依旧指向文件末尾。
* `w` ，覆盖写入，**文件指针指向开头**。在使用open创建文件对象的时候会用空文件**自动覆盖旧文件**，打开之后写入不会覆盖原先内容。
* `r `，只读打开，**文件指针指向开头**。`r+`，可读可写，**覆盖写入（不会往后推）**

在每个模式后附带的`+`，会使当前兼具读写模式。

> 假设有文本内容为 ”love python“，以不同模式写入“ha! ”
>
> | 模式 | 读取                   | 写入           |
> | ---- | ---------------------- | -------------- |
> | r+   | love python            | ha!e python    |
> | w+   | 空                     | ha!            |
> | a+   | 空（因为指针在文件尾） | love pythonha! |



CRLF(carriage return line feed，意为回车换行)，在文本模式下，**字符串的`\n`在存入硬盘时，转为`\r\n`，会多出1字节**，这是因为windows早期系统只有遇到`\r\n`时才会显示回车。Linux的LF（line feed）换行与二进制`b`存储时`\n`即是`\n`，不会多出1字节。

```python
"""比较\r\n在rb模式和r模式下的写入读取
假设有文本内容为'ha!\nhei!'以r+模式写入 

当读取模式为r+时，读取内容为，大小为8字节
ha!
hei!

当读取模式为rb+时，读取内容为，大小为9字节
b'ha!\r\nhei!'

====================================
假设有文本内容为b'ha!\nhei!'以rb+模式写入 

当读取模式为r+时，读取内容为，大小为8字节
ha!
hei!

当读取模式为r+时，读取内容为，大小为8字节
b'ha!\nhei!'
"""
```



## pickle 和json

pickle和json都企图把python里的数据类型保存到文本，**json**是轻量的数据库，很多编程语言之间可以**通用**，但不支持复杂的数据类型（比如函数地址）。**pickle是给python专用的，功能更强大**。 



`json(import json as js)`：pickle类似

* `json.dumps(序列对象)`：返回字符串
* `json.dump(序列对象，文本对象)`：将序列对象转为字符串存进文本。写入模式取决于文本对象的打开模式
* `json.loads(字符串对象)`：将字符串对象转为序列对象
* `json.load(文本对象，变量)`：将文本对象所存字符串转为序列对象赋值给变量

```python
#Pickle示例
import pickle #这是一个二进制形式的保存模块

my=[1,2,3,"test"]  #列表
pkl_file=open("E:\\test.pkl","wb")  #二进制可写文件对象

pickle.dump(my,pkl_file)   #将数据以二进制形式写到文本中
my1=pickle.load(pkl_file)  #从文本中取出并恢复2进制数据


#json示例
import json

a={'sex':'male','age':21}
f=open('test.txt','w')

json.dump(a,f)    # 将字典数据导到文本
a1=json.load(f)   # 解析文本对象
```

## OS模块

路径相关`os.path`

* `os.path.abspath(__file__)`：规范化地输出当前脚本所在目录的绝对路径。`__file__`返回的路径可能是相对路径，也可能是绝对路径。
* `os.path.basename(路径名)`：**分隔路径名**，得到一个二元组，取最后一个元素。如果是文件路径，最后的结果就是文件名。如果是目录名，最后的结果就是最后一层目录。
* `os.path.dirname(路径名)`：分隔路径名，与`basename`相对，得到一个二元组，但是取前一个元素。最后的结果就是文件目录的父目录。得到的路径可以直接用open打开
* `os.path.expanduser(路径名)`：把path中包含的"~"和"~user"转换成用户目录
* `os.path.exists(文件路径)`：判断文件路径是否存在，支持相对路径写法，返回True/False
* `os.path.isdir(路径)、os.path.isfile(路径)`：判断该路径是文件夹还是文件
* `os.path.join('路径1','路径2')`：合成路径。自动处理不同系统间文件分隔符（windows`\`与Linux`/`）的差异
* `os.getcwd()`：获取当前工作路径
* `os.chdir(路径)`：支持相对路径写法，更改工作路径。



文件相关

* `os.mkdir(文件夹)`：创建文件夹。已存在时会报错
* `os.rmdir(文件夹)`：删除空文件夹
* `os.listdir(路径)`：列出路径下的所有文件
* `os.rename('name1','name2')`：重命名文件（文件夹）
* `os.stat(文件名)`：获取文件的inode信息，随后可以获取文件的大小`.st_size`、修改时间等。inode不含文件名，文件名存储于目录表中。 

* `os.walk(绝对路径,topdown=True)`：深度优先遍历路径下的文件、文件夹，是一个生成器（generator），每次返回1个三元组`(root,dirs,files)`分别表示当前路径（字符串）、路径下文件夹（列表）、路径下文件（列表）。默认参数为`topdown=True`表示自上而下递归遍历。

```python
#深度优先，遍历指定目录下所有文件
from os import listdir
import os.path as p


def find_all_file(path):
    if not p.isdir(path):	#递归边界
        print(path)
        return

    for x in listdir(path):
        x=p.join(path,x)	#形成绝对路径
        find_all_file(x)	

path=p.abspath(input('输入路径'))
find_all_file(path)

```

```python
# 深度优先，使用os.walk自下而上删除非空文件夹（从叶节点开始往上走）
import os
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:	#必须先删除非空文件
        os.remove(os.path.join(root, name))
        for name in dirs:	#删除空文件夹
            os.rmdir(os.path.join(root, name)) 
```



# 函数

## 函数的定义和文档

函数文档：
* `help('xx')`：获取函数的长字符串，最详细的一种。
* `obj.__doc__`：获取置于对象顶部的文档。同样适用于类
* `dir(obj)`：获取对象的属性，方法。返回一个列表，相当于简略信息。同样适用于类 



定义：**函数的定义必须要在函数调用之前**。函数命名推荐使用匈牙利命名法（使用下划线，如`get_index`），变量使用小驼峰命名。

```python
def  func(参数):
   """
    此处写函数文档
   """
    pass

```

## 注解

直观地表示函数地参数类型和返回类型，方便人类阅读和IDE检查，但python本身不会做额外的工作。

```python
# 即使定义了xy为int，但运行 add(3.14,0.62) 也不会报错
def add(x: int =0, y: int ) -> int:
    return x+y
```



## 参数

* 普通（位置）参数：func(para1,para2)。按照定义时的顺序依次传入
* 关键字（传）参数：`func(key=par1)`，调用函数时，指定关键字传入
* 默认参数：定义函数的时候就为其附上初值，**但默认参数要放在最后一个位置参数之后（否则函数调用不知道跳过该值还是覆盖该值）**。
* 收集参数：`*args,**kwargs`。星号`*`的使用场景是多样的：
  1. 在函数声明时候使用分别表示非关键`*args`、关键字收集参数`**kwargs`
  2. 函数**调用时使用表示**解包（序列）**，也就是打散列表或者字典**，`myfunc(*[1,2],**{'name':'holluis'})` 
  3. 赋值时使用表示收集等号右边的多个参数，如`a,*b=1,2,3·`得到` b=[2,3]` 

```python
#函数声明 
def my(a,*arg,b=5,**arv):  #b是关键字给定参数
    print(a,arg,b,arv)
    
my(1,2,3,c=4,d=6,b=10)
#输出结果如下 可以发现 args是元组 kwargs是字典
1 (2,3) 10 {'d':6,'c':2} 
```

参数声明顺序：普通参数，非关键字收集参数（`*args`），**默认关键字参数**，关键字收集参数（`**kwargs`） 。注意，**默认关键字参数必定在非关键字参数之后，关键字收集参数要放在最后**！



函数调用传参顺序：普通参数（xx）非关键字收集参数（xx）关键字收集参数（xx）。（xx）表示此时默认参数允许在该位置，因为调用时会按名字赋值。



**参数在函数内部的修改**：python中不区分传址、传值，实际过程中**统统以传址形式**，但是**基于变量的“标签”机制**，参数修改稍有区别！对于原地可变对象，**例如列表/字典/集合等**，python将**直接修改**，函数内部修改等效于外部直接修改。对于原地不可变对象，**例如字符串/数字/元组**，python**另外创建对象**，函数内部修改对外部无效。



返回值：当不写return的时候，函数默认返回None函数可以返回多个值，这几个值在返回的时候会被打包成元组。如return x,y,z 。因为","是元组的标志，同时元组的括号可以省略。接收的时候按顺序写好元素即可为其一赋值。x,y,z=func()

## 匿名函数与内置函数

**lambda匿名函数表达式**：精简的函数表示形式，很多时候配合一些高级内置函数使用

```python
#return the address of func
func=lambada x:x**x
```

高阶内置函数

* `filter(func,iterator)`：**筛选**迭代对象中使func为True的元素，返回新的迭代对象。

* `zip(iterator1,iterator2,...)`：称作拉链函数，将多个对象一一对应集合成一个zip对象，可以迭代。

  ```python
  for  x,y in zip((1,2),('a','b')):
  	print(x,y)
  
  '''
  1 a
  2 b
  '''
  ```

  

* `map(func,iterable)`：将迭代对象中的元素依次传入func，返回map对象（可迭代）。可以使用解包方法直接得到元素，例如，输入处理中常用的`n,m=map(int,input().split())`，将输入字符串以空格分隔处理并逐个转换为Int型 。

  

## 装饰器

装饰器：不影响函数原先功能和调用的基础上，可拔插式的给函数增加一些新功能。如同装饰物，因此被称为装饰器。**本质是函数闭包，更改被修饰函数的入口地址**

### 一般装饰器

**一般装饰器函数的结构**：

```python
def decorator(func):
    def inner(*args,**kwargs):
        #do something before func
        res=func(*args,**kwargs)	#res保存原函数的执行结果，便于后续步骤返回
        #do something before func
        return res
    return inner  # 返回新的函数地址

@decorator	
def myfunc():
    pass
```

**使用`@`时发生的过程**：`myfunc=decorator(myfunc)` ，将@下一行的函数地址`myfunc`作为参数传入装饰器`decorator`，然后更改`myfunc`函数的入口地址为`inner`。inner使用收集参数来接收调用时的多个参数，并传给func。

当装饰器内不实现函数入口地址的更改（`return func `），默认就会自动返回一个None给原来的函数名，这样就会造成调用错误。

```python
#错误示例
def decorator(func):
    #返回1个非函数地址 或者 什么都不做
    #return None
    pass

@decorator
def my_func():	#my_func=None 
    pass
```

### 带参数装饰器

普通的装饰器在修饰时不允许传递参数，写法固定为`@decorator`，第一个参数就是紧跟在下一行的被修饰函数的地址。当装饰器需要带参数时，也就是希望一个功能大抵相当但稍存差异的装饰器去修饰不同函数时，其写法如下：需要3层的函数内嵌：

```python
#装饰器带参数
def decorator(args):
    def set_func(func):
        def inner(*args,**kwargs):
            #print(args)	#作用域为LEGB，当然能访问到args
            #do something before func
            res=func(*args,**kwargs)
            #do something after func
            return res
        return inner
    return set_func

@decorator('your arg')	#等效于@set_func
def my_func():
    pass
```

可以看到，装饰器在装饰时的写法发生了差异，`@decorator('your arg')`，这中间发生的过程为：

1. 执行了最外层的装饰函数`decorator('your arg')`，并接受了参数，保存在函数上下文中
2. 返回了新的函数地址`set_func`，所以，其修饰效果等效于`@set_func`，真正的装饰器是从第2层开始的。**最外层的装饰函数仅仅是为了保存上下文信息并返回一个真正的装饰函数。** 这么做的时候，最里一层的inner函数自然可以访问到个性化的参数`args`，这就是带参数的装饰器实现原理。



装饰器利用函数保存上下文信息，相比于类实例化对象来保存对象属性，更加地节省资源。



**多个装饰器修饰一个函数时的装饰顺序与执行顺序**：装饰顺序指的装饰语句的执行顺序，执行顺序指的是inner函数的执行顺序。

```python
def decorator1(func):
    #装饰语句部分，在使用@符号时就被执行的语句
    print('deco1')
    def inner(*args,**kwargs):
        #执行语句部分，只有在被修饰函数调用时才会真正执行的语句 
        print('inner1 begin...')
        res=func(*args,**kwargs)	
        print('inner1 end...')
        return res
    return inner

def decorator2(func):
    print('deco2')
    def inner(*args,**kwargs):
        print('inner2 begin...')
        res=func(*args,**kwargs)	
        print('inner2 end...')
        return res
    return inner

@decorator1
@decorator2
def my_func():
    print('hello world')
    
'''运行结果 装饰倒序，执行顺序 
deco2
deco1
inner1 begin...
inner2 begin...
hello world
inner2 end...
inner1 end...
'''
```

分析`@decorator1`的时候发生了什么：`decorator1(@decorator2)=decorator1(decorator2(myfunc) )` ，后装饰的函数先得到了执行，但函数入口的地址是从下往上逐级变更的。因为，装饰语句的执行过程为：decorator2--->decorator1，执行的顺序为inner1-->inner2--->func（入栈回弹）。

结论：**多个装饰器装饰函数时，装饰倒序，执行顺序** 

### 类装饰器

利用类的魔法方法`__call__(self,)`来实现装饰效果的一种技巧。

```python
class decorator:
    def __init__(self,func):
        self.func=func
    
    def __call__(self,*args,**kwargs):
        #do something before func
        res=self.func(*args,**kwargs)
        #do something after func
        return res
    
    
def my_func():print('hello world')

if __name__='__main__':
    my_func=decorator(my_func)	#实例化对象
    my_func()	#call函数的实现可以使得实例可以像函数一样在后面加()被调用 

```





## 迭代器

迭代器：访问数据流的一种方式，使其支持迭代。迭代器的实现依赖于对象的魔法方法`__iter__()`、`__next__()`。

迭代器区别于固化的数据流（如列表），**迭代器本身只存储对应的迭代算法，也只关注下一次迭代的值，节约内存，处理较大数据时，迭代器具备优势**。在迭代的过程中，其只能向后，不能回退。

在实现迭代器时，**`__iter__()`函数应当返回对象实例本身，`__next__()`函数返回下一次迭代的值，并设计好迭代边界和异常抛出`raise StopIteration`**。当对象用于for循环时，会隐式地触发对象的iter、next函数。

python内置函数`iter(obj)`会隐式调用对象的`__iter__`方法，`next(obj)`会隐式调用对象的`__next__()`方法。

```python
#for循环原理
iters=iter(obj)	#获得一个可迭代对象，等于iters=obj.__iter__()
while True:
    try:
        next_value=next(obj)	#获取对象本次迭代至，等于obj.__next__()
    except StopIteration:
        break 
    else:
        #do something
        pass
```

```python
#自定义列表类 
class MyList:
    def __init__(self):
        self.arr=list(range(10))
        self.len=len(self.arr)

    def __iter__(self):
        self.count=-1    #每次触发迭代器，重新复位
        return self

    def __next__(self):
        self.count += 1
        if self.count>=self.len:	#越界判断
            raise  StopIteration
        else:
            return self.arr[self.count]


if __name__ == '__main__':
    myList=MyList()
    for i in myList:print(i,end=' ')	#打印 0 1 2 3 4 5 6 7 8 9 
```

**一个对象只要实现了`__iter__()`方法，就被python认为是可迭代`Iterable`的，若同时实现`__iter__()`、`__next__()`方法就可以作为迭代器`Iterator`。**

```python
#可迭代 迭代器判断
from collections import Iterable,Iterator
tests=[[1,2],(1,2),{'a':1},{1,2}]

for test in tests:
    print('变量：{} 类型：{} 是否可迭代Iterable: {} 是否为迭代器：{}'.
          format(test,type(test),isinstance(test,Iterable),isinstance(test,Iterator)))

'''运行结果
变量：[1, 2] 类型：<class 'list'> 是否可迭代Iterable: True 是否为迭代器：False
变量：(1, 2) 类型：<class 'tuple'> 是否可迭代Iterable: True 是否为迭代器：False
变量：{'a': 1} 类型：<class 'dict'> 是否可迭代Iterable: True 是否为迭代器：False
变量：{1, 2} 类型：<class 'set'> 是否可迭代Iterable: True 是否为迭代器：False

'''
```



## 生成器

生成器：**如果将函数中的return被替换成yield，那么该函数就是一个生成器（generator）**。其迭代点就是函数`yield`处 ，**生成器在此悬挂也在此重新进入。**当函数结束时（return），生成器迭代结束。

除了上述操作外，还有一种生成生成器的办法，当列表推导式最外层的[]改为()时，返回的就是生成器，例如`y=(x for x in range(10))` 



生成器的操作：

* 悬停：`yield n`，函数悬停，向外返回n
* 唤醒：唤醒的位置在上次的yield 处
  * `g.__next__()`，恢复并取得下一次迭代值。
  * `g.send(VAL)`：恢复并向生成器传入VAL值，作为yield语句返回的结果，此时yield语句应当写作`val=yield  n`，val将被赋值VAL。同时`send`会返回生成器下一次`yield`的值。



```python
def my_iterator(times):
    ctr=1
    while ctr<=times:
        yield ctr**2	#函数在此悬挂，既是本次出口也是下一次的入口
        ctr+=1

a=my_iterator(10)
print(type(a))	#<class 'generator'>
print(a.__next__())	#1
for i in a: print(i,end=' ')	#打印4 9 16 25 36 49 64 81 100，没有从1开始，注意

a=list(my_iterator(10))	#生成器也可以固化，捕获StopIteration为止
```



## 错误和异常

```python
try:
    #任何代码块,如果出错，将会跳转到except语句执行
except Exceptions:	 #捕捉任何异常
   pass
except XX as YYY: #捕捉XX异常并创建名为YYY的变量保存   
    print("%s" % YYY)
else:	#try正常执行完毕后走else分支
    pass
finally:	#此处方式即使出错也要执行的代码
    pass
```

异常若不被捕获，便可以层层向上传递，直到main函数。若main函数也没有处理，程序才会报错。这意味着可以在主函数统一捕获异常，便于维护代码。



自定义异常：` myException=Excepion('name')`，不可被`except`捕捉，但可以自己主动抛出异常`raise myException`。自定义异常便于**复杂项目错误的快速定位**。

# 类和对象

## 创建

类的创建：`class 类名(object):`，类名命名推荐使用大驼峰命名。



对象的创建：`obj=类名()`

```python
#self参数类似于C 中的指针，在调用"."运算符的时候，会先传入实例对象。
#可以更名，但self是约定俗成。每个实例函数第一个参数都是self。

class person(object):
    def __init__(self):
        pass

p=person()	#创建person对象 
```



## 类属性与实例属性

在类顶层中赋值的变量为**类属性**，**类属性相当于静态属性，可以被所有实例共享**，以`className.xx`或`objName.xx`的形式访问，**python中当一个对象属性空间不存在该变量名时会自动去类空间搜索**。

实例属性在`__init__()`函数或其他实例函数以`self.xx`的形式声明，仅实例拥有，类不可访问。**若实例属性与类属性重名，会屏蔽类属性**。

```python
class A:
    count=10	#类属性
    def __init__(self,count=None):
        if count!=None: self.count=count	#实例属性，屏蔽类属性 

a,a1=A(),A(25) #前者是类属性，后者是实例属性
print('a.count:{} a1.count:{}'.format(a.count,a1.count))	#a.count:10 a1.count:25
```



**类、对象的相关属性**：

* `__class__`：返回对象的所属类
* `__base__`：返回类的父类



对象之间的操作：

* 对象的布尔判断：

  * `if obj`：若实例被分配了内存，if判断为True
  * `a==b`：若未实现魔法方法`__eq__`、`__neq__`方法。两个对象直接使用`==`判断，实际效果为`id(a)==id(b)` 

* 对象的引用：若有`a=b=className` ，此处变量a、b指向同一个内存对象。`del a`会删除变量名（标签a），但b的引用依旧还在。另外，**当使用原地可变变量（如列表）初始化实例时**，实例属性作为另外一个标签同样指向该变量的同一内存，**实例方法的修改对外变量也起作用**。但一般情况下，实例属性不会暴露在顶层修改。

  ```python
  class Test:
      def __init__(self,l):
          l.append(2)
  
  a=[1]	#不应该暴露在顶层 
  t=Test(a)
  print(a)	#[1,2]
  ```



## 类的相关函数

* `dir(obj)`：查看对象的所有属性，返回列表 
* `getattr(obj,'attr',default=None)`：获取对象的属性，若无且未指定default参数，报错。
* `setattr(obj,'attr',val)`：设定一个实例的属性值，该属性事先不必在实例中拥有
* `hasattr(obj,'attr')`：判断对象是否存在属性`attr`，返回`True/False` 
* `@property`：修饰符，使实例函数变为类的属性，调用函数不需要加()，因此也要求该函数不能有形式参数。
* `@staticmethod`：修饰符，定义静态函数，**类和实例都可调用，不允许访问类属性、实例属性**，但允许接收参数。多用于显示帮助信息。
* `@classmethod`：修饰符，定义类函数形如`func(cls,..)`），**类和实例都可调用**。第一参数为`cls`，类似于self，调用时自动传入对象、类的cls属性，**类函数可以访问类属性，不可访问实例属性**
* `@abstractmethod`：修饰符，定义抽象方法，需要[导入`import abc`配合`ABCMeta`使用](##抽象类 接口类)。



## 单例模式

所谓单例，**指的是一个类只能创建1个实例**。所有被创建出来的实例都是同一个内存的引用。单例模式的应用有系统回收站、音乐播放器等。

### `__new__`与`__init__`

**在类的实例化时，实际的过程**是先调用类的`__new__(cls,*args,**kwargs)`（静态）函数，主要的第一个参数是类名，分配得到内存空间（相当于C语言的`malloc`），然后`__new__(cls)`函数**返回内存的引用**作为`self`参数传递给`__init__(self)`进行初始化。`__new__(cls)`是类级别的函数，继承自基类`object`。`__init__(self)`是实例级别的函数。

### 实现单例

策略就是**让类的`__new_(cls)`函数与实例的`__init__(self)`函数只调用1次**！为了实现这一点，创建两个类属性，标记是否已分配（new函数得到执行）、是否已初始化内存（init函数得到执行），并在每次试图实例化时检查这两个属性。

```python
#单例模式
class A:
    instance=None  #是否已经分配示例
    first_init=False #是否已经初始化
    count=0 #实例个数

    count=0 #显示实例数目
    def __new__(cls, *args, **kwargs):	#类名+收集参数
        if not cls.instance:
            cls.instance=super().__new__(cls)
            cls.count+=1	#引用计数+1
        return cls.instance		#返回内存的引用

    def __init__(self,name):
        if not self.first_init:     #实例获取类属性
            print('init初始化')
            self.name=name
            self.first_init=True    #实例属性覆盖类属性


a1=A('a1')  #第一次实例对象
a2=A('a2')  #第2次实例对象，init函数不会再次初始化，所传参数实际不起作用
print('id(a1):{} id(a2):{} a1 is a2:{}'.format(id(a1),id(a2),a1 is a2))
print('a1.name:{} a2.name:{}'.format(a1.name,a2.name))
print('A的实例个数为：{}'.format(A.count))


#---------------运行结果-----------
#init初始化
#id(a1):2759332025344 id(a2):2759332025344 a1 is a2:True
#a1.name:a1 a2.name:a1
#A的实例个数为：1

```



## 继承

继承：`class 子类(父类名1,父类名2,...)`，在类名的大括号里写上父类，python支持继承多个父类

**经典类**继承和**新式类**继承：

* Python2.7中，如果不显式地继承自object（`class(object)`），则采用经典类继承。当子类调用方法时，采用深度优先的顺序搜索父类。
* Python3中，默认为新式类继承，即`class xx:=class xx(object):`，**采用广度优先的顺序搜索父类（向上水平搜索）**。
* 多继承的搜索顺序查看：`类名.__mro__`，会显示该类的继承搜索顺序 、super的父类顺序。

```python
'''
菱形继承 
	A
B		C
	D
'''
class A:
    def __init__(self):
        print('A的初始化函数被调用')

class B(A):
    def __init__(self):
        print('B的初始化函数被调用')
        # 跳转到C，注释这句对比结果 
        # 如果没有这一句 D的init方法就会选择
        super().__init__()      

class C(A):
    def __init__(self):
        print('C的初始化函数被调用')
        super().__init__()      #跳转到A 


class D(B,C):pass  #D没有自定义init，会继承父类B的init


if __name__ == '__main__':
    print('D类的继承搜索顺序为：',D.__mro__)
    d=D()

'''运行结果
D类的继承搜索顺序为： (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
B的初始化函数被调用
C的初始化函数被调用
A的初始化函数被调用
'''
```

上例中，D没有自定义init，那么它会继承父类B的init（这里没有C）。在实例化D的时候，就会自动触发`B.__init__()`函数，如果没有在B的init里调用父类的super()方法，D的初始化就到此结束，但显然，这不应该，因为D同时还继承了C，而super()的巧妙之处，就在于这种多类继承时，**它能自动分辨此时的父类是谁**。

可以见到，B类在执行super方法后，跳转到了C类的init，然后C类再跳到了父类A，与mro显示的顺序一致 



多态：子类继承父类所有的属性、方法的同时，可以重写父类的属性、方法（覆盖）。同一个函数根据不同的类表现出不同的特性，此即为”多态“。

**如何安全地继承：**

1. 类中所要用到的属性在`__init__(self)`中初始化，子类如果需要重写`__init__()`方法，先调用其父类的方法继承其相关属性，调用的方法是使用`super().__init__()`。**super()函数会按照mro的顺序寻找基类**，这是一种优秀的明智的做法，当**修改继承关系的时候，代码改动会很少**。 

2. 类属性在内存中只保存一份，**子类以引用的形式继承父类的类属性 ，当父类修改该类属性值时，所有继承的子类都会得到更新，除非子类重写该属性**。而实例属性在每个对象初始化的时候都单独开辟一个空间（new方法），父类对象的属性更改与子类对象属性独立。

   这里类属性的引用与C的二级指针有点类似，当子类没有重写类属性时，id始终与父类保持一致，尽管父类的类属性可能是一个原地不可变类型，如Int，这点与python的直接引用有所不同（或许是采用了哈希机制）。

   ```python
   #python的直接引用 
   a=1
   b=a	#b指向了内存1
   a=2
   print(a,b,id(a)==id(b))	#2 1 False
   
   #类属性引用示例 
   class A:
       count=1	#类属性
   
   class B(A):pass
   
   #直接更改父类类属性，子类伴随更改，且id一致
   A.count+=1
   print(A.count,B.count,id(A.count)==id(B.count))	#2 2 True
   #子类重写类属性，父子id发生变化 
   B.count+=1
   print(A.count,B.count,id(A.count)==id(B.count))	#2 3 False 
   ```

   



![](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/%E7%B1%BB%E5%B1%9E%E6%80%A7%E4%B8%8E%E5%AE%9E%E4%BE%8B%E5%B1%9E%E6%80%A7.png)



## 公有和私有

**Python没有私有机制**，成员和函数对外界总是透明的。如果一定要实现私有，可有采用**伪私有的机制。**

* **所谓伪私有，即是在变量名前加双下划线，Python会自动扩展此类属性，为其更名为`_class__var`（单下划线+类名+双下划线+属性名），类属性、实例属性均是如此**。这种伪私有机制在外部访问、子类继承时得到体现，但对于类内部函数，依旧为可见变量，直接使用`__var`访问即可。 

  **当子类继承父类时，子类可以得到父类的所有属性，包括私有属性**，只不过这些私有属性已被更名为`_parentClass__var` 。子类以传统的方法`self.__var`、`self.var`访问是不可能的，访问这些私有属性的办法（1）以完整形式访问变量，但这极容易出错，一旦父类更名，这些访问全部失效 （2）调用父类的接口`super().func()`，父类的私有属性对父类的函数是可见的。 

  在编程时，出于简单考虑，可以认为私有变量不被子类继承。

  另外 ，**一个特例**是，若变量前后均被双下划线包裹`__val__`，则该变量被认为是魔法方法，不会被更名。

* **如果在属性前只是加单下划线**，是一种**约定俗成**，相当于protect属性。不会轻易被子类重写覆盖、外界感知，比如pycharm就不联想`_`开头的方法，但实际上，依旧可以使用`_var`的形式访问。

```python
class A:
    count=10	#类属性
    _count1=11
    __count=12
    def __init__(self):
        self.ctr=1  #实例属性


class B(A):pass

class C(A):
    def __init__(self): #重写父类的init方法
        pass

objs=[('B类',B),('C类',C),('B实例',B()),('C实例',C())]
for obj_name,obj in objs:
    print('obj name: ',obj_name)

    for x in dir(obj):
        if not x.endswith('__'):
            print(x,end=' ')
    print('\n','='*30)

    
'''
obj name:  B类
_A__count _count1 count 
 ==============================
obj name:  C类
_A__count _count1 count 
==============================
obj name:  B实例
_A__count _count1 count ctr 
 ==============================
obj name:  C实例
_A__count _count1 count 
 ==============================

B和C均继承了A的类属性：_A__count _count1 count 
私有变量__count被更名为_A__count

B类继承了父类的init方法，未重写，所以可以看到 具备实例属性 ctr
C类重写了父类的init方法，并且未调用super()方法，不具备实例属性 ctr
由此，也能验证 实例属性由init等方法创建，类属性为静态属性 
'''
```




## 魔法方法

魔法方法：函数的名字被**双下划线包围**，如`__init__()`。魔法方法是**Python自有的**，双下划线被认为是系统的变量，**会为每个类创建**，用户也可以通过**重写的方式覆盖**原有的魔法方法，魔法方法会**在适当的时机被Python自动调用。**


### **常见魔法方法**

* `__init__(self)`：初始化对象，**return None或者不写**
* `__call__(self)`：让实例化后的对象也可以像函数一样被调用
* `__del__(self)`：使用`del class`时触发 
* `__str__(self)`：打印的时候让类返回一个字符串。给人看，print/str()的时候会调用
* `__repr__(self)`：返回代表对象的一个字符串，给机器看，eval的时候会用到
* 比较：
  * `__eq__`、`__neq__`：在`==`和`!=`时触发，neq默认委托给eq取反实现。
  * `__le__`、`__lt__`：在`<`和`<=`时触发
  * `__gt__`、`__ge__`：在`>`和`>=`时触发。python中，若未实现类`>、>=`的魔法方法实现，将自动调用右操作数的`<、<=`魔法方法。

```python
class A:
    def __init__(self,num):
        self.num=num

    def __eq__(self, other):
        return  self.num==other.num

    def __le__(self, other):
        return  self.num<other.num


    def __lt__(self, other):
        return self.num<=other.num

    def __str__(self):
        return  str(self.num)


    def __call__(self, *args, **kwargs):

        return  str(self.num+sum(args))

#富比较测试
a=A(10)
b=A(12)
print(a>=b) #调用b的<=方法
print(a!=b) #调用a的__eq__方法，并取反

#字符串测试
print(a)    #__str__，10
print(a(1,2))   #10+1+2=13
```

### 序列相关

* `__len__()`：当len(obj)的时候，返回大小
* `__getitem__(self,key)`：当使用索引操作如`a[key]`时，返回容器中的指定元素，可用于字典、列表、元组 
* `__setitem__(self,key,value)`：当使用索引操作赋值时a[key]=value
* `__delitem__(self,key)`：删除对应键的值 
* `__contains__(self,item)`：当使用成员测试符时，等于`item in/not in a`。
* `__iter__()`：生成迭代器。在for循环等自动触发迭代协议的时候，将会**隐式调用**此方法，应当返回一个可以迭代对象，配合`__next__`使用。
* `__next__()`：配合`__iter__()`使用，只能向后不能向前，返回自定义迭代器中的下一个值。



## 元类

元（meta），第一的意思。元类（metaclass），就是类的类。

在python中，一切皆对象，**类class本身也是一个对象（object）**。既然是一个对象，就可以通过`.__class__`查看其所属类。

```python
print([].__class__.__classs__)	#list的类：<class 'type'>
```

也就是说，**type是创建类实例的类，即是元类**。



**type是实例链的顶端，而object是继承链的顶端**。type和object是共生的关系。

```python
type==>class==>your object	#实例链
object--->class 	#继承链
```



**type作为默认的元类**，允许python在代码执行过程中，**动态地创建类**。其格式为`type('cls_name',(parentCls,),cls_attr_dicts)`  

事实上，在使用`class`关键字定义类的时候，实际发生的过程就是默认的元类type**拦截**了类的创建，**读取了类名、父类（元组）、类属性（字典）后**，然后通过new()函数实例化**返回一个类对象**。

```python
#自定义一个类，名为MyCls，无父类（默认继承自object），拥有类属性name='jhk'
class MyCls:
    name='jhk'

MyCls=type('MyCls',(),{'name':'jhk'})	#与以上类定义等效
```

简单概括元类在定义类时的动作为：

1. **拦截类的创建**
2. **修改类属性**
3. 返回修改后的类（对象）

因此，使用元类，就可以对子类进行操作，就像装饰器那样可以动态定制和修改被装饰的类。并且，这些操作不会被用户感知。



如有必要，就可以自己实现元类，定义自己的修改规则。实现自定义元类的步骤为：

1. 定义1个类，使其继承自type（`class MyMeta(type)`），然后重写new函数（注意调用super方法），不然毫无意义。此时，该类就是元类。**元类不可以直接实例化**
2. 在另外一个类中，**通过关键字参数声明`class clsName(metaclalss=MyMeta)`后。该类在定义时就会交由自定义元类控制，**而不是默认的type类。

```python
'''
自定义一个元类 重定义new函数（只是多了一行打印） 随后调用super方法返回实例
观察new所传参数 和 打印结果 去了解 class关键字在定义时发生的事情 
注意到main中并未实例化任何对象，说明所有的 打印信息都只是在定义的时候发生 
'''
class MyMeta(type):
    def __new__(cls,*args,**kwargs):	#注意这里传入的参数
        print('==>MyMeta new')
        print('args:{} kwargs:{}'.format(args,kwargs))
        return super().__new__(cls,*args,**kwargs)
    

class MyClass(metaclass=MyMeta):
    name='jhk'

if __name__ == '__main__':
    pass

'''运行结果
==>MyMeta new
args:('MyClass', (), {'__module__': '__main__', '__qualname__': 'MyClass', 'name': 'jhk'}) kwargs: 
'''
```

metaclass可以不是严格的一个类，可以是一个函数，只要符合type()动态创建类的语法规则即可。下例中的metaclass就是一个函数。

```python
'''拦截类的创建，修改类属性为大写'''

def alter_class(cls_name,cls_parents,cls_attrs):
    print('cls_name:%s cls_parent:%s' %(cls_name,cls_parents))
    print(cls_attrs)
    tmp={}
    for name,attr in cls_attrs.items():
        tmp[name.upper()]=attr 

    return type(cls_name,cls_parents,tmp)	#返回 一个类对象 


class Girl(metaclass=alter_class):	#传入一个参数
    nation='The US'

    def language(self):
        print('speak english')

g=Girl()
print('g.nation',g.NATION)	#The US
g.LANGUAGE()	#speak english 
```



**关于元类的作用机制**：python会以“ 类——>父类——>模块顶层 ”的顺序寻找metaclass ，如果找到，就将该类交由其管理。如果找不到，就交给默认的type元类管理。这意味着，**在一个类的继承链中，只要有1个父类实现了metaclass ，该类就会被自定义元类拦截创建**。  

元类与继承：元类不影响继承。先继承后拦截。 



## 抽象类 接口类

**抽象类**：如果一个类函数具备一个或多个抽象方法（abstractmethod），该类就是抽象类，不可实例化。**子类必须实现所有的抽象方法后才可以实例化**。抽象方法通常只定义函数体，而不实现函数。通过`@abstractmethod`的手段规范子类的接口名称。抽象类一般是对” 属性+方法 “的抽象，一个抽象类可以包含非抽象方法。



**接口类**：属于抽象类，但侧重对功能的抽象。对众多类中抽象出单一的接口。

```python
from  abc import  abstractmethod,ABCMeta

class Plant(metaclass=ABCMeta):		#注意这里的metaclass元类
    def __init__(self,attack=1):    #抽象类的共有属性 
        self.hp=100
        self.attack=attack

    @abstractmethod
    def shoot(self):pass	#抽象方法，只定义了函数体 


class IceShooter(Plant):	#继承抽象类 
    def shoot(self):
        print('Iceshooter is shooting...')

class PeanutShooter(Plant): #继承抽象类 
    def shoot(self):
        print('Peanutshooter is shooting...')


if __name__ == '__main__':
    ice=IceShooter(10)
    pea=PeanutShooter(15)

    ice.shoot()
    pea.shoot()

    print('iceshooter.attck:{} peanutshooter.attack:{}'.format(ice.attack,
                                                               pea.attack))

```



抽象类与接口类的异同： 

* 相似
  1. 都是对某一物体的抽象，方法使用abstract修饰，不可被实例化
  2. 子类必须实现抽象方法才可以实例化对象 ，否则也属于抽象类 
* 不同：
  1. 抽象类是对物的抽象，包含方法+属性的抽象，可以包含非抽象方法的实现 
  2. 接口类是对功能的抽象，只包含方法体、固定常量，不包含方法实现 
  3. 接口类，鼓励多继承；抽象类，鼓励单继承 



# 模块

## 模块和包

模块：单独的py文件/代码块都可以作为模块。

包：存放模块文件。**文件夹中必须要有一个`__init__.py`文件，里面内容可以为空**。文件夹的名字就是包的名字。

```python
if __name__=='__main__':
    #模块作为脚本导入，__name__等于脚本（文件、文件夹）名字，if判断为False
    #模块作为主函数执行，__name__就会等于__main__
    pass 
```

## 导入

### 搜索顺序

* 判断是否是built-in即内建模块，如果是则引入内建模块。
* 接着进入`sys.path`的list中寻找，sys.path在python脚本执行时动态生成，包括以下3个部分：（1）当前的工作路径，或者pycharm标记位`source_root`的目录（2）环境变量中的PYTHONPATH, 即.bash_profilec（2）安装python时的依赖位置

### 相对、绝对导入

import语句**导入**模块后，**模块里的语句会自动执行** ；导入包时，包的`__init__.py`文件会自动运行

* `import module`：模块里的所有代码会执行一遍，然后赋值给变量module。**调用模块里面的函数的时候，需要用`module.xx`的形式。**

* `import module as r`，可以简写模块名，当路径很长的时候，简写可以降低重复使用的工作量

* `from xx import yy`：

  关于绝对导入和相对导入的问题：

  当xx中的路径以`.`开头时，**表示使用相对路径的方式导入模块**，如`from . import xxx`，这种方式有几个问题需要注意：

  1. `.`是一种显式地从本包内部导入的语法。**要求当前文件夹是一个包package**，也就是含有`__init__.py`文件
  2. 使用相对导入语法的脚本能否正确执行取决于该脚本执行时的`__name__`。**当一个脚本作为`__main__`被运行时**，（1）**该脚本自身所有的相对导入都将失败**，会提示`'__main__' is not a package`。（2）该脚本可能使用绝对路径导入本包的其余脚本，那些脚本的相对导入就不能超过顶层的包，所谓顶层就是和被执行脚本平级的目录（[参考](https://www.cnblogs.com/linkenpark/p/10909523.html)）。

  以下是相对导入常见的几种形式

  ```python
  from . import a #导入当前包的a模块
  from .a import name #导入a模块的name变量
  ```

  

  当xx中的路径不是以`.`开头时，就是绝对导入，路径统统以`.`分隔，如`from pkg.a import name` 。绝对导入的搜索路径为sys.path。

  当yy是一个变量、函数时，**效果等同于将yy等代码直接粘贴在此处**，此后解释器执行，不需要用"."运算符。**这种方式有变量名冲突的风险**。在使用`from xx import`形式从多个模块导入变量时，如果后面的模块和前面的模块有相同的变量、函数，后面导入的会覆盖前面的。

  

  看一个例子，测试相对导入、绝对导入

  ```python
  '''目录结构
  test
  	pkg
  		__init__.py
  		spam.py
  		eggs.py
      my.py
  '''
  
  #pkg/init.py
  print('pkg init')
  
  #spam.py
  from .eggs import x #相对导入，包内导入eggs的x
  print('spam name is ',__name__) #脚本名
  
  #eggs.py
  x='eggs'
  
  #my.py 包外
  from pkg import spam   #绝对导入，test/已经动态添加到sys.path中去了，下面的pkg自然可以找到
  import sys
  #from .import pkg 相对导入会错误
  for x in sys.path:print(x) #查看当前的path
  ```

  直接运行`spam.py`，会报错，提示`No module named '__main__.eggs'; '__main__' is not a package`。这是因为spam.py此时名为`__main__`，pkg不再作为一个包。

  运行`my.py`，结果为

  ```
  pkg init
  spam name is  pkg.spam
  ```

  

  

模块动态导入：以字符串的形式在代码执行的中间过程导入，而非一开始就在头部导入。字符串为模块的相对路径

```python
from importlib import import_module

mod=import_module('lib.mod',package=None) #导入lib.mod，等效于import lib.mod as mod
#package参数为顶层可见的包名，默认为None,下述语句与上面等效
#mod=import_module('.mod',package='lib')
print(mod.s)	#可以直接访问mod里的属性
```



***

发布自己的包：

* 在包下建立`setup.py`，文件内容如下

  ```python
  from distutils.core import setup	#dist=distribution 分发，发布
  
  setup(name="wd_message", # 包名
      version="1.0", # 版本
      description="day11-homework", # 描述信息
      long_description="learn to setup packages", # 完整描述信息
      author="JiangHuiKai", # 作者
      py_modules=["t1", "t2"])	#与setup.py同级别的模块名，列表里的脚本将被复制打包到压缩文件
  
  ```

  

* 命令行进入包目录，执行`python setup.py sdist`，会自动生成得到`tar.gz`文件

* 将该文件发布到合适的机器上，拷贝到对应的安装目录，`tar -xzf xx.tar.gz`解压

* 执行`python setup.py install` 

* 若需要删除，则需手动进入安装目录，删除相应的模块文件（[非pip官方社区发布的卸载方法](https://cloud.tencent.com/developer/ask/196670)）

## 常见模块

### sys

* `sys.argv`：当python作为脚本在命令行界面被调用时，如`python test.py 1 2 3`，`sys.argv`作为一个列表，接收这若干参数，第一个参数是脚本名字，此后即为传入参数。
* `sys.setrecursionlimit(num)` ：修改函数最大递归深度。

****

### random

`random(import random as r)`：随机模块

* `r.random()`：随机生成0-1之间的小数
* `r.randint(l,r)`：随机生成l与r之间的整数，闭区间
* `r.choice(list[...])`：随机在给定列表元素中选择一个
* `r.shuffle(list[..])`：打乱列表
* `r.sample(range(n,m),l)`：在[n,m)之间不重复地选取l个数 ，也就是$C_{m-n}^l$ 

****

### time

`time（import time as t）`：时间模块。**时间戳（timestamp）指的是自1970-1-1 0:0:0经历的秒数**

* `struct_time`：time模块的类，形如`time.struct_time(tm_year=2020, tm_mon=1, tm_mday=15, tm_hour=11, tm_min=43, tm_sec=3, tm_wday=2, tm_yday=15, tm_isdst=0)`，可以进行列表、元组类型转换。
* `t.sleep(t)`：睡眠t秒 
* `t.time()`：返回自epoch（January 1, 1970, 00:00:00 (UTC) ）经历的秒数，浮点数
* `t.localtime(secs=None)`：返回当地时间的结构化时间，参数secs可以缺省 
* `t.mktime(struct_time)`：将结构时间戳转为秒数（浮点数）
* `t.stftime('%Y-%m-%d H%:%M:%S',struct_time)`：按指定字符串格式转换结构时间，注意年月日和时分秒的大小写
* `t.strptime("2020-1-15 11:26:40","%y-%m-%d H%:%M:%S")`：按指定格式将字符串解析（parse）成结构时间

### datetime

`datetime`：date（年月日）与time（时分秒）的结合，**是一个类（类名小写）**。

* `dt.datetime(year=,month=,day=,hour=,...)`：初始化一个datetime对象
* `dt.datetime.now()`：返回datetime对象，包含年月日-时间，可以与`.datetime.delta(days=?)`进行加减运算，获得几天前（后）的日期。并且，与`time`对象相同，支持`strftime()`格式化字符串输出 

```python
import datetime as dt

ago=int(input("想要推算几天前的时间？"))

s=(dt.datetime.now()-dt.timedelta(days=ago))

print("%d天前的时间为%s"%(ago,s))

#方法2，也可以通过time.time()-ago*24*3600来计算
str_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-ago*24*3600))
print("%d天前的时间为%s"%(ago,str_time) )

```

## conda

清华源设置 https://mirror.tuna.tsinghua.edu.cn/help/anaconda/ 



```shell
# 修改清华源 安装好以后配置
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes

conda config --remove-key channels # 删除全部源

# 查看当前通道 
conda config --show channels 
conda info 

# conda 升级
conda update conda 
conda update -n base conda #update最新版本的conda


# 环境管理 
conda info -e # 查看创建的环境 
conda --version #查看conda版本，验证是否安装
conda create -n xxxx python=3.5 #创建python3.5的xxxx虚拟环境
conda activate xxxx #开启xxxx环境
conda deactivate #关闭环境
conda env list #显示所有的虚拟环境
conda info -e #显示所有的虚拟环境
conda remove -n xxxx --all # 删除xxx虚拟环境
conda install python=3.6 #重设当前环境的python版本
# 清除缓存  
conda clean --all 

# 包管理
conda list #查看已经安装的文件包
conda list -n xxx #指定查看xxx虚拟环境下安装的package
conda update xxx #更新xxx文件包
conda uninstall xxx #卸载xxx文件包
conda install nb_conda # 让jupyter支持虚拟环境
# jupyter notebook 提示只能在主线程运行
# pip install "pyzmq==17.0.0" "ipykernel==4.8.2"
```



## 正则表达式

### 正则语法

* 限定符：匹配限定符**之前的表达式（用小括号包围）或者字母**，这与一些系统（如windows、linux）的通配符并不相同。
  
  * `* `：匹配0次或多次，等效于`{0,}`；`*?`，星号默认贪婪匹配，**后面添加?可以开启非贪婪模式**。例如，对于字符串”< h1>匹配示例<\h1>"，`<.*?>`将在匹配到第一个`>`时就结束匹配，而`<.*>`将匹配到字符串的最后一个`>`
  * +：匹配1次或多次，等效于`{1,}`，默认贪婪
  * ？：匹配0次或1次，等效于`{0,1}`，默认贪婪
* `{m,n}`：匹配至少m次，至多n次；`{n}`，匹配确定的n次；`{n,}`：至少匹配n次
  
* 单个字符：
  * `.`：匹配任意字符
  * `\d`，匹配数字，0-9;`\D`，匹配非数字
  * `\s`，匹配空格、tab。`\S`，匹配非空格
  * `\w`，匹配单词，包括字母、数字、下划线，在python3 中re默认支持的是unicode字符集，支持汉字，可以使用`flag=re.A`使\w仅支持ASCII码。`\W`，匹配非单词。
  
* 其他：

  * `[]`：字符集，可以包含**多个字母或一段范围**，如`[abc]、[0-9]`、`[a-zA-z]`等，范围不可以倒着写 。**对应位置只要符合字符集中任意一个字母（范围）即可。所有特殊字符在字符集中都失去其原有的特殊含义，相当于原生字符，如`.`仅仅表示点，不再代表任意字符。**在`[]`中，`^`表示**取反字符集所有内容**的意思，如`[^abc]` 表示匹配非(abc)开头的字符串。 

  * `|`：或OR，如果不是在`()`分组中使用，或的范围是整个表达式。 `|`使用**短路运算**，若字符串已经符合最先的条件，则不再匹配后面的条件。如`0?[0-9]|1[0-9]`，输入14，正则发现符合1符合条件`0?[-9]`而4不返回，则返回1。只要交换严格条件与宽松条件前后位置`1[0-9]|0?[0-9]`就可以正常捕获14。

  * `()`：分组，将若干匹配规则作为一个子表达式，如`m|food`与`(m|f)ood` 。组编号从1开始计数，可以使用`.group(num)`捕获相应分组。若未分组，group(0)等效于group()，捕获符合匹配的全部字符串。

    分组的特殊用法：**以下的P大写**

    * `(?P<name>)`：除了原有的数字编号外，再取一个name名字 ，可以作为参数传递（如Django视图函数的应用）
    * `(?P=name)`：引用名为name的分组

  * 反斜杆：`\`。**转义**，如`\d `、`\\`；`\+数字`，**引用**相应编号的分组。

  * 开头：`^`；结尾：`$` 





转义困扰：需要注意的是，**`\`会在编程语言中转义1次，接下里在正则语法中再转义1次，总计转义2次**。一个很好的例子就是，为了匹配反斜杆`\`，匹配规则应当写作`\\\\`，经过python第一次转义变为`\\`，再经过正则转义1次才可以匹配`\`。 为了避免这种转义的困扰，**应当在正则匹配表达式前加上`r''`**，表示是python的原生字符，禁止python的转义。

```python
#转义困扰
import re

res=re.match('\\\\','\\').group()   #不使用r匹配反斜杆
res1=re.match(r'\\','\\').group()   #使用r
print('res:{} res1:{} res==res1:{} '.format(res,res1,res==res1)) 
#运行结果：res:\ res1:\ res==res1:True 

```



### 常用函数

`import re`，导入正则模块

* `re.match(pattern,string)`：**以指定规则从字符串开头匹配**。match方法返回`<class '_sre.SRE_Match'>` 对象或None（无匹配），若要获取字符串，则当使用类方法`.group()` 

  * Match对象其他常用方法：
    * `.group(num=0)`，提取使用`()`分组截获的字符串，从1开始计数，默认num=0为匹配表达式的整体结果 ，如`re.match('a/.*','a/a/txt').group()`
    * `.start()`、`.end()`返回开始、结束的位置；`.span()`返回元组`(start,end)` 

* `re.compile(re_rule)`：编译相应的正则表达式，返回正则对象。随后可以调用类方法`.match()`、`.search()`等方法

  ```python
  re_obj=re.compile('a/.*')   #以匹配规则作为参数生成正则对象
  re_obj.match('a/a.txt')	#类方法
  ```

* `re.search(pattern,string)`：**字符串内查找**模式匹配，只要找到第一个匹配即**返回Match对象**，若无则返回None。类似于KMP 

* `re.findall(pattern,string)`：查找所有符合条件的字符串，**以列表形式返回**，列表中的每个元素为元组形如`(group1,group2,'',...)` 

* `re.split(pattern,string,[,maxsplit])`：以pattern作为分隔符分割字符串，类似`str.split(pattern)`，返回切割后的子串列表

* `re.sub(pattern,repl,string,count)`：在字符串string中找到符合pattern规则的字符串，替换为repl，返回修改后的字符串。repl可以是一个函数地址，传入参数为Match对象。 

  ```python
  #将字符串中的空格' '替换为'[ ]'
  #返回 xixi[ ]haha[ ]heihei
  re.sub(r'\s', lambda m: '[' + m.group() + ']','xixi haha heihei')#
  ```

  在repl中，可以使用`\g<n>`来获取分组，简写为`\n` 
  
  ```python
  # 将分组顺序 设置为 2-3-1
  a = re.sub('(\d{4})-(\d{2})-(\d{2})', r'\2-\3-\1', '2018-06-07')
  # '06-07-2018'
  ```
  
  

### 正则使用范例

对字符串按结构**逐段分析**，使用`()`分组，最后整合。



获取域名：

* 第一部分，https://、http://。s可有可无，可以写作`https?://`
* 第二部分，xxx.xxx.xxx/，可以拆成“xxx”（一定存在），`[a-zA-Z0-9]+`；".xxx.xxx/"（可能有多个，允许有下划线），`(\.[a-zA-Z0-9-]+)*/`

综上可得，最后的正则表达式可以写作`r'https?://[a-zA-Z0-9]+(\.[a-zA-Z0-9-]+)+/'` 

```python
urls=['http://www.interoem.com/messageinfo.asp?id=35',
'http://3995503.com/class/class09/news_show.asp?id=14',
'https://lib.wzmc.edu.cn/news/onews.asp?id=769',
'http://www.zy-ls.com/alfx.asp?newsid=377&id=6',
'http://www.fincm.com/newslist.asp?id=415']

host_re=re.compile(r'https?://[a-zA-Z0-9]+(\.[a-zA-Z0-9-]+)+/')
```



获取时间——“ 年-月-日 时:分:秒”，此处不考虑闰年与大小月问题

* 年，假设为4位，则为`1\d{3}`；月，01-12，则为`(1[012]|0?[1-9])`，注意`|`短路运算的性质，这里将可有可无的01-09月份写在了后面；日。01-31，则为`3[01]|[12][0-9]|0?[1-9]` 。

  所以，年月日部分应当为：`year_re=r'(1\d{3})-(1[012]|0?[1-9])-(3[01]|[12][0-9]|0?[1-9])'`

* 时，00-23，则为`(2[0-3]|1[0-9]|0?[0-9])`；分与秒均为0-59，则为`([1-5][0-9]|0?[0-9])` 

  所以，时分秒部分应当为：`time_re=r'(2[0-3]|1[0-9]|0?[0-9]):([1-5][0-9]|0?[0-9]):([1-5][0-9]|0?[0-9])'`

综上，最后的正则表达式为`r''+year_re+time_re`

## logging日志模块

导入：`import logging` 

创建输出日志的一般流程如下

```python
import logging 

# 创建logger对象 
logger=logging.getLogger()
# 日志等级从低到高分为，debug，info，warning，error，critical  
# setLevel 设定过滤等级 过滤小于INFO的信息
logger.setLevel(logging.INFO) 

# 添加输出句柄 此处表示输出到控制台 
logger.addHandler(logging.StreamHandler()) 

# 输出日志信息 
message='log test'
logger.debug(message) # 因为一开始设定的等级是InFO 所以debug会被过滤 不会输出 
logger.info(message)
```





除了输出我们指定的日志信息外，还可以利用一些格式来输出日志的辅助信息。 



<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/log%E6%97%A5%E5%BF%97%E6%A0%BC%E5%BC%8F.png" style="zoom:67%;" />



额外的唯一工作就是需要在句柄上绑定Format对象，`logger_handler.setFormatter(Format对象)`   

```python
# 创建 logger 对象 
logger=logging.getLogger()
logger.setLevel(logging.INFO) # 过滤小于INFO的信息

# 创建Formatter对象 时间 - 日志等级 : 日志信息 
Format = '%(asctime)s - %(levelname)s: %(message)s'
Format = logging.Formatter(Format)

# 创建句柄
handler = logging.StreamHandler()
handler.setFormatter(Format)

# 添加句柄
logger.addHandler(handler) 

message='log test'
logger.debug(message) # 会被过滤
logger.info(message)
logger.warning(message)
logger.critical(message)
```

输出如下 

```
2021-09-16 14:21:26,774 - INFO: log test
2021-09-16 14:21:26,774 - WARNING: log test
2021-09-16 14:21:26,774 - CRITICAL: log test
```







除了输出信息到控制台，可能还需要输出到文本。 

```python
# 文件输出句柄 filename,mode,encoding 
handler = logging.FileHandler('./hollis_log.log',mode='w',encoding='utf8')
```

其余可以设置可以完全不变，**并且一个logger可以同时添加多个句柄**，表示日志将一并输出到这些句柄上。 

```python
Format = '%(asctime)s - %(levelname)s: %(message)s'
Format = logging.Formatter(Format)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(Format)
# stream_handle.setLevel(日志等级) # 句柄也可以设定等级 

# 除了创建 其余操作都相同 
file_handler = logging.FileHandler('./hollis_log.log', mode='w', encoding='utf8')
file_handler.setFormatter(Format)

logger.addHandler(stream_handler)  # 添加句柄
logger.addHandler(file_handler)
```



## pymysql

pymysql，第三方库（`pip install pymysql`），用于与mysql数据连接。



连接步骤：`import pymysql as pm`

1. 创建连接，`conn=pm.connect(host,port,user,passwd,db)`，参数以关键字参数形式传入。
2. 创建游标，`cursor=conn.cursor()`，**通过游标操作数据库**。cursor和conn的关系可以类比为文件和文件指针，同一个文件允许创建（open方法）多个文件指针同时读写。



cursor的常用命令：

* 读操作：必须先执行select语句`cursor.execute(select_command)`获取查询数据后才能进行以下操作
  * `cursor.fetchone()`：迭代器，每次读取一行数据，返回元组，每个元素是字段值，类似于文件`readline()`
  * `cursor.fetchall()`：从光标处读取至数据库尾部，返回一个大元组`((行数据1),(行数据2),...)` ，类似于文件的`read()`

* 命令执行：`cursor.execute(sql_command)` ，返回影响的行数rows（select则返回查询到的行数），可以用于迭代计数或判断。**sql命令可以是固定的常量字符串或者参数化的字符串**。

  参数化书写时，格式为`'sql_command',[args]`。command命令中的待定参数用`%s`作为占位符。**此处的%s区别于字符串的格式化，只起到占位作用，不进行str类型转换**。可以理解为mysql真正执行的语句就是command字符串包裹内%s原样替换后的命令。

  ```python
  cursor.execute('select * from student where name=%s',['zhangsan'])
  #等价于 select * from student where name='zhangsan' 
  
  cursor.execute("select * from student where name='%s' ",['zhangsan'])	#%s外面多了一层引号 
  #等价于 select * from student where name=''zhangsan''	，两个单独引号不等于"，会直接报错 
  
  cursor.execute("select * from student where id=%s",[5])	
  #等价于 select * from student where id=5 ，注意5是int 
  ```

  
  
  因此，类型控制应当在参数列表中控制，如`['zhangsan',10]`，而**表名也不可直接参数化**（但可以提前通过%s控制替换或者写死）。
  
  ```python
  #常量字符串写死
  cursor.execute('update student set name="lisi" where name="ZhangSan" ')
  
  #参数化字符串
  name=['lisi','ZhangSan']
  sql_command='update {} set %s where name=%s'.format('student')	#表名间接参数
  cursor.execute(sql_command,name) 	#参数化的命令 %s占位控制
  ```
  
  常量字符串作为`.execute()`的参数时，可能会引起SQL注入问题。如下例。
  
  ```python
  cm=input()
  sql_command='select * from test where name=%s' % cm
  
  '''
  此时，若用户非法输入 x or 1，则命令为
  select * from test where name=x or 1
  由于1始终被where判断为True，因此，此命令将暴露所有数据给该用户，极具隐患
  '''
  ```
  
  



pymysql基于事务读写，在写操作完成后，只有`conn.commit()`提交之后才会从内存写入磁盘，换言之，出现任何异常操作后，都可以使用`conn.rollback()`回滚到初始状态。注意，此时的提交对象为`conn` 对象。同时，需要在最后关闭连接。

```python
conn.commit()	#事务提交
cursor.close()	#游标关闭
conn.close()	#socket关闭 
```



# Socket网络通信

socket：意译为套接字，英文意为“网络插座”，指两台计算机通信的接口，`ip:port`。进程在本地以PID被标识，在网络则以端口号标识。IP只负责点到点的通信，进程间的通信则依赖其上的TCP、UDP传输层协议。相关知识可查看计算机网络。



创建socket：使用模块`socket`的类`socket`，同时指定IP协议和传输层协议。

```python
from socket import * 
s=socket(family=AF_INET, type=SOCK_STREAM)	#默认为ipv4 tcp
s.close()	#关闭该套接字
```

* family：协议族，默认为`AF_INET`，表示ipv4。
* type：`SOCK_STEAM` ，流式套接字，表示tcp；`SOCK_DGRAM`，数据报套接字，表示udp。



查看端口状态：`netstat -an|grep [TCP| UDP| port]`，显示`LISTEN`表示监听中，`ESTABLISHED`表示正在与另外1台主机通信。

## UDP通信

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/udp_socket.png" alt="udp_socket" style="zoom:67%;" />

收方双方的准备步骤：通信双方无需建立连接，准备好数据即可发送。对于发送方，事前准备好接收方的地址，**但是无需`bind`，因为系统会为进程随机分配1个端口。**在进程结束前，该端口不会改变。

```python
#client
from socket import *
addr=('localhost',2000)	#是1个2元组，列表也不可以
client=socket(type=SOCK_DGRAM)
client.sendto(bytes,addr)	#给目标端口发送数据
```

对于接收方，需要先`bind`与发送方事先约定的端口，保证客户端能够发送数据给自己。随后使用`recvfrom`接收数据，即可知道此时发送方动态分配的套接字。UDP的服务端与客户端是多对多的关系。

```python
#server 
from socket import *
addr=('localhost',2000)
server=socket(type=SOCK_DGRAM)
server.bind(addr)	#绑定本地端口，对于UDP而言，bind的同时就开始监听
data,address=client.recvfrom(1024)	#最大接收1024字节
```



数据的读写：读写基于字节流`bytes`进行，需要编解码。

* 读：`recv(size)`，最大接收size个字节，直接返回接收到的字节流。`recvfrom(size)`，返回1个二元组为`(data,(ip,port))`，第1个元素为对应数据，第二个为发送方的地址。
* 写：`sendto(bytes,des_addr)`，第1个参数为字节流，第2个参数为2元组的目标地址。udp是无连接的，所以需要接收方地址。



udp是无连接的，当一端断开时，另外一端并无影响，也不会接收到任何数据。



聊天室实现

```python
#chat_server.py
from socket import  *

def server():
    addr=('localhost',2000)		
    udp_server=socket(AF_INET,SOCK_DGRAM)
    udp_server.bind(addr)	#绑定端口
    dest_addr=None
    print('监听中……')
    
    while True:
        res=udp_server.recvfrom(1024)	#这里使用了recvfrom
        if not dest_addr:dest_addr=res[1]   #更新发送方的地址
        print('客户端IP:{} 数据：{}'.format(res[1], res[0].decode('utf-8')))
        if not res[0]:break		#数据为空，对方下线，直接退出

        print('='*30)
        content=input('请输入：')
        udp_server.sendto(content.encode('utf-8'), dest_addr)
        if not content:break
        print('等待对方回复……')

    udp_server.close()


if __name__ == '__main__':
    server()
```

```python
#chat_client.py
from socket import  *


def client():
    dest_addr = ('localhost', 2000)
    udp_client = socket(AF_INET, SOCK_DGRAM)
    
    while True:
        content=input('请输入：')
        udp_client.sendto(content.encode('utf-8'), dest_addr)
        if not content: break

        print('等待对方回复……')
        res=udp_client.recv(1024)
        print('来自服务器的数据：{}'.format(res.decode('utf-8')))
        if not res: break

        print('='*30)

    udp_client.close()


if __name__ == '__main__':
    client()
```



## TCP通信



<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/tcp_socket.png" style="zoom:80%;" />



TCP的通信面向连接，是点对点的，收发双发需要建立连接。对于客户端，事先准备好接收方的地址，然后使用`client.connect(addr)`连接接收方，`connect`是阻塞的，与UDP相同，发送端也无需`bind`。

```python
from socket import *
addr=('localhost',2000)
client=socket(type=SOCK_STREAM)
client.connect(addr)	#连接对端，阻塞
pass	#do something 
```

对于接收端，需要3步

1. `server.bind(addr)`，绑定到相应端口
2. `server.listen(10)`，默认创建的socket是主动的，调用listen方法使其变为被动监听。**参数`10`表示连接等待队列最大数是10，**超过该数量的连接即被丢弃，此时若客户端尝试`connect`连接，将报错`ConnectionRefusedError: [WinError 10061] 由于目标计算机积极拒绝，无法连接`。
3. `connect,address=server.accept()`，调用`accept()`方法从等待队列（listen）中取出1个连接请求，与之建立连接，**并返回针对此连接的套接字和请求连接方的地址，此后接收方在该次连接的收发数据均使用`conect`对象进行，而非`server`本身**。

接收端的监听端口虽然固定，但**允许客户端使用不同的端口与该端口来建立多个连接**。



tcp双方通信过程中，当有一端断开时，会发生以下情况：

1. 另外一端的`recv`会始终处于可读状态，返回空数据。所以，**应当对接收到的数据加以判断，及时断开连接**，否则就会出现疯狂打印换行（`print(b'')`）。这与另外一端直接回车是有区别的，回车并不会在发送端被写入输出缓冲（UDP会直接发送），接收端的recv自然也不会收到数据。

```python
if not recv_data:
    connect.close()	#断开连接
else:
    print(recv_data.decode('utf-8'))
```

2. **主动断开的一方会出现四次挥手的`TIME-WAIT`**，由于客户端每次重启进程都会随机分配1个端口，所以没有太大影响。但是服务器端绑定固定端口监听，就要出现端口被占用无法迅速重启的问题。解决的办法就是在`bind`前使用`sercer_socket.setsocketopt(SOL_SOCKET,SO_REUSEADDR,1)`，使得该端口可以迅速重用。

```python
#tcp_chat_server
from  socket import *

addr=('localhost',2000)
server=socket(type=SOCK_STREAM)
server.bind(addr)	#绑定
server.listen(10)	#监听

while True:
    print('等待客户端连接……')
    connect, addr = server.accept()	#建立连接
    print('连接客户端；', addr)
    
    while True:
        print('等待接收……')
        recv_data=connect.recv(1024).decode('utf-8')	#注意到这里是connect对象
        if not recv_data:break
        print('接收数据大小：{} 内容：{}'.format(len(recv_data),recv_data) )

        send_data=input('请输入：').encode('utf-8')
        if not send_data:break
        connect.send(send_data)

        print('='*30)

    print('*'*30)
    connect.close()
```

```python
#tcp_chat_client
from  socket import *

addr=('localhost',2000)

client=socket(type=SOCK_STREAM)
client.connect(addr)

while True:
    send_data=input('请输入内容：').encode('utf-8')
    if not send_data:break
    client.send(send_data)

    print('等待接收……')
    recv_date=client.recv(1024).decode('utf-8')
    if not recv_date:break
    print('接收数据大小：{} 内容：{}'.format(len(recv_date),recv_date))

    print('='*30)

client.close()
```



## 输入输出缓冲

### UDP

udp实际并无输入缓冲，由于其无连接特性，不必保存应用层的数据拷贝，数据沿协议栈向下传递并以某种形式拷贝到内核缓冲区，当数据链路层送出数据后就把内核缓冲区中的数据删除。通过`SO_SNDBUF`设置的缓冲区大小实际只是UDP报文上限大小。

udp套接字的缓冲区是以报文为单位排队的队列，**调用一次recvfrom即提取相应大小的报文，后面的报文即被丢弃，这和TCP基于字节流的方式是不同的**。当接收到的数据报装不进udp接收缓冲区时，也被丢弃。

### TCP

系统为建立TCP连接的套接字建立输入（收到数据）、输出缓冲（待发数据），这里的缓冲是在内核中，而非标准输入、输出缓冲。

`send`将数据拷贝进入socket的内核发送缓冲区，拷贝成功即返回拷贝的数据大小。

* 当拷贝数据大于整个缓冲区大小时，系统报错“ 溢出（OverflowError） ”（对于较大数据，应该分开多次发送）
* 当数据大于缓冲区剩余空间大小时，进入阻塞，等待接收方`recv`数据后，为发送方的缓冲腾出空间，发送方`send`阻塞解除。若接收方在发送方`send`阻塞情况下断开连接，会返回`-1`，可以借此判断对方是否下线。

`recv`从输入缓冲区取出数据，若无数据，进入阻塞。数据会一直留在输入缓冲直到`recv`读取，当接收缓冲区满后，收端发送窗口关闭（win=0），此即TCP的滑动窗口流量控制。



## IO模式

网络通信在执行IO操作的时候，例如recv、send，实际发生的过程为：

1. 函数执行时，从用户态转为内核态，执行相应的系统调用
2. 等待数据准备完成，随后再返回用户态

按照对此过程的不同解决方案，IO操作可分为以下几种。[IO模式的比较](https://www.cnblogs.com/alex3714/articles/5876749.html)  

1. 阻塞IO，收发操作均进行阻塞，**等待内核数据准备完成再返回**。不能在单线程内实现并发，一个**卡住**，随后的socket也会被卡住。
2. 非阻塞IO，收发均不阻塞，**若有数据则取出（发送），若无数据，则报错**。在`while`循环内判断，可以在1个线程内实现并发。
3. IO多路复用，使用`epoll`、`select`等**阻塞式地监听**多个文件描述符的状态，**有更新了通知用户，再去收发数据**。可以在1个线程内实现并发。
4. 异步IO：用户发出调用请求后，随后就返回处理自己的事情。相关部件将数据准备完毕并拷贝到用户态后，再以某种方式通知用户。 



### 多路复用

Socket默认使用阻塞模式，所谓阻塞，即是在使用`recv`接收数据，`send`、`input`发送数据时，程序会在此卡住，直到接收到数据或者输入数据。这样的程序不具备并发能力，例如服务器存在多个tcp连接，当逐个检查是否有新消息到达时，一个卡住后面所有的都会卡住。解决阻塞的办法之一就是使用IO多路复用。

IO多路复用，使用`select`、`epoll`之类的系统调用，**监听相应文件（Linux中一切皆文件）的读写状态**，一旦状态更新，就返回所有更新的事件列表。windows下只能使用`select`，linux下均可以使用，`epoll`是对`select`的改进。此类系统调用在监听时默认是阻塞的。

epoll和select的使用均要先导入模块`import select as se`

#### epoll

epoll在内核中使用红黑树来添加、删除文件，用列表类存储更新事件列表。[epoll详解](https://blog.csdn.net/luolaifa000/article/details/84190836)

epoll的使用：`import select as se` 

1. 创建1个epoll对象，`epoll=se.epoll()`

2. 注册监听事件，`epoll.register(fd,event)`，fd是相应的文件描述符，event是事件状态。

   fd：文件描述符，对于socket对象，可以使用`SockrtObj.fileno()`获取，

   event：

   * `se.EPOLLIN `， 可读事件
   * `se.EPOLLOUT`，可写事件
   * `se.EPOLLHUP`  ，客户端断开事件

3. 获取事件更新列表：`for fd,event in epoll.poll(timeout=-1)`，将会返回状态更新的文件列表。timeout表示监听时间，默认-1表示阻塞监听，直至事件更新。

4. 销毁监听事件，`epoll.unregister(fd)` 



```python
#chat_room_server.py
import select as se
import  datetime as dt
from  socket import *

addr=('192.168.145.128',2000)
server=socket(type=SOCK_STREAM)		
server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)	#设置ip地址重用
server.bind(addr)
server.listen(100)

def chat_server():
    epoll=se.epoll()
    epoll.register(server.fileno(),se.EPOLLIN)	#监听可读事件，等待用户连接
    timeFormat='%H:%M:%S'
    clientLists = []	#客户端在线列表
    while True:
        for fd,event in epoll.poll():	#监听事件
            if fd==server.fileno():		#有新的连接
                connect,address=server.accept()
                clientLists.append((connect,address))
                epoll.register(connect.fileno(),se.EPOLLIN)	#为该连接注册
                print('{} {}上线了'.format(dt.datetime.now().strftime(timeFormat),address))

            for client,address in clientLists:	#遍历所有连接
                if fd==client.fileno():	#判断是否是该连接的事件
                    recv_data=client.recv(1024)
                    print(recv_data.decode('utf-8'))	
                    if not recv_data:	#对端下线
                        epoll.unregister(client)	#接注册
                        clientLists.remove((client,address))	#从在线列表中移除
                        client.close()
                        print('{} {}下线了'.format(dt.datetime.now().strftime(timeFormat),address))
                    else:	#群发该数据
                        for _client,_address in clientLists:
                            if _client!=client:	#如果不是发端，就发送
                                _client.send(recv_data)


if __name__ == '__main__':
    chat_server()

```



```python
#chat_room_client.py
from  socket import *
import select as se
import  sys
import datetime as dt
addr=('192.168.145.128',2000)
client=socket(type=SOCK_STREAM)


def chat_client():
    epoll=se.epoll()
    epoll.register(sys.stdin.fileno(),se.EPOLLIN)
    epoll.register(client.fileno(),se.EPOLLIN)

    name=input('输入用户名：')
    client.connect(addr)
    off_line=False
    while True:
        for fd,event in epoll.poll():
            if fd==sys.stdin.fileno():	#标准输入有数据可读
                send_data=input()	#使用input取缓冲区
                if not send_data:	#数据为空，置位下线标志
                    off_line=True	
                    break
                else:
                    now=dt.datetime.now().strftime('%H:%M:%S')
                    send_data='{} {}: {}'.format(name,now,send_data).encode('utf-8')
                    client.send(send_data)

            elif fd==client.fileno():	#socket有新的消息可读
                recv_data=client.recv(1024).decode('utf-8')
                if recv_data:print(recv_data)

        if off_line:
            client.close()
            exit('连接断开！')


if __name__ == '__main__':
    chat_client()


```



#### select

进程指定内核监听指定事件，等待状态更新。使用`import se`

当我们调用select()时：

1. 上下文切换转换为内核态，将fd从用户空间复制到内核空间
2.  内核遍历所有fd，查看其对应事件是否发生
3.  进程阻塞直至事件更新或tImeout为0
4.  返回遍历后的fd
5. 将fd从内核空间复制到用户空间



select参数解释：`readList,WriteList,errorList=se.select(rlist, wlist, xlist, [timeout])`

* 参数： 可接受四个参数（前三个必须）。windows下，监听对象必须为套接字，而linux下可以是文件描述符、对象。
  * rlist：监听直至可读
  * wlist：监听直至可写
  * xlist: wait：监听错误
  * timeout: 超时时间，默认为-1，阻塞直至事件更新 

* 返回值：3个列表，为可读事件更新列表、可写事件更新类表、错误事件更新列表。

```python
 #sys.stdin ，需要在linux下运行，windows会报错——“在一个非套接字上操作”
    while True:
    if se.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):	#监听直至标准输入可读更新
        data=input()
        pass
```

### 非阻塞模式

在套接字建立之后，通过`socketObj.setblocking(False)`设置该套接字为非阻塞模式，在该连接断开前始终有效。在非阻塞模式下，`accept` 、`recv`等操作都会一次性返回，若成功，则正常返回值，否则，立即抛出异常。因此可以使用`try`来捕获异常，`except Exception` 忽略所有异常，`else`执行正常情况下的操作。

非阻塞模式会大量耗费CPU，但是适合读取大量数据，因为相邻两次`recv`调用资源耗费会比epoll等系统调用少。

在使用epoll、select时，建议使用非阻塞模式。

> Under Linux, select() may report a socket file descriptor as "ready for reading", while nevertheless a subsequent read blocks.  This could for example happen when
>        data has arrived but upon examination has wrong checksum and is discarded.  There may be other circumstances in which a file descriptor is spuriously reported  as
>        ready.  Thus it may be safer to use O_NONBLOCK on sockets that should not block





```python
#chat_room_server_noblocking.py
import  datetime as dt
from  socket import *

addr=('192.168.145.128',2000)
server=socket(type=SOCK_STREAM)
server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
server.bind(addr)
server.listen(100)
server.setblocking(False)	#设置非阻塞模式，用于accpet

def chat_server():
    timeFormat='%H:%M:%S'
    clientLists = []
    while True:
        try:
            connect,address=server.accept()	#当抛出异常时，并不会覆盖原来的值 
        except Exception:	
            pass
        else:	#当接收到新的客户端时
            print('{} {}上线了'.format(dt.datetime.now().strftime(timeFormat), address))
            clientLists.append((connect,address))
            connect.setblocking(False)		#为该连接设置非阻塞，用于recv
        finally:	#始终要遍历查看是否有新的消息到达 
            for client,address in clientLists:
                try:
                    recv_data=client.recv(1024)
                except Exception:
                    pass
                else:	#当该连接有新的消息时 
                    if recv_data:
                        print(recv_data.decode('utf-8'))
                        for _client,_address in clientLists:
                            if _client!=client:_client.send(recv_data)
                    else:
                        print('{} {}下线了'.format(dt.datetime.now().strftime(timeFormat), address))
                        client.close()
                        clientLists.remove((client,address))

if __name__ == '__main__':
    chat_server()

```



```python
#client.py 
from  socket import *
import select as se
import  sys
import datetime as dt
addr=('192.168.145.128',2000)
client=socket(type=SOCK_STREAM)


def chat_client():
    name=input('输入用户名：')
    client.connect(addr)
    client.setblocking(False)	#设置非阻塞
    while True:
        #timeout设置为0，使select为非阻塞模式 ，不然程序会一直卡住，执行不到收数据
        if se.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):	#监听标准输入直至可读
            send_data=sys.stdin.readline().strip()
            if not send_data:
                client.close()
                exit('连接断开！')
            else:
                now = dt.datetime.now().strftime('%H:%M:%S')
                send_data = '{} {}: {}'.format(name, now, send_data).encode('utf-8')
                client.send(send_data)

        try:
            recv_data=client.recv(1024)
        except Exception:
            pass
        else:	#当收到新的数据时 
            if recv_data:print(recv_data.decode('utf-8'))


if __name__ == '__main__':
    chat_client()
```



## 粘包

tcp通信时，发送方连续多次`send`，接收方未及时取出，数据一并进入接收方的缓冲区，混在一起。等到接收方下次`recv`的时候，数据一并取出，无法区分每次发送的数据边界，此为粘包。

粘包只发生在缓存数据保留的tcp通信。udp通信中，超出`recv(size)`的多余数据即被丢弃，`send`和`recv`是一一对应的。



解决粘包的问题有两种思路，第一种是自定义数据的结束标志，第二种是提前发送下一次发送数据的长度，然后再发送数据。此处介绍后者。

假设下一次发送的数据长度为`size`。python中整数int是没有位数限制的，也就是说，如果简单的采用`str(size).encode('utf-8')`作为数据长度，通知给接收方是不合理的，因为这个bytes对象长度并不确定，例如`b'9'` 、`b'100'`长度分别为1、2。粘包的时候依旧无法区分哪部分表示长度。所以，解决思路应该是取固定长度的字节来表示`size`。

使用`struct`模块可以解决这个问题，`struct.pack(mode,num)`将数字打包成C语言的指定[数据类型](https://blog.csdn.net/D_R_L_T/article/details/91910774)，例如4个字节的`int(i)`、`unsigned int(I)`，返回字节`bytes`类型。

```python
import  struct

num=str(1).encode('utf-8')	#尝试直接编码
num_trans=struct.pack('I',1)	#小端模式存储
print('数据：{} 类型：{} 长度：{}'.format(num,type(num),len(num)))
print('数据：{} 类型：{} 长度：{}'.format(num_trans,type(num_trans),len(num_trans)))

'''运行结果
数据：b'1' 类型：<class 'bytes'> 长度：1
数据：b'\x01\x00\x00\x00' 类型：<class 'bytes'> 长度：4
'''

```



一旦收发双方约定这个自定义的规则——“ 先发数据长度size ，再发数据 ”，粘包问题就可以解决。

收方先固定接收4个字节，使用`struct.unpack(mode)[0]`解析出发送方此次发送的数据长度，`unpack`返回1个元组（因为pack可以一次接收多个参数），每个元素为python的int类型，可以直接使用。随后循环接收即可，直至接收长度等于约定的size大小。

```python
#接收方
import struct 
size=size.unpack('I')[0]	#返回元组，索引后得到python的int 类型，
recv_size=0
while recv_size<size:	#直至接收完毕
    recv_data=client.recv(1024)	
    recv_size+=len(recv_data)
    
```



## HTTP协议

HTTP协议：规定浏览器和服务器之间的请求和响应格式的规则，属于应用层协议，基于TCP连接进行可靠传输。HTTP1.0时仅支持短连接，每请求一个对象都需要一次“ 连接-断开 ”的规程。HTTP1.1后支持长连接（keep-alive）。 

短连接下，每次close就意味着数据传输完毕。

长连接下，需要有`content-length`字段或`Transfer-Encoding:chunked` 字段。前者统计出本次消息的传输长度，后者表示本次数据为分块数据（[content-length字段作用](https://www.cnblogs.com/nxlhero/p/11670942.html) ）。若保持长连接，而两个字段均没有，客户端请求将会陷入超时状态。



HTTP的报文头：分为客户端到服务端的请求报文、服务端到客户端的响应报文。

报文格式：分为 “ 头部（header）+实体（body）”。头部又可分为“ 开始行+ 首部行 “

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/HTTP%E8%AF%B7%E6%B1%82%E6%8A%A5%E6%96%87.jpg" style="zoom:60%;" />

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/HTTP%E5%93%8D%E5%BA%94%E6%8A%A5%E6%96%87%20.jpg" style="zoom:70%;" />



头部header：

* 开始行：头部的第一行。对于请求报文，格式为“ 请求方法 请求URL HTTP协议”，以空格区分。对于响应报文，格式为“ HTTP协议版本 状态码及描述 ”
* 首部行：可有可无，用于说明本次连接的一些信息，格式为`field: value`，如`Content-Length: xxx`。

实体body：可有可无，用于携带本次传输的消息。



头部的每行以CRLF分隔，即`\r\n`，头部与实体以空行分隔`\r\n`。

```python
#自定义报文 
body='hello world'	#实体 

header = 'HTTP/1.1 200 OK \r\n'		#开始行，注意尾部结束符
header+='Content-Length: %d\r\n'%len(body)		#首行，content-length字段 
header+='\r\n'		#header+body的空行分隔 

connect.send((header+body).encode('utf-8')) 	#以2进制字节流形式发送 
```



## NAT穿透

这里只简单展示NAT穿透的原理。

在NAT未穿透的情况下，内网主机A与内网主机B不可直接通信，因为双方都是私有IP。需要以一已知的服务器为中介，转发各自的消息。以qq通信为例，通信双方的IP地址被保存在中间服务器上，进行转发，并非双方直接通信。

NAT穿透的手段就是**让通信双方知道对方的公网IP，进而绕过server**，直接给对方发送消息。

NAT的类型有很多，这里简单考虑，假设AB主机在会话期间始终被路由器映射为同一个公网 `(IP:PORT)`，则可令中间服务器server，分别收取AB的信息，得到AB的公网IP地址（源IP地址在路由过程中不会被更改）并保存，然后将双方公网IP发送给彼此。在AB都知道对方的公网IP后，便可以实现“ 打洞 ”效果，直接通信。

![](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/NAT%E7%A9%BF%E9%80%8F.png)



```python
'''
server
'''
from  socket import *

def get_public_ips():
    addr=('172.19.34.126',2000) #私有IP
    server=socket(type=SOCK_DGRAM)
    server.bind(addr)
    
    #等待收取AB的IP地址
    client_a_address=server.recvfrom(1024)[1]
    client_b_address=server.recvfrom(1024)[1]
    bytes_a_address=(client_a_address[0]+' '+str(client_a_address[1])).encode('utf-8')  #ip port
    bytes_b_address=(client_b_address[0]+' '+str(client_b_address[1])).encode('utf-8')
    print("a's ip:{} b's ip:{}".format(client_a_address,client_b_address))
    
    #交换IP
    server.sendto(bytes_b_address,client_a_address)
    server.sendto(bytes_a_address,client_b_address)
    print('swap ip over!')

if __name__ == '__main__':
    get_public_ips()
```

```python
'''
client
'''
from  socket import *
import  select,sys

def client_socket():
    addr=('149.129.47.10',2000)
    client=socket(type=SOCK_DGRAM)

    client.sendto(b'hello',addr)    #发送内容随意，主要是向服务器暴露自己的公网IP
    peer_addr=client.recv(1024).decode('utf-8').split()
    peer_addr=(peer_addr[0],int(peer_addr[1]))
    print('peer_addr is {}'.format(peer_addr))  #对端公网IP
    
    #进入AB直连，此处采用非阻塞+select 进行会话 
    client.setblocking(False)   
    while True:
        if select.select([sys.stdin],[],[],0)==([sys.stdin],[],[]):
            send_data=input()
            if not send_data:client.close()
            client.sendto(send_data.encode('utf-8'),peer_addr)

        try:
            recv_data=client.recv(1024)
        except Exception:
            pass
        else:
            print(recv_data.decode('utf-8'))


if __name__ == '__main__':
    client_socket()
```





# 进程 线程 协程

## 进程

进程，CPU分配资源的单位。Python中，多进程可以使用多核。



进程的操作：`from multiprocessing import Process`

* 创建进程：`p=Process(target,args)`，target指定目标函数，args为函数所传参数。

* 启动进程：`p.start()` ，为子进程创建`task_struct`之后父进程就返回。

* 强制关闭进程：`p.terminate()`，杀死进程

* 回收进程：`p.join()`，等待进程结束回收其资源

* 获取进程退出码：`p.exitcode` ，必须在`.join`之后使用。

  > 进程结束后，大部分资源均被回收，剩下task_struct这个空壳和极少一部分资源，成为僵尸（Z）。
  > 之所以保留task_struct，是因为task_struct里面保存了进程的退出码、以及一些统计信息。而其父进程很可能会关心这些信息。比如在shell中，$?变量就保存了最后一个退出的前台进程的退出码，而这个退出码往往被作为if语句的判断条件。

* 获取进程的id、父进程的id：`p.getpid()`、`p.getppid()` 

```python
from multiprocessing import Process
import os
import  time

def run(name):
    process_id=os.getpid()
    print('{} 的id是{}'.format(name,process_id))
    time.sleep(1)


if __name__ == '__main__':
    p=Process(target=run,args=('子进程',))
    p.start()
    run('父进程')
```



若父进程启动了多个子进程，由于进程创建时间的耗费、调度周期、进程本身代码等因素，进程的执行顺序不一定是原先的启动顺序。使用`Process()`创建的子进程再启动后，运行即与父进程独立，当其结束后，若父进程仍在运行，会转为僵死态Z，等待被父进程回收。若父进程已经消亡，会被1号进程收养进行回收操作。



### 进程通信

父进程创建子进程后，子进程复制父进程的资源（实际只是创建虚拟地址与物理地址的映射关系）。**子进程对变量的修改，无论是全局变量、原地可变类型，父进程均不可见**。父子进程的通信要使用特殊的机制。

> CopyOnWrite写时复制技术_：
>
> fork()之后，kernel把父进程中所有的内存页的权限都设为read-only，然后子进程的地址空间指向父进程。当父子进程都只读内存时，相安无事。当其中某个进程写内存时，CPU硬件检测到内存页是read-only的，于是触发页异常中断（page-fault），陷入kernel的一个中断例程。中断例程中，kernel就会把触发的异常的页复制一份，于是父子进程各自持有独立的一份。

#### 队列

队列操作：`from multiprocessing import Queue`

* 创建：`queue=Queue(num)`，num缺省时队列动态增长。 
* 存放：`queue.put(obj,block=True)`，默认阻塞，队列满时触发
* 取出：`queue.get(block=True)`，默认阻塞，若队列为空，将等待直到有消息出现。
* 队列长度：`queue.qsize()` 



主进程创建变量queue后，必须显式传入子进程。

```python
import  os
import time
from multiprocessing import Process,Queue

def queue_puts():	#往队列中存放消息
    for i in b'123':	
        queue.put(i)
        print('进程{}放入消息：{}'.format(os.getpid(), i))
        time.sleep(1)

def queue_gets(queue,count):	#往队列中取出消息 
    ctr=0
    while ctr<count:
        print('进程{}取出消息：{}'.format(os.getpid(), queue.get()))
        ctr+=1


if __name__ == '__main__':
    queue=Queue()
    p1=Process(target=queue_gets,args=(queue,3,))
    queue_puts()
    p1.start()
    p1.join()	#阻塞等待p1取出3个消息

```



#### 管道

管道，实质是一个缓冲区，用于两个进程间通信。



管道操作：`from multiprocessing import Pipe` 

* 创建：`read_port,write_port=Pipe(duplex=False)`，**默认半双工机制**，返回2元组，前一个端口只能读、后一个端口只能写。设置关键字参数`duplex=True`可以使管道为全双工，两个端口均可读写。
* 收发：`port.send()`，发送数据。`port.recv()` ，阻塞接收数据。与TCP的读写不同，管道的读写一一对应，不存在多次`send`一次`recv`取出的情况。



主进程中创建管道变量后，需要显式往子进程传入另外一个管道端口。

```python
import os
from multiprocessing import  Process ,Pipe

def pipe_recv(read_port):
    info=read_port.recv() 
    print('进程{}接收到数据{}'.format(os.getpid(),info))	#在子进程中读取管道数据 


if __name__ == '__main__':
    read_port,write_port=Pipe(duplex=True)
    p=Process(target=pipe_recv,args=(read_port,))	#传递管道口

    write_port.send('hello')	#主进程中往管道写入数据'hello'
    p.start()

```



#### 进程池

进程池，批量创建子进程，初始状态均为sleep，当有任务分配时被唤醒，任务完成后继续进入sleep状态。若进程中所有进程均在忙碌，则该任务等待某一个进程结束。**主进程结束后进程池中的子进程结束运行**。



进程池操作：`from multiprocessing import Pool` 

* 进程池创建：`pool=Pool(num)`，创建大小为num的进程池，num缺省时默认为CPU核数。创建的进程池变量必须被函数、或者`if __name__=='__main__'`包裹，否则会报错`AttributeError` 。理由是出于`import your module`安全考虑，若直接将`Pool()`定义在顶层，则导入的时候脚本执行，会自动创建若干Sleep的线程，这显然不安全。

  > The `multiprocessing` module needs to be able to **import your module safely.** Any code not inside a function or class should be protected by the standard Python import guard

* 任务分发：使用`pool.apply_async(func,args)`为进程池中的的进程非阻塞性地**分配任务**，任务提交到进程池即返回。**func函数必须定义在顶层，不可以是类函数**，否则报错。args为参数。当所传参数错误时，子进程不会被启动也不会有报错提示。 

* 关闭进程：
  * `pool.terminate()`：不等进程池中的进程运行完，强制结束所有子进程。等效于`kill -15`
  * `pool.close()`：通知进程池的进程关闭，但会等待其运行结束。同时，进程池不再分发新的任务给子进程。若进程池的函数退出使用了`exit`，将会使`close`运行异常。
  * `pool.join()`：阻塞，等待进程结束，回收进程池的资源。

```python
from multiprocessing import Pool

def run(s):	#函数必须定义在顶层
    print(s)

if __name__ == '__main__':
    pool=Pool(2)	#线程池数量为2
    pool.apply_async(func=queue_gets,args=('hello',))	#分发任务
    pool.close()	#关闭进程池
    pool.join()	#回收
```



进程池间的进程通信需要使用`multiprocessing.Manage().Queue(num)`队列，对于由`Process()`类创建的进程，只需要使用`Queue()`通信即可，注意区分。当队列长度num缺省时，默认动态增长。

队列`queue`可以在父进程中声明为全局变量，当子进程需要以该队列进行通信时，需要显式地传入该`queue`对象作为参数。队列的操作与普通`Queue()`相同。



```python
'''
多进程下载文件夹，递归遍历，保持原目录结构
当下载完第一层文件目录时，存放消息队列
父进程取出比对长度
'''


import os
from  multiprocessing import Pool,Manager

def copy_file(file_name,dest_path,queue,recur_depth=0):	
    base=os.path.basename(file_name)	#取源文件文件名
    next_path=os.path.join(dest_path,base)	#拼接目的路径

    if os.path.isfile(file_name):	#文件，直接写入
        with open(file_name,'rb') as f1,open(next_path,'wb') as f2:
            f2.write(f1.read())
    else:	#文件夹，递归遍历
        if not os.path.exists(next_path): os.mkdir(next_path)  #创建文件夹
        for x in os.listdir(file_name):
            x=os.path.join(file_name,x)
            copy_file(x,next_path,queue,recur_depth+1)

    download_message='进程{}下载{}完毕'.format(os.getpid(),file_name)
    if recur_depth==0:queue.put(download_message)	#仅在第一层深度时打印消息 


def main(source_path,dest_path):	
    if os.path.exists(source_path):
        source_path=os.path.abspath(source_path)
        if os.path.isfile(source_path): 	#文件，直接写入
            with open(source_path,'rb') as f1,open(dest_path,'wb') as f2:
                f2.write(f1.read())
        else:
            if not os.path.exists(dest_path):os.mkdir(dest_path)	#创建

            process_pool=Pool()		#进程池创建
            queue=Manager().Queue()		#进程池进程通信
            total_files=[]
            for file_name in os.listdir(source_path):
                file_name=os.path.join(source_path,file_name)
                total_files.append(file_name)	#1级目录共有文件
                #启用子进程下载 
                process_pool.apply_async(func=copy_file,args=(file_name,dest_path,queue))

            download_files=[]
            while len(download_files)<len(total_files):
                download_files.append(queue.get())	#从子进程中取出已下载消息 
                download_percent=len(download_files)*100//len(total_files)
                print('\rprogress:[{}] {}%   {}'.format('#'*(download_percent//10),
                                                       download_percent,download_files[-1]))
    else:
        print('目标路径不存在!')

if __name__ == '__main__':
    source_path='../../week3'
    dest_path='hello'
    main(source_path,dest_path)
```



## 线程

线程，操作系统CPU分配的最小单位。python中多线程只能共用1核（使用一个解释器），无法像多进程一样使用多核（每个进程资源独立，有1个自己的GIL）。在进行IO密集型操作时，多线程具备优势。而在进行CPU密集型操作时，由于GIL锁的限制，任意时刻始终只有一个线程在运行，多线程可能因为切换的额外开销反而不如单线程。

* GIL锁：全局解释器锁，Cpyhton解释器的遗留产物（也就是说python和GIL可以无关）。为了保证线程安全，每个线程在执行的时候都需要先获取GIL，使得同一时刻只有1个线程在执行。在遇到IO阻塞操作、执行时间耗尽时，线程释放GIL。

  > In CPython, the global interpreter lock, or GIL, is a mutex that prevents multiple native threads from executing Python bytecodes at once. This lock is necessary mainly because CPython’s memory management is not thread-safe. (However, since the GIL exists, other features have grown to depend on the guarantees that it enforces.) 



线程操作：

* 创建线程：`threading.Thread(target,args)`创建线程，`target`为调用函数地址，`args`为函数所需参数，元组形式。

* 启动线程：使用`.start()`启动线程。Linux下，可用`ps -elLf`、`top`之后按`H`查看启动线程。

* 查看当前线程运行数目：`threading.enumrate()`，返回当前存活线程列表。`threading.active_count()`，返回当前存活线程数目。
* 回收线程：`.join()`，阻塞，等待线程结束。

```python
#多线程

import threading
import time 
def run(n):
    print("%d is running  " %n )
    time.sleep(2)

for i in range(3):
	t = threading.Thread(target=run,args=(i,))	
	t.start()

```



线程之间运行独立，**主线程结束并不会对子线程有影响**。进程默认会等待其所属线程全部运行完毕后再结束，若设置线程为“ 守护线程 ”，则进程不再等待该线程。

### 线程资源

线程本身只拥有运行时必需的一部分极少资源，但可与隶属同一进程的其他线程**共享其进程资源**。进程中的全局变量（global关键字）、原地可变变量（列表、字典、集合）在某个线程中被修改，其余线程可见。



线程锁（互斥锁mutex）：线程的执行顺序异步（参考《操作系统》进程同步），对变量的修改可能会发生**写覆盖**。应当设置互斥锁，使其成为临界资源，使得线程间访问互斥。

```python
import threading 
mutex=threading.Lock()	# 创建一个互斥锁

mutex.acquire()	#p操作，在修改前加锁
#修改临界资源
mutex.release()	#v操作，解锁 在修改后释放资源

```

一些情况下，可能对muex进行多次加锁，如函数递归调用、函数A调用了另外一个使用锁的函数B。由于mutex作为全局变量，**第一次被上锁后尚未释放，此时再次对其尝试上锁，就会被阻塞造成死锁的情况**。解决的办法就是将`Lock`替换成递归锁`RLock()`，在子函数被调用入栈时，以函数名为映射和另外再创建一锁`func_name:lock`解决冲突。

```python
import  threading
import  time

lock=threading.RLock()	#递归锁
#lock=threading.Lock()	#普通锁会造成死锁 

def jc(num,rec=0):
    lock.acquire()  #上锁
    print('rec:%d'%rec)
    if num==1 or num==0:
        res=1
    else:
        res=num*jc(num-1,rec+1)

    lock.release()  #在退出前解锁
    return  res


if __name__ == '__main__':
    t=threading.Thread(target=jc,args=(3,))
    t.start()
    lock.acquire()

    while True:
        time.sleep(1)
        print('alive threading:',threading.active_count())
```



信号量semaphore：设置资源数量num，同一时间访问量不超过num。mutex相当于资源数量为1的信号量。可以使用信号量实现类似进程池同一时间最大进程运行数的效果。信号量的使用和mutex类似。

```python
import threading 

def run():	#同一时间最多只运行5个
    semaphore.acquire()	#p操作-1
    #pass
    semaphore.release()	#v操作+1

if __name__=='__main__':
    semaphore=threading.BoundedSemaphore(5)	#设置5把锁 
    t=threading.Thread(target=run)
    
```



## 协程

协程（Coroutine），又名微线程，从属于线程，是单线程内函数协同工作的一种方式。

一个进程可以创建若干线程，一个线程又可以创建若干协程。进程是操作系统资源最小分配单位，线程是CPU运行最小调度单位，但协程本身不被操作系统感知，本质其实就是单线程内的函数，其调度由用户决定，其工作方式也一定是串行的。



协程的优点：

* 只是在线程内子函数切换，切换成本小于线程
* 单线程内串行执行，不用考虑互斥锁的问题
* 异步操作，尽可能利用CPU，执行效率高。

协程的缺点：

* 从属于线程，不能使用CPU多核优势。若希望程使用CPU多核资源，可以使用“ 多进程+协程 ”的方式。

* 进行IO操作时，如果其他函数依赖于该IO操作，则协程的调度毫无优势，其他函数依然需要阻塞等待。 

  

Python对协程的支持是通过generator实现的，原理是借助`yiled`在众多函数中来回切换。在不进行IO等阻塞操作时，函数正常执行，反之，函数挂起，切换到另一个函数执行。

***

`gevnet`是python中的第三方框架（需要`pip install gevent`安装），能够更轻松地使用协程。

在程序运行前，使用gevent的猴子补丁`monket.patch_all()`，该补丁在**运行时修改类或模块，替换相应的方法**，而不去改变源码，达到hot patch的目的。**猴子补丁必须放在所有import前，否则补丁无效。**



gevnet库操作：

* 启动：`g=gevent.spawn(func,*args)` ，创建一个greenlet对象放入gevent的调度队列，**但并不立即启动，在主函数下次遇到IO阻塞操作时，gevent才会进行调度**。换言之，若主函数一直没有遇到阻塞操作，那么gevnt就不会进行任何调度。
* 回收：`g.join()`，g为greenlet对象 ，阻塞等待其运行结束。
* 批量启动、回收：`gevent.joinall([greenlet_obj,gevent.spawn(func,*args),...])` ， 参数为greenlet对象列表 

```python
#批量请求网页时 协程与未使用协程的时间比对 
from gevent import monkey
monkey.patch_all()	#补丁，放在程序开头

from  urllib import  request
import time as t,gevent


def time_cost(func):		#时间耗费计算 
    def inner(*args,**argvs):
        t1=t.time()
        res=func(*args,**argvs)
        t2=t.time()
        print('\n耗时：{:.2f} ms '.format((t2-t1)*1000))
        return res
    return inner

def get_html(url):	#请求网页
    print('尝试打开网页：%s' % url)
    content=request.urlopen(url)
    print('{}返回码：{}'.format(url,content.getcode()))

@time_cost
def main(is_cr=True):	
    if not is_cr:
        print('未使用协程')
        for url in urls: get_html(url)
    else:
        print('使用协程')
        gevent.joinall([gevent.spawn(get_html, url) for url in urls])

if __name__ == '__main__':
    urls=['http://www.baidu.com/',
           'http://www.cskaoyan.com/',
           'https://www.cnblogs.com/']

    for i in [False,True]:
        main(i)
        print('='*30)
```





