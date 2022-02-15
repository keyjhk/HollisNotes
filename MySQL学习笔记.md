[toc]

# Mysql

mysql，一种关系型数据库，基于TCP通信（各类语言都支持mysql的原因之一），默认开放3306端口，传输SQL语句。



关系型数据库：以行和列的形式来存储数据，对应一张二维表。二维表的行定义被称作“关系模式”，即是对该表关系的描述。**一个关系型数据库就是由多个二维表及其之间的关系组成的一个数据组织**。

关系型数据库的读取、查询较为方便，强调[事务](##事务) 的ACID原则。存储海量数据时，由于多表关联、表级锁等特性，读写性能不足，且只具备纵向扩展的能力。



# 配置



**Mysql语法规范：**

* 语句末尾使用`;`结束

* 不区分大小写，但**建议关键字大写，表名、列名小写**

* 每条命令根据需要，可以进行缩进或换行，以增强可读性

* 注释：（1）#注释（2）`-- `+注释，注意两个横杠之后有空格（3）`/*注释*/`

* 不区分字符、字符串，统统使用单引号包裹；当表名、字段名等与sql关键字重名时，需要使用**反引号**包裹。

  ```mysql
  create table `select` (`desc` char(32));	#反引号使用示例
  insert into student(name) values('ZhangSan');	#插入示例
  ```

  

Mysql服务相关：

* 查看当前mysql的版本：mysql环境，`select version()`；命令行，`mysql --version`或者`mysql -V`

* Mysql启动/停止：

  * windows：以管理员权限进入**cmd界面**，执行`net start(stop) mysqlxxx`，mysqlxxx表示服务名（我的计算机，右键，管理可查）
  * linux：`sudo service mysql start` ，使用`ps -elf|grep mysql`查看相关服务是否启动

* 用户登录：**必须先启动mysql服务才可以登录**
  * windows下，roo用户可以通过安装以后自动生成的“ mysql command line ”启动
  * 命令行，执行`mysql [-h localhost] [-P 3306] -u user_name  -p[password]`，p参数和密码之间不允许有空格，或者省略直接回车，在下一行提示输入。
  
* 退出mysql环境：`exit`或者`crtl+c`

* mysql历史命令记录：`~/.mysql_history`  

* **mysql 备份、恢复**：备份并非直接备份数据，而是备份生成该数据库的执行语句；当只备份一个数据库或数据库的若干表时，恢复前必须先创建一个空的数据库（因为sql语句不含创建数据库语句）。

  ```mysql
  #命令行环境执行 
  
  #备份
  mysqldump -u user_name -p'password' db_name>backup.sql	#备份指定数据库
  mysqldump -u user_name -p'password' db_name t_name [t1_name..]>backup.sql#备份指定数据库的若干表 
  mysqldump -u user_name -p'password' db_name>backup.sql	#备份指定数据库
  mysqldump -u user_name -p'password' --databases db1 [db2 ...]>backup.sql #备份若干数据库
  mysqldump -u user_name -p'password' --all-databases>backup.sql #备份所有数据库
  
  #备份的同时压缩，利用管道符|
  mysqldump -u user_name -p'password' db_name|gzip>back.sql	#备份指定数据库
  
  #恢复
  mysql -u user_name -p'password' new_db_name<backup.sql #恢复
  ```



# 账户管理

查看所有用户：用户信息存储于 mysql.user 表中。

```mysql
select host,user,authentication_string from user;	#查看主机，用户，密码
```



**单独创建账户**：`CREATE 'user'@'host' IDENTIFIED BY 'passwd' ` ，该命令创建的用户默认只有登录权限。

**创建账户并授权**：`GRANT privilege_list ON db_name TO 'user'@'host' IDENTIFIED BY 'passwd'` ，可以助记为“on+地点 ，to+用户，by+密码” 。该命令在创建用户的同时授权，且只能root账户执行。

* `privilege_list`，权限分配列表，多个权限以逗号分隔：

  常用权限：

  * 建表：create
  * 删除：drop
  * 改：insert；modify；change；alter；
  * 查：select
  * 全部权限：`all privileges` 

* `user@host`：“用户+访问主机名”，作为一个授权单位

* `db_name`，数据库：可以指定数据库的某几个表`db.xx`，或者数据库的全部表`db.*`，或者全部数据库的表`*.*`  

**查看账户权限**：`SHOW GRANTS FOR 'user'@'host'` 

**修改存在用户的权限**：

* 授予：`GRNAT privilege_liost ON db_name TO 'user'@'host' WITH GRANT OPTION`，修改权限后需要刷新`FLUSH PRIVILEGES` 。
* 撤销：`REVOKE privilege_list ON db_name from 'user'@'host'` ，同样权限修改后要刷新。

**删除用户**：`DROP USER 'user_name'@'host'`  

**用户密码修改**：需要以root用户登录

* 密码修改：`alter user 'user_name'@'host' IDENTIFIED BY 'passwd'`  。
* 加密规则修改（5.7+）：`ALTER USER 'user_name'@'host' IDENTIFIED WITH mysql_native_password ` 。mysql5.7版本以后将加密规则从 “ mysql_native_password ”改为“ caching_sha2_password ” 。
* 关于root用户密码修改：5.7版本，root用户的`plugin`为`auth_socket`，**该plugin不关心密码也无法设置密码**，只要是本地就可以直接使用`sudo mysql -u root`登录（不加sudo会提示permission denied）。使用`alter`修改密码时，即使显示修改成功也不会生效。因此，在修改root密码前，需要先修改plugin为`mysql_native_password`或者修改的同时使用`identified with mysql_native_password ` `修改加密规则 ，然后设置host=%（允许远端登录） 。



**允许用户远程连接**：实际操作时，发现5.7版本除以下操作外，还需要额外修改配置文件`/etc/mysql/mysql.conf.d/mysqld.cnf` ，注释其中的`bind_address=127.0.0.1` 

```mysql
update mysql.user set host='%' where user='user_name';
flush privileges;
```

# 数据库

* 新建：`create database dbname [charset utf-8]` 
* 删除：`drop database dbname` 
* 显示：`show databases`，查看当前用户可见的数据库  
  * 显示某个数据库的创建信息：`show create database dbname`
* 进入 ：`use d1`，必须先进入数据库才能查看该库中的表 ，类似于`cd folder_name`进入文件夹
* 显示：`select database()` ，查看当前使用数据库 。类似于`pwd` 

# 表

## 常用命令

* 创建表：`create table table_name (column_name column_type [,...])`，创建t1表，其后跟`()`创建字段，声明顺序为“ 字段名 字段类型 字段属性”，彼此以空格分割。[mysql数据类型](https://www.runoob.com/mysql/mysql-data-types.html)  

  ```mysql
  /*创建学生表
  设置字段的属性为 NOT NULL， 在操作数据库时如果输入该字段的数据为NULL ，就会报错。
  AUTO_INCREMENT 定义列属性 自增 ，一般用于主键，数值会自动加1，默认初值为1
  default 指定默认值，不用写SET关键字
  PRIMARY KEY关键字用于定义列为主键，可以使用多列来定义主键，列间以逗号分隔
  */
  create table student(
  id int auto_increment primary key,
  name char(32) not null,
  age int not null default 20,
  register_date date not null);
  
  
  #使用desc student;查看该表结构 
  +---------------+----------+------+-----+---------+----------------+
  | Field         | Type     | Null | Key | Default | Extra          |
  +---------------+----------+------+-----+---------+----------------+
  | id            | int(11)  | NO   | PRI | NULL    | auto_increment |
  | name          | char(32) | NO   |     | NULL    |                |
  | age           | int(11)  | NO   |     | NULL    |                |
  | register_date | date     | NO   |     | NULL    |                |
  +---------------+----------+------+-----+---------+----------------+
  ```


* 删除表：`DROP TABLE [IF EXISTS] table_name1 [ ,table_name2,...]` ，批量删除表；若未使用IF EXISTS，删除不存在的表会报错 

* 查看表结构：`desc t1`，desc=describe

* 显示：

  * `show tables [from db_name]`：显示指定数据库的表，缺省时为当前数据库。
  * `show create table table_name`：显示该表的创建信息
  
* 查询：SELECT关键字 （[select完整语法和执行顺序及虚拟表](https://www.jb51.net/article/161719.htm)  ）。可以使用`EXPLAIN select_command`模拟mysql的查询顺序，分析性能瓶颈（[关于explain语句的执行结果](https://www.jianshu.com/p/ea3fc71fdc45)）

  ```mysql
  /* 
  *表示查询所有
  as 可以为列名，表名取别名，在返回结果时将以别名显示，
  distinct表示对查询结果去重
  limit表示分页查看，从start条记录起（含）开始查看count条记录，序号从0开始计数 
  	limit不支持运算表达式，仅支持常数 
  */
  select [distinct] c [as c1] [,..] 	
  from table_name [as t_name] 
  [limit start,count]	
  
  #查询常量，可以是表达式、函数
  select version();
  select 5*8;
  
  #多表查询as示例, “.”运算符用于“表名.字段名”
  select s.id as student_id, c.id as class_id from student as s,class as c
  ```

  

* 插入：`insert into table_name (column1,column2 [,...]) values (var1,var2 [,...])`，

  ```mysql
  #指定字段名插入,缺省的字段应当允许其为null或具备默认值 
  insert into student (name,age,register_date) values ('ZhangSan',23,'2020-01-01') 
  #特别地，当字段是自增auto_increment时，插入分以下情况
  #1. 缺省该字段 insert into student(name) values('test');	序列成功自增
  #2. 指定序号0，自增默认从1开始，若指定序号0，不会和已存在字段值冲突 ，且会自增 
  #3. 指定1个已经存在的序号插入，会报错，
  
  #全字段插入
  insert into student values('ZhangSan',23,'2020-01-01');
  
  #一次插入多行，values部分以，分隔
  insert into student(name,age) values('ZhangSan',12),('Lisi',20);
  ```
  
* 删除：`delete from table_name where condition` ，根据指定条件筛选相关数据并删除 ，是行删除。当where子句缺省时，就是删除全表数据。

  ```mysql
  delete from student where name='ZhangSan';	#删除表中所有名为ZhangSan的数据项
  ```
  
* 修改：`update table_name set filed_name=var,[...] [where column2=var2]` ，支持一次修改多个字段 。当没有where做条件限制时，update会修改全部信息。

  ```mysql
  update student set name='ZhangSan',age=33 where id>4; #修改所有id>4的数据项
  ```

* 修改字段名：`alter table table_name [drop| add| modify| change| alter]`，分别对应删除、增加、修改字段名、修改默认值。**注意，alter相比其他关键字其后多了一个`table`** 

  ```mysql
  #drop示例
  alter table student drop age #删除表中age字段，是 列删除
  
  #add示例
  #新增sex字段，int类型，默认添加在表尾，可使用after、first指定该字段的位置
  alter table student add sex int [after field_name|first] 
  
  #modify小改，改字段类型；change大改，改字段名+字段类型
  alter table student modify sex char(1)	#modify相当于重新声明字段，会覆盖上一次的信息
  alter table student change sex SEX char(10)	#change +旧子字段名+新字段名+类型 
  
  #alter示例
  alter table student alter sex set default 'MALE'	#修改sex默认值
  alter table student alter sex drop default 'MALE'	#丢弃sex默认值
  ```

  由于增删改查是最常用的几个命令，所以放在一起，总结如下

  | 命令 | 语法                                       |
  | ---- | ------------------------------------------ |
  | 增   | insert into tb_name() values()             |
  | 删   | delete from tb_name where col=var          |
  | 改   | update tb_name set col=var where col1=var1 |
  | 查   | select col from tb_name where col1=var1    |

  

* 条件判断：`where condition1 [and or] condititon2 [,...] `，类似于编程语言中的`if`判断，其后跟条件。


  * 逻辑判断符号：等于：`=`；不等于，`<>`、`!=`；大于：`>`、`>=`，小于号类似；`in` （相当于or运算）、`not in`；`any()`、`all()` ，类似于python里的any 、all，但仅支持对select返回的结果运算。

  ```mysql
  select * from student where (name,age)=('ZhangSan',19);	#支持类似于python元组解包的写法
  select * from student where name='ZhangSan' and age=19;	#与上一种写法类似 
  select * from student where hometown in ('杭州','宁波');#in 用法示例 
  ```

  * 模糊搜索：`LIKE`配合`%`、`_`实现模糊搜索。`%`类似于`*`通配符表示任意多个字符，`_`类似于`.`匹配任意1个字符。当单独使用LIKE语句时，效果相当于`=`。

  ```mysql
  select * from student where name like Zhang% 	#搜索表中所有Zhang开头的数据 
  select * from student where name like Zhang_ 	#搜索表中所有名为Zhangx形式的数据  
  ```

  * 范围判断：`in (a,...)`，判断是否属于集合，可以不只是数字；`between start and end`，连续范围闭区间[start,end]判断 

  ```mysql
  select * from student where id in (3,8);	#查找编号为3、8的学生
  select * from student where id between 3 and 8;	#查找编号为3-8的学生
  ```

  * null的特殊性，**mysql中null必须用专门的语句`is null`、`is not null`来判断，不可使用`=`、`<>`运算符**。

  ```mysql
  select * from student where sex is null;
  ```

* 排序：`SELECT field1 [,..] FROM table_name ORDER BY [RAND()] filed1 [ASC|DESC] [,field2 DESC]`。rand()表示随机排序，字段排序默认按照升序排序 。排序+limit配合使用可以实现取“ 前k大 ”的效果

  ```mysql
  select * from student order by grades desc,id asc;	#按照grades字段降序排列，id字段升序
  select * from student order by grades desc limit 0,3	#取成绩前3名 
  ```

* 连接运算：`inner join`（A交B）、`left join`（A-B）、`right join` （B-A），`on`指定两个表参与运算的字段。执行顺序在where之前  。

  * 交：`SELECT * FROM A INNER join B ON A.column_a=B.column_b`，求A、B两张表各自column_a与column_b的值的交集
  * 差：`SELECT * FROM A LEFT JOIN B ON A.column_a=B.column_b` ，求差集 
  
  

## 聚合函数

```mysql
#统计行数count(*)
select count(*) from student where sex='f';	#统计男生数

#求某个字段的最大值max,最小值min
select max(id) from student where sex='m';	

#求和sum
select sum(grades) from student where sex='f';	#女生的总成绩

#均值 avg
select avg(grades) from student where sex='f';	#女生的平均成绩

```



## 分组

假设有表如下：

```mysql
+----+------+-----+----------+
| id | name | age | hometown |
+----+------+-----+----------+
|  1 | 张三 |  25 | 杭州     |
|  2 | 李四 |  20 | 台州     |
|  3 | 王五 |  16 | 台州     |
|  4 | 赵六 |  17 | 宁波     | 
|  5 | 钱七 |  29 | 宁波     |
+----+------+-----+----------+ 
```



使用`group by`关键字按指定字段对表数据分组，语法为`select FIELD from table_name group by FIELD`，前后字段名FIELD相同，将返回数据表按照FIELD字段的分组结果。 

```mysql
select hometown from student group by hometown;	#按照家乡对学生分组
+----------+
| hometown |
+----------+
| 台州     |
| 宁波     |
| 杭州     |
+----------+
```



group by单独使用的情况下，和`select distinct field from table_name`无异，均可以实现分组效果（也就是去重）。但group可以配合其他函数实现更强大的功能。

在下列函数使用时，便于理解，**可以认为先分组（group）再查询（select）。**

* 配合`group_concat(expr [order by field asc] [seperstor 'str'])` **显示每个分组信息**，可以指定order、separator等关键字，定制返回信息。
* 配合聚合函数实现统计功能，例如count()、avg()
* 配合having 函数实现分组过滤，作用和where类似，但只能用于group by之后 
* 配合rollup函数，rollup会在最后新增一行，统计每个字段的总和 

```mysql
SELECT hometown,GROUP_CONCAT(name) FROM student GROUP BY hometown;	#x显示分组的信息
+----------+--------------------+
| hometown | GROUP_CONCAT(name) |
+----------+--------------------+
| 台州     | 李四,王五          |
| 宁波     | 赵六,钱七          |
| 杭州     | 张三               |
+----------+--------------------+

# 分隔符使用
SELECT hometown,GROUP_CONCAT(name SEPARATOR '--') FROM student GROUP BY hometown;
+----------+-----------------------------------+
| hometown | GROUP_CONCAT(name SEPARATOR '--') |
+----------+-----------------------------------+
| 台州     | 李四--王五                        |
| 宁波     | 赵六--钱七                        |
| 杭州     | 张三                              |
+----------+-----------------------------------+

# 配合count函数使用
SELECT hometown,GROUP_CONCAT(name),COUNT(*) FROM student GROUP BY hometown;
+----------+--------------------+----------+
| hometown | GROUP_CONCAT(name) | COUNT(*) |
+----------+--------------------+----------+
| 台州     | 李四,王五          |        2 |
| 宁波     | 赵六,钱七          |        2 |
| 杭州     | 张三               |        1 |
+----------+--------------------+----------+

#配合having 函数
SELECT hometown,GROUP_CONCAT(NAME),COUNT(*)
FROM student
GROUP BY hometown
HAVING COUNT(*)>1;	#筛选组员数大于1的分组
+----------+--------------------+----------+
| hometown | GROUP_CONCAT(NAME) | COUNT(*) |
+----------+--------------------+----------+
| 台州     | 李四,王五          |        2 |
| 宁波     | 赵六,钱七          |        2 |
+----------+--------------------+----------+

#配合with rollup函数
SELECT hometown,GROUP_CONCAT(NAME),COUNT(*) FROM student
GROUP BY hometown
WITH ROLLUP;
+----------+--------------------------+----------+
| hometown | GROUP_CONCAT(NAME)       | COUNT(*) |
+----------+--------------------------+----------+
| 台州     | 李四,王五                |        2 |
| 宁波     | 赵六,钱七                |        2 |
| 杭州     | 张三                     |        1 |
| NULL     | 李四,王五,赵六,钱七,张三 |        5 |
+----------+--------------------------+----------+
```



## 自关联

类似于树的双亲表示法，通过`self.id` 指向不同的数据项（顶层id指向null），实现一张表内的级联操作。常见应用有省份市区级联、网盘虚拟目录、树形菜单。

地区级联操作示例

| aid（地区ID） | pid（父id） | atitle（地区名） |      |
| ------------- | ----------- | ---------------- | ---- |
| 01            | null        | 浙江省           |      |
| 02            | 01          | 杭州市           |      |

[自关联](https://blog.csdn.net/hubingzhong/article/details/81277220) 查询示例 

```mysql
#查询浙江省的所有市
select * from  areas as city	#取别名为city
inner join areas as province 	#取别名为province
on city.pid=province.aid	
where  province.atitle='浙江省' 
```



## 子查询 视图

子查询：查询时用到了多个select。最前的一个select称作主查询，其余select作为子查询。子查询一般充当主查询的数据源、条件。



子查询分类：依据`select`返回的结果分类

* 标量子查询：子查询返回`1*1`的数据
* 行向量子查询：子查询返回`1*n`，一行多列的数据。与`and`连接多个条件同理。
* 列向量子查询：子查询返回`n*1`，一列多行的数据  





在使用子查询时，若条件复杂，可以先分解条件，再逐步编写，类似正则的” 逐步拆解，增量编写 “。书写上，子查询向右缩进一格，便于辨认。

标量子查询示例：

* 查询班级中身高大于平均身高的学生信息：

  ```mysql
  select * from student where height>(
  	select avg(height) from student;
  ```

行向量子查询示例：

* 查询班级里身高最高且年龄最大的学生所有信息

  ```mysql
  select * from student where (height,age)=(
  	select max(height),max(age) from student);
  ```

列向量子查询示例：字段筛选条件需要用到子查询 

* 此处仅示例，表示子查询返回的是列信息  

  ```mysql
  select name from classes where id in (
      select cls_id from students); 
  ```



子查询还可以充当insert语句的数据源，此时不用再加values关键字。如

```mysql
insert into student(name,age) (
    select name,age from student where id=1)`; 
```

***

**视图**：**存储select语句返回的结果，一张虚表**，数据源于原表。若原表数据发生变化，视图也会跟随变化，**可以认为视图是一个自定义的select函数**，输入源数据，输出目的数据。使用视图，可以降低复杂查询的select语句编写难度，在子查询中，一旦条件增加，**多个select嵌套一来使语句可读性下降，二来不利用重用**。而视图作为虚表存储此中间结果，正能解决问题。



视图操作：

* 创建视图：`CREATE VIEW view_name as (select语句)` ，使用view关键字 ，视图名建议以V开头，便于区分 
* 查看视图：`show tables`，被视作table对待
* 查询视图：`select field [,..] from view_name`，被视作table对待
* 删除视图：`DROP VIEW view_name` 



## 主键 

主键：唯一的，一个数据表只能包含一个主键。但主键可以包含多个字段，此时称作“ 复合键 ”。

主键在选择时，不仅要考虑非空、唯一这两个条件，实际上这只是最小要求。还要考虑下面的因素

1. 简单性：例如用户的指纹就不适合拿来当主键。因为它过于复杂了。主键通常都会在多个表中做为关联字段使用的，过于复杂的主键会增加表的存储负担。
2. 稳定性：主键的更改会给数据库系统造成灾难，所以主键一定要稳定，不会因为任何因素发生更改。所以身份证号码其实不适合拿来当主键。
3. 业务无关性：这和稳定性相关联，只要和具体业务相关，就很难避免编码规则的更改。
4. 独立性：一个主键必须能标识一条记录，一条记录也必须只有一个主键（或主键集）。比如电话号码就不适合当主键，虽说它也具有非空性和唯一性，但不能避免某人有多个电话卡。

## 外键 

关联两张表，约束本表该字段数据，使其只能**引用另外一张表的列值**。外键引用保持数据的一致性，但大量关联会降低查改速度（每次会检查插入数据是否合法）。

外键创建语法：

1. 创建表时一同创建外键

```mysql
create table(
id int PRIMARY KEY,
KEY `field` (`field`),	#一定要有先这句 
#此处创建外键 
)

[CONSTRAINT symbol] 	#外键别名
FOREIGN KEY (field) REFERENCES ref_table_name(ref_tab_field)		#外键创建 
[ON DELETE|UPDATE {RESTRICT|CASCADE|SET NULL|NO ACTION|SET DEFAULT}]	#修饰字段

/*
CONSTRAINT为该外键约束命名，可以在删除外键时使用，若省略，系统会自动命名
field字段为本表外键字段名，t_field表示主表table_name里的引用字段名
ON DELETE|UPDATE 为事件触发，当主表引用字段发生相应动作时触发，其动作含义如下
    RESTRICT（限制外表中的外键改动）
    CASCADE（跟随外键改动）
    SET NULL（设空值）
    SET DEFAULT（设默认值）
    NO ACTION（无动作，默认的
*/
```

2. 通过`alter .. add` 为已有字段增加外键。外键字段类型应当和本表已有字段类型一致，否则添加失败。添加时有无数据均可。

```mysql
ALTER TABLE table_name ADD [CONSTRAINT symbol]	#为外键取别名
FOREIGN KEY (field) REFERENCES ref_table (ref_tab_field);	#field为本表已有字段，ref_tab为引用表
```

外键信息可以通过`show create table tabl_name`查看。



删除外键约束：`ALTER TABLE table_name DROP FOREIGN KEY symbol`，symbol为外键别名，非字段名。外键约束字段必须先解除外键约束，才可以删除（alter..drop）该字段，否则报错。



外键约束体现：

* 从表插入的数据不可以是主表引用字段未出现的数据
* 主表不可随意删除已经被子表引用的字段

## 索引

索引，一种数据结构，便于快速查询。

**对数据库的字段建立索引可以显著加快查询速度**（当表数据较小时不明显）。但另一方面，**索引存储本身需要占用一定空间，建立太多的索引同时**，为了维护索引，相对地也会增加修改（索引）、删除（索引）、增加（索引）等操作的耗时。



mysql索引分类：

* 按照索引类型：
  * 普通索引：index，无限制
  * 唯一索引：unique，要求字段值唯一，字段允许为空。允许多个字段组合作为唯一索引
    * 主键索引：primary ，特殊的唯一索引，但不允许值为空，一个表必定拥有1个主键索引。
  * 全文索引：fulltext，检索文本关键字时具备优势，仅MyISAM引擎支持

* 按照索引字段数：

  * 单列索引：索引只包含一个字段

  * 联合（多列）索引：索引包含多个字段，遵循“最左匹配原则”，比单独地为每个字段建立索引更加高效。

    * **mysql创建联合索引的规则**：先创建最左字段的索引，也就是排序，在第一个字段的基础上再进行第2字段的索引，以此类推。可见，第一字段在该复合索引中是绝对有序的，而之后的字段仅在第一字段重复排序相同时才能有序。例如，对字段`index(a,b,c)`建立联合索引，直接`where c=xx`是不能利用索引优势的，只能遍历得到。复合索引的这个特性直接决定了最左匹配原则 

    * 最左匹配原则（[mysql索引最左匹配原则的理解? - 沈杰的回答 - 知乎](https://www.zhihu.com/question/36996520/answer/93256153)）：检索数据时从联合索引`index(a,b[,..])`的最左字段开始匹配，可以加速以该字段开始的多字段索引，如`(a)、(a,b)、(a,b,c)`等。查询优化器会确定最终的索引方案，和`and`的书写顺序无关，如`where a and b`和`where b and a`等价。 

* 索引与行记录是否分开存储（[聚集索引与非聚集索引](https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961494&idx=1&sn=34f1874c1e36c2bc8ab9f74af6546ec5&chksm=bd2d0d4a8a5a845c566006efce0831e610604a43279aab03e0a6dde9422b63944e908fcc6c05&scene=21#wechat_redirect)）：

  * 聚集索引：InnoDB的索引，主键索引与行记录一起存储。普通索引存储主键索引（因此要求主键索引不要太长）。 

    <img src="pictures/聚集索引.webp.jpg" style="zoom: 50%;" /> 

  * 非聚集索引：MyISAM的索引，索引与行记录分开存储，叶子节点存储索引和对应行的指针

    

<img src="pictures/非聚集索引.webp.jpg" style="zoom: 50%;" /> 



mysql使用哈希、B+树等数据结构建立索引（[哈希值、B+树索引区别_](https://www.cnblogs.com/heiming/p/5865101.html)）：

哈希索引（key-value形式）：

* 哈希索引利于等值查询，时间复杂度为`O(1)`，优于B+树。但面对范围查询时，退化为`O(n)`，同时不支持**多列联合索引的最左匹配原则**。 

* 当表中存在大量重复键值时，由于哈希冲突的存在，索引效率降低。
* 哈希索引对磁盘的连续存储空间要求较高。

B+树：B+树为多路查找树，查找效率平均为`O(log_n)`。树的高度可以很低（意味着较少的IO次数），相邻叶子节点之间存在指针，范围查找效率高。对磁盘的连续存储空间要求低。





索引相关操作：

* 创建索引：`CREATE INDEX index_name ON table_name(file_name(len))`，若索引对象为字符串，需要指定索引长度，一般与该字符串字段等长。若不是字符串，可以不指定长度
* 添加索引：`ALTER TABLE table_name ADD INDEX(field)`  
* 查看索引：`SHOW INDEX FROM table_name` 
* 删除索引：`DROP INDEX index_name ON table_name` 

## 事务

事务：一些不可被中断的操作序列，要么均执行成功，要均不执行。事务只在innoDB引擎被支持。

事物的ACID原则：

* 原子性（Atomicity）：事务是一个不可分割的工作单位，事务中的操作要么都发生，要么都不发生。
* 一致性（Consistency）：事务前后数据的完整性必须保持一致，从一个状态到另一个状态
* 隔离性（Isolation）：多个用户并发访问数据库时，数据库为每一个用户开启的事务，彼此操作相互隔离
* 持久性（Durability）：事务一旦被提交，它对数据库中数据的改变就是永久性的



事务创建、提交、回滚：

```mysql
#方法1
begin;		#标记事务开始
#do something here
rollback;	#回滚
commit;		#提交
	
#方法2 与方法1等价
start transaction;
#do something here
rollback work;	#回滚
commit work;	#提交
```

事务只有在commit操作之后才会将修改后的数据写入磁盘，否则修改只在缓存中发生。若有必要，可以使用`rollback`回滚到初始状态，当然，回滚操作必须在提交之前。

***

事务的并发问题：

* 脏读：事务A读取了事务B更改的数据，**但事务B最后回滚了**，此时事务A读取到的数据就是脏读。
* 不可重复读：事务A执行期间，**事务B更改数据并提交**，导致事务A前后读取到的数据并不一致。
* 幻读：事务A执行期间，**事务B新增、删除数据并提交**，导致事务A执行完后，发现莫名多（少）了一行数据，好像出现了幻觉。

为了解决事务的并发问题，设定[事务的隔离级别](https://www.cnblogs.com/wyaokai/p/10921323.html)。隔离级别越高，越能保证数据的完整性和一致性，但是对并发性能的影响也越大。

| 事务隔离级别                              | 脏读 | 不可重复读 | 幻读 |
| ----------------------------------------- | ---- | ---------- | ---- |
| 读未提交（read-uncommitted）              | 是   | 是         | 是   |
| 不可重复读（read-committed）              | 否   | 是         | 是   |
| 可重复读（repeatable-read，默认隔离级别） | 否   | 否         | 是   |
| 串行化（serializable）                    | 否   | 否         | 否   |



事务隔离级别：便于阐述，假设存在事物A、B

* 读未提交：即使事务B未提交，数据的更改对事物A也可见。
* 不可重复读（行锁）：只有事务B提交之后，数据更改对事务A才可见。但这会造成“ 不可重复读 ”问题，存在不可重复读的问题，自然也一定会存在“ 幻读 ”的问题。
* 可重复读（检索条件存在索引时为行锁，否则为表锁）：只有事务B提交之后，数据更改对事务A才可见。但是事物A进行`select`操作时，**保存的是事物A开始时的历史快照**，进行`insert、update`等修改操作时，会选择最新的数据快照，也就是事务B提交只有的数据版本。这可以解决“ 不可重复读 ”问题 ，但仍然存在幻读问题。（[锁升级导致的死锁案例](https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651962432&idx=1&sn=3459e82428cb9bb1de4677fa6b5a1c2d&chksm=bd2d099c8a5a808af5926a8be9c900c0bca57a8b8e61b192272d919e38d607a03b5ac4e0990a&scene=21#wechat_redirect)）
* 串行化（表级锁）：pass 



# 主从同步

主从同步：主机负责写，从机拷贝主机的数据，增量更新，负责读。主从集群可以实现数据备份，提升容灾能力和并发时数据库的读性能。

主从同步是单向同步，从机允许修改数据库，但从机的修改不会对主机造成影响。



主从同步的机制：基于主机的二进制日志，主服务器使用二进制日志来记录数据库的变动情况，从服务器通过读取和执行该日志文件来保持和主服务器的 数据一致。

![](pictures/主从同步日志机制.jpg) 



主从同步配置：主从数据库版本最好一致，否则会出现各种兼容错误。即使主从同步成功，也会在实际同步过程中执行sql语句失败导致停止同步。

**主机配置：**

1. [备份数据库](#配置)，供从机还原使用。根据需要，可以备份整个数据库或若干指定数据库。

2. 编辑server配置文件（需要root权限），开启二进制日志，配置唯一id（**range from 1 to 2^32 − 1**） 。linux下，配置文件分为global（[mysql]）、client（[client]）、server（[mysqld]），其中server配置文件为`/etc/mysql/mysql.conf.d/mysqld.cnf`，windows下，配置文件为`programdata/mysql/my.ini`  

   ```shell
   log-bin=mysql-bin #开启二进制日志
   server-id=1 #在主从集群中该id必须唯一
   
   #默认同步所有，可以额外配置不同步、同步指定数据库，多个数据库要分多行写
   binlog-ignore-db = mysql   	#不同步 
   binlog-ignore-db = test	#换行写
   binlog-do-db = game	#只同步
   ```

3. 重启mysql服务`sudo service mysql restart`使配置生效，可以使用`show variables like 'log%'`验证二进制日志是否已经开启（variables是mysql的环境变量）。

4. 进入mysql，`show master status`查看二进制日志文件名File及其位置Position，记录用于从机读取。

   ```mysql
   +------------------+----------+--------------+------------------+-------------------+
   | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
   +------------------+----------+--------------+------------------+-------------------+
   | mysql-bin.000007 |      154 |              |                  |                   |
   +------------------+----------+--------------+------------------+-------------------+
   
   ```

   

5. 创建一个用于从机同步的账号，赋予`replication slave`权限，**并允许从机登录ip为远端登录**，可以是`%`或指定ip。

   ```mysql
   create user 'slave';	#不添加host即默认为%允许远端登录 
   grant replication slave on *.* to 'slave' with grant option;
   ```

**从机配置：**

1. 还原主服务备份的数据库

2. 编辑server配置文件，从机只需配置唯一id即可，该id在主从集群中必须唯一。重启mysql使配置生效。

3. 进入mysql，使用主机分配的账号连接主机。格式如下

   ```mysql
   CHANGE MASTER TO
   MASTER_HOST='192.168.145.130',
   MASTER_USER='slave',
   MASTER_PASSWORD='slave_passwd',
   MASTER_LOG_FILE='mysql-bin.000003',
   MASTER_LOG_POS=73;
   ```

4. 启动slave线程`start slave` 

5. 查看主从同步是否成功`show slave status\G`（\G表示将结果旋转，便于查看）。若结果中同时显示即为成功，转步骤7。

   ```mysql
   Slave_IO_Running: Yes
   Slave_SQL_Running: Yes
   ```

6. 当同步失败时，必须先`stop slave`停止同步线程，`show slave status\G`查看具体的同步报错` Last_IO_Errno`、`Last_SQL_Errno`。然后**重新开始步骤3-5**，直至显示成功。

   常见的错误：

   * `IO_Running: NO`：主机日志文件名、位置填写错误；主机ip填写错误、主机配置的从机账号不允许远端访问（可以`mysql -h host -u slave -p'slave'`验证）
   * `SQL_Running: NO`：主从句数据库版本不兼容，导致执行语句失败，如默认字符集不一样。

7. 简单验证主从同步，主机对数据库进行操作，从机成功同步，即同步成功。当未同步时，转步骤6。

***

**关于字符集的一些坑**：主从同步中若主机数据库和从机数据库默认创建字符集不一样，则会大概率同步出错。可以使用`show variables like 'char%'`查看当前环境的字符集设置。这与当前选中的数据库、编辑工具有关，当未选中某个具体数据库，命令返回的是全局设置。使用Navicat时，选择“编辑连接，编码：自动”，保持工具的编码规则与mysql的设置一致。

使用字符集的各个场景解析： 

| 场景       | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| client     | 为客户端使用的字符集                                         |
| connection | 为连接数据库的字符集设置类型，如果程序没有指明连接数据库使用的字符集类型则按照服务器端默认的字符集设置。 |
| database   | 为数据库服务器中某个库使用的字符集设定，如果建库时没有指明，将使用服务器安装时指定的字符集设置。 |
| results    | 为数据库给客户端返回时使用的字符集设定，如果没有指明，使用服务器默认的字符集。 |
| server     | 为服务器安装时指定的默认字符集设定。                         |
| system     | 为数据库系统使用的字符集设定。                               |

其中client、connection、results是客户端与mysql服务端交互直接相关的[三个设置](https://www.cnblogs.com/sunzn/archive/2013/03/14/2960248.html)。mysql本质是一种tcp通信，底层基于字节流传输，因此服务端有必要清楚客户端的编码方式，才能顺利解码传过来的字节流，然后按照自己的编码方式存储。这个过程如下：

```python
'sql command'.encode('gbk') # 客户端使用gbk编码，输入一条sql指令
command=data.decode('gbk') # 服务端按照gbk解码得到指令
# execute ，执行指令
```



5.7版本中，数据库默认字符集为`latin`，修改默认字符集的办法为：

1. 进入server（[mysqld]）配置文件，添加如下两行：

```mysql
[mysqld]
character-set-server=utf8
collation-server=utf8_general_ci
```

2. 进入global（[mysql]）配置文件`/etc/mysql/my.cnf`，添加一行 

```mysql
[mysql]
default-character-set=utf8
```

查看修改结果`show variables like 'char%'`

```mysql
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8                       |
| character_set_connection | utf8                       |
| character_set_database   | utf8                       | 
| character_set_filesystem | binary                     |
| character_set_results    | utf8                       |
| character_set_server     | utf8                       |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
```





# 设计范式

范式：[数据库的设计规范](https://www.jianshu.com/p/3e97c2a1687b)。遵循范式设计可以减少数据冗余，但实际使用时，可以适当反范式，在冗余、速度之间取舍。



ER（entry-relationship，实体关系）模型： 

* E（实体），设计实体就像定义一个类一样，指定从哪些方面描述对象，一个实体转为数据库的一个表
* R（关系），描述两个实体之间的对应规则，关系包括一对一、一对多、多对多 



## 1NF

1NF：列不可再分，且表具备主键。不符合1NF的表，应当拆分字段信息。

下表不遵循1nf范式，联系方式字段可以拆分

![](pictures/1nf不规范.webp.jpg) 

拆分“ 联系方式 ”字段后，遵循1NF

![](pictures/1nf规范.webp.jpg) 

## 2NF

2NF：非主键字段完全依赖于主键，不可只依赖于主键的部分。

下表 主键=（学生编号，教师编号），但“ 学生姓名 ”仅依赖于学生编号，“教师姓名”同理，不遵循2nf

![](pictures/2nf不规范.jpg)



将主键拆分，单独建表后遵循2nf。

![](pictures/2nf规范.jpg)

## 3NF

3NF：非主键字段不可传递性地依赖于主键。

下表主键为学生编号，但是班级名称字段依赖于班级编号，班级编号再依赖于主键“ 学生编号 ”。不遵循3nf。

![](pictures/3nf不规范.webp.jpg) 



将“ 班级编号：班级名称 ”单独建表后，遵循3nf。

![](pictures/3nf规范.webp.jpg)

# 《架构师之路》 摘记

[架构师之路](https://mp.weixin.qq.com/s/syli7vs7Jw_VOTl5B2YUqg) 

****

[架构分类](https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651963031&idx=1&sn=f52b724ff33ef008668ef9165c51d39b&chksm=bd2d0b4b8a5a825df41252dd381d0206e141f6a54f253086030113f14584bb11612308ce8e16&scene=21#wechat_redirect) ：

* 单库架构：字面意思，一个库进行数据存储

* 分组架构：**一主多从，主从同步。读写分离，主写从读**。常用于解决数据库的高并发读写，提升数据库的读性能

  > 分组架构为什么可以提升数据库的读性能？
  >
  > 互联网的应用往往是“读多写少”的需求，采用读写分离的方式，可以实现更高的并发访问。原本所有的读写压力都由一台服务器承担，现在有多个“兄弟”帮忙处理读请求，这样就减少了对后端大哥（Maste)的压力。同时，我们还能对从服务器进行负载均衡，让不同的读请求按照策略均匀的分配到不同的从服务器中，让读取更加顺畅。

* 分片架构：解决单库数据量大的问题，将一个数据库拆分成多个数据库。
  * 水平切分：同一张表切分到不同的数据库中**，按照行切分**。常用的有哈希拆分（按照某个字段的规律，例如求余）、范围拆分（若干行为一分片）。
  * 垂直切分：按照业务需求，可以对同一数据库的不同表拆分，也可以对同一张表的不同查询频率的字段拆分。对于后者，将常用的、较短的字段拆分为一个分片，将另外一些拆分为另一个分片，当数据库调取数据（block）的时候，一次就能加载更多常用的查询数据。这种形式的切分可以提升数据库的读写性能。

***