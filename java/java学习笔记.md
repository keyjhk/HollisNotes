---

typora-copy-images-to: upload
---



# jdk、jre、jvm

* JVM**（Java Virtual Machine ）：Java虚拟机，简称JVM，是Java程序的运行环境之一。我们编写的Java代码，最终都运行在**JVM** 之上。
* **JRE ** (Java Runtime Environment) ：是Java程序的运行时环境，包含`JVM` 和运行时所需要的`核心类库`。
* **JDK**  (Java Development Kit)：是Java程序开发工具包，包含`JRE` 和开发人员使用的工具。

三者之间的关系

![image-20220621111858498](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220621111858498.png)

java是跨平台的，但是jvm不是跨平台的，它需要对接不同操作系统然后暴露同样的API给JAVA层调用。

![image-20220621111915931](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220621111915931.png)

# java ee  /se 

java se（standard edition）为标准版本，是整个java体系的基石，包含了最基础的规范，如面向对象、IO流等。

java ee （enterprise edition）为企业版本，**在se的基础上，添砖加瓦，增加了规范**，如servlet、mybatis等，用以b/s架构开发。

![img](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxNTY2MjE5,size_16,color_FFFFFF,t_70.png)



一台电脑安装多个版本JAVA：https://zhuanlan.zhihu.com/p/355793060  ，通过环境变量名区分 



版本变迁：

* 1.5是个版本变迁的时间点，在此之前，以`1.x`命名。
* 1.5 版本，为了表示版本重要性，更名为`5.0`版本，又称为java5，延续至java8（1.8） 
* java9以后取消`1.x`开头的前缀 



![image-20220624161106106](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220624161106106.png)

# IDEA

## 快捷键

| 按键         | 功能                                             |
| ------------ | ------------------------------------------------ |
| psvm         | 生成main方法                                     |
| **sout**     | 生成System.out.println();                        |
| soutp        | 生成对方法参数的打印                             |
| soutv        | 生成对前面已声明变量的打印                       |
| **fori**     | 生成带循环变量的for循环结构                      |
| ifn          | 生成判断某个变量是否为null的if语句               |
| inn          | 生成判断某个变量是否非null的if语句               |
| Ctrl+Alt+l   | 格式化代码                                       |
| Ctrl+d       | 复制行                                           |
| Ctrl+x       | 剪切行                                           |
| Ctrl+v       | 粘贴                                             |
| Ctrl+y       | 删除行                                           |
| Ctrl+/       | 添加或去除单行注释                               |
| shift+F6     | 重命名类或变量                                   |
| shift+Alt+↑  | 向上移动当前行代码                               |
| shift+Alt+↓  | 向下移动当前行代码                               |
| shift+enter  | 即使光标在行的中间，也能直接去下一行开始继续输入 |
| **Ctrl+n**   | 搜索类                                           |
| Ctrl+F12     | 显示类的成员                                     |
| Ctrl+shift+U | 切换大小写                                       |
| ctrl + p     | 在函数括号内，显示形参                           |



创建module时，公司或组织域名的倒序.项目名称.模块名称.具体包名.类名，最后一个大写的单词会作为类文件常见，前面的作为包名。

> com.atguigu.mall.product.service.ProductService



# 程序入口

Java程序的入口是main方法

```java
public static void main(String[] args){
    
}
```

源文件格式为`.java`，可以有多个类，**其中的public类必须唯一且与源文件名一致**。main入口推荐写在public类中。

main方法详解

- public 最大权限 : main方法的调用者是JVM
- static 无需对象,被类名直接调用。 JVM启动的时候使用类名.main启动程序
- void 无返回值，因为调用者是JVM
- main 固定方法名称
- args  字符串的数组。JVM调用方法main必须传递参数，后期对JVM设置参数

# 编译

```shell
javac HelloWorld.java # c表示compile的意思
java HelloWorld # 运行字节码文件.class 后缀不需要添加  因为JVM实际调用的是 类名.main 

# 在使用javac命令式，可以指定源文件的字符编码
javac -encoding utf-8 Review01.java
```



# 标识

变量命名规范

1. 类名、接口名等：每个单词的首字母都大写，形式：XxxYyyZzz。例如：HelloWorld，String，System等
2. 变量、方法名等：从第二个单词开始首字母大写，其余字母小写，形式：xxxYyyZzz。例如：age,name,bookName,main
3. 常量名等：每一个单词都大写，单词之间使用下划线_分割，形式：XXX_YYY_ZZZ，例如：MAX_VALUE,PI
4. 包名等：每一个单词都小写，单词之间使用点.分割，形式：xxx.yyy.zzz，例如：java.lang

# 输入输出

输入

```java
import java.util.Scanner 
    
Scanner scanner = new Scanner(System.in);  // inital ,read from stdin

// int 
int age = scanner.nextInt();  // int(input)
System.out.println("age="+age);

// boolean 
System.out.print("请输入一个布尔值：");
boolean flag = scanner.nextBoolean();

// string 
String strValue = scanner.next(); // 读取到空格停止
strValue = scanner.nextLine(); // 读取到回车停止 input()
```



****

输出

* **换行输出语句**：输出内容，完毕后进行换行，格式如下：

  ```java
  System.out.println(输出内容);
  ```

* **直接输出语句**：输出内容，完毕后不做任何处理，格式如下

  ```java
  System.out.print(输出内容);
  ```



# 流程控制

循环

```java
while( 布尔表达式 ) {
  //循环内容
    break;
    continue;
}

// 
do {
       //代码语句
}while(布尔表达式);

// for 
for(int x = 10; x < 20; x = x+1) {
}

// for 迭代数组
String [] names ={"James", "Larry", "Tom", "Lacy"};
for(String name: names){
    // type var: arr
}
```



条件控制

```java
if(){
    
}else if (){
    
}else{
    
}


// switch
switch(expression){
    case value :
       break; //可选
    case value :
       //语句
       break; //可选
    default : //可选
       //语句
}
```





# 数据类型

## 基本数据

四类八种基本数据类型，其中整数、浮点数又可以看做是数字类

![image-20220621171634305](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220621171634305.png)



Java的数据类型分为两大类：

- **基本数据类型**：包括 `整数`、`浮点数`、`字符`、`布尔`。 
- **引用数据类型**：包括 `类`、`数组`、`接口`  



使用`instanceof`判断某个对象是否属于实例

```java
( Object reference variable ) instanceof  (class/interface type)
```



不同进制的书写

```java
//十进制：正常表示

System.out.println(10);

// 二进制：0b或0B开头

System.out.println(0B10);

// 八进制：0开头

System.out.println(010);

// 十六进制：0x或0X开头

System.out.println(0X10);
```



## 类型转换

#### 自动类型转换

1. 高低精度混合运算给高精度时，低精度的会转化为高精度的

   ```java
   int i = 1;
   byte b = 1;
   double d = 1.0;
   
   double sum = i + b + d;//混合运算，升级为double
   ```

2. **当byte,short,char数据类型进行算术运算时，按照int类型处理**

   ```java
   byte b1 = 1;
   byte b2 = 2;
   // 编译报错，b1 + b2自动升级为int，short同理
   byte b3 = b1 + b2;
   byte b3 = (byte)(b1 + b2)
   
   char c1 = '0';
   char c2 = 'A';
   System.out.println(c1 + c2); //113 
   ```

3. 当把存储范围小的值（**常量、变量、表达式计算的结果值**）赋值给了存储范围大的变量时

   ```java
   short age = 15;
   int _age =  age;
   ```



#### 强制类型转换

格式：`(type)var`， boolean类型不参与运算

```java
// 高精度转为低精度 
int i = (int)3.14;//强制类型转换，损失精度
int i = 200;
byte b = (byte)i;//溢出

// 提升精度
int i = 0;
int j = 0;
double shang = (double)i/j;  
```



![image-20220621171716697](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220621171716697.png)

#### 特殊的数据类型转换

1、任意数据类型的数据与String类型进行“+”运算时，看作拼接操作

```java
System.out.println("" + 1 + 2); // 12
```

2、但是String类型不能通过强制类型()转换，转为其他的类型

```java
String str = "123";
int num = (int)str;//错误的
int num = Integer.parseInt(str);//后面才能讲到，借助包装类的方法才能转
```



## 基本数据类型对象包装类



  基本数据类型,一共有8种. 可以进行计算,但是功能上依然不够用，JDK提供了一套基本数据类型的包装类,功能增强,全部在lang包

| 基本数据类型 | 对应的包装类 |
| :----------: | :----------: |
|     byte     |     Byte     |
|    short     |    Short     |
|   **int**    | **Integer**  |
|     long     |     Long     |
|    float     |    Float     |
|    double    |    Double    |
|   boolean    |   Boolean    |
|     char     |  Character   |



基本数据类型的包装类：扩展基本类的功能 

Integer

```java
/**
* 创建Integer类的对象
* 构造方法,new
* static方法 valueOf
*/
public static void getInstance(){
    Integer i1 = new Integer(100);  // int 
    Integer i2 = new Integer("120"); // str2int 
    System.out.println(i1);
    System.out.println(i2);
	
    
    // valueOf 是类的静态方法 返回Integer类型
    Integer i3 = Integer.valueOf(200); 
    Integer i4 = Integer.valueOf("220");
    System.out.println(i3);
    System.out.println(i4);
    
    // 和String 相互转换 
    int i = Integer.parseInt("100"); // 返回int基本类型
    
    
}
```



自动装箱和自动拆箱在编译阶段会自动完成 

* 自动装箱 : 基本数据类型自动转成引用类型 int -> Integer
* 自动拆箱 : 引用类型自动转成基本数据类型 Integer ->int



```java
Integer a = Integer.valueOf(200);  // int 转 Integer 
a.intValue() // Integer 转 int 
```



# 数组

创建。数组的长度一经确定，就不再允许修改

```java
dataType[] arrayRefVar = new dataType[arraySize];  

// 动态创建
ageArray = new int[5];
// 静态创建 创建时就指定元素  无长度 
nameArray = new String[]{"foo", "bar", "biz"};
int[] numberArray = {5, 7, 11, 13, 17, 19};
```



![image-20220621171744632](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220621171744632.png)





**Arrays类位于 java.util 包中，主要包含了操纵数组的各种方法**，使用时导入`import java.util.Arrays`。 

* 排序：`.sort(Object[] array,func)` ，原地排序，第二个参数是比较排序的函数，可以是匿名函数

* 填充：`.fill(Object[] array,Object object)`  

* 转为字符串输出打印：`.toString(Object[] array)` ，直接打印会显示数据的地址

  ```java
  int[] nums = {2,5,0,4,1,-10};
  System.out.println(Arrays.toString(nums));
  /*
  * 结果:[2, 5, 0, 4, 1, -10]
  */

* 转换stream流 ：`.stream(array)`  

* 切片拷贝：`.copyOfRange(array,from,to)` ，左闭右开



二维格式数组

```java
// 格式1：动态初始化——创建数组对象时就指定了两个维度的数组长度
int[][] arr2d01 = new int[3][2];

// 格式2：动态初始化——仅指定第一个维度的数组长度
int[][] arr2d02 = new int[3][];
// Java中多维数组不必都是规则矩阵形式
arr2d02[0] = new int[]{3, 5, 7};
arr2d02[1] = new int[]{14, 21, 66, 89};
arr2d02[2] = new int[]{90, 100};
```

# String

```java
// 字符串一经创建，不允许修改
String name = "hollis"; // 存储在公共池中
String name = new String("hollis"); // 存储在堆中
```



* 获取字符串长度 ：`.length()`

* 拼接：`concat(string2)`  或者`+` 操作符，返回 string2 连接 string1 的新字符串

* 格式化：静态函数，`String.format("格式控制符",变量)`

  ```java
  double age = 25;
  String name = "hollis";
  System.out.println(String.format("name:%s\nage:%.2f\n",name,age));
  ```

* 返回第i个字符：`.chatAt(index)` 



### String

字符串的实现原理是用char[]数组表示。



String类的构造方法：

* `String(byte[] b)` 字节数组转成字符串,使用平台的默认字符集

  ```java
  byte[] bytes = {97,98,99,100};
  String str = new String(bytes);
  ```

* `String(byte[] b,int off,int len)` 字节数组转成字符串,使用平台的默认字符集,参数off数组的开始索引,len要转的个数

* `String(byte[] b,int off,int,len,String,charsetName)` ：字节数组转成字符串,使用平台的默认字符集,参数off数组的开始索引,len要转的个数,charsetName参数是你自己可以指定编码表



String 和 char数组互换

```java
char[] s = {'1','2','3'};
String a = new String(s); // char[] ==> string 
char[] b = a.toCharArray(); // string ==> char[]
```





String类的常用方法：

- **boolean equals(Object obj) 字符串之间的比较,两个字符串相同,返回true**
- boolean equalsIgnoreCase(String str ) 字符串之间的比较,两个字符串相同,返回true,忽略大小写
- boolean startWith(String str)判断字符串是否以另一个字符串开头,是开头就返回true
- boolean endsWith(String str)判断字符串是否以另一个字符串结尾,是结尾就返回true
- boolean contains(String str) 判断字符串中是否包含另一个字符串,完全包含返回true
- boolean isEmpty()判断字符串的长度是不是0,如果是0返回true
- **int length() ：字符串的长度获取依赖函数调用**
- char **charAt(int index) 返回指定索引上的单个字符**
- int indexOf(String str) 返回指定的字符串,在当前字符串中第一次出现的索引
- int lastIndexOf(String str) 返回指定的字符串,在当前字符串中最后一次出现的索引
- String **substring(int start,int end) ：截取字符串,参数表示开始索引和结束索引,包含开头索引,不包含结束索引**



String类的转换方法

- `String toLowerCase()` ：字符串中的所有内容转成小写
- `String toUpperCase()` ：字符串中的所有内容转成大写
- `char[] toCharArray() `：字符串转成字符数组
- `byte[]  getBytes() `：字符串转成字节数组 (查询编码表),平台默认字符集
- `byte[]  getBytes(String charsetName)` ：字符串转成字节数组 (查询编码表),指定编码表
- `static String valueOf(任意类型参数)` ：参数转成字符串对象
- `int compareTo(String str) `：字符串之间的比较,谁大谁小,按照字典顺序(自然顺序)
- `String trim()` ：去掉字符串两边空格,中间空格不去掉
- `String replace(String oldString,String newString)`：替换字符串
- `String[] split("规则字符串") `：对字符串进行切割
- `.matches(reg)`：reg是正则表达式 ，java中没有原生字符串这个概念，因此，正则表达式中要用`\`转义`\`。 



**在java中，尤其注意`==`表示内存地址比较，而`.equals()`可以自定义，常用于内容比较。**

注意下面的`s7 == (s5+s6)`，和 `s7 == ("how"+"you")`，两者结果并不相等。

```java
String s1= "hello",s2 = "world";
System.out.println((s1 + s2).equals("helloworld")); // true
System.out.println(s1 + s2 == "helloworld"); // false
```

​	

### StringBuilder

 StringBuilder，**一个可变的字符序列**，字符序列就是字符数组。 StringBuilder类是线程不安全的类,运行速度快 , 推荐使用StringBuilder。StringBuffer是线程安全的类,运行速度慢,多线程的程序,使用StringBuffer 

```java
// String 的原理就是一个被final修饰的char数组 
String: private final char[] value;  // final 锁死
StringBuilder : char[] value; // 可变
```

 创建对象的时候，StringBuilder中的数组的初始化长度为16个字符，StringBuilder自动的进行数组的扩容，新数组实现将原来数组的中元素复制到新的数组。



* `StringBuilder append(任意类型) `：参数追加成字符串，相当于是字符串里面的 + String(value)

* `StringBuilder insert(int 索引, 任意类型)`：可以将任意类型的参数,插入到字符串缓冲区,指定索引

  ```java
  /*
  * StringBuilder类的方法insert,指定位置,插入元素
  */
  
  public static void builderInsert(){
      StringBuilder builder = new StringBuilder();
      builder.append("bcdef");
      //指定的索引上,添加字符串,原有字符,顺延
      builder.insert(2,"QQ");
      System.out.println("builder = " + builder);
  }
  ```

* `int length() `：返回字符串缓冲区的长度

* `StringBuilder delete(int start,int end)`：删除缓冲区中的字符,包含开头索引，不包含结束索引

* `void setCharAt(int 索引,char ch)`：修改指定元素上的字符

* `StringBuilder reverse()` ：翻转字符串



StringBuilder对象和String对象转换：

```java
/*
*  StringBuilder -> String
*/
    public static void stringBuilderToString(){
        StringBuilder builder = new StringBuilder();
        builder.append("我是字符串的缓冲区");

        String str = builder.toString();  //builder对象转成String对象
        System.out.println(str);

        String s = new String(builder);  //String类的构造方法
        System.out.println(s);
   }
```



# 集合

## Collection

存储对象的容器，但是不定长。**另外，其只能存储对象，基本类型并不适用**。



集合框架的继承体系，接口作为抽象类，不能直接实例化，实现类才是最后可以创建实例的类 

- Collection (集合) 接口  **单列集合**
  - List 接口
    - ArrayList (数组列表) 实现类
    - LinkedList (链表) 实现类
  - Set 接口
    - HashSet(哈希表) 实现类
      - LinkedHashSet(链表哈希表) 实现类,继承HashSet
    - TreeSet(红黑树) 实现类
  - Queue 接口
    - Deque
    - LinkedList 实现类  
    - PriorityQueue
    - BlockingQueue
  
  

Collection类是一个集合接口，作为List、Set等类的父类，提供了集合对象的基本操作接口，使操作趋于统一。

|      方法的定义       |                        方法作用                         |
| :-------------------: | :-----------------------------------------------------: |
|  **get(int index)**   |                   访问集合的对应元素                    |
|  **boolean add(E)**   |                     元素添加到集合                      |
|     void clear()      |                  清空集合容器中的元素                   |
|  boolean contains(E)  |                  判断元素是否在集合中                   |
| **boolean isEmpty()** |            判断集合的长度是不是0,是0返回true            |
|    **int size()**     |             返回集合的长度,集合中元素的个数             |
| **boolean remove(E)** | 移除集合中指定的元素（最先遇到的那个）,移除成功返回true |
|  T[] toArray(T[] a)   |                      集合转成数组                       |



Collecitons 类是一个工具类，该类不能实例化，**类的静态接口多服务于Collection类**，就像Arrays工具类服务于Array一样

`import java.util.Collections`

* `.max(col)` ，`.min(col)`：求取最大值、最小值

* `.binarySearch(Col,val)`： 在集合中二分查找  一个值 

* `.sort(list,<Collections.reverseOrder()>)`：对集合进行排序 ，第二个参数表示逆序从大到小 

  



### Iterator

迭代器是为了遍历集合而生，Collection类定义了方法`iterator() `，**该方法返回一个迭代器**。



Iterator的方法：

- boolean hasNext() 判断集合中是否有下一个可以遍历的元素,如果有返回true
- E next() 获取集合中下一个元素
- void remove() 移除遍历到的元素



```java
public static void main(String[] args) {
    //迭代器遍历集合
    //接口多态创建集合容器对象,存储的数据类型是字符串
    Collection<String> coll = new ArrayList<>();
    //集合对象的方法add添加元素
    coll.add("hello");
    coll.add("world");
    
    // 集合对象,调用方法iterator() 获取迭代器接口的实现类对象
    // 迭代器类型取决于集合类型 
    Iterator<String> it = coll.iterator();
    //2 迭代器对象的方法,判断集合是否有下元素
    while ( it.hasNext() ){
        String str =  it.next();  // 获取到下一个元素
        System.out.println(str);
    }
}
```

迭代器在遍历集合的时候，不应该修改集合长度，否则会异常。



迭代器实现原理

```java
interface Iterator{
    boolean hasNext();
    E next();
    void remove();
}

public class ArrayList {
    public Iterator iterator(){
        return  new Itr();
    }
    
    private class Itr implements Iterator{
         boolean hasNext(); //重写
    	 E next(); //重写
         void remove(); //重写
    }
    
}
```





### List

实现类：

* ArrayList 基于数组 
* LinkedList 基于链表



List 常用接口

```java
List<String> list = new ArrayList<>();
list.add("a") ;//集合的尾部添加
list.add(0,"a") ;// index = 0 处添加 
list.get(1); // get
list.set(1,"https://www.baidu.com"); // set 
list.remove(1); // remove  
```



list 和 数组的相互转换： 

* list --> 数组： `list.toArray()`
* 数组 --> list： `Arrays.asList()`





List 有其特有的迭代器，`ListIterator` 

- boolean hasNext()
- E next()
- boolean hasPrevious() 判断集合中是否有上一个元素,反向遍历
- E previous() 取出集合的上一个元素





### Set

Set集合,是接口Set，**继承Collection接口**。Set集合不存储重复元素 

```java
public static void main(String[] args) {
    //Set集合存储并迭代
    Set<String> set = new HashSet<String>();
    //存储元素方法 add
    set.add("a");
    
	// 遍历 
    Iterator<String> it = set.iterator();
    while (it.hasNext()){
        System.out.println(it.next());
    }
}
```



HashSet 底层实现是哈希表HashMap，Object类拥有哈希值计算等方法。

```java
public native int hashCode(); // C++语言编写,不开源 

//  两个对象的哈希值相同,equals不一定返回true.因为这两个内存地址可能不在一处
// 两个对象的equals返回true（意味着是同一个东西）,两个对象的哈希值必须一致


// e.g 
public static void main(String[] args) {
    Person p = new Person();
    int code = p.hashCode();
    System.out.println(code);
 }
```



* Object push(Object element)：压入栈顶

### Stack

vector的子类，实现了标准的先进后出栈。

* boolean empty() ：栈是否为空 
* Object peek( )：返回栈顶元素 ，但是不弹出 
* Object pop( )：弹出栈顶元素 



### Queue

Queue类除了继承Colleciton类的接口以外，还有自己的方法：

* `boolean offer(E e)`：尾部添加元素 
* `E poll()`：出队队首元素 
* `E peek()`：（注意和栈顶的peek区分）获取队首元素但不删除



Dequeue 双向队列，接口类：

* **addFirst():** 向队头插入元素，如果插入成功返回true，否则返回false
* **addLast():** 向队尾插入元素，如果插入成功返回true，否则返回false
* **removeFirst():** 返回并移除队头元素，如果队列无元素，则返回*null*
* **removeLast():** 返回并移除队尾元素，如果队列无元素，则返回*null*
* **peekFirst():** 获取队头元素但不移除，如果队列无元素，则返回*null*
* **peekLast():** 获取队尾元素但不移除，如果队列无元素，则返回*null*



**Dequeue被推荐代替stack的实现类**。 



实现类：

* LinkedList 基于链表实现的链式双向队列
* ArrayDeque:基于数组实现的线性双向队列

## Map

Map (映射键值对) 接口  **双列集合**  

- HashMap(哈希表) 实现类
  - LinkedHashMap(链表哈希表) 实现类,继承HashMap
- TreeMap(红黑树) 实现类 
- ConCurrentHashMap (哈希表) 线程相关



### HashMap

HashMap 类位于 java.util 包中，使用前需要引入它，语法格式如下

```java
import java.util.HashMap; // 引入 HashMap 类
// 创建 HashMap 对象 Sites
// 前一个是key类型 后一个是value类型 
HashMap<Integer, String> Sites = new HashMap<Integer, String>() 
    
// add
Sites.put(1, "Google");

// get
Sites.get(2)  // 访问key=3 
Sites.getOrDefault(2,0) // 如果key不存在 返回0

// delete
Sites.remove(1);  // 移除键值对

// size 
Sites.size(); // 计算元素数量 
```



常用接口：

- `.values()`：返回所有value的集合 

- `boolean containsKey(K)`：判断集合是否包含这个键，

- `boolean containsValue(V)`：判断集合是否包含这个值

- `.entrySet()` ：以set的形式返回map中的键值对集合，类似python的`set(dict.items())`  。集合的每一个元素都是`Map.Entry<K,V>` 对象 ，对于每一个键值对，使用`.getKey()`、`.getValue()`分别得到键和值。 

  ```java
  Map<String,Integer> map = new HashMap<>();
  map.put("hollis",1);
  map.put("jhk",1);
  Set<Map.Entry<String,Integer>> entrySet = map.entrySet(); // 键值对集合 
  for(Map.Entry<String,Integer> m:entrySet){ // 集合里的每个元素都是Entry对象 
      System.out.println(String.format("key: %s value : %s",m.getKey(),m.getValue()));
  }
  ```
  
  
  
  

**迭代：**

如果你只想获取 key，可以使用 keySet() 方法。如果你只想获取 value，可以使用 values() 方法。当然也可以使用`.entrySet()`迭代。

```java
// 输出 key 和 value
for (Integer i : Sites.keySet()) {
            System.out.println("key: " + i + " value: " + Sites.get(i));
}

// 返回所有 value 值
for(String value: Sites.values()) {
    // 输出每一个value
    System.out.print(value + ", ");
}
```



## 泛型

泛型，**定义的时候并不明确声明类型，而是在实例化的时候才明确**，例如集合中的ArrayList等。



自定义泛型类

```java
// 自定义泛型类 
public class Factory<QQ> {
    private QQ q; // q的类型取决于实例化时候得到的类型

    public void setQ(QQ q){
        this.q = q;
    }

    public QQ getQ(){
        return q;
    }
}


// 自定义泛型接口 
public interface Inter <T> {
    public abstract void inter(T t);
}

// 继承泛型类 或者 实现泛型接口的时候做法如下

// 1. 保持泛型
public class InterImpl<T> implements Inter<T>{
    public void inter(T t){
        System.out.println(t);
    }
}

// 2. 实现泛型
public class InterImpl2 implements Inter<String> {

    public void inter(String s) {
        System.out.println("s=="+s);
    }
}
```



泛型通配符号：代指其中一种java类型 ，约定俗成如下：

* ？表示不确定的任意java 类型

* T (type) 表示具体的一个java类型

* K V (key value) 分别代表java键值中的Key Value

* E (element) 代表Element

* ？ extends T ：上界通配符，任意继承T的类或者T类

  ```java
  // 获取任意类型集合 并迭代它 
  public static void each(List<?> list){
      Iterator<?> it = list.iterator();
      while (it.hasNext()){
          Object obj = it.next();
          System.out.println(obj);
      }
  }
  ```

  

* ? super T ： 下界通配符，任意T的父类或者T类 



T 和 ？ 的区别在于 T表示明确的，这在函数参数声明的时候有用

```java
public <T> void test(List<T> dest, List<T> src); // 前后两个参数类型应该一致 

// 在实际调用时如果这么写 就会报错  
// 如果 List<?> 就不会有问题 ，因为？表示任意
test(List<T> dest, List<T> src); 
```





# 异常捕获

-   java.lang.Throwable : 所有异常和错误的父类
    - java.lang.Error : 所有**错误**的父类
    - java.lang.Exception : 所有**异常**的父类
      - java.lang.RuntimeExeption : 所有的运行异常父类

> 错误: 程序中出现了错误,程序人员只能修改代码,否则不能运行
>
> 异常: 程序中出现了异常,可以把异常处理调用,程序继续执行

Throwable 的方法

- String toString() 返回异常信息简短描述  (控制台红色部分)
- **String getMessage()** ：返回异常信息的详细描述
- void printStackTrace() 异常信息追踪到标准的错误流



抛出异常：

1. throw：代码块中主动抛出 

   ```java
   throw new NumberFormatException();
   ```

2. throws ： 声明方法时抛出异常 

   ```java
   public void function() throws Exception
   {......
   }
   ```

   



一个异常捕获的代码块 

```java
// try 代码后不能既没 catch 块也没 finally 块
try{
  // 程序代码
}catch(异常类型1 异常的变量名1){
  // 程序代码
}catch(异常类型2 异常的变量名2){
  // 程序代码
}finally{
  // 程序代码 无论异常与否 都需要执行的 
  // 比如资源释放 
}
```



自定义异常 ，继承继承Exception或者RuntimeException

```java
public class ScoreException extends RuntimeException{
    public ScoreException(String s){
        super(s); // 调用父类的构造方法，传递异常信息
    }
}
```







## 函数

函数内部不再允许声明函数。

java没有默认参数，转而使用多态的形式。

### 重载

```java
// 参数个数不同
public int add(int a, int b)
public int add(int a, int b, int c)
    
// 参数类型不同 或 返回值不同 
public int add(int a, int b)
public double add(double a, double b) 
```

### 可变参数

`type ... name `，特殊之处在于省略号，可变参数的位置必须在整个参数列表的最后。

```java
public String add(String ... args) {
	// args 将作为一个数组 
    System.out.println("暗号：可变参数");

    String sum = "";

    // 在方法体内，可变参数按照数组形式来处理
    for (int i = 0; i < args.length; i++) {
        sum = sum + args[i];
    }

    return sum;
}
```





# 类

类在结构上，包含成员变量field和成员函数method。



```java
public class Person {

    // 属性/成员变量
    int weight;
   	
   	Person(){  // constructor
        // 构造函数和类名同名，且没有返回值
        // 构造函数允许有形式参数 
        weight = 10;
    }
    // 方法/成员函数
    public void eat(int food) {
        weight = weight + food;
    }

}

Person p = new Person();
```



### equals 和 ==

`==` 操作符被用于比较内存地址，

`.equals()` 方法被用于引用对象的比较，**不被重写的情况下**，等效于`==`。



### 修饰符

修饰符的位置在函数返回类型前，如

```java
public static void main(String args[])
```

#### 权限修饰

访问控制修饰

* public ：全部可见
* private ：类内可见，仅用于成员变量
* protected ：类内和子类可见。protected是特殊的，一旦方法受保护，正解是在子类中使用`super.method()` 调用。

| 修饰符名称 | 含义   | 本类 | 同包其他类 | 子类 | 同工程其他类 |
| ---------- | ------ | ---- | ---------- | ---- | ------------ |
| private    | 私有   | √    | ×          | ×    | ×            |
| default    | 缺省   | √    | √          | ×    | ×            |
| protected  | 受保护 | √    | √          | √    | ×            |
| public     | 公共   | √    | √          | √    | √            |



#### 静态修饰符 

静态修饰符：`static` 

被static修饰的成员变量或者函数归属于类本身，**无论实例化多少次，只有一份拷贝**。

**静态函数内部不允许访问非静态成员变量**，因为后者属于实例变量，而静态数据会优先于实例进入内存。 同时，对象可以访问静态变量，这会被编译器翻译为`类名.变量` 

```java
public class Person {
    String name;
    static String country = "中国";  // 静态变量 
}
```



#### final

* 被final修饰的类，称为最终类，不能被其他的类继承,无子类.

* 被final修饰的方法，不能被子类重写

* 被final修饰的局部变量，看做是常量

* final修饰了方法的参数，调用者传递值后，方法的参数值就锁死

  ```java
  public static void show(final int x){
      x = 6; //final修饰,不可改变,报错
  }
  ```

* final修饰成员变量 **，在构造函数阶段允许赋值，之后就不再允许修改** 





### package

用来声明当前类所在的包。package声明所在包的语句必须是在类的第一行。若缺省该语句，则指定为无名包。

![image-20220621171811772](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220621171811772.png)



格式为`package 包名`

### this

java中，**this不是必须的**。this指向当前对象

* 调用成员方法时，this可以省略，编译器会知道调用哪一个

* **如果成员函数的形参和成员变量同名，则加上this可以区分**

* 构造函数之间的调用，因为构造函数和类名是重名的，直接`类名()`这种形式会被认为尝试新建一个对象。

  ```java
  public class Tiger {
  
      private String tigerName;
      private int tigerAge;
  
      public Tiger() {
          System.out.println("这里是Tiger类的无参构造器");
      }
  
      public Tiger(String tigerName) {
  
          this();  // 构造函数互相调用时，this必须放在第一行 
  
          this.tigerName = tigerName;
  
          System.out.println("这里是Tiger类的一参构造器");
  
      }
  
      public Tiger(String tigerName, int tigerAge) {
  
          this("aaa");
  
          this.tigerName = tigerName;
          this.tigerAge = tigerAge;
  
          System.out.println("这里是Tiger类的两参构造器");
      }
  }
  ```

  

### import

在JDK编译Java源程序的时候，并不能保证所有的类都能够被JDK默认识别

```java
import java.util.Scanner; // 精确导入 某个类
import java.util.*; // 全部导入
```

- 使用的位置：在package声明和类声明之间
- **如果导入的类或接口是java.lang包下的，或者是当前包下的，则可以省略此import语句。**
- **如果导入一个类之后，又需要用到另一个同名的类，那么就需要使用全类名来引用**（没有pytho中取别名的做法）

```java
// 这里导入了一个Book类
import java.awt.print.Book;

public class ImportTest {

    public static void main(String[] args) {
        
        // 但是这里又要使用另外一个Book类
        // 为了区分二者，这里使用全类名来引用
        com.atguigu.object.test.Book book = new com.atguigu.object.test.Book();
    }
    
}
```

- import static组合的使用：静态导入。让当前类可以直接调用导入的类中的静态属性或方法，不必写类名了。





### 继承

格式

```java
// 一个类只能继承一个类,不允许同时继承多个类
class B{}
class A extends B{}  // A 继承 B类
```

继承以后，`super` 关键字可以调用父类

```java
super.变量   // 调用父的成员变量
super.方法() // 调用的是父类的成员方法
```



**继承的子类构造方法特点:** 子类的构造方法中,第一行存在隐式代码 (写不写都存在),代码是**super();** 会调用父类的无参数构造方法。 

```java
public class Fu  {
    public Fu(){
        System.out.println("父类构造方法");
    }
}

public class Zi extends Fu {
    public Zi(){
        super(); //调用父类的无参数构造方法.
        System.out.println("子类构造方法");
	}
}
```

#### 重载overload

重载发生在类内部或者父子类之间（因为子类会继承得到父类的方法），**多个同名的成员方法依靠参数类型、数量来区分**，使得同一种函数在实际传参不同时，有不同的表现。

```java
class Animal {

    void bark(){
        System.out.println("barking……");
    }

    void bark(String b){
        System.out.println("barking……"+b);
    }
}
```

#### 重写override

子类的成员变量和成员函数允许被重写，当访问子类不存在的成员时，会顺着继承链条逐级往上。 **注意，这里的覆盖更类似于“屏蔽”**，子类的成员变量即使和父类成员变量同名，他们的内存地址也不相同。在调用`super`关键字，依旧能够访问到父类的成员。

```java
class A {
    int a = 1;
    double d = 2.0;

    void show() {
        System.out.println("Class A: a=" + a + "\td=" );
    }
}

class B extends A {

    int a = 3;
    double d = 10.0;
    
    void show() {  // 重写了父类的show()
        super.show();
        System.out.println("Class B: a=" + a + "\td=" + d );
    }
}



// 尝试如下代码 
A  a = new A();
a.show();  
B b = new B(); // 父类A的属性依旧能被访问到
b.show();	

/*
Class A: a=1	d=2.0
说明super在B实例的情况下，也是能访问到A类中的成员变量
据此推测 B的实例在内存中的结构应该是 instanceA + instanceB 
Class A: a=1	d=2.0 
Class B: a=3	d=10.0 

*/
```



**重写和重载的区别在于，重载以参数类型和参数数量来区分彼此，实际是不同的东西。但是重写则明确地是覆盖了同一个东西**，他们的参数形式和返回类型完全一致，只是内在实现不同。在重写时，java可以使用`@Override`来表示紧跟着的方法是被重写的，它不是明确要求的，但是编译器会检查 重写的方法名字和参数是否与父类保持一致。

```java
class Cat extends Animal{

    @Override
    void bark(){
        System.out.println("cat miao~");
    }
}
```



方法重写需要考虑权限，**保证子类方法的权限要大于或者等于父类方法权限**（不然就会存在权限缩小，导致接口消亡，继承也无从谈起）



### 对象多态性

即使是被声明为一个类，但是也具备不同的形态。



对象多态性的前提：

- **必须有继承或者是接口实现**
- **必须有方法的重写**



**多态的语法规则:** 父类或者接口的引用指向自己的子类的对象

```properties
父类 变量(对象名)  =  new 子类对象(); //多态写法
```

如上创建实例后，子类实例会向上转型到父类，子类添加的方法将不能被访问。

**在调用成员变量或者函数时，编译阶段会检查 `=` 左边的类，即声明类是否存在，然而在实际运行阶段，调用函数会实际指向右边的子类实例，这就是方法的多态性。而成员变量自始至终都指向`=`左边的类，在编译阶段即可确定，不具备多态性。**



由于父类的声明可以兼容子类的对象实例，**所以在函数声明时，使用父类形参，就可以让函数支持多态**。





### 抽象类

使用`abstract` 修饰方法，若一个类中存在抽象方法，那么该类也必须作为抽象类

```java
public abstract class Animal {
	// eat方法使用了abstrac关键字修饰 
    // 对于抽象类 在()后直接;结束 也不需要{}
    public abstract void eat();
}
```

抽象类本身不能实例化，即不能new对象。**它需要子类继承并实现它的所有抽象方法，否则，该子类依旧是抽象类**。

```java
public class Cat extends Animal{
	// Cat 类继承了Animal 并实现了eat方法
    public  void eat(){
        System.out.println("猫吃鱼");
    }
}

public static void main(String[] args) {
    //创建Animal的子类对象
    Animal animal = new Cat();
    //eat方法不可能执行父类,运行子类的重写
    animal.eat();
}
```



抽象类虽然不允许直接实例化对象，但是它可以拥有构造函数、成员变量、非抽象的方法等和其余正常类一样的成员。



### 接口类

  **接口：就是一个规范,或者称为标准**  , 无论什么设备,只要符合接口标准,就可以正常使用。



接口是特殊的抽象类，当一个类方法全部都是抽象方法时，该类其实就是接口类。 

```java
public interface 接口名{}
```

当使用关键字interface创建一个接口类时，类方法默认就是`public abstract`。

```java
// public static final关键字 和 public abstract 多余 
public static final 数据类型  变量名 = 值 ;
public abstract 返回值类型 方法名(参数列表) ; 
```

JDK8以后，支持为方法添加static修饰符（类名调用）、default修饰符（抽象类的实现类的实例），被这些修饰符添加的方法，**可以定义方法体，不被子类重写**，调用时直接以`类名/对象.方法()`。

```java
public interface JDK8Interface {  
    // static修饰符定义静态方法  
    static void staticMethod() {  
        System.out.println("接口中的静态方法");  
    }  
  
    // default修饰符定义默认方法  
    default void defaultMethod() {  
        System.out.println("接口中的默认方法");  
    }  
} 
```





由于接口是抽象类，自然不能实例化，需要子类继承实现，实现的格式 `class 类 implements 接口名{}`。 

```java
public interface MyInterFace {
    //接口的成员变量
    public static final int A = 1;
    //接口的成员方法
     void myInter();
}

// 重写接口
public class MyInterFaceImpl implements MyInterFace{
   public void myInter(){
       System.out.println("实现类实现接口,重写方法");
    }
}


public static void main(String[] args) {
    // 多态 即使声明类型是接口类 但是new的时候是实现类 所以没有问题
    MyInterFace my = new MyInterFaceImpl(); 
    my.myInter();
    System.out.println(my.A);
}
```

接口是对单继承的改良，允许一个类同时实现多个接口。当一个类继承了多个类、实现多个接口时：

* 如果子类（或实现类）继承的父类和其实现的接口**定义了同名同参的方法**，并且接口中的方法为default方法（都有函数体），那么该子类的对象调用该方法时（在子类没有重写该方法的情况下），**默认是父类的方法（类优先性）**
* **如果类实现了多个接口**，而且多个接口中定义了同名同参数的default方法（有函数体）**，在该类没有重写的情况下，就会报错（接口冲突）。如果想解决这个问题，就必须在该类中重写此方法。**



接口类属于抽象类，他们包含的抽象方法会影响是否可以创建实例，**类与类之间的继承并无影响，即抽象类可以被继承，也可以继承自其余类。**



### 静态代码块

使用`{}`包裹的，static修饰，新建实例的时候，会被运行一次

```java
class Person{
    static{
        // 静态代码块 只有第一次new的时候才会运行 
    }
    {
        // 非静态代码块
        // 每new一次就会运行一次
    }
}
```



当一个类中存在静态代码块、非静态代码块时，他们的执行顺序是这样的：

* 静态的优于非静态的 
* 代码块优于构造器 



e.g 

- 父类.class文件先进入内存
- 子类.class文件再进入内存
- 初始化父类的静态成员(变量,代码块,方法)
- 初始化子类的静态成员
- **运行父类的静态代码块 static{}**
- 运行子类的静态代码块
- **运行父类的构造代码块 {}**和构造方法
- **运行子类的构造代码块**和构造方法



### 内部类

  概述 : 所谓内部类,就是在一个类的内部,定义了另外的一个类

```java
class A{ //外部类,封闭类
    class B{} //内部类,嵌套类
}
```

 依据内部类的位置，分为

#### 成员内部类

成员内部类,是一个类定义在了另一个类的成员位置。这个内部类可以使用成员修饰符。内部类可以看见外部类的成员

```java
// 外部类名.内部类名 = new 外部类对象().new 内部类对象()

public class Outer {

    public void outer(){
        System.out.println("外部类的方法outer");
    }

    //内部类
    public class Inner{
        public void inner(){
            System.out.println("内部类的方法inner");
        }
    }
}

public static void main(String[] args) {
    //调用内部类的方法inner()
    Outer.Inner oi = new Outer().new Inner();
    oi.inner();
}
```

#### 局部内部类

定义在方法里面。方法内部可见

```java
class A{
    public void a(){
        class B{} //局部内部类
    }
}
```



e.g

```java
public class Outer {
    /**
     *  Inner类,是方法Outer的局部
     *  依然方法,才能被外界访问
     */
    public void outer(){
        class Inner{
            public void inner(){
                System.out.println("局部内部类的方法!!");
            }
        }
        
        //outer 方法内部可见
        Inner inner = new Inner();
        inner.inner();
    }
}
```



#### 匿名内部

简化书写的局部内部类。

匿名内部类使用的前提：

- 必须有接口实现,或者是类的继承。

- 格式 : 

  ```java
  new 接口或者父类(){
      //重写抽象方法
  };
  格式 == 实现类,实现接口,重写方法,创建对象
  ```



```java
interface MyInter {
    public abstract void inter();
    public abstract void inter2();
}

public InnerClassTest {
    public static void main(String[] args) {
        //匿名内部类,简化书写,不写实现类
        //同时调用多个重写方法
        /*
         *  new MyInter(){}; 是接口实现类的匿名对象
         * 多态 : 接口 变量 = 实现类对象
         */
       MyInter my =  new MyInter(){

            @Override
            public void inter() {
                System.out.println("实现类实现接口重写方法");
            }

            @Override
            public void inter2() {
                System.out.println("实现类实现接口重写方法2222");
            }
        };
       my.inter();
       my.inter2();
    }
}
```

## 常用类

### Object

万物源于Object，每个类都继承了object自带的诸多方法。

* toString()：对象的字符串展现形式，默认展现内存地址 。可以重写以后自定义对象的字符串展现形式

  ```java
  
  public String toString(){
      //结果是字符串,就是对象内地地址
  }
  ```

* equals()：对象之间用于比较，返回布尔值。默认比较内存地址

  ```python
  public boolean equals(Object obj){
      return this == obj ;
  }
  ```

### System类

  System系统类 : 定义在java.lang包中，该类不能实例化对象，不能new。类中的成员全部是静态修饰，类名直接调用



* static long currentTimeMillis() 返回自1970年1月1日,午夜零时,到你程序运行的这个时刻,所经过的毫秒值

* static void arrayCopy( Object src,int srcPos,Object dest, int destPos,int length  )复制数组的元素.

  - src : 要赋值的数据源,源数组
  - srcPos : 源数组的开始索引
  - dest : 要复制的目标数组
  - destPos : 目标数组的开始索引
  - length : 要复制的元素个数

  ```java
      public static void systemArraycopy(){
          int[] src = {1,3,5,7,9};
          int[] dest = {2,4,6,8,0};
          //数组元素的赋值 : src数组中的3,5 复制到dest数组中0索引开始
          System.arraycopy(src,1,dest,0,2);
          for(int x = 0 ;  x < src.length ;x++ ){
              System.out.println(dest[x]);
          }
      }
  ```

* static Properties getProperties() 返回当前的操作系统属性

  ```java
      /**
       *  static Properties getProperties() 返回当前的操作系统属性
       *  System.getProperty(String 键名)
       */
      public static void systemGetProperties(){
          Properties properties = System.getProperties();
          System.out.println(properties);
          String str = System.getProperty("os.name");
          System.out.println(str);
      }
  ```

### Math

- static double PI  圆周率
- static double E 自然数的底数
- static int abs(int a) 返回参数的绝对值 
- static double ceil(double d)返回大于或者等于参数的最小整数
- static double floor(double d)返回小于或者等于参数的最大整数
- static long round(double d)对参数四舍五入
- static double pow(double a,double b ) a的b次幂
- **static double random() 返回随机数 0.0-1.0之间**
- static double sqrt(double d)参数的平方根





### 大数运算

 基本数据类型long ,double 都是有取值范围。遇到超过范围的数据就需要引入了大数运算对象

java.math包 : BigInteger大整数, BigDecimal大浮点(高精度,不损失精度)

- BigInteger类使用,计算超大整数的
  - 构造方法直接new BigInteger(String str) 数字格式的字符串,长度任意
  - BigInteger  add(BigInteger b)计算两个BigInteger的数据求和
  - BigInteger  subtract(BigInteger b)计算两个BigInteger的数据求差
  - BigInteger  multiply(BigInteger b)计算两个BigInteger的数据求乘积
  - BigInteger  divide(BigInteger b)计算两个BigInteger的数据求商

```java
public static void main(String[] args) {
        //创建大数据运算对象
        BigInteger b1 = new BigInteger("2345673456786554678996546754434343244568435678986");
        BigInteger b2 = new BigInteger("8765432345678987654323456787654");

        //b1+b2 求和
        BigInteger add = b1.add(b2);
        System.out.println("add = " + add);

        //b1 - b2 求差
        BigInteger subtract = b1.subtract(b2);
        System.out.println("subtract = " + subtract);

        //b1 * b2 求积
        BigInteger multiply = b1.multiply(b2);
        System.out.println("multiply = " + multiply);
        
        //b1 / b2 求商
        BigInteger divide = b1.divide(b2);
        System.out.println("divide = " + divide);
    }
```



BigDecimal 类使用,计算超大浮点数

- 构造方法,和BigInteger一样

- 方法 + - * 和BigInteger一样

- BigDecimal  divide除法运算

- divide(BigDecimal  big,int scalar,int round)方法有三个参数

  - big 被除数

  - scalar 保留几位

  - round 保留方式， 该类的静态成员变量。可以取下列值

    - BigDecimal.ROUND_UP  向上+1

    - BigDecimal.ROUND_DOWN 直接舍去

    - BigDecimal.ROUND_HALF_UP 四舍五入

### 日期和日历

#### Date

构造：`new Date(int seconds)`。seconds可以缺省，会将毫秒数转为当前日期。

```java
 Date date = new Date();
//Tue Apr 13 10:33:40 CST 2021
System.out.println("date = " + date);
```

常用方法：

* long getTime() 返回当前日期对应的毫秒值
* void setTime(long 毫秒值) 日期设定到毫秒值上 

#### calendar

导入：java.util.Calendar。

Calendar属于抽象类，不能直接实例，用它的静态方法为其创建实例：`static Calendar getInstance()`，返回的是Calendar 的子类的对象GregorianCalendar （格林威治时间） 

```java
 Calendar calendar = Calendar.getInstance() ;
```



常用方法：

* 获取年月日时分秒：`.get(int field)`，filed是Calendar类定义的字段，包括 Calendar.YEAR、Calendar.MONTH等 
* 设置字段：
  * `.set(int field,value)`，字段即上述filed所言
  * `set(int,int,int) `传递年月日



日期格式化 ：使用类SimpleDateFormat()，可以将Date和字符串互相解析

```java
/**
* 日期格式化,自定义格式
*/
import java.text.SimpleDateFormat;
    
public static void format(){
    // 参数是 字符串
    SimpleDateFormat sdf = new SimpleDateFormat("yyyy年MM月dd日 HH点mm分ss秒");
    String str = sdf.format(new Date());  // format来格式化Date对象
    System.out.println(str);
    
    String dateString = "2021-04-13";
    //sdf对象的方法parse
    Date date = sdf.parse(dateString);
    System.out.println("date = " + date);
    
}
```



####  LocalDate

获取该类的对象,静态方法

- `static LocalDate now()`：获取LocalDate的对象,跟随操作系统
- `static LocalDate of(int year,int month,int day)`：获取LocalDate的对象,自己设置日期
- 获取日期字段：
  - `int getYear()`： 获取年份
  - `int getDayOfMonth()`：返回月中的天数
  - `int getMonthValue()` ：返回月份





# File

创建File对象

```java
File(String pathname)  // 文件路径
File(File parent, String child); // 父路径 + 子文件名
```



java的思路和python有所不同：

1. **创建/删除文件（夹）等操作完全取决于File对象初始化时的路径参数**

2. **相对路径默认以包路径开始，而非当前文件** 。

   ```java
   System.out.println(new File(".").getAbsolutePath()); // 查看当前文件路径 



常用api

* `list()`：列出当前路径下的文件，返回字符串
* `listFiles()`：同上，只是返回File对象 
* `long length()`：获取文件的字节数
* `public boolean mkdirs()`：创建多层文件夹
* `boolean createNewFile()`：创建一个文件 
* `boolean delete()`：删除文件
* `boolean exists() `：判断构造方法中的路径是否存在
* `boolean isDirectory()`：判断构造方法中的路径是不是文件夹
* `boolean isFile()`：判断构造方法中的路径是不是文件
* `boolean isAbsolute() `：判断构造方法中的路径是不是绝对路径 
* `File getParentFile()` ：获取父路径,返回值是File类型
* `String getPath()` ：获取File构造方法中的路径，完整的路径转成String返回
* `String getName()` ：获取basename名字



# 枚举

特殊的java类，用以提供有限选择。

```java
// 创建枚举类 
enum Gender{
    MALE,
    FAMALE; //  约定俗称大写 
}


// person类的性别中使用枚举 
class Person{
    String name;
    Gender gender; // 枚举类
    Person(String name,Gender gender){
        this.name=name;
        this.gender=gender;
    }
}

// 实例化时 
Person p = new Person("hollis",Gender.MALE);  // Gernder无需实例化 
```



枚举类，同样可以添加成员属性和函数。比如，为了便于阅读，在上面的gender类中添加tag

```java
enum Gender{
    MALE("man"),  // 其实是一个Gnder类 ，所以看做是构造函数
    FAMALE("woman"); 
    String tag; // 可以考虑将其私有化 然后提供getter方法 
    Gender(String tag){
        this.tag = tag;
    }
}

// main
Person p = new Person("hollis",Gender.MALE);
System.out.println(p.gender.tag); // man 
```





# IO流

IO：input and output，字节的输入输出流。

在java中，输入输出针对的是java程序，输出流——程序向外输出写入，输入流——程序接纳读入。



IO 对象分类：

- 字节输出流 : OutputStream 抽象类
- 字节输入流 : InputStream 抽象类
- 字符输出流 : Writer 抽象类
- 字符输入流 : Reader 抽象类



## 字节流

### OutputStream

`  java.io.OutputStream`，所有字节输出流的超类，可以写入任何类型文件。

**输出流的写入单位都是基于字节，不允许直接写字符串，但是可以使用`"".getBytes()`来得到字节数组**

* `void write(int b)` ：单个字节，int对应ASCII码表
* `void write(byte[] b)`：写入字节数组
* `void write(byte[] b,int off,int len) `：写入数组的一部分,开始索引,写入的个数



FileOutputStream用以向文件输出，构造方法：

* `FileOutputStream(File file,false)`，第二个参数为true时表示追加写入（append），默认为覆盖写入overwrite
* `FileOutputStream(String file)`

```java
/*
输出步骤：
创建输出流对象 
写入
关闭文件
*/

// 单字节写入 
FileOutputStream fos = new FileOutputStream("c:/1.txt");
//写入单个字节
fos.write(45);
fos.write(49); // 不带回车\n 
//释放资源
fos.close();

// 字节数组写入 
// 要抛出异常 
public static void writeByteArray() throws IOException {
    //创建字节输出流对象,构造方法中,绑定文件路径,写入目的
    FileOutputStream fos = new FileOutputStream("c:/1.txt");
    
    byte[] bytes = {97,98,99,100,101,102}; // ascii 
    fos.write(bytes);
    fos.write("\r\n".getBytes()); // 写入换行 
    fos.write("你好,我好,大家好".getBytes());
    fos.write(bytes,1,3); // 写入一部分 
    //释放资源
    fos.close();
}
```



安全地关闭资源，将文件操作放在try-catch代码块里，然后在finally中写close操作。

```java
// 写法1 自动close 类似python的with open
 try (FileOutputStream f = new FileOutputStream("test.txt")) {
     // 试图打开文件
     f.write("我爱北京天安门\n".getBytes(StandardCharsets.UTF_8));
     f.write("天安门上太阳升\n".getBytes(StandardCharsets.UTF_8));
} catch (IOException e) {
   e.printStackTrace();
}

// 写法2 手动捕获异常并close
FileOutputStream f  = null; // 指向null

try{
    f  = new FileOutputStream("test.txt"); // 试图打开文件
    f.write("我爱北京天安门\n".getBytes(StandardCharsets.UTF_8));
    f.write("天安门上太阳升\n".getBytes(StandardCharsets.UTF_8));
}catch (IOException e){

}finally {
    // 这里在打开多个文件时 还是要尝试try-catch
    try{
        if(f!=null) f.close(); // 关闭文件
    }
    catch (IOException e){}
}
```



### InputStream

`  java.io.InputStream`是所有字节输入流的超类 ， 可以读取任何类型文件

读取：基于字节

- `int read() `：读取单个字节（不适合中文1个字符对应多个字节），返回读取到的字节ascii码， **读取到流的末尾返回 -1**
- `int read(byte[] b)`：读取字节数组 , 返回此次读取到的字节数，读取到流的末尾返回 -1。 



` FileInputStream`用于文件读取，构造方法：

* `FileInputStream(File file)` 
* `FileInputStream(String file)`



```java
// 单字节读取 
try(FileInputStream f = new FileInputStream("test.txt")){
    int r;
    while ((r=f.read())!=-1){
        System.out.print((char) r);
    }

}catch (IOException i){
} 


// 字节数组
// 字节数组是每次重用的，即使读取到文件末尾的-1时，字节数组的也存在内容
// 所以，在转为字符串内容时，只取我们要的字节
try(FileInputStream f = new FileInputStream("test.txt")){
    byte[] buffer = new byte[1024];
    int r;
    while ((r=f.read(buffer))!=-1){
        System.out.print(new String(buffer,0,r)); // 只要读取到的r个字节
    }

}catch (IOException i){

}
```



基于字节输入输出流的文件复制

```java
FileInputStream fis = new FileInputStream(source);
FileOutputStream fos = new FileOutputStream(target);

byte[] buffer = new byte[1024];
int r;
while ((r = fis.read(buffer)) != -1) {
    fos.write(buffer, 0, r);
}
fis.close();
fos.close();
```



### Buffered

Buffered意为缓冲，java提供的缓冲输入输出流包括`BufferedInputStream`、`BufferedOutputStream` 。缓冲流为高级流，其余则为基准流，前者利用缓冲池对读写进行了优化。**基准流每次写都要进行一次IO操作，而缓冲流会在底层缓冲满以后才进行一次IO。**



**用缓冲流接管基准流的操作是简单的，只要在构造函数中传入基准流即可。关闭缓冲流，会一并关闭其接管的基准流。**

```java
FileInputStream fis = new FileInputStream(source);
FileOutputStream fos = new FileOutputStream(target);
BufferedInputStream bis = new BufferedInputStream(fis); // 接管输入流
BufferedOutputStream bos = new BufferedOutputStream(fos); // 接管输出流 

byte[] buffer = new byte[1024];
int r;
while ((r = bis.read(buffer)) != -1) {
    bos.write(buffer, 0, r);
}
bis.close();  // 关闭高级流即可 
bos.close();
```



## 字符流

**用于文本文件，以字符为单位写入。底层过程其实为字符到字节的编解码。**

字符流的使用过程中，仍旧要先创建字节流对象，然后作为参数初始化为字符流。

### Writer/Reader

Writer类，是所有字符输出流的父类 

- `write(int c) `：写入单个字符
- `write(char[] ch)`: 写入字符数组
- `write(char[] ch,int off,int len)`：写入字符数组一部分,开始索引,写入的个数
- `write(String str)`：写入字符串
- `void flush()`：  刷新该流的缓冲 (写入数据,先写入到内存), 只有刷新了数据才会到达目的文件



Reader类，是所有字符输入流的父类 

- `int read()`：读取单个字符

- `int read(char[] ch)`：读取字符数组

  


OutputStreamWriter继承Writer，是字符的输出流

* `OutputStreamWriter(OutputStream out,String 编码表名)`：传递任意字节输出流，编码表名默认跟随系统 ，以字符串形式指定如`gbk`、`utf8` 

```java
try(FileOutputStream fis = new FileOutputStream("test.txt");){
    OutputStreamWriter osw = new OutputStreamWriter(fis); // 创建字符输出流
    osw.write("海上明月共潮生");
    osw.close();
}catch (IOException e){

}
```

同理，存在InputStreamReader用于字符读取 

* `InputStreamReader(InputStream out,String 编码表名)`：传递任意字节输入流

```java
try(FileInputStream fis = new FileInputStream("test.txt");){
    InputStreamReader  isr= new InputStreamReader(fis);
    char[] tmp = new char[1024];
    int r;
    while((r=isr.read(tmp))!=-1){
        System.out.println(new String(tmp,0,r));
    }
    isr.close();
}catch (IOException e){
}
```



### Buffered

字符流同样存在缓冲流，用以高效的输入输出。和字节流类似，他需要接管一个Read类/Writer类 



BufferedReader**提供了按行读取的方法，换行符读取后最后会被丢弃**

- `String readLine() `：读取文本一行，**文件末尾会返回null**


- `BufferedReader(Reader r)`：可以传递任意字符输入流

```java

try(FileInputStream fis = new FileInputStream("test.txt");){
    BufferedReader bfr = new BufferedReader(new InputStreamReader(fis)); // 接管Reader类 
    String line;
    while((line=bfr.readLine())!=null){ 
        System.out.println(line);
    }
}catch (IOException e){

}
```



BufferWrite 提供了一个与平台无关的`newLine()`方法，构造方法与BufferRead类似。

```java
try(FileOutputStream fis = new FileOutputStream("test.txt");){
    BufferedWriter bfw = new BufferedWriter(new OutputStreamWriter(fis));
    String[] poems={"君不见黄河之水天上来，奔流到海不复回",
                    "君不见高堂明镜悲白发，朝如青丝暮成雪"};
    for(String poem:poems){
        bfw.write(poem);
        bfw.newLine(); // 在上文的末尾添加\n或者\r\n 取决于平台 
        bfw.flush();  // 将内存里的字符串写入到文本
    }
    bfw.close();
}catch (IOException e){

}
```



## 打印流

- PrintStream : 字节输出流
- PrintWriter : 字符输出流

打印流特性负责输出打印，不关心数据源，方便的打印各种形式数据

```java
/**
* 打印流输出,在打印流的构造方法中,传递流(字节,字符)
* 自动刷新 : 构造方法第二个参数写true,第一个参数必须是IO流对象,不能是字符串
* 调用方法: println,printf,format 三个其中的一个,启用自动刷新
*/
public static void print()throws IOException {
    //便捷类
    FileWriter fw = new FileWriter("day20/print.txt");
    //创建打印流对象,传递便捷类
    PrintWriter pw = new PrintWriter(fw,true);
    pw.println(1.5); //方便打印,原样输出
}
```



## 序列化

序列化用于将对象转化为字节序列，方便从内存中存储到磁盘，反序列化反之。

使用`ObjectOutputStream(OutputStream out)` 进行序列化，构造方法传递字节输出流

```java
// 序列化的类要求实现 implements Serializable 接口
// 静态属性不能序列化 
public static void writeObject(Object obj){
    try(FileOutputStream fos = new FileOutputStream("test.txt")){
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(obj);  // 写入对象到文件 
        oos.close();

    }catch (IOException e){}
}
```

反序列化同理，但是序列化后的类要求可见

```java
public static void readObj(){
    try(FileInputStream fis = new FileInputStream("test.txt")){
        ObjectInputStream ois = new ObjectInputStream(fis);
        Object person = ois.readObject();
        ois.close();

    }catch (IOException | ClassNotFoundException e){
        // 读取时该类需要可见
        e.printStackTrace();
    }

}
```



# 多线程

线程也是对象，Thread类是线程对象的描述类。



实现线程程序的步骤 :

- 定义类继承Thread
- 子类重写方法run
- 创建子类对象 
- 调用子类对象的方法start()启动线程

```java
//- 定义类继承Thread
//- 子类重写方法run
public class SubThread extends Thread {
    public void run(){  
        // 实现run方法
        for(int x = 0 ; x < 50 ;x++)
            System.out.println("run..."+x);
    }
}
```



```java
public static void main(String[] args) {
    //创建线程程序
    SubThread subThread = new SubThread();
    subThread.start();  // start 启动线程
    for(int x = 0 ; x < 50 ;x++)
    	System.out.println("main..."+x);
}
```



常用方法：

* getName()：返回线程的名字

* currentThread()：静态方法，返回当前的线程对象

* join()：等待线程结束，与start相对 

  ```java
      public static void main(String[] args) throws InterruptedException {
          JoinThread t0 = new JoinThread();
          JoinThread t1 = new JoinThread();
  
          t0.start();
          t0.join(); // 等待t0结束 
          t1.start();
      }
  ```

* yield：静态方法，让出线程的CPU使用权 

* sleep(n)：当前线程睡眠n毫秒，进入阻塞状态。sleep只会让出当前线程的时间片，并不释放对象锁 ，同时睡眠时间到，会自己醒来  

* wait：继承自object，主动使当前线程进入阻塞状态，**并释放对象锁。必须由当前对象锁调用，写在synchronized同步代码块的try里**

  ```java
  synchronized(lock){
      while(条件){
          try{
              lock.wait(); // 沉睡
          }catch(Exception ex){
              
          }
      }
      // 执行代码
      lock.notify(); // 同步代码结束 唤醒其余线程 
      
  }
  ```

  

* notify()：继承自object，唤醒第一个等待的线程（阻塞态转为就绪态），**必须由当前对象锁调用，在synchronized同步代码块里调用。被唤醒的线程不会立即抢占当前线程，而是等待当前线程执行完同步代码** 

* notifyAll()：唤醒所有等待的线程，至于具体让那个线程执行，由操作系统处理 



## Runnable接口

自定义类时，选择实现Runnable接口。**该类表示线程即将执行的任务，以便实现线程执行内容和线程本身的解耦**

```java
public class SubRunnable implements Runnable{ // 实现runable 接口 
    @Override
    public void run() {
        for(int x = 0 ; x < 50 ;x++){
            System.out.println(Thread.currentThread().getName()+"x.."+x);
        }
    }
}


 public static void main(String[] args) {
     // 下例中 多个线程 针对一个执行任务 
     // 如果使用 extends Thread，多个线程各自执行自己的任务 
     Runnable r = new SubRunnable();  // 执行任务 
     Thread t0 = new Thread(r); // thread ,用runable类初始化它
     Thread t1 = new Thread(r); // 再创建一个线程执行该任务
     
     t0.start();
     t1.start();  

     for(int x = 0 ; x < 50 ;x++){
         System.out.println(Thread.currentThread().getName()+"x.."+x);
     }
    }
```

## 线程安全

多个线程操作一个资源时 ，因为执行可能是乱序的，容易发生线程安全问题。细节可以参考《操作系统》。

> 例：并发进程p1、p2，共享初值为1的变量x。其过程分别如下，则x的最终结果可能为？
>
> ```c
> p1()
> {
>   load  r1,x	//将x存到寄存器r1 
>   inc r1;  //x++;
>   store x,r1;	//将r1的内容存入x
> }
> 
> p2()
> {
>   load  r2,x	//将x存到寄存器r2
>   dec r1;  //x--;
>   store x,r2;	//将r2的内容存入x
> }
> 
> ```
>
> 
>
> 答：(1)顺序执行，则x++、x--，最终结果不变，x=1
>
> （2）乱序执行，同时读，写完以后依次覆盖结果，最终结果为0或2。
>
> 故其最终结果可能为1,0,2。



### Synchronized

synchronized ：用于线程操作，只能被同一时间被一个线程使用



对其中某个对象上锁 ，然后执行代码块。上锁后，线程执行到同步代码块时，会检查是否存在对象锁，**若锁存在，则证明此时并没有其余线程在操作此处代码块，可以拿到锁以后安全进入，执行完以后再次上锁。**反之，证明有其余线程正在操作同步代码块，该线程等待（上锁）。

这种机制可以确保同步代码块同一时间只有一个线程在操作，当然，代价是执行速度有所下降。

```java
// 任意对象要是固定的 不能每次都new 
Object lock = new Object();
synchronized(lock){ // 检查对象锁
    //线程操作的共享资源
}

// 自动归还对象锁
```



当/整个函数作为代码块时，可以使用修饰符synchronized，作用于整个函数。

```java
// 修饰符 对于非静态函数 锁的是this对象 
// 对于静态函数 锁的是 类名.class 对象
public synchronized  void scale(); // 
```





### Lock 锁

  JDK5新的特性 : java.util.concurrent.locks包，定义了接口Lock。Lock接口替代了synchronized，可以更加灵活，性能更好

```java
// ReentrantLock 是lock的子类 
private Lock lock = new ReentrantLock(); // 创建锁 ，锁应该唯一 
private void sale(){
    //获取锁
    lock.lock();  
    // 执行你的代码 
    //释放锁
    lock.unlock();
}
```



随lock锁而来的是``Condition`，该类是一个集合（队列），用于存储阻塞的线程，每一个lock锁都可以有多个Condition。Condition对应阻塞和唤醒的操作分别是：

* `.signal()`：唤醒队列中的所有线程，并出队第一个线程
* `.await()`：阻塞当前线程，释放lock锁，并进队阻塞队里 

上述两个方法都要求被`lock.lock()`和`lock.unlock()`方法包裹。



```java
class Resource {
    int item = 0;
    boolean flag = true; // 用于标记当前是否允许生产/消费
    Lock lock = new ReentrantLock();
    Condition prod = lock.newCondition();  // 生产者阻塞队列
    Condition cust = lock.newCondition();  // 消费者阻塞队列 

    void produce() {
        while (item < 100) {
            lock.lock();
            while (!flag) {
                try {
                    prod.await();  // 主动阻塞，进入生产者队列
                } catch (Exception e) {
                }
            }
            item++;
            System.out.println(Thread.currentThread().getName()+"生产第" + item + "个");
            flag=!flag;
            cust.signal(); // 唤醒消费者阻塞队列 
            lock.unlock();
        }

    }

    void consume(){
        while (item<100){
            lock.lock();
            while (flag){
                try {
                    cust.await(); // 主动阻塞，进入消费者队列
                } catch (Exception e) {
                }
            }
            System.out.println(Thread.currentThread().getName()+"消费第" + item + "个");
            flag=!flag;
            prod.signal();  // 唤醒生产者阻塞队列 
            lock.unlock();
        }
    }

}
```



lock锁的原理简介：每次读取时，拿回版本号和值，准备回写时，判断中间是否发生过写，若有，则重新读取再写。如此循环，称为CAS(compare and swap)锁，又称自旋锁。



## 单例模式

自始至终保持内存中只有一个对象实例。

```java
class Player{
    private static Player instance= null; // 私有

    private Player(){ // 构造方法私有化，保证不被new 调用
    }


    // synchronized 修饰符保证多线程调用时安全
     public synchronized static Player getInstance(){
         if (Player.instance == null) {
             instance = new Player();
         }
         System.out.println(instance);
         return instance;
     }
}
```



## volatile 

volatile 关键字，一个线程修改变量后，其余线程立即可见 

```java
public class MyRunnable implements Runnable {
    private volatile boolean flag = true;

    @Override
    public void run() {
        m();
    }

    private void m(){
        System.out.println("开始执行");
        while (flag){
			// 死循环
        }
        System.out.println("结束执行");
    }


    public void setFlag(boolean flag) {
        this.flag = flag;
    }
}


 public static void main(String[] args) throws InterruptedException {
        MyRunnable myRunnable = new MyRunnable();

        new Thread(myRunnable).start(); 

        Thread.sleep(2000);

        // main线程修改变量
        // 如果不使用volatile修饰符 flag会始终在上面那个线程判断为true
        // 即使main线程修改了堆的变量 但因为while一直没退出 cpu取到后一直放在了缓存里
        myRunnable.setFlag(false);
    }
```



## 线程池

线程池可以回收线程再利用，减小了每次new Thread的损耗。



Executors类

* `static newFixedThreadPool(int 线程的个数)`：创建线程池
* `submit (Runnable r)`：提交线程执行的任务
* `shutdown()`：销毁池子 

```java
ExecutorService pool = Executors.newFixedThreadPool(2);
pool.submit(new PoolTest());
pool.shutdown();
```



**Runable对象不支持返回值、抛出异常，相较而言，Callable接口改进了这点。**

```java
public class MyCall implements Callable<String> {
    public String call() throws Exception{
        return "返回字符串";
    }
}

// Future<> 接收返回的值
Future<String> future = es.submit(new MyCall());//返回接口类型 Future
//接口的方法get,获取线程的返回值
String str = future.get();
System.out.println("str = " + str);
```





# 网络编程

##  InetAddress类 

InetAddress类主要表示IP地址，提供了如下几个 静态方法来获取InetAddress 实例

* `public static InetAddress getLocalHost()`：获取当前主机，包括主机名/IP地址
* `public static InetAddress getByName(String host)`：获取网络中对应主机名的主机
* `public static InetAddress getByAddress(byte[] addr)`：同上，但是凭借IP地址 



所有的网络异常均属于IO异常。

```java
import java.net.InetAddress;
InetAddress localHost = InetAddress.getLocalHost();  // Hollis/192.168.145.1
InetAddress atguigu = InetAddress.getByName("www.atguigu.com"); 

byte[] addr = {(byte)192,(byte)168,24,56}; // 强转int 
InetAddress atguigu = InetAddress.getByAddress(addr);
```



## socket

套接字（IP:PORT）通信，分为客户端和服务端。



对于客户端，调用`Socket类` 

* `public Socket(InetAddress address,int port)`：创建一个流套接字并将其连接到指定 IP 地址的指定端口号。
* `public Socket(String host,int port)`：同上 

```java
import java.net.Socket;
Socket client = new Socket("127.0.0.1",8080); // 连接目标主机端口
```

**Socket类的常用方法**：

* `public InputStream getInputStream()`：**返回此套接字的输入流，用于接收消息**
* `public OutputStream getOutputStream()`：**返回此套接字的输出流，用于发送消息**
* `public InetAddress getInetAddress()`：此套接字连接到的远程 IP 地址；如果套接字是未连接的，则返回 null。
* `public InetAddress getLocalAddress()`：获取套接字绑定的本地地址。
* `public int getPort()`：此套接字连接到的远程端口号；如果尚未连接套接字，则返回 0。
* `public int getLocalPort()`：返回此套接字绑定到的本地端口。如果尚未绑定套接字，则返回 -1。
* `public void close()：`关闭此套接字。套接字被关闭后，便不可在以后的网络连接中使用（即无法重新连接或重新绑定）。需要创建新的套接字对象。 关闭此套接字也将会关闭该套接字的 InputStream 和 OutputStream。 
* `public void shutdownInput()`：从输入流读取将返回EOF（文件结束符），此后禁止从该流读取
* `public void shutdownOutput()`：**禁用此套接字的输出流**。对于 TCP 套接字，任何以前写入的数据都将被发送，并且后跟 TCP 的正常连接终止序列。 如果在套接字上调用 shutdownOutput() 后写入套接字输出流，则该流将抛出 IOException。 即不能通过此套接字的输出流发送任何数据。



客户端的连接步骤：

1. 初始化socket对象 
2. 创建输出流向服务器发送数据，输入流从服务器读取数据
3. 关闭socket 

```java
class Client{

    Client() throws IOException {
        Socket client = new Socket("127.0.0.1",8080);
        // send to server
        OutputStream ops = client.getOutputStream();
        ops.write("hello world".getBytes(StandardCharsets.UTF_8));
        client.shutdownOutput(); // 告诉服务器数据传输完毕 服务器从输入流将读取到EOF
        
        // 等待服务器反馈
        InputStream is = client.getInputStream();
        int r;
        byte[] buffer = new byte[1024];
        while((r=is.read(buffer))!=-1){
            System.out.println(new String(buffer,0,r));
        }
        
        // 关闭
        client.close();
    }
}
```



对于服务端，使用`ServerSocket`类 

* `ServerSocket(int port) `：创建绑定到特定端口的服务器套接字。
* `Socket accept()`：阻塞式地监听等待客户端连接 



服务端的通信过程和客户端基本类似，只是采取了等待姿态 

```java
class Server{
    Server() throws IOException {
        ServerSocket server = new ServerSocket(8080);
        // 阻塞得等待客户端连接
        Socket client = server.accept();
        System.out.println(client); // Socket[addr=/127.0.0.1,port=14439,localport=8080]

        // 读取客户端的输入
        InputStream is = client.getInputStream();
        int read;
        byte[] buffer = new byte[1024];
        while((read=is.read(buffer))!=-1){ // 客户端要在输出流中调用shutdown才可以读取到-1 
            System.out.println(new String(buffer,0,read));
        }
        // 反馈给客户端
        OutputStream os = client.getOutputStream();
        os.write("server has recived".getBytes(StandardCharsets.UTF_8));
        client.shutdownOutput();
        client.close(); // close connection
    }
}
```

# 反射

## 类的加载

类在内存中的生命周期：加载-->使用-->卸载。



类加载的步骤：

1. 加载：该类class字节码数据读入内存 
2. 链接：

①验证：校验合法性等 

②准备：准备对应的内存（方法区），创建Class对象，为类变量赋默认值，为静态常量赋初始值。

③解析：把字节码中的符号引用替换为对应的直接地址引用

![image-20220621171838242](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220621171838242.png)



触发类初始化的操作：

* 运行main入口所在的类 
* 实例化/调用静态成员（static final除外）时，会检查是否初始化 
* 子类初始化时，发现它的父类还没有初始化的话，那么先初始化父类
* 反射操作某个类

```java
class Father{
	static{
		System.out.println("main方法所在的类的父类(1)"); //初始化子类时，会初始化父类
	}
}

public class TestClinit1 extends Father{
	static{
		System.out.println("main方法所在的类(2)"); //主方法所在的类会初始化
	}
	
	public static void main(String[] args) throws ClassNotFoundException {
		new A(); //第一次使用A就是创建它的对象，会初始化A类
		
		B.test(); //直接使用B类的静态成员会初始化B类
		
		Class clazz = Class.forName("com.atguigu.test02.C"); //通过反射操作C类，会初始化C类
	}
}
class A{
	static{
		System.out.println("A类初始化");
	}
}
class B{
	static{
		System.out.println("B类初始化");
	}
	public static void test(){
		System.out.println("B类的静态方法");
	}
}
class C{
	static{
		System.out.println("C类初始化");
	}
}
```



同时，也有一些操作不会触发类的初始化 

1. 通过子类调用父类的静态变量，静态方法，只会导致父类初始化，不会导致子类初始化，**即只有声明静态成员的类才会初始化**
2. 用某个类型声明数组并创建数组对象时，不会导致这个类初始化

```java
public class TestClinit2 {
	public static void main(String[] args) {
		System.out.println(D.NUM);  // final 不加载
		
		System.out.println(F.num); // 父类初始化 F不会 它的父类E会初始化
		F.test();  // 上面一句已经将E初始化了 所以这次不会再初始化 
		
		G[] arr = new G[5];  // 数组创建 不会初始化 
	}
}

class D{
	public static final int NUM = 10;
	static{
		System.out.println("D类的初始化");
	}
}
class E{
	static int num = 10;
	static{
		System.out.println("E父类的初始化");
	}
	public static void test(){
		System.out.println("父类的静态方法");
	}
}
class F extends E{
	static{
		System.out.println("F子类的初始化");
	}
}

class G{
	static{
		System.out.println("G类的初始化");
	}
}
```



## 类加载器

当需要**支持类的动态加载或需要对编译后的字节码文件进行加密解密操作**，就需要你自定义类加载器。

因此了解类加载器及其类加载机制也就成了每一个Java开发人员的必备技能之一。



类加载器分为：

1. 引导类加载器（Bootstrap Classloader），又称为根类加载器，负责加载jre/lib中的核心库
2. 扩展类加载器（Extension ClassLoader），负责加载jre/lib/ext扩展库
3. 应用程序类加载器（Application Classloader），负责加载项目的classpath路径下的类 
4. 自定义类加载器，比如需要加载特定目录的类、对字节码文件加解密时 



类加载时的双亲委托模式：

* 自下而上：下一级的类加载器，如果接到任务时，会先搜索是否加载过，如果没有，会先把任务往上传，如果都没有加载过，一直到根加载器
* 自上而下：如果根加载器在它负责的路径下没有找到，会往回传，如果一路回传到最后一级都没有找到。那么会报ClassNotFoundException或NoClassDefError，如果在某一级找到了，就直接返回Class对象。

##  java.lang.Class类

**Class类可以理解为对一个类的描述信息类**，通过Class，可以在运行时，**动态地获取类的所有属性和方法**。这种动态获取信息功能称为Java语言的反射机制。

### 获取class对象

获取class对象的四种方式

1. `类型名.class `
2. `对象.getClass()` 
3. `Class.forName(类型全名称)`，通常需要配置文件配置配合使用
4. `ClassLoader的类加载器对象.loadClass(类型全名称)`



```java
//第一种方式获取Class: 类型名.class
Class clazz = Person.class; 

//第二种方式获取Class: 对象.getClass()
Class clazz = new Person().getClass();

//第三种方式获取Class: Class.forName("类的全限定名")
Class clazz = Class.forName("com.atguigu.Person");
```



### 反向获取类信息

可以获取的信息包括：包、修饰符、类型名、父类（包括泛型父类）、父接口（包括泛型父接口）、成员（属性、构造器、方法）、注解（类上的、方法上的、属性上的）。

对于成员属性，java将其抽象为Field。对于成员函数，java将其抽象为Method。 

```java
// clazz是class对象

Package pkg = clazz.getPackage(); // 包信息
int mod = clazz.getModifiers();  // 修饰符 public对应编码1 以此类推
String name = clazz.getName(); //  获取类名
Class superclass = clazz.getSuperclass(); // 获取父类的字节码对象
Class[] interfaces = clazz.getInterfaces(); // 获取该类实现的所有接口

/*
Declared有无的区别是：
declared 用于获取 类本身 的所有声明属性 无论公开与否
无declared 用于获取 该类及其父类的所有public属性 即公开属性 
*/
Field[] declaredFields = clazz.getFields();  // 获取该类的所有公开属性 包括父类的
Field[] declaredFields = clazz.getDeclaredFields(); // 获取该类的所有属性

Construcor[] constructors = clazz.getDeclaredConstructors(); // 获取该类的所有构造函数

Method[] declaredMethods = clazz.getDeclaredMethods(); // 获取该类的所有方法
```



### 操作对象

创建对象 

两种方式：

1、`.newInstance()`调用Class对象的无参构造，来实例化

2、通过获取构造器对象来进行实例化



```java
// 方法1 通过class对象实例化
Class<?> clazz = Class.forName("com.atguigu.test.Student");
Object stu = clazz.newInstance();
System.out.println(stu);

// 方法2 构造器对象
Class clazz = Person.class;
// 返回特定类型的构造器 
// 当然也可以返回无参构造器 clazz.getDeclaredConstructor()
Constructor constructor = clazz.getDeclaredConstructor(int.class,String.class, String.class);
//使用构造函数创建对象
Person person = (Person) constructor.newInstance(40,"奥巴马","召唤师峡谷");
System.out.println(person);
```





**操作对象属性**

* 获取的属性是Field对象 
* 非静态属性需要传入Object对象 ，静态属性可以传null

```java
// 操作示例 
Class clazz = Class.forName("com.atguigu.bean.User"); // 获取class对象

// 获取字段信息
Field field = clazz.getDeclaredField("username"); // 注意，返回的是Field对象，因为该属性可能是任何类型
field.setAccessible(true); // 即使是私有也可以访问 

// 绑定具体的实例 
Object obj = clazz.newInstance(); 
// 读取字段信息
Object value = field.get(obj);
// 写字段信息 
field.set(obj,"chai"); 
```





**操作对象方法** ，思路和操作对象属性是一致的，先获取再调用

```java
Class clazz = Class.forName("com.atguigu.service.UserService"); // 获取class对象
// 获取方法： 方法名；参数1
Method method = clazz.getDeclaredMethod("login",String.class,String.class); 

Object obj = clazz.newInstance(); // 创建实例
// method.setAccessible(true); // 如果方法是私有的话 就要设置为可读权限
Object result = method.invoke(obj,"chai","123); // 实例 参数1。。。
```





**操作对象数组**

`java.lang.reflect` 下提供了一个Array类，Array对象可以代表所有的数组，用它可以地动态地创建数组、操作数组元素等。

* `public static Object newInstance(Class<?> componentType, int dimensions)`：创建一个具有指定的组件类型和维度的新数组
* `public static void setXxx(Object array,int index,xxx value)`：将array数组中[index]元素的值修改为value，此处的Xxx对应8种基本数据类型
* `public static xxx getXxx(Object array,int index,xxx value)`：将array数组中[index]元素的值返回。此处的xxx对应8种基本数据类型，如果该属性的类型是引用数据类型，则直接使用get(Object array,int index)方法。

```java
public static void main(String[] args) {
    //使用反射操作数组
    //1. 使用反射创建一个String类型的数组，长度是5
    Object array = Array.newInstance(String.class, 5);

    //2. 往数组中存入数据
    for (int i=0;i<5;i++){
        Array.set(array,i,"value"+i);
    }

    //使用Array获取数组中的元素
    for (int i=0;i<5;i++){
        System.out.println(Array.get(array, i));
    }
}
```



## Type

pass



# 注解

## 注解

注解，以`@`开头，是一种特殊的接口，用于标记程序。



JDK本身提供的三个注解：

1. `@Override`:描述方法的重写.
2. `@SuppressWarnings`:压制警告.
3. `@Deprecated`:标记过时 



自定义注解

```java
// 格式 @interface 

// 一个空的注解
public @interface Annotation01 {
    
}
```



**添加注解属性可以让注解存储数据（常用于配置文件），所谓的注解属性**，类似于成员变量，只是格式上稍有不同，`Type var()` 。注解属性的支持类型：

1. 基本类型 
2. tring

​	3.枚举类型

​	4.注解类型

​	5.Class类型  

​	6.以上类型的一维数组类型

```java
public @interface Annotation02 {
	int a();//基本类型
	
	String b();//String
	
	Annotation01 d();//注解类型
	
	Class e();//Class类型  
	
	String[] f() default {"hello","world"}; //一维数组类型 并设置了默认值
	
}

// 一旦注解添加了注解属性 在添加注解时就要传值 
@MyAnnotation3(a=0,b="hollis")
```



## 元注解

元注解是标记自定义注解的注解。



常用的元注解

`@Target`：定义该注解作用在什么上面(位置)。默认注解可以在任何位置。可选值为`ElementType`的枚举值

* `METHOD`:方法
* `TYPE`:类 接口
* `FIELD`:字段
* `CONSTRUCTOR`:构造方法声明



`@Retention`：定义该注解保留到那个代码阶段，值为`RetentionPolicy`类型。**默认只在源码阶段保留**

* `SOURCE`:只在源码上保留(默认)
* `CLASS`:在源码和字节码上保留
* `RUNTIME`:在所有的阶段都保留 



```java
@Target(value = {ElementType.METHOD,ElementType.TYPE})
@Retention(value = RetentionPolicy.RUNTIME)
public @interface MyAnnotation03 {
	int a();
	String b();
}
```



## 注解解析

通过反射手段，来获取注解的应用消息。

- **T getAnnotation(Class<T>annotationType):得到指定类型的注解引用。没有返回null。**
- **boolean isAnnotationPresent(Class<?extends Annotation> annotationType)**：判断指定的注解有没有，可以应用在方法、类上等
- `Annotation[] getAnnotations()`：得到所有的注解，包含从父类继承下来的。
- `Annotation[] getDeclaredAnnotations()`：得到自己身上的注解。 



```java
// 定义注解
@Retention(RetentionPolicy.RUNTIME)
@interface MyAnnotation{
    int age() default 0;
    String name() default "hollis";
}


// 定义一个使用注解的类 
class UseAnnotation{
    @MyAnnotation(age = 25,name="hollis jiang")
    public void print(){
        System.out.println("hello world");
    }
}


import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.reflect.Method;

public class AnnotationTest {
    public static void main(String[] args) {
        Class clazz= UseAnnotation.class;
        Method[] methods = clazz.getDeclaredMethods(); 
        
        for(Method m:methods){
            System.out.println("method: "+m); 
            System.out.println(m.isAnnotationPresent(MyAnnotation.class)); // 是否应用了该注解
            Annotation[] annotations = m.getDeclaredAnnotations(); // 获取该方法上所有应用的注解
            for(Annotation annotation:annotations){
                System.out.println("annotation: "+annotation);
            }
        }
    }
}
```



# Junit

Junit是Java语言编写的第三方单元测试框架。在Java中，一个单元指的就是一个类，单元测试指的就是对类中的方法进行功能测试或逻辑测试。



测试类的命名规范：使用驼峰命名法。以Test开头，以业务类类名结尾，例如（大驼峰）TestProductDao，测试方法名（小驼峰）叫testSave。

测试方法规范：

* 必须是public修饰的，没有返回值，没有参数
* 必须使注解@Test修饰

```java
import org.junit.Assert;

@Test
public void testName(){
    Assert.assertEquals("hello world","你好世界"); // 断言两者是否相对 
}
```





Junit常用注解 

* @Before：用来修饰方法，该方法会在每一个测试方法执行之前执行一次。
* @After：用来修饰方法，该方法会在每一个测试方法执行之后执行一次。

```java
@Before
public void init(){
    System.out.println("global initing...");
}

@After
public void close(){
    System.out.println("close after...");
}
```





# 匿名函数

## 函数式接口

**java对函数的参数类型有严格检查**，所以不像python，凭借一个`lambda`关键字即可创建匿名函数。**java对匿名函数的创建，依赖函数式接口**。所谓函数式接口，即是只实现了一个抽象方法的接口。**匿名函数，在设计上，即是一个抽象接口的具体实现**。

使用`@FunctionalInterface`注解来定义接口，编译器将会强制检查该接口是否确实有且仅有一个抽象方法，否则将会报错。 



### 自定义函数式接口

```java
@FunctionalInterface
public interface Calculator {
    int calculator(int a,int b); // 函数形参 返回类型
}
```

在创建具体的匿名函数式，格式为`()->{}` 

```java
int invokeCal(int a,int b,Calculator c){  // 声明 第三个参数是上述声明的接口
    return c.calculator(a,b); // 外面只是一个空壳 里面实际调用的是接口的具体方法
}

// 对比调用 和 形参声明的区别
// 只要符合形参声明 和 返回类型 即可 
int sum=invokeCal(5,5,(a,b)->{return a+b;}); 
int sum=invokeCal(5,5,(a,b)->{return a-b;}); // 返回int类型即可 
```



## 内置接口

按照形参有无以及是否返回，jdk将内置接口分为以下几种

### 消费性接口

消费型接口的抽象方法特点：有形参，但是返回值类型是void

| 接口名               | 描述                       | 抽象方法                       |
| -------------------- | -------------------------- | ------------------------------ |
| Consumer<T>          | 接收一个对象用于完成功能   | void accept(T t)               |
| BiConsumer<T,U>      | 接收两个对象用于完成功能   | void accept(T t, U u)          |
| DoubleConsumer       | 接收一个double值           | void accept(double value)      |
| IntConsumer          | 接收一个int值              | void accept(int value)         |
| LongConsumer         | 接收一个long值             | void accept(long value)        |
| ObjDoubleConsumer<T> | 接收一个对象和一个double值 | void accept(T t, double value) |
| ObjIntConsumer<T>    | 接收一个对象和一个int值    | void accept(T t, int value)    |
| ObjLongConsumer<T>   | 接收一个对象和一个long值   | void accept(T t, long value)   |



例如，JDK1.8中Collection集合接口的父接口Iterable接口中增加了一个默认方法：`public default void forEach(Consumer<? super T> action) `，遍历Collection集合的每个元素。

```java
public void testForEach(){
    List<Integer> list = new ArrayList<>();
    for (int i = 0; i < 10; i++) {
        list.add(i);
    }
    list.forEach((x)->{
        System.out.println("current element is: "+x);
    });
}
```



### 供给型接口

这类接口的抽象方法特点：无参，但是有返回值

| 接口名          | 抽象方法               | 描述              |
| --------------- | ---------------------- | ----------------- |
| Supplier<T>     | T get()                | 返回一个对象      |
| BooleanSupplier | boolean getAsBoolean() | 返回一个boolean值 |
| DoubleSupplier  | double getAsDouble()   | 返回一个double值  |
| IntSupplier     | int getAsInt()         | 返回一个int值     |
| LongSupplier    | long getAsLong()       | 返回一个long值    |

### 断言型接口

这里接口的抽象方法特点：有参，但是返回值类型是boolean结果。

| 接口名           | 抽象方法                   | 描述             |
| ---------------- | -------------------------- | ---------------- |
| Predicate<T>     | boolean test(T t)          | 接收一个对象     |
| BiPredicate<T,U> | boolean test(T t, U u)     | 接收两个对象     |
| DoublePredicate  | boolean test(double value) | 接收一个double值 |
| IntPredicate     | boolean test(int value)    | 接收一个int值    |
| LongPredicate    | boolean test(long value)   | 接收一个long值   |



JDK1.8时，Collecton<E>接口增加了一下方法，其中一个如下：`public default boolean removeIf(Predicate<? super E> filter)` 用于删除集合中满足filter指定的条件判断的。 

```java
import java.util.ArrayList;

public class TestLambda {
	public static void main(String[] args) {
		ArrayList<String> list = new ArrayList<>();
		list.add("hello");
		list.add("java");
		list.add("atguigu");
		list.add("ok");
		list.add("yes");
		
		list.forEach(str->System.out.println(str));
		System.out.println();
		
		list.removeIf(str->str.length()<5);
		list.forEach(str->System.out.println(str));
	}
}
```





### 功能型接口

这类接口的抽象方法特点：既有参数又有返回值

| 接口名                  | 抽象方法                                        | 描述                                                |
| ----------------------- | ----------------------------------------------- | --------------------------------------------------- |
| Function<T,R>           | R apply(T t)                                    | 接收一个T类型对象，返回一个R类型对象结果            |
| UnaryOperator<T>        | T apply(T t)                                    | 接收一个T类型对象，返回一个T类型对象结果            |
| DoubleFunction<R>       | R apply(double value)                           | 接收一个double值，返回一个R类型对象                 |
| IntFunction<R>          | R apply(int value)                              | 接收一个int值，返回一个R类型对象                    |
| LongFunction<R>         | R apply(long value)                             | 接收一个long值，返回一个R类型对象                   |
| ToDoubleFunction<T>     | double applyAsDouble(T value)                   | 接收一个T类型对象，返回一个double                   |
| ToIntFunction<T>        | int applyAsInt(T value)                         | 接收一个T类型对象，返回一个int                      |
| ToLongFunction<T>       | long applyAsLong(T value)                       | 接收一个T类型对象，返回一个long                     |
| DoubleToIntFunction     | int applyAsInt(double value)                    | 接收一个double值，返回一个int结果                   |
| DoubleToLongFunction    | long applyAsLong(double value)                  | 接收一个double值，返回一个long结果                  |
| IntToDoubleFunction     | double applyAsDouble(int value)                 | 接收一个int值，返回一个double结果                   |
| IntToLongFunction       | long applyAsLong(int value)                     | 接收一个int值，返回一个long结果                     |
| LongToDoubleFunction    | double applyAsDouble(long value)                | 接收一个long值，返回一个double结果                  |
| LongToIntFunction       | int applyAsInt(long value)                      | 接收一个long值，返回一个int结果                     |
| DoubleUnaryOperator     | double applyAsDouble(double operand)            | 接收一个double值，返回一个double                    |
| IntUnaryOperator        | int applyAsInt(int operand)                     | 接收一个int值，返回一个int结果                      |
| LongUnaryOperator       | long applyAsLong(long operand)                  | 接收一个long值，返回一个long结果                    |
| BiFunction<T,U,R>       | R apply(T t, U u)                               | 接收一个T类型和一个U类型对象，返回一个R类型对象结果 |
| BinaryOperator<T>       | T apply(T t, T u)                               | 接收两个T类型对象，返回一个T类型对象结果            |
| ToDoubleBiFunction<T,U> | double applyAsDouble(T t, U u)                  | 接收一个T类型和一个U类型对象，返回一个double        |
| ToIntBiFunction<T,U>    | int applyAsInt(T t, U u)                        | 接收一个T类型和一个U类型对象，返回一个int           |
| ToLongBiFunction<T,U>   | long applyAsLong(T t, U u)                      | 接收一个T类型和一个U类型对象，返回一个long          |
| DoubleBinaryOperator    | double applyAsDouble(double left, double right) | 接收两个double值，返回一个double结果                |
| IntBinaryOperator       | int applyAsInt(int left, int right)             | 接收两个int值，返回一个int结果                      |
| LongBinaryOperator      | long applyAsLong(long left, long right)         | 接收两个long值，返回一个long结果                    |



## lambda表达式简化

1. 方法引用，lamda表达式，形参全部用上，执行体也只有一句话，且是通过调用方法名。那么可以以`对象::方法` 来简化代码

   ```java
   Runnable r = () -> System.out.println("hello lambda");
   Runnable r = System.out::println;//打印空行
   
   Stream<Double> stream = Stream.generate(() -> Math.random());	
   Stream<Double> stream = Stream.generate(Math::random);
   ```

   





# Stream流

Stream流是对集合计算的抽象，集合collection负责存储数据，**而它负责计算**。Steam流**很好地融合了匿名函数，支持链式调用**，有效地简化代码。

Stream流不会改变源对象，**每次操作都会返回一个新的对象**。同时，**它是惰性的**，只有等终止操作发生时，**先前的动作才会立即执行。** 



## 创建stream流 

集合接口

* `public default Stream<E> stream() `: 返回一个顺序流
* `public default Stream<E> parallelStream()` : 返回一个并行流

```java
List<Integer> list = Arrays.asList(1,2,3,4,5);
Stream<Integer> stream = list.stream();  //JDK1.8中，Collection系列集合增加了方法
```



数组接口

Java8 中的 Arrays 的静态方法 stream() 可以获取数组流：`public static <T> Stream<T> stream(T[] array)`

```java
import java.util.Arrays;
String[] arr = {"hello","world"};
Stream<String> stream = Arrays.stream(arr);
```



Stream流创建

可以调用Stream类静态方法 of()，支持任意数量参数。`public static<T> Stream<T> of(T... values)` 

```java
Stream<Integer> stream = Stream.of(1,2,3,4,5);
```





合并两个已有的流

```java
Stream<Integer> s1 = Stream.of(1,2,3);
Stream<Integer> s2 = Stream.of(4,5,6);

Stream<Integer> s3 = Stream.concat(s1,s2);
```





创建无限流 

Stream的静态方法，迭代式和生成式

* `public static<T> Stream<T> iterate(final T seed, final UnaryOperator<T> f)`：返回一个无限流
* `public static<T> Stream<T> generate(Supplier<T> s) `：返回一个无限流

```java
// iterate 
Stream<Integer> stream = Stream.iterate(1, num -> num+=2);
stream.forEach(System.out::println);

// generate 
Stream<Double> stream = Stream.generate(Math::random);
stream.forEach(System.out::println);
```



## 中间操作 

多个中间操作可以连接起来形成一个流水线，**除非流水线上触发终止操作，否则中间操作不会执行任何的处理。**



* `filter(Predicate p)`， 从流中排除某些元素

  ```java
  Stream<Integer> stream = Stream.of(1,2,3,4);
  stream=stream.filter(x->(x%2==0)); // 保留偶数
  stream.forEach(System.out::println); // 遍历打印

* `distinct()`，通过流所生成元素的equals() 去除重复元素

  ```java
   Stream.of(1,2,3,4,5,6,2,2,3,3,4,4,5)
          .distinct()   // 去重
          .forEach(System.out::println);
  ```

  

* `limit(long maxSize)`截断流，使其元素不超过给定数量

  ```java
  Stream.of(1,2,3,4,5,6,2,2,3,3,4,4,5)
      .limit(3)
      .forEach(System.out::println);
  ```

  

* `skip(long n)`，返回一个扔掉了前 n 个元素的流。若流中元素不足 n 个，则返回一个空流。与 limit(n) 互补

  ```java
  Stream.of(1,2,3,4,5,6)
      .skip(5).forEach(System.out::println);
  ```

* `sorted()`产生一个新流，按自然顺序排序。可以传入比较器，自定义排序

  ```java
  Stream.of(11,2,39,4,54,6,2,22,3,3,4,54,54)
      .sorted()  // 从小到大
      .sorted((n1,n2)-> n2-n1) // 负数表示n1比较小 反之表示n1比较大，所以这刚好是从大到小
      .forEach(System.out::println);
  ```

  

* `map()`，映射流的每一个元素 

  ```java
  Stream.of(1,2,3,4,5)
      .map(x->Math.pow(x,2))
      .forEach(System.out::println);





## 终结操作 

终端操作会从流的流水线生成结果。其结果可以是任何不是流的值，流进行了终止操作后，相当于文件的close操作，不能再次使用。

* `forEach` 

* `count` ：返回流中元素总数

* `allMatch` ：检查是否匹配所有元素

*  `anyMatch` ：检查是否至少匹配一个元素 

  ```java
  boolean result = Stream.of(1,3,5,7,9)
      .anyMatch(t -> t%2==0);
  System.out.println(result);
  ```

* `findFirst` ：返回第一个元素

* `max` ：返回流中最大值

* `reduce` ：可以将流中元素反复结合操作起来，得到一个值

* `toArray()`：转换数组 

* ` collect `，将流转换为其他形式(很重要)。将流转换为其他形式，接收一个 Collector接口的实现 

  ```java
  // .toList() 
  // .toSet()
  // .toMap()
  List<Integer> list = Stream.of(1,2,4,5,7,8)
      .filter(t -> t%2==0)
      .collect(Collectors.toList());
  ```
  



## 数组 - 集合 - 流 

数组，只存放基本类型。以int为例，主要是基本类型 和 包装类型的相互转换。

```java
int[] nums = {1,2,3,4,5};

// 数组 转 List
List<Integer> ans = Arrays.stream(nums) // IntStream
    .boxed()  // int -> Integer
    .collect(Collectors.toList()); // List

// 数组 转 Stream
Stream<Integer> s = Arrays.stream(nums)
    .boxed();


// List 转 数组 ，先转为stream 
int[] nums1 = ans.stream().mapToInt(Integer::intValue).toArray(); // 拆箱
```





# Optional类

Optional是个容器，它可以保存类型T的值，或者仅仅保存null。它的作用在于，省去代码的显式空值检测。



创建Optional对象 

1. `static <T> Optional<T> empty() `：用来创建一个空的Optional 

2. `static <T> Optional<T> of(T value)` ：用来创建一个非空的Optional

3. `static <T> Optional<T> ofNullable(T value)` ：用来创建一个可能是空，也可能非空的Optional

   ```java
   Optional<String> opt = Optional.empty();
   Optional<String> opt = Optional.of(str);
   Optional<String> opt = Optional.ofNullable("hollis");
   ```

   

从optinal容器中取出对象 

* `T get() ` ：要求Optional容器必须非空 

  ```java
  String str = "hello";
  Optional<String> opt = Optional.of(str);
  System.out.println(opt.get());
  ```

* `T orElse(T other)`：为空则返回参数，不为空则返回元素本身。相当于进行了一次if检查

  ```java
   String str = "hello";
  Optional<String> opt = Optional.ofNullable(str);
  String string = opt.orElse("world"); // str 为null 则返回world 否则为hello
  System.out.println(string);
  ```

  

* `boolean isPresent()  `：判断Optional容器中是否有值

  ```java
  Optional<String> op = Optional.of("hello");
  boolean present = op.isPresent(); 
  ```

  

* `void ifPresent(Consumer<? super T> consumer) `：判断Optional容器中的值是否存在，如果存在，就对它进行Consumer指定的操作，如果不存在就不做

  ```java
  Optional<String> op = Optional.of("hello");
  op.ifPresent(s -> System.out.println("存在值"));
  ```

* <U> Optional<U> map(Function<? super T,? extends U> mapper)  

  判断Optional容器中的值是否存在，如果存在，就对它进行Function接口指定的操作，如果不存在就不做

  ```java
  @Test
  public void test10(){
      String str = "Hello";
      Optional<String> opt = Optional.ofNullable(str);
      //判断是否是纯字母单词，如果是，转为大写，否则保持不变
      String result = opt.filter(s->s.matches("[a-zA-Z]+")).
          map(s -> s.toLowerCase()).
          orElse(str);
      System.out.println(result);
  }
  ```

# ====数据库连接===

# JDBC

## 概念 

JDBC：Java Database Connectivity，**一组独立于任何数据库管理系统（DBMS）的API**。

它的声明在java.sql与javax.sql包中，是SUN提供的**一组接口规范**。由各个数据库厂商来提供实现类，这些实现类的集合构成了数据库驱动jar。

![image-20220506094048348](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220506094048348.png)



## 连接使用

连接数据库的基本步骤

1. 创建connection ，数据库所在服务器的地址、数据库名、账户、密码 
2. 创建 statement ，用于执行 sql语句 
3. 处理结果集 
4. 关闭资源 

```java
public void testConnection() throws ClassNotFoundException, SQLException {
    Class.forName("com.mysql.jdbc.Driver");  // reflect, create a JDBC object 

    // schema://host:port/database?params
    String url = "jdbc:mysql://localhost:3306/day04?useUnicode=true&characterEncoding=utf8";
    String user = "root";
    String password = "root";
    Connection connection = DriverManager.getConnection(url, user, password);  // connection
	
    // connect 
    Statement statement = connection.createStatement(); // statement , used to execute sql statement
    ResultSet resultSet = statement.executeQuery("select *from user");

    // next() to obtain next row value
    while (resultSet.next()) {
        //获取每一列的数据 columnIndex
        System.out.println(resultSet.getObject(1));
        System.out.println(resultSet.getObject(2));
        System.out.println(resultSet.getObject(3));
        System.out.println(resultSet.getObject(4));
        System.out.println("-----------");
    }

    // close
    if (resultSet != null) {
        resultSet.close();
    }

    if (statement != null) {
        statement.close();
    }

    if (connection != null) {
        connection.close();
    }
}
```



## PreparedStatement

使用statement方式，查询数据的时候，会发生SQL注入问题。所谓SQL注入，**指的是在 字符串拼接SQL语句时，发生了结构的改变。**

SQL注入

```java
String username = "hahahahha' or '1'='1"; 
String sql = "SELECT * FROM user where username='" + username + "'";
//结果会把所有数据都查询出来
Statement st = conn.createStatement();
ResultSet rs = st.executeQuery(sql);
```



PreparedStatement可以避免SQL注入的问题。它会**对参数化的SQL语句进行预编译** 

```java
// connection 同上 

// 参数化sql
String sql = "insert into user values(null,?,?,?)";  // 参数化的sql语句 ？表示待定参数 
PreparedStatement pstm = connection.prepareStatement(sql); //预编译

//设置参数 
pstm.setObject(1, username);  // 参数序号 参数值
pstm.setObject(2, password);
pstm.setObject(3, nickname);

// 执行
int count = pstm.executeUpdate();//此处不能传sql
System.out.println(count);
```



### 获取自增长键

`executeUpdate()` 返回受影响的行数，某些业务场景下，需要返回自增长的主键。 

```java
public void testAutoKey() throws Exception {
    String sql = "insert into user (username,password,nickname) values(?,?,?)";
    // 第二个参数 要求预编译返回自增主键
    ps = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);  

    // 设置参数
    ps.setObject(1, "hollis");
    ps.setObject(2, "root");
    ps.setObject(3, "jhk");
	
    ps.executeUpdate();
    ResultSet rst = ps.getGeneratedKeys();  // 自增长的主键 结果集
    while (rst.next()) {
        Long id = (Long) rst.getObject(1); // 获取第一列 
        System.out.println("auto key:" + id);
    }

    if (rst != null) {
        rst.close();
    }

}
```



### 批量更新

1. url 补充参数 `rewriteBatchedStatements=true`  
2. 批量设置参数 ，每次更新参数以后 使用`addBatch()` 
3. 执行 `executeBatch()` 

```java
public void testBatch() throws Exception{
    	// 更新url 协议 ，补充参数 `rewriteBatchedStatements=true` 
        String url = "jdbc:mysql://localhost:3306/day04?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true";
        String user = "root",pwd = "root";
		
        Class.forName("com.mysql.jdbc.Driver");
        Connection conn = DriverManager.getConnection(url,user,pwd);

        String sql = "insert into user(username,password,nickname) values(?,?,?)";
        PreparedStatement ps = conn.prepareStatement(sql);
		
    	// 批量设置参数 
        for(int i=0;i<1000;i++){
            ps.setObject(1, "aobama"+i);
            ps.setObject(2, "000000"+i);
            ps.setObject(3, "圣枪游侠"+i);

            ps.addBatch(); // 添加到batch
        }

        ps.executeBatch();  // 执行batch 

        // 关闭
        ps.close();
        conn.close();

    }
```



## 事务

使用事务步骤：

1. 关闭连接的自动提交 
2. 使用 `try-catch-finally` 包裹代码块，异常则回滚，最后关闭资源，恢复自动提交 

```java
public void testTransfer() throws Exception{
    // transfer
    String sql = "update account set money=money+? where name=?";
    ps = connection.prepareStatement(sql); // connection 是初始化的Conneciton实例 

    try{
        connection.setAutoCommit(false); // 关闭自动提交
        ps.setObject(1,-500);
        ps.setObject(2,"zs");

        ps.executeUpdate();

        ps.setObject(1,500);
        ps.setObject(2,"ls");

        ps.executeUpdate();

        connection.commit();
    }catch (Exception e){
        System.out.println("发生异常");
        System.out.println(e);
        connection.rollback(); // 发生异常回滚
    }finally {
        connection.setAutoCommit(true); // 恢复自动提交
        // 关闭资源 
        ps.close();
        connection.close();
    }
}
```



## 连接池

单个连接的反复创建销毁会浪费CPU资源，降低响应时间，尤其不利于多用户并发的场景。 

连接池，是**多个连接（connection）的缓冲池，可以设置每次连接的最大数量，同时能够复用这些连接**，免去创建销毁之间的开销。

连接池的原理类似于队列，划分一个空闲池 和 激活池，每次新建连接的时候就从空闲池拿出一个连接，销毁的时候就从激活池放回一个连接到空闲池，如此往复。如果激活池达到了最大连接数量，则等待。



### 连接池的实现

JDBC 的数据库连接池使用 javax.sql.DataSource 来表示，DataSource 是一个接口，所有的连接池都要实现该类。



常见连接池 

* **DBCP** 是Apache提供的数据库连接池，**速度相对c3p0较快**，但因自身存在BUG，Hibernate3已不再提供支持
* **C3P0** 是一个开源组织提供的一个数据库连接池，**速度相对较慢，稳定性还可以**
* **Proxool** 是sourceforge下的一个开源项目数据库连接池，有监控连接池状态的功能，**稳定性较c3p0差一点**
* **HikariCP** 俗称**光连接池**,是目前速度最快的连接池
* **Druid** 是阿里提供的数据库连接池，据说是集DBCP 、C3P0 、Proxool 优点于一身的数据库连接池



使用步骤

1. 加入jar包到lib文件夹，例如：druid-1.1.10.jar 

2. 添加配置文件`druid.properties`到 类路径的`resources`下  。配置内容如下 

   ```java
   driverClassName=com.mysql.jdbc.Driver
   url=jdbc:mysql://localhost:3306/test
   username=root
   password=123456
   initialSize=5
   maxActive=10
   maxWait=1000
   ```

3. 创建连接池对象，取出新连接

   ```java
   import com.alibaba.druid.pool.DruidDataSourceFactory;
   import javax.sql.DataSource;
   import java.io.File;
   import java.io.FileInputStream;
   import java.io.InputStream;
   import java.sql.Connection;
   import java.util.Properties;
   
   public void testDruid() throws Exception {
       // 创建一个Properties对象，读取druid.properties文件
       Properties properties = new Properties();
   	
       // 可以从输入流读取配置文件 也可以使用类加载器 读取到resources的资源文件夹 
       // FileInputStream is = new FileInputStream("resources/druid.properties");  // 使用文件流
       // TestDruid 是类名 
       InputStream is = TestDruid.class.getClassLoader().getResourceAsStream("druid.properties");   // 使用类加载器
       properties.load(is); // 加载配置 
   
       // 创建连接池
       DataSource dataSource = DruidDataSourceFactory.createDataSource(properties);
       // 获取一个连接
       Connection connection = dataSource.getConnection();
   }
   ```
   



实际应用时，保证代码中只初始化一次连接池对象，**可以使用静态代码块或者单例模式，来封装项目中的连接池。**

他们的思想是一致的，只是实现手段有所区别。

静态代码块

```java
public class JDBCTool {
    private static DataSource ds = null;

    static {
        Properties properties = new Properties();
        // 使用类加载器
        InputStream is = TestDruid.class.getClassLoader().getResourceAsStream("druid.properties");   
        try {
            properties.load(is);
            ds = DruidDataSourceFactory.createDataSource(properties);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    public Connection getConnection(){  // 创建连接对象 
        try{
            return ds.getConnection();
        }catch (Exception e){
            throw  new RuntimeException(e.getMessage());
        }
    }
}
```



单例模式 

```java
public class JDBCTool {
    private static DataSource ds = null;
    private static JDBCTool instance = null;

    private JDBCTool() throws Exception {  // 构造函数 负责初始化连接池
        Properties properties = new Properties();
        InputStream is = TestDruid.class.getClassLoader().getResourceAsStream("druid.properties");   // 使用类加载器
        properties.load(is);
        ds = DruidDataSourceFactory.createDataSource(properties);
    }

    public static JDBCTool getInstance() {
        try {
            if(JDBCTool.instance==null){
                System.out.println("初始化");
                JDBCTool.instance = new JDBCTool();
            }
            return JDBCTool.instance;
        } catch (Exception e) {
            System.out.println(e);
            throw new RuntimeException(e.getMessage());
        }
    }

    public Connection getConnection(){
        try{
            return JDBCTool.ds.getConnection();
        }catch (Exception e){
            throw  new RuntimeException(e.getMessage());
        }
    }
}
```

## DBUtils

commons-dbutils 是 Apache 组织提供的一个开源 JDBC工具类库，**对JDBC的增删改查进行了封装，使用更简单。** 

它对SQL的操作，向外暴露最基本的3个参数：connection对象、sql语句、待定参数。 



创建QueryRunner以执行SQL语句。

`.update(Connection conn, String sql, Object... params)`方法，用于执行增删改的SQL语句

```java
import org.apache.commons.dbutils.QueryRunner;

QueryRunner queryRunner = new QueryRunner();

// update , insert, delete 同理 
String sql = "update user set password = ? where username = ?";
Object[] params={"222","zs"};

// 第一个参数是 connection对象，sql语句,sql参数 
queryRunner.update(JDBCTool.getConnection(),sql, params); 
```



`.query(String sql, ResultSetHandler<T> rsh, Object... params)`方法用于查询，它的第二个参数如下：

| **BeanHandler**     | 将结果集中第一条记录封装到一个指定的javaBean中。             |
| ------------------- | ------------------------------------------------------------ |
| **BeanListHandler** | **将结果集中每一条记录封装到指定的javaBean中**，将这些javaBean在封装到List集合中 |

```java
@Test
public  void selectById() throws SQLException{
    //创建queryRunner对象
    QueryRunner queryRunner = new QueryRunner();
    String sql = "select * from user where id = ?";
    Object[] params = {1};
		
    // query 
    User user = queryRunner.query(JDBCTools.getConnection(),sql, new BeanHandler<>(User.class), params);
    System.out.println(user.toString());
}
```



批处理多条sql语句

```java
@Test
public void testQR() throws SQLException {
    QueryRunner queryRunner = new QueryRunner();

    String sql = "insert into user(username,password) values(?,?)";
    int items=20;
    Object[][] params= new Object[items][2];  // 二维数组
    for(int i=0;i<items;i++){
        params[i] = new String[]{"hollis_"+i,"6666_"+i}; // 设置参数 
    }
	
    // 批处理
    queryRunner.batch(JDBCTool.getConnection(),sql, params); // connection对象，sql语句,sql参数

}
```
