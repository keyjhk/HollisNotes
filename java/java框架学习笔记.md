---
typora-copy-images-to: upload
---

# Maven

maven用于解决jar包的依赖，项目的编译部署。 

## 配置 

解压程序包，依次修改配置文件`settings.xml`

1. 修改本地仓库位置，默认在家目录下 

   ```xml
   <localRepository>D:\maven-rep1026</localRepository>
   ```

2. 修改下载镜像源为阿里镜像源

   ```xml
   
   <mirrors>
       <mirror>
           <id>nexus-aliyun</id>
           <mirrorOf>central</mirrorOf>
           <name>Nexus aliyun</name>
           <url>http://maven.aliyun.com/nexus/content/groups/public</url>
       </mirror>
   </mirrors>
   ```

3. 修改maven工程默认的jdk版本

   ```xml
   <profiles>
       <profile>
         <id>jdk-1.8</id>
         <activation>
           <activeByDefault>true</activeByDefault>
           <jdk>1.8</jdk>
         </activation>
         <properties>
           <maven.compiler.source>1.8</maven.compiler.source>
           <maven.compiler.target>1.8</maven.compiler.target>
           <maven.compiler.compilerVersion>1.8</maven.compiler.compilerVersion>
         </properties>
       </profile>
   </profiles>
   ```

   

添加环境变量 

* MAVEN_HOME 指向 maven的bin目录的上一级 
* `%MAVEN_HOME%/bin` ，指向maven的执行文件目录 

cmd下，`mvn -v` 测试是否配置正确，输出版本号则为正常。 

## 坐标

坐标：maven体系中，对jar包的唯一定位方式，由3部分组成：

* groupId：公司或组织域名的倒序，通常也会加上项目名称，例如：com.atguigu.maven
* artifactId：模块的名称
* version：模块的版本号，根据自己的需要设定。SNAPSHOT表示快照版本，RELEASE表示正式版本

示例坐标如下

```xml
 <groupId>javax.servlet</groupId>
  <artifactId>servlet-api</artifactId>
  <version>2.5</version>
```

上述坐标对应的jar包位置为：`groupId\artifactId\artifactId-version` 

```
Maven本地仓库根目录\javax\servlet\servlet-api\2.5\servlet-api-2.5.jar
```

***

依赖信息查询：https://mvnrepository.com/ 



## 仓库与下载

maven查找依赖的顺序为，本地仓库，中央仓库。 本地仓库即为配置的仓库，而中央仓库为其创始公司统一维护，需要联网下载到本地。 



maven在下载jar包的时候，会添加后缀`lastUpdated`。在jar下载完成后，再删除后缀。但是，这个过程存在下载失败的隐患。如果下载中途网络连接失败，maven并不会继续下载那些`lastUpdated`的包。 

为了让其重新下载，借助工具`clearLastUpdated.ba`可以批量删除这些不完整的包，在此，仅记录解决思路。 

## 目录结构

maven工程的目录结构：

![image-20220623160632286](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220623160632286.png)



约定俗成如下：

* pom.xml：maven工程的配置文件。pom（project object model）意为  工程对象模型。
* src  
  * main 
    * java：项目的java代码
    * resources：项目的资源文件，如property文件
    * webapp
      * WEB-INF：web应用目录 ，存放xml、图片、文件等 
  * test 
    * java：项目的测试类 
    * resources：测试用的资源 
* target： 打包输出目录 
  * classes：源码编译输出目录 
  * test-classes：测试编译输出目录 



## 命令 



**编译** 

* `mvn compile` ： 编译源代码文件，编译结果存放于`target/classes`
* `mvn test-compile`：编译测试代码文件，编译结果存放于`target/test-classes`  



**清理**编译文件：`mvn clean`，会删除target目录



**测试**： `mvn test`，执行测试程序，测试的报告会存放在target/surefire-reports目录下



**打包**：`mvn package`，打包的结果会存放在target目录下



**安装**：`mvn install`，将本地构建过程中生成的jar包存入Maven本地仓库，同时将xml文件转为pom文件存入本地仓库。放入本地仓库以后，其他java工程就可以解决引用该工程。 



显示依赖信息：

* `mvn dependency:list `，显示jar包依赖。

  > 显示信息格式如下：
  >
  > javax.servlet:javax.servlet-api:jar:3.1.0:provided 
  >
  > groupId:artifactId:打包方式:version:依赖的范围

* `mvn dependency:tree` ：树形显示

## 创建web项目

1. 执行命令如下。观察pom文件，发现打包方式为war

   工程生成命令

   ```shell
   mvn archetype:generate -DarchetypeGroupId=org.apache.maven.archetypes -DarchetypeArtifactId=maven-archetype-webapp -DarchetypeVersion=1.4
   ```

   打包方式

   ```xml
   <packaging>war</packaging>
   ```

2. 打包：`mvn package` ， target目录下生成war包。
3. 将war包拷贝到tomcat的`webapp`目录下。执行tomcat命令，`startup` ，部署项目 



## 依赖可见范围

dependency的scope属性，表示依赖的可见范围，取值为：

* compile：默认的范围
* provided
* test

他们的差别在于编译、部署项目时，可见范围不同：

|          | main目录（空间） | test目录（空间） | 开发过程（时间） | 部署到服务器（时间） |
| -------- | ---------------- | ---------------- | ---------------- | -------------------- |
| compile  | 有效             | 有效             | 有效             | 有效                 |
| provided | 有效             | 有效             | 有效             | 无效                 |
| test     | 无效             | 有效             | 有效             | 无效                 |



部署到服务器无效的应用场景是，服务器已经存在相应jar包，例如servlet包。为了减轻部署负担和jar包导入冲突，就仅限于本地开发时可见，打包时，就跳过这些依赖。

## 依赖传递和排除

ABC三个项目之间彼此依赖，**A对C是否可见？**这取决于B项目的对C的依赖配置。如果scope范围不是compile，那么A对C就不可见。 



**依赖排除**

A => B => X-1.0.jar，同时，A=>C=>X.2.0.jar。这两个不同版本的jar包，可能会导致冲突，为了在引入B工程时，排除X.10.jar的引入，就需要修改对B工程的配置项 ，增加`exclusions`标签 

```xml
<dependency>
    <!-- 假设 这是A工程的pom.xml 正在配置对B工程的依赖    -->
    <groupId>com.atguigu.maven</groupId>
    <artifactId>pro01-maven-java</artifactId>
    <version>1.0-SNAPSHOT</version>
    <scope>compile</scope>
    <!-- 使用excludes标签配置依赖的排除    -->
    <exclusions>
        <!-- 在exclude标签中配置一个具体的排除 -->
        <exclusion>
            <!-- 指定要排除的依赖的坐标（不需要写version） -->
            <groupId>commons-logging</groupId>
            <artifactId>commons-logging</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```





![image-20220624155040811](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220624155040811.png)



## 继承&聚合

在maven的工程管理体系中，工程可以存在父子继承关系，就像java工程的project和modules的关系。**让子工程继承父工程的好处，就是便于统一管理多个子工程共同的依赖信息。父工程中声明依赖，一处修改，处处生效。** 

在实际开发中，版本之间的依赖是一个耗费心神的问题，将子工程的依赖版本组合交给成熟的父工程，可以节省时间。 



**继承的步骤：**

1. 创建父工程，同时修改父工程的pom文件，将其中的打包方式修改为`pom`。 

   ```xml
   <packaging>pom</packaging>
   ```

2. 在父工程的根目录下，创建子工程 。或者移动子工程，手动创建下列信息。 

   

观察子工程的pom文件，会发现其中多了一个`parent`属性，指向他们的父工程。

```xml
<parent>
    <!-- 父工程的坐标 -->
    <groupId>com.atguigu.maven</groupId>
    <artifactId>pro03-maven-parent</artifactId>
    <version>1.0-SNAPSHOT</version>
</parent>
```

观察父工程的pom文件，会发现多了modules属性，指向他的子工程。 

```xml

<modules>  
    <module>pro04-maven-module</module>
    <module>pro05-maven-module</module>
    <module>pro06-maven-module</module>
</modules>
```



**父工程统一声明依赖信息：** 

在父工程不干预的情况下，多个子工程可以独立地声明自己的依赖，这当然会存在一种情况，**就是子工程对于同一个jar包的依赖版本不一致**，不利于管理。为此，需要借助继承，在父工程中统一声明依赖。 

1. 子工程取消对版本号的声明，在无声明的情况下，子工程会去父工程寻找版本声明。 

   ```xml
   <dependencies>
       <dependency>
           <!-- 子工程引用父工程中的依赖信息时，可以把版本号去掉。  -->
           <groupId>org.springframework</groupId>
           <artifactId>spring-core</artifactId>
       </dependency>
       <dependency>
           <groupId>org.springframework</groupId>
           <artifactId>spring-beans</artifactId>
       </dependency>
       </dependency>
   </dependencies>
   ```

   

2. 父工程中创建标签，`dependencyManager`，在标签中声明具体的依赖信息和版本号。**Manager标签只负责版本信息的管理，而不会真的为工程引入这些依赖。依赖引入的发生与否，取决于工程的dependencies标签是否导入了该依赖。**

   ```xml
   <dependencyManagement>
       <dependencies>
           <dependency>
               <!-- 父工程声明版本信息 -->
               <groupId>org.springframework</groupId>
               <artifactId>spring-core</artifactId>
               <version>4.0.0.RELEASE</version>
           </dependency>
           <dependency>
               <groupId>org.springframework</groupId>
               <artifactId>spring-beans</artifactId>
               <version>4.0.0.RELEASE</version>
           </dependency>
       </dependencies>
   </dependencyManagement>
   ```




父工程也可以选择直接创建`dependencies`标签，指定依赖版本信息。子工程就会直接继承这些依赖项，这种继承是全盘继承的。 





**创建变量，实现版本号的管理：**

pom文件中，可以定义变量，存储具体的版本号信息。让`dependencyManager`中的版本信息，替**换具体的数字版本为变量，实现进一步封装，类似硬编码和软编码的关系**。

声明变量 

```xml
<!-- 通过自定义属性，统一指定Spring的版本 -->
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <!-- 自定义标签，维护Spring版本数据 -->
    <atguigu.spring.version>4.3.6.RELEASE</atguigu.spring.version>
</properties>
```

使用`${变量名}`引用变量 

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-core</artifactId>
    <!--4.3.6.RELEASE-->
    <version>${atguigu.spring.version}</version>
</dependency>
```



***

**聚合**：

当工程实现了继承的关系时，实际上就已经完成了聚合。这似乎是从不同的角度在描述同一件事情，对于子工程而言，称呼为“继承”，对于父子工程这个整体而言，称呼为“聚合”。

聚合，可以让maven安装工程时更加方便。在父工程中执行`mvn install`命令，maven会解决子工程的依赖顺序问题，先安装被依赖的，再安装依赖的，最终实现整个工程的有序安装。



## 配合idea

### 创建普通工程

idea中创建maven工程的操作基本符合直觉，唯一需要注意的是，要为每个project配置自己的maven路径以及相应的配置文件路径。

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628105308714.png" alt="image-20220628105308714" style="zoom:80%;" />

添加子模块：

1. 

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628105227632.png" alt="image-20220628105227632" style="zoom:80%;" />

2. 选中父工程

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628105249125.png" alt="image-20220628105249125" style="zoom:67%;" />

### 创建web工程

创建web工程的步骤略显繁琐，大致上分为两个步骤

1. 手动补充，完善目录结构。 创建`src/main/webapp/WEB-INF`文件夹，这种目录结构是maven的约定结构。 webapp就是将来部署到tomcat时被打包的文件夹目录 。同时修改pom的打包方式为`war` 

   ```xml
   <packaging>war</packaging>
   ```

   

2. 让idea创建 web.xml 文件。idea形容web.xml为`deployment description`（部署描述），“facet”单词的意思为切面。从用词的角度出发，可以理解这些配置旨在让idea理解项目的结构。 

   <img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628104751350.png" alt="image-20220628104751350" style="zoom: 80%;" />



<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628104809357.png" alt="image-20220628104809357" style="zoom:80%;" />

修改web.xml的存储路径，和 web资源的相对路径，也就是`webapp`文件夹

![image-20220628104847940](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628104847940.png)

![image-20220628104853101](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628104853101.png)

3. pom文件中添加必要的依赖，如servlet-api。然后点击下载执行导入，检查dependency下，是否引入了依赖。 

   ```xml
       <dependencies>
           <dependency>
               <groupId>javax.servlet</groupId>
               <artifactId>javax.servlet-api</artifactId>
               <version>3.1.0</version>
               <scope>provided</scope>
           </dependency>
       </dependencies>
   ```

   

   ![image-20220628105146350](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628105146350.png)





# Mybatis

mybaits：一个具备ORM(Object Relataion Mapping)的java持久层框架。所谓ORM，就是将数据库的表映射为编程语言中的类。一个表对应了一个class，字段对应类属性，而每一行数据就对应类的每一个实例对象。

mybaits对比JDBC：

| mybatis                                         | JDBC                                                         |
| ----------------------------------------------- | ------------------------------------------------------------ |
| 将sql语句编写在xml配置文件，实现源码和sql的分离 | 在DAO层，硬编码了大量的sql语句，和java源码混合在一块，不利于后期维护 |
| 几乎避免了JDBC的操作                            | 手动编写连接创建、sql语句参数确定、结果集解析等从操作，代码冗长 |



## 准备工作

### 引入依赖

pom文件中导入依赖

```xml
<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis</artifactId>
    <version>3.5.7</version>
</dependency>
```

### 创建模型类

ORM的思想就是每一张数据表都对应一个java实体类，实体类的称呼可能有多种，例如POJO(plain ordinary java object)、entity（实体）、domain（领域模型）、java bean对象等，**但就它们的表现形式而言，其实是同一个东西**：

* 私有的类属性名，和字段一一对应，小驼峰命名。
* 用于获取私有属性的get\set方法 

**无论是从确定sql参数，还是封装返回结果，准备实体类都可以让sql操作变得更优雅。**



职员实体类

```java
public class Employee {
    // 数据库的字段 emp_id emp_name ...
    private Integer empId;
    private String empName;
    private double empSalary;

    public Employee(Integer empId,String empName, double empSalary) {
        this.empId = empId;
        this.empName = empName;
        this.empSalary = empSalary;
    }

    @Override
    public String toString() {
        return "Employee{" +
                "empId=" + empId +
                ", empName='" + empName + '\'' +
                ", empSalary=" + empSalary +
                '}';
    }

    public long getEmpId() {
        return empId;
    }

    public void setEmpId(Integer empId) {
        this.empId = empId;
    }


    public String getEmpName() {
        return empName;
    }

    public void setEmpName(String empName) {
        this.empName = empName;
    }


    public double getEmpSalary() {
        return empSalary;
    }

    public void setEmpSalary(double empSalary) {
        this.empSalary = empSalary;
    }
}

```



### 配置文件

mybatis的配置文件可以分为两类：

* 全局的配置文件：用于指定数据库的连接信息、mapper的资源文件位置。
* mapper配置：mapper的操作单位是每一个具体的表，在mapper中，要明确具体的sql语句。 

![image-20220701103813255](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220701103813255.png)



全局配置文件  mybatis-config.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>

    <properties resource="jdbc.properties"/>
    <!-- environments表示配置Mybatis的开发环境，可以配置多个环境
	使用default属性指定实际运行时使用的环境。 -->
    <environments default="development">
        <!-- environment表示配置Mybatis的一个具体的环境 -->
        <environment id="development">

            <!-- Mybatis的内置的事务管理器 -->
            <transactionManager type="JDBC"/>

            <!-- 配置数据源 来自上文指定的外部数据源信息 jdbc.properties文件-->
            <dataSource type="POOLED">
                <!-- 建立数据库连接的具体信息 -->
                <property name="driver" value="${wechat.dev.driver}"/>
                <property name="url" value="${wechat.dev.url}"/>
                <property name="username" value="${wechat.dev.username}"/>
                <property name="password" value="${wechat.dev.password}"/>
            </dataSource>
        </environment>
    </environments>

    <mappers>
        <!-- mapper标签：配置一个具体的Mapper映射文件 -->
        <!-- resource属性：指定Mapper映射文件的实际存储位置，以类路径根目录为基准的相对路径 -->
        <!-- 对Maven工程的目录结构来说，resources目录下的内容会直接放入类路径classes，所以这里我们可以以resources目录为基准 -->
        <mapper resource="mappers/EmployeeMapper.xml"/>
    </mappers>
</configuration>
```



EmployeeMapper.xml 文件 

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

        <!-- mapper是根标签，namespace属性：在Mybatis全局范围内找到一个具体的Mapper配置 -->
<mapper namespace="com.hollis.mybatis.entity.EmployeeMapper">
    <!-- 编写具体的SQL语句，使用id属性唯一的标记一条SQL语句 -->
    <!-- resultType属性：指定封装查询结果的Java实体类的全类名 -->
    <select id="selectEmployee" resultType="com.hollis.mybatis.entity.Employee">
        <!-- Mybatis负责把SQL语句中的#{}部分替换成“?”占位符，在#{}内部还是要声明一个见名知意的名称 -->
        select emp_id empId,emp_name empName,emp_salary empSalary from t_emp where emp_id=#{empId}
    </select>

    <insert  id="insertEmployee">
        insert into t_emp(emp_name,emp_salary) values(#{empName},#{empSalary})
    </insert>

    <delete id="deleteEmployeeById">
        delete from t_emp where emp_id=#{empId}
    </delete>

    <update id="updateEmployeeById">
        update t_emp set emp_name=#{empName},emp_salary=#{empSalary}  where emp_id=#{empId}
    </update>
</mapper>
```

namespace的作用：一是标识该mapper，方便之后被解析成java对象时，成功地被框架找到。**二是，关联下文介绍的Mapper对象，所以namespace的格式看上去是一个类的全限定名** 。

select/insert/update/delete 等标签与sql的操作增删改查操作一一对应，每一个标签，用id来标识，resultType指定返回的数据格式。这两个属性同样要与马上介绍的Mapper对象关联。

sql语句，用`#{}`来表示待定参数，更详细的配置参考Mapper一节。

## Mapper

sql语句的具体执行已经在配置文件中说明 ，实体类也已经创建完毕。Mapper类扮演的角色类似于JDBC中的DAO层，负责联系两者，用一个可读性更强的函数来封装具体的sql语句。框架让这这部分工作完成地更加简单优雅。

### 创建

Mapper是一个接口类，该接口类的全限定名，应当见名知意，**知道它是对哪一个实体类负责。同时，它和对应的mapper配置文件中的namespace要保持一致。**

![image-20220701105948402](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220701105948402.png)

EmployeeMapper.xml

```xml
<mapper namespace="com.hollis.mybatis.entity.EmployeeMapper"></mapper>
```

Mapper接口类的方法声明要注意：

1. 方法名和sql语句的id一致 
2. 返回类型和resultType一致
3. **形参格式要符号sql的待定参数要求，这个不是简单的一一对应关系**



示例：

sql语句

```xml
<select id="selectEmployee" resultType="com.hollis.mybatis.entity.Employee">
    select emp_id empId,emp_name empName,emp_salary empSalary from t_emp where emp_id=#{empId}
</select>

<insert  id="insertEmployee">
    insert into t_emp(emp_name,emp_salary) values(#{empName},#{empSalary})
</insert>

<delete id="deleteEmployeeById">
    delete from t_emp where emp_id=#{empId}
</delete>

<update id="updateEmployeeById">
    update t_emp set emp_name=#{empName},emp_salary=#{empSalary}  where emp_id=#{empId}
</update>
```

完整的Mapper接口类

```java
public interface EmployeeMapper {
    Employee selectEmployee(long empId);

    void insertEmployee(Employee emp);

    void deleteEmployeeById(long empId);

    void updateEmployeeById(Employee emp);
}

```



### 使用

虽然我们只是创建了一个接口类，但是框架会为我们动态生成一个实体类。方法体自然就是执行具体的sql语句。

使用Mapper：通过`@Before` 、`@After`、`@Test` 来区分三个阶段：

1. 初始化：加载全局的mybatis配置，创建sessionFactory对象，该对象负责开启每一次和数据库会话
2. `getMapper(class<T>)`拿到具体的Mapper对象，然后执行具体的方法 
3. 关闭此次会话

```java
import com.hollis.mybatis.entity.Employee; // 实体类
import com.hollis.mybatis.entity.EmployeeMapper; // 映射类

import org.junit.*;

import org.apache.ibatis.io.Resources;  // 加载全局配置文件
import org.apache.ibatis.session.*; // 负责开启会话

import java.io.IOException;


public class ImprovedMybatisTest {
    SqlSessionFactory sessionFactory;
    SqlSession session;
    @Before
    public void  init() throws IOException {
        sessionFactory = new SqlSessionFactoryBuilder()
                .build(Resources.getResourceAsStream("mybatis-config.xml"));

    }

    @Test
    public void testSelectEmployee(){
        session = sessionFactory.openSession();
        // getMapper 拿到具体的Mapper类 并具体创建 
        EmployeeMapper empMapper = session.getMapper(EmployeeMapper.class);
        Employee emp =  empMapper.selectEmployee(1); // 执行方法
        System.out.println("employee = " + emp);
    }


    @After
    public void  destroy(){
        session.commit();
        session.close();
    }

}

```





### 参数格式

接口类的方法声明提到一点，函数的参数要符合sql待定参数的要求。其中学问不浅，直观地，可以通过待定参数的多少来分类：

* 单个参数
* 多个参数：实体类/mapper



sql语句中，使用`#{变量名}`来表示待定参数。

#### 单个参数

sql语句 

```xml
<select id="selectEmployee" resultType="com.atguigu.mybatis.entity.Employee">
    select emp_id empId,emp_name empName,emp_salary empSalary from t_emp where emp_id=#{empId}
</select>
```

方法声明时，参数名可以是任意的。框架不会做特殊处理

```java
Employee selectEmployee(Integer empId);
Employee selectEmployee(Integer empIdTest); // 同样可以
```

#### 多个参数

https://blog.csdn.net/qq_43052725/article/details/105577159 

sql语句

```xml
<insert  id="insertEmployee">
    insert into t_emp(emp_name,emp_salary) values(#{empName},#{empSalary})
</insert>
```

声明形参时，使用`@Param(param)`注解 ，与参数名一一对应

```java
void insertEmployee(@Param("empName") String empName, @Param("empSalary") Double empSalary);

```



当函数参数过多时，使用注解的形式不如封装。

1. 使用实体类：逻辑上要求这些参数归属于一个实体类。对于sql的待定参数，框架会调用类的getXXX方法去获取。 例子中的`#{empName}` 等于`emp.getEmpName()`。 

   函数声明 

    ```java
    // 参数是职员类
    void insertEmployee(Employee emp);
    ```

	职员类

    ```java
    public class Employee {
        // 数据库的字段 emp_id emp_name ...
        private Integer empId;
        private String empName;
        private double empSalary;
   
        // 省略getEmpSalary() 和 getEmpName 方法
    }
    ```

​				它们的关系 

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220701151316782.png" alt="image-20220701151316782" style="zoom: 50%;" />


2. 使用Map：逻辑上归属不到一个实体类，就用Map封装。待定参数名就是Map中的key 

   ```java
   int updateEmployeeByMap(Map<String, Object> paramMap);
   ```

   调用时 

   ```java
   EmployeeMapper mapper = session.getMapper(EmployeeMapper.class);
   
   Map<String, Object> paramMap = new HashMap<>();
   
   paramMap.put("empSalary", 999.99);
   paramMap.put("empName", 5);
   
   int result = mapper.updateEmployeeByMap(paramMap);
   ```

   

### 返回结果

通过指定`resultType`指定返回类型

#### **简单数据类型** 

示例：int

```xml
<select id="selectEmpCount" resultType="int">
select count(*) from t_emp
</select>
```

```java
int selectEmpCount();
```



#### **实体类**

查询的字段名和类属性应该一致，否则该类属性为空。 

```xml
<select id="selectEmployee" resultType="com.atguigu.mybatis.entity.Employee">
    <!-- 给每一个字段设置一个别名，让别名和Java实体类中属性名一致 -->
    select emp_id empId,emp_name empName,emp_salary empSalary from t_emp where emp_id=#{maomi}
</select>
```

```java
Employee selectEmployee(Integer empId);
```

由于`select` 返回的字段数量并不一定和实体类的属性数量一致，**因此，实体类要求存在一个无参构造函数，确保mybatis在反射过程中，可以成功地动态创建类。 **

```java
Employee emp = new Employee();
// 根据select的返回字段 逐一设置 
emp.empName = xxx;
```



#### **Map类型** 

返回的多个数据，并不能被一个实体类封装，就用Map

```xml
<select id="selectEmpNameAndMaxSalary" resultType="map">
        SELECT
            emp_name 员工姓名,
            emp_salary 员工工资,
            (SELECT AVG(emp_salary) FROM t_emp) 部门平均工资
        FROM t_emp WHERE emp_salary=(
            SELECT MAX(emp_salary) FROM t_emp
        )
</select>
```

```
Map<String,Object> selectEmpNameAndMaxSalary();
```



#### **List类型** 

不需要特殊处理，resultType属性中还是设置实体类类型即可。

```xml
<select id="selectAll" resultType="com.atguigu.mybatis.entity.Employee">
    select emp_id empId,emp_name empName,emp_salary empSalary
    from t_emp
</select>
```

```java
List<Employee> selectAll();
```



#### **自增主键**

某些场景下，插入数据后，需要拿到新增的主键。 **框架中，自增的主键获取依靠实体类，而不是返回值**。

**sql语句需要声明`useGeneratedKeys="true"`表示需要获取返回主键，`keyProperty="empId">`表示主键对应的实体类属性。**

```xml
<insert id="insertEmployee" useGeneratedKeys="true" keyProperty="empId">
    insert into t_emp(emp_name,emp_salary)
    values(#{empName},#{empSalary})
</insert>
```

```java
int insertEmployee(Employee employee);
```

调用时

```java
@Test
public void testSaveEmp() {
    SqlSession session = sessionFactory.openSession();
    
    EmployeeMapper employeeMapper = session.getMapper(EmployeeMapper.class);
    
    Employee employee = new Employee();
        
    employee.setEmpName("john");
    employee.setEmpSalary(666.66);
    
    employeeMapper.insertEmployee(employee);
    // 主键存储在实体类中 通过这种形式获取
    System.out.println("employee.getEmpId() = " + employee.getEmpId());
    
    session.commit();
    session.close();
}
```



## 数据库字段和实体类属性

书写sql语句时，为了让返回的结果能够被正常地封装为一个实体类，我们对字段名取了别名。 

```xml
<select id="selectEmployee" resultType="com.atguigu.mybatis.entity.Employee">
    <!-- 给每一个字段设置一个别名，让别名和Java实体类中属性名一致 -->
    select emp_id empId,emp_name empName,emp_salary empSalary from t_emp where emp_id=#{maomi}
</select>
```

除了别名，也有其他办法完成它们两者的映射

1. 让框架帮我们处理：建立在表字段都是`单词_单词`这种下划线分隔的情况 。在全局的配置文件中，开启配置

   ```xml
   <!-- 使用settings对Mybatis全局进行设置 -->
   <settings>
       <!-- 将xxx_xxx这样的列名自动映射到xxXxx这样驼峰式命名的属性名 -->
       <setting name="mapUnderscoreToCamelCase" value="true"/>
   </settings>
   ```

2. 在mapper文件中，使用resultMap标签定义对应关系，再在后面的SQL语句中引用`resultMap`属性

```xml
<!-- 专门声明一个resultMap设定column到property之间的对应关系 -->
    <resultMap id="selectEmployeeByRMResultMap" type="com.atguigu.mybatis.entity.Employee">

        <!-- 使用id标签特殊设置 主键列和主键属性之间的对应关系 -->
        <!-- column属性用于指定字段名；property属性用于指定Java实体类属性名 -->
        <id column="emp_id" property="empId"/>

        <!-- 使用result标签设置普通字段和Java实体类属性之间的关系 -->
        <result column="emp_name" property="empName"/>
        <result column="emp_salary" property="empSalary"/>
    </resultMap>
    
<!-- Employee selectEmployeeByRM(Integer empId); -->
<select id="selectEmployeeByRM" resultMap="selectEmployeeByRMResultMap">
    select emp_id,emp_name,emp_salary from t_emp where emp_id=#{empId}
</select>
```



## 关联关系 

表之间存在一对一、一对多、多对多的关系，这些关系如何反映在实体类，以及如何封装结果集，正是关联关系要考虑的事情。 



### 一对一 

场景：每一个订单对应一个顾客

表字段名

| order_id | order_name | customer_id |
| -------- | ---------- | ----------- |

主动关联的实体类中设置被关联属性，此例为order => customer  

```java
public class Order {
    private Integer orderId;
    private String orderName;
    private Customer customer;// 体现的是对一的关系

    public Order(Integer orderId, String orderName, Customer customer) {
        this.orderId = orderId;
        this.orderName = orderName;
        this.customer = customer;
    }
	
    // 无参构造
    public Order() {
    }
}
```

在mapper配置文件中，创建`resultMap`标签，用以构造结果集。**现在的字段，有一部分属于Order类，另一部分属于Customer类，用`asscociation`标签来指定外部的关联类。**

```xml
<resultMap id="selectOrderByIDResultMap" type="com.hollis.mybatis.entity.Order">
    <id column="order_id" property="orderId"></id>
    <result column="order_name" property="orderName"></result>
    <!--关联外部类 property 用于指定类属性 javeType用于指定封装实体类-->
    <association property="customer" javaType="com.hollis.mybatis.entity.Customer">
        <!--关联类的具体映射-->
        <result column="customer_name" property="customerName"></result>
        <result column="customer_id" property="customerId"></result>
    </association>
</resultMap>

<!--按照select 返回的字段取结果集一一封装 order_xx 属于 Order类属性-->
<!-- customer_xx 属于Customer属性-->
<select id="selectOrderByID" resultMap="selectOrderByIDResultMap">
    select order_id,order_name,tc.customer_id,tc.customer_name  from t_order
    left join t_customer tc on t_order.customer_id = tc.customer_id
    where order_id=#{orderId};
</select>
```



查询示例 

```java
Order order = orderMapper.selectOrderByID(1);
System.out.println(order);

/* 打印结果 customer的属性已经被封装 
Order{orderId=1, orderName='o1', customer=Customer{customerId=1, customerName='c01', orderList=null}}
*/
```

### 一对多 

场景：一个顾客可以有多个订单。 

一对多的设置，并不比一对一复杂多少。在“一”中，创建集合，表示“多”。 

```java
public class Customer {

    private Integer customerId;
    private String customerName;
    private List<Order> orderList;// 体现的是对多的关系
}
```

mapper文件配置中，同样创建resultMap标签，但是用于指定集合属性的标签是collection和它的ofType属性。

```xml
<resultMap id="selectCustomerByIDResultMap" type="com.hollis.mybatis.entity.Customer">
    <id column="customer_id" property="customerId"></id>
    <result column="customer_name" property="customerName"></result>
	<!--property对应类的集合属性 ofType指定集合中每个元素封装的实体类-->
    <collection property="orderList" ofType="com.hollis.mybatis.entity.Order">
        <!--关联类的具体映射-->
        <id column="order_id" property="orderId"></id>
        <result column="order_name" property="orderName"></result>
    </collection>
</resultMap>
<select id="selectCustomerByID" resultMap="selectCustomerByIDResultMap">
    select tc.customer_id, tc.customer_name,t.order_id,t.order_name from t_customer tc
    left join t_order t on tc.customer_id = t.customer_id
    where tc.customer_id = #{customer_id};
</select>
```

查询示例 

```java
Customer customer = orderMapper.selectCustomerByID(1);
System.out.println(customer); 
/* 打印结果 与其关联的Order实例 
Customer{customerId=1, customerName='c01', orderList=[Order{orderId=1, orderName='o1', customer=null}, Order{orderId=2, orderName='o2', customer=null}, Order{orderId=3, orderName='o3', customer=null}]}
*/
```



### 分步查询

**关联查询采用“一次到底的”查询策略，这导致它在封装结果集时，不管使用与否，都会将关联类封装起来**。例如，虽然一个顾客关联了多个订单，但可能大部分时间，我们只查询顾客本身的信息，而不会捎带着去查询订单，继续沿用原查询策略的话，内存中会存在大量的订单列表，导致浪费。

Customer的mapper配置文件： 在查询Customer时，orderList会一并查询

```xml
<collection property="orderList" ofType="com.hollis.mybatis.entity.Order">
    <!--关联类的具体映射-->
    <id column="order_id" property="orderId"></id>
    <result column="order_name" property="orderName"></result>
</collection>
```



“分步查询”可以解决这个问题，它符合直觉。**具体而言，它将查询拆分，第一次只查询类本身的信息，跳过关联类。当调用者需要访问关联类的信息时，再去查询关联类。** 这种分布查询的技术，也称为“延迟加载”，或者“懒加载”。 

要实现分步查询，要先完成对查询语句的拆分，**使得每次查询只保留自身信息，类似于解耦的思想。**

以Customer查询为例，为了实现分布查询，需要准备如下工作：

1. 修改customer的mapper配置文件

   select只查询 customer本身的信息

   ```xml
   <select id="selectCustomerByID" resultMap="selectCustomerByIDResultMap">
       select tc.customer_id, tc.customer_name from t_customer tc
       where tc.customer_id = #{customer_id};
   </select>
   ```

   修改resultMap 属性的关联属性标签collection，取消ofType属性，这样就不会立刻封装结果。创建select属性，表示该关联属性的查询跳转到此处select语句处理，值是`namesapce.id` 。column表示要传递给该select语句的参数

   ```xml
   <collection property="orderList"
               column="customer_id"
        	 select="com.hollis.mybatis.entity.Mapper.OrderMapper.selectOrderByCustomerID">
       <id column="order_id" property="orderId"></id>
       <result column="order_name" property="orderName"></result>
   </collection>
   ```

2. 同时修改 order的查询，同样为查询自身，注意id要与跳转的select对应 

   ```xml
   <select id="selectOrderByCustomerID" resultType="com.hollis.mybatis.entity.Order">
      select order_id,order_name from t_order
       where t_order.customer_id = #{customer_id};
   </select>
   ```

3. 开启懒加载配置文件

   ```xml
   <settings>
       <!-- 开启延迟加载功能：需要配置两个配置项 -->
       <!-- 1、将lazyLoadingEnabled设置为true，开启懒加载功能 -->
       <setting name="lazyLoadingEnabled" value="true"/>
       <!-- 2、将aggressiveLazyLoading设置为false，关闭“积极的懒加载” -->
       <setting name="aggressiveLazyLoading" value="false"/>
   </settings>
   ```

   

测试实例：一个customer对应一个orderList 

```java
@Test
public void testCustomerSelect() throws InterruptedException {
    session = sessionFactory.openSession();
    CustomerMapper customerMapper = session.getMapper(CustomerMapper.class);
    Customer customer = customerMapper.selectCustomerByID(1);
    System.out.println(customer.getCustomerName()); // 只用到了customer属性
    System.out.println("lazy loading");
    System.out.println(customer.getOrderList()); // 用到了order属性
}
```

结果：拆成了多次sql查询处理 

![image-20220704143627825](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220704143627825.png)



## 动态sql

在结构上动态地拼接sql语句，而不是仅仅设置参数。 

例如，根据实体对象属性来设置查询条件，where可能有，也可能没有，结构是变化的，这种场景就需要使用到动态sql。

动态sql可以看做是mybatis的一种语法，也是使用标签来管理。 

### if 和 where

```xml
<!--    Employee selectByCordination(Employee emp);-->
<select id="selectByCordination" resultType="com.hollis.dynamic.entity.Employee">
    select emp_name,emp_salary from t_emp
    <!--where条件是否存在取决于传入的emp对象的属性参数-->
    <!--test属性是语法规定-->
    <where>
        <if test="empName != null">
            <!-- #{}访问参数 -->
            or emp_name=#{empName}
        </if>
        <!--大小写符号使用了转义-->
        <!--因为多个条件可能同时成立 所以使用了or或者and-->
        <!--where标签会自动处理这些多余的or/and-->
        <if test="empSalary &gt; 2000">
            or emp_salary>#{empSalary}
        </if>
    </where>
</select>
```

当两个条件都满足时，上述sql语句为

```sql
select emp_name,emp_salary from t_emp
where emp_name={?} or emp_salary>{?};
```

只有其中一个条件满足时，sql语句为 

```sql
select emp_name,emp_salary from t_emp
where emp_name={?};
```

其余情况依次类推 。

### choose/when/otherwise

if会每个条件都进行判断 ，choose当满足一个条件时，就终止其余判断 。

```xml

<!-- List<Employee> selectEmployeeByConditionByChoose(Employee employee) -->
<select id="selectEmployeeByConditionByChoose" resultType="com.atguigu.mybatis.entity.Employee">
    select emp_id,emp_name,emp_salary from t_emp
    where
    <choose>
        <when test="empName != null">emp_name=#{empName}</when>
        <when test="empSalary &lt; 3000">emp_salary &lt; 3000</when>
        <!--otherwise 表示都不满足时的情况-->
        <otherwise>1=1</otherwise>
    </choose>
</select>
```

### set 

实体对象只有部分属性是有意义的，其余可能为初始值。为了动态的决定更新哪些字段，使用set标签 

```xml
<!--    int updateEmployee(Employee emp);-->
<update id="updateEmployee" >
    update t_emp
    <set>
        <!--这些if判断都是为了验证这些字段是否有效 避免初始值覆盖原有数据-->
        <if test="empSalary != 0">
            emp_salary=#{empSalary},
        </if>
        <if test="empName != null">
            emp_name=#{empName},
        </if>
    </set>
    where emp_id= #{empId};
</update>
```

### foreach

循环生成多个sql片段，常配合列表对象，完成批量操作，例如批量更新 

```xml
<!--    int batchInsertEmployee(@Param("empList") List<Employee> empList);-->
<insert id="batchInsertEmployee">
    insert  into t_emp(emp_name,emp_salary)
    <!--collecction 指定参数 参数名和接口使用Param注解名一致-->
    <!--item指定集合中每个元素的别名 用在 循环体里-->
   	<!--open表示循环体里每一句的前缀-->
    <!--sepabtor表示循环体后的每一句分隔符号-->
    <foreach collection="empList" item="emp" open="values" separator=",">
        <!-- 每一个元素 emp.xxx-->
        (#{emp.empName},#{emp.empSalary})
    </foreach>
</insert>
```

当使用foreach来完成批量更新时，对数据库的url连接要添加参数`allowMultiQueries=true`

```shell
wechat.dev.url=jdbc:mysql://localhost/mybaits-example?allowMultiQueries=true
```

update不像insert，sql语句需要写在循环体里。

```xml
<!--    int batchUpdateEmployee(List<Employee> empList);-->
<update id="batchUpdateEmployee" >
    <foreach collection="empList" index="index" item="emp">
        update t_emp
        set emp_name=#{emp.empName},
        emp_salary=#{emp.empSalary}
        where emp_id = #{emp.empId};
    </foreach>
</update>
```

使用循环体一次生成多条sql语句，发送到数据库，相对分多次发送sql语句，可以节省时间。

测试示例 

```java
@Test
public void EmployeeBatchUpdate() {
    session = sessionFactory.openSession();
    EmployeeMapper empMapper = session.getMapper(EmployeeMapper.class);

    List<Employee> list = new ArrayList<>();
    Employee emp;
    for(int i = 0; i<5; i++){
        emp = new Employee();
        emp.setEmpId(i);
        emp.setEmpName("hollis_"+i);
        emp.setEmpSalary(500+i*10);
        list.add(emp);
    }
    empMapper.batchUpdateEmployee(list); // 传入list
}
```

### 重复sql

使用重复的sql片段 

```xml
<!-- 使用sql标签抽取重复出现的SQL片段 -->
<!-- 在mapper节点下创建--->
<sql id="mySelectSql">
    select emp_id,emp_name,emp_age,emp_salary,emp_gender from t_emp
</sql>
```

引用 

```xml
<!-- 使用include标签引用声明的SQL片段 -->
<include refid="mySelectSql"/>
```

## 缓存

缓存sql语句的查询结果，下次在做同样的操作时，跳过与数据库的IO操作，直接从内存中取数据。

测试是否存在缓存，简单的一个办法，就是发起多次查询操作，看日志输出的是一条sql语句，还是多条。



<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220706051553339.png" alt="image-20220706051553339" style="zoom:50%;" />



一级缓存的范围限定于同一个SqlSession，二级缓存的范围限定在`sessionFactory`。

缓存的查询顺序是从大到小：**先二级，再一级，最后才是去数据库查询。 一级缓存的发生先于二级缓存，因为它是在一个SqlSession里发生。如果开启了二级缓存，当该session关闭时，数据会向下存入二级缓存。**



### 一级缓存

一级缓存的范围限定于同一个SqlSession，无需额外设置 

sql语句如下 

```xml
<select id="selectById" resultType="com.hollis.dynamic.entity.Employee">
    select emp_name,emp_salary from t_emp
    where emp_id = #{empId};
</select>
```

测试程序

```java
@Test
public void testFirstCacheLevel() {
    SqlSession session = sessionFactory.openSession();
    EmployeeMapper empMapper = session.getMapper(EmployeeMapper.class);
    for (int i = 0; i < 2; i++) {
        Employee emp = empMapper.selectById(1); // 连续查询多次 
        System.out.println("i-th run: "+emp);
    }

}
```

![image-20220706051209134](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220706051209134.png)



一级缓存在以下场景下失效：

- 对象变更：不是同一个SqlSession对象
- 查询变更：同一个SqlSession但是查询条件发生了变化
- 数据变更：
  - 同一个SqlSession两次查询期间执行了任何一次增删改操作
  - 同一个SqlSession两次查询期间手动清空了缓存，即`.clearCache()` 
  - 同一个SqlSession两次查询期间提交了事务

### 二级缓存



二级缓存开启步骤：

1. mapper 配置文件开启 cache 标签 

    ```xml
    <mapper namespace="com.atguigu.mybatis.EmployeeMapper">
        <!-- 加入cache标签启用二级缓存功能 -->
        <cache/>
    </mapper>
    ```

2. 让实体类支持Serializable接口 

   ```java
   public class Employee implements Serializable {}
   ```




**二级缓存的范围限定在`sessionFactory`，只有当它的一个session事务提交关闭后，一级缓存的内容才会并入二级缓存**

测试程序

```java
@Test
public void testSecondCacheLevel() {
    List<SqlSession> sessions = new ArrayList<>();
    for (int i = 0; i < 2; i++) {
        sessions.add(sessionFactory.openSession());
    }

    for(int i=0;i<sessions.size();i++){
        System.out.println("i-th select: "+i);
        SqlSession session = sessions.get(i);
        EmployeeMapper empMapper = session.getMapper(EmployeeMapper.class);
        empMapper.selectById(1);
        session.commit();
    }

}
```

# Spring

## IOC容器

容器是spring的核心，这里的容器不仅仅负责存储组件，还负责组件的创建销毁、工作等。 

IOC意为 inversion of control，反转控制。这里的“反转”指的是反转资源获取的方式，在此之前，资源的获取由组件主动获取，这样的方式需要开发者明确知道资源在容器中的获取方式，比价费力。反转之后，资源的获取由容器主动向组件推送，组件只需要确认资源的获取方式即可。 主客之势互易，可以这么理解。 

DI意为dependency injection，依赖注入，是组件预定义资源依赖方式来接收资源，是IOC思想的具体实现。



IOC容器接口：

* BeanFactory ： Spring 内部使用的接口，面向 Spring 本身，不提供给开发人员使用。**IOC容器中的组件也叫Bean** 
* ApplicationContext：BeanFactory 的子接口，提供了更多高级特性，面向 Spring 的使用者，几乎所有场合都使用 ApplicationContext 而不是底层的 BeanFactory。



ApplicationContext的具体实现类：

| 类型名                          | 简介                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| ClassPathXmlApplicationContext  | 通过读取**类路径下**的 XML 格式的配置文件创建 IOC 容器对象   |
| FileSystemXmlApplicationContext | 通过**文件系统路径**读取 XML 格式的配置文件创建 IOC 容器对象 |
| ConfigurableApplicationContext  | ApplicationContext 的子接口，包含一些扩展方法 refresh() 和 close() ，让 ApplicationContext 具有启动、关闭和刷新上下文的能力。 |
| WebApplicationContext           | 专门为 Web 应用准备，基于 Web 环境创建 IOC 容器对象，并将对象引入存入 ServletContext 域中。 |

## 用xml管理bean

### 创建

### 获取

```xml
<bean id="happyComponent" class="com.hollis.ioc.component.HappyComponent">
</bean>
```

每一个bean，都可以依据它的id或者class来获取。

```java
// 依据类名
HappyComponent happyComponent = (HappyComponent) iocContainer.getBean(HappyComponent.class);

// 依据id
HappyComponent happyComponent = (HappyComponent) iocContainer.getBean("happyComponent");
```

通过class来获取时，框架判断的标准是`instanceof`。**如果配置文件中有多个bean都使用了该Class，框架就无法准确地找到唯一的那个bean**，会导致报错。 类似于html里的元素id是唯一的，但是class却可以重复。

还有一种情形是，组件实现了某个接口，通过接口的class，也是可以找到的。这同样要确保应用了该class的bean是唯一的。

```java
// 假设 HappyComponent 实现了 HappyImp 接口
HappyComponent happyComponent = (HappyComponent) iocContainer.getBean(HappyImp.class);

```

### 属性赋值

每一个bean其实都是一个类，类属性的赋值问题自然是避免不了。 

有如下类

```java
public class HappyComponent implements HappyImp{
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void doWork() {
        System.out.println("component do work ...");
    }
}
```

**所有的类属性赋值，都是基于property标签。**

#### value

通过value属性，赋值常量，格式如下

```xml
<bean id="happyComponent" class="com.hollis.ioc.component.HappyComponent">
    <!--name 属性对应get/set方法 不直接对应属性名 因为那是私有的属性-->
    <!--value表示常量赋值-->
    <property name="name" value="hollis jiang"></property>
</bean>
```

这等效于`new HappyComponent().setName("hollis jiang") `  。



value属性用于指定字面常量，如果常量中出现了一些特殊字符，则要使用转义或者xml自带的纯文本格式。

```xml
<!--转义-->
<property name="expression" value="a &lt; b"/>
<!--<![CDATA[  这里面的东西会被当做纯文本 ]>-->
<value><![CDATA[a < b]]></value>>
```



#### bean

常量赋值过于简单，有时候属性可能是一个类。这时候就要使用bean赋值。由于bean在xml配置文件里，就是指代一个对象，**所以原理就是让property能够引用另外一个bean。**



创建类 

```java
public class HappyMachine {
    private  String machineName;
}
```

在Happy类中创建类属性引用该类 

```java
package com.hollis.ioc.component;

public class HappyComponent implements HappyImp{
    private String name;
    private HappyMachine machine; // machine 类 
    // 省略了get/set方法
}

```



##### **外部bean**

外部bean指的是两个bean标签是平级关系

bean 文件示例 

```xml
<bean id="happyMachine" class="com.hollis.ioc.component.HappyMachine">
    <property name="machineName" value="times back"></property>
</bean>

<bean id="happyComponent" class="com.hollis.ioc.component.HappyComponent">
    <property name="name" value="hollis jiang"></property>
    <!--引用 ref属性 指向另外一个bean标签的id-->
    <property name="machine" ref="happyMachine"></property>
</bean>
```

##### **内部bean**

在bean自身内部，再创建一个bean标签，作为一个对象给property赋值 

```xml
<bean id="happyComponent" class="com.hollis.ioc.component.HappyComponent">
    <property name="name" value="hollis jiang"></property>
    <property name="machine" >
        <!--在property属性里面-->
        <!--内部bean对象 不需要id-->
        <bean class="com.hollis.ioc.component.HappyMachine">
            <property name="machineName" value="times back inner"></property>
        </bean>
    </property>
</bean>
```

##### 级联属性赋值

属性的属性，即为级联属性。对于HappyComponent而言，属性HappyMachie的属性machineName就是级联属性。 

级联属性赋值，要求一级属性不为空，才能以`一级属性.二级属性` 这种形式调用 

```xml
<bean id="happyComponent6" class="com.atguigu.ioc.component.HappyComponent">
    <!-- 使该属性不为空 -->
    <property name="happyMachine" ref="happyMachine2"/>
    <!-- 对HappyComponent来说，happyMachine的machineName属性就是级联属性 -->
    <property name="happyMachine.machineName" value="cascadeValue"/>
</bean>
```



#### 构造器注入

根据参数形式和个数，反射来获取指定的构造器创建 。实体类必须要有一个无参构造器，当没有参数传入时，也能正常被实例化 

```java
public class HappyComponent implements HappyImp{
    private String name;
    private HappyMachine machine;

    public HappyComponent(String name){
        this.name = "constructor "+name;

    }

    public HappyComponent() {
    }
}
```

通过标签 `constructor-arg` 创建 ，name属性指定形参名字用以关联 

```xml
<bean id="happyComponent" class="com.hollis.ioc.component.HappyComponent">
    <constructor-arg name="name" value="happyByConstructor"/>
</bean>
```

#### p:

简化的属性注入，需要引入新的约束。 `p:属性名="属性值"` 

输入`p:`，等待idea提示后，输入alt+enter 即可。 

```xml
<bean id="happyMachine" class="com.hollis.ioc.component.HappyMachine"
      p:machineName="p_namespace_machine"
      >
</bean>
```

#### 集合属性



```java
public class HappyComponent implements HappyImp{
    private String name;
    private HappyMachine machine;
    private List<String> members = new ArrayList<>(); // 集合属性
    private Map<String,String> map = new HashMap<>(); // map属性
    
    // 省略get/set方法 
}
```

bean 文件配置

```xml
<bean id="happyComponent" class="com.hollis.ioc.component.HappyComponent">
    <property name="members">
        <list>
            <value>member01</value>
            <value>member02</value>
            <value>member03</value>
        </list>
    </property>
    <property name="map" >
        <map>
            <entry key="sex" value="male"></entry>
            <entry key="age" value="25"></entry>
        </map>
    </property>
</bean>
```

#### 关联外部属性文件 

创建外部属性文件 

![image-20220709090501853](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220709090501853.png)



jdbc.properties 

```properties
jdbc.user=root
jdbc.password=root
jdbc.url=jdbc:mysql://localhost:3306/mybaits-example
jdbc.driver=com.mysql.jdbc.Driver
```

bean 文件配置 

创建 context 属性 

```xml
<!--类路径下的文件-->
<context:property-placeholder location="classpath:jdbc.properties"/>
```

使用`${}` 引用该属性文件的属性 

```xml
<bean id="druidDataSource" class="com.alibaba.druid.pool.DruidDataSource">
    <property name="url" value="${jdbc.url}"/>
    <property name="driverClassName" value="${jdbc.driver}"/>
    <property name="username" value="${jdbc.user}"/>
    <property name="password" value="${jdbc.password}"/>
</bean>
```

#### 自动装配 

设置属性autowire ，让框架根据属性名（byName）或者根据类型（byType），去找对应id的bean对象，然后装载 

```java
public class HappyComponent implements HappyImp{
    private String name;
    private HappyMachine machine; // 注意这个属性名 
}
```

```xml
<!--id名为machine 和 类属性名字一致-->
<bean id="machine" class="com.hollis.ioc.component.HappyMachine"
      p:machineName="p_namespace_machine"
>
</bean>

<bean id="happyComponent" class="com.hollis.ioc.component.HappyComponent"
autowire="byName">
</bean>
```

### 集合类型的bean



将若干bean组合成一个集合 ，该集合是一个整体 

```xml
<util:list id="machineList">
    <bean class="com.atguigu.ioc.component.HappyMachine">
        <property name="machineName" value="machineOne"/>
    </bean>
    <bean class="com.atguigu.ioc.component.HappyMachine">
        <property name="machineName" value="machineTwo"/>
    </bean>
    <bean class="com.atguigu.ioc.component.HappyMachine">
        <property name="machineName" value="machineThree"/>
    </bean>
</util:list>
```

使用

```java
public void testBeanList() {
    List<HappyMachine>  machineList = (List<HappyMachine>) iocContainer.getBean("machineList"); // 根据id去创建
    System.out.println(machineList);
}
```





### 作用域 

bean的属性scope 用来控制bean实例化对象的方式，单例模式或者多实例模式 

| 取值      | 含义           | 创建对象的时机      |
| --------- | -------------- | ------------------- |
| singleton | 单实例         | IOC容器初始化时创建 |
| prototype | 允许有多个实例 | getBean()调用时     |





## 用注解管理bean

摒弃xml，使用`@注解`的形式来更优雅方便地管理bean。 

### 扫描 

通过在xml文件中，配置扫描的java包位置，来实现容器对bean的添加。 

#### 创建组件类 

以注解的形式创建组件类 。组件的含义以及使用形式如下，**它们在底层其实是一个东西。彼此之间是等价的，标记不同名字的注解是为了增强可读性。** 

```java
//@Repository // dao持久层
//@Service   // 业务层
//@Controller // 控制层 类似 servlet
@Component  // 普通组件
public class CommonComponent {
}
```

其余几个类的创建，依法炮制 

![image-20220709151300949](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220709151300949.png)

在配置文件中，创建标签，**添加扫描的位置** 

```xml
<context:component-scan base-package="com.hollis.ioc.components"/>
```

这么一来，上述组件类，就已经添加到容器了。**可以通过类名或者id获取，id是默认是类名首字母小写的形式。** 但也可以在添加注解时，命名该bean的id。

```java
@Component(value = "hollisComponent")  // 普通组件 id命名为 value对应的值 
```

 测试示例；

```java
public class IOCTest {
    private ApplicationContext iocContainer = new ClassPathXmlApplicationContext("applicationContext.xml");

    @Test
    public void testAnnotationcScanBean() {
        CommonComponent commonComponent = (CommonComponent) iocContainer.getBean(CommonComponent.class); // 类名
        CommonComponent commonComponent1 = (CommonComponent) iocContainer.getBean("commonComponent"); // 默认id

        System.out.println("commonComponent = " + commonComponent);
        System.out.println("commonComponent1 = " + commonComponent1);
    }
}
```

### 自动装配

组件之间互相引用时，执行自动装配，即让框架为我们自动赋值。 

确保被装配的属性类已经在容器中，然后使用`@AutoWired`注解，甚至都不需要提供setter方法。如下 

```java
@Component  // 普通组件
public class CommonComponent {
    @Autowired // 自动装配下述类属性
    private SoldierController controller;
}
```

自动装配流程： 

![image-20220709191702069](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220709191702069.png)

* 根据类型class查找 

* 根据id查找

  * 在使用qualifier注解的情况下，按照注解属性去找对应id

    ```java
    @Autowired // 自动装配下述类属性
    @Qualifier("hollisQ") // 指定对应bean的id = hollisQ
    private SoldierController controller;
    ```

  * 否则，使用属性名查找



### 注解配置 

用注解完成对框架的配置，放弃对xml文件的控制。  



创建类 

```java
@Configuration  // 该注解旨在将该类包装成一个配置类 
public class MyConfiguration {

    // bean 注解标记的方法会被放入IOC容器 
    @Bean
    CommonComponent getComponent(){
        return  new CommonComponent(); // 返回一个实例 
    }
}
```

当然，它也可以执行自动装配 

```java
@Configuration
@ComponentScan("com.hollis.ioc.components")
public class MyConfiguration {

    // bean 注解标记的方法会被放入IOC容器
    @Bean
    CommonComponent getComponent(){
        return  new CommonComponent();
    }
}
```



获取IOC容器

```java
// 使用xml配置文件
private ApplicationContext iocContainer = new ClassPathXmlApplicationContext("applicationContext.xml");

// 使用注解配置
private ApplicationContext iocContainerAnnotation = new AnnotationConfigApplicationContext(MyConfiguration.class);
```



## 和Junit整合

Spring框架整合了Junit以后，会让对bean的测试更加容易。 因为可以使用注解，自动装配，免去了获取IOC容器、获取bean实例的方法

### juni4

导入依赖 

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-test</artifactId>
    <version>5.3.1</version>
</dependency>
```

一个整合以后的测试类 

```java
@RunWith(SpringJUnit4ClassRunner.class)
// Spring的@ContextConfiguration指定Spring配置文件的位置
@ContextConfiguration(value = {"classpath:applicationContext.xml"})
public class JunitTest {

    @Autowired
    private SoldierController soldierController; // 自动装配

    @Test
    public void testIntegration() {
        System.out.println("soldierController = " + soldierController);
    }

}
```

### junit5

导入依赖

``` xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-api</artifactId>
    <version>5.7.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-test</artifactId>
    <version>5.3.1</version>
</dependency>
```



junit5只需要一行注解 

```java

// spring的xml配置文件
@SpringJUnitConfig(locations = {"classpath:spring-context.xml"})
public class Junit5IntegrationTest {
    
    @Autowired
    private EmpDao empDao;
    
    @Test
    public void testJunit5() {
        System.out.println("empDao = " + empDao);
    }
    
}
```



## AOP

AOP的逻辑，有点像python装饰器的逻辑，不破坏原有方法的代码情况下，完成一些装饰功能的添加。

更专业的称呼叫做 代理模式， 不直接调用原有方法，而是通过代理类间接地调用原来的方法。

### 术语解析

#### 横切关注点

横切关注点 ，方法执行前后的位置，客观存在。

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220711111507028.png" alt="image-20220711111507028" style="zoom:67%;" />



#### 通知 

在横切关注点上，完成的方法就叫做，通知方法。可以细分如下 

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220711111635367.png" alt="image-20220711111635367" style="zoom:67%;" />



通知方法格式，使用try-catch包裹 

```java
// 整个try-catch 代码块叫做 环绕通知
try{
    // 前置通知 
    // 执行目标方法 并保存执行结果
    // 返回通知
    
}catch{
    // 异常通知
    
}finally{
    // 后置通知
}
```

#### 切面 

实现了上述通知的类，叫做切面，可以理解为 切面包含了多个切入点。 

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220711112054784.png" alt="image-20220711112054784" style="zoom:50%;" />

#### 目标 

被代理对象 

#### 代理 

向目标对象应用通知之后创建的代理对象。



### 使用注解创建切面类

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220711112414120.png" alt="image-20220711112414120" style="zoom:67%;" />

- 动态代理（InvocationHandler）：JDK原生的实现方式，要求目标类必须实现接口。
- cglib：通过继承被代理的目标类，所以不需要目标类实现接口。
- AspectJ：本质上是静态代理，**将代理逻辑“织入”被代理的目标类编译得到的字节码文件**，所以最终效果是动态的。weaver就是织入器。Spring只是借用了AspectJ中的注解。



pom文件加入依赖

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-aspects</artifactId>
    <version>5.3.1</version>
</dependency>
```

xml配置文件中开启aop注解 

```xml
<!-- 开启基于注解的AOP功能 -->
<aop:aspectj-autoproxy/>
```



假设有接口 

```java
public interface Calculator {

    int add(int i, int j);

    int sub(int i, int j);

    int mul(int i, int j);

    int div(int i, int j);

}
```

其实现类如下 

```java
@Component // 加入容器
public class CalculatorPureImpl implements Calculator {

    @Override
    public int add(int i, int j) {

        int result = i + j;

        System.out.println("方法内部 result = " + result);

        return result;
    }

    @Override
    public int sub(int i, int j) {

        int result = i - j;

        System.out.println("方法内部 result = " + result);

        return result;
    }

    @Override
    public int mul(int i, int j) {

        int result = i * j;

        System.out.println("方法内部 result = " + result);

        return result;
    }

    @Override
    public int div(int i, int j) {

        int result = i / j;

        System.out.println("方法内部 result = " + result);

        return result;
    }
}
```

那么一个通过注解实现的切面类如下 ：不同注解类的含义见注释。

```java
// @Aspect表示这个类是一个切面类
@Aspect
// @Component注解保证这个切面类能够放入IOC容器
@Component
public class LogAspect {

    // @Before注解：声明当前方法是前置通知方法
    // value属性：指定切入点表达式，由切入点表达式控制当前通知方法要作用在哪一个目标方法上
    // 切入点指向了 接口，所有实现该接口的类都会被代理
    @Before(value = "execution(public int com.hollis.Calculator.add(int,int))")
    public void printLogBeforeCore() {
        System.out.println("[AOP前置通知] 方法开始了");
    }

    @AfterReturning(value = "execution(public int com.hollis.Calculator.add(int,int))")
    public void printLogAfterSuccess() {
        System.out.println("[AOP返回通知] 方法成功返回了");
    }

    @AfterThrowing(value = "execution(public int com.hollis.Calculator.add(int,int))")
    public void printLogAfterException() {
        System.out.println("[AOP异常通知] 方法抛异常了");
    }

    @After(value = "execution(public int com.hollis.Calculator.add(int,int))")
    public void printLogFinallyEnd() {
        System.out.println("[AOP后置通知] 方法最终了");
    }

}
```

该切面类绑定了Calculator接口中的add方法，用@注解在4个切点处实现了方法。**通知方法叫什么不重要，能够决定它注入位置的是方法声明上的注释**

* After： 后置通知 
* AfterThrowing：异常通知 
* AfterReturning：返回通知 
* Before：前置通知 





环绕通知是上述4种通知的总和，实现它，可以一次性覆盖4个切点。只是，它的实现方式和上述几种略有不同，需要用户来实现结构，并手动调用目标方法。

```java
public Object notifyAround(ProceedingJoinPoint pjp) {
    Object res = null; // 目标方法返回值
    try {
        System.out.println(String.format("方法名：%s 实际参数：%s", pjp.getSignature().getName(),
                Arrays.toString(pjp.getArgs())));
        System.out.println("前置通知");
        res = pjp.proceed(pjp.getArgs()); // 调用目标方法 传入实际参数
        System.out.println("返回通知");
    } catch (Throwable e) {
        System.out.println("异常通知");
        System.out.println(e.getMessage());

    } finally {
        System.out.println("后置通知");
    }
    return res;
}
```





关于切面类更详细的使用参考后续小节 



#### 切面优先级 

当有多个切面类绑定同一方法时，使用`@Order()` 注解来表明它们的优先级，数值越小，表明优先级越高。优先级高的切面类会包裹在最外面，依次类推。

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220714085136420.png" alt="image-20220714085136420" style="zoom:67%;" />





#### 获取方法细节

通知方法，在切入点位置被执行。但是，其作用不仅仅于此，**它也可以通过一些手段来获取目标类的方法细节，目标方法的返回值、所抛出的异常等。**

核心思想是：用目标方法的签名对象，来获取方法的所有细节，例如权限修饰符、返回值、方法名、实际参数等。 

```java
import org.aspectj.lang.JoinPoint; 

public void notifyReturn(JoinPoint jp){
    System.out.println("返回通知");
    Signature signature = jp.getSignature();
    String methodName = signature.getName(); // 方法名
    String typeName = signature.getDeclaringTypeName(); // 类全限定名
    List<Object> args = Arrays.asList(jp.getArgs()); // 获取调用时的实参

    System.out.println(String.format("methodName:%s typeName:%s args:%s",methodName,typeName,args));
}

```



获取目标方法的返回值 

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220712202249375.png" alt="image-20220712202249375" style="zoom: 67%;" />

```java
// @AfterReturning注解标记返回通知方法
// 1.在@AfterReturning注解中通过returning属性设置一个名称
// 2. 使用returning属性设置的名称在通知方法中声明一个对应的形参，该形参在实际调用时就是目标方法的实际返回值

@AfterReturning(
        value = "execution(public int com.atguigu.aop.api.Calculator.add(int,int))",
        returning = "targetMethodReturnValue"
)
public void printLogAfterCoreSuccess(JoinPoint joinPoint, Object targetMethodReturnValue) {
    
    String methodName = joinPoint.getSignature().getName();
    
    System.out.println("[AOP返回通知] "+methodName+"方法成功结束了，返回值是：" + targetMethodReturnValue);
}
```



获取异常的方法类似

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220712202320977.png" alt="image-20220712202320977" style="zoom:67%;" />



```java
// @AfterThrowing注解标记异常通知方法
// 1：在@AfterThrowing注解中声明一个throwing属性设定形参名称
// 2：使用throwing属性指定的名称在通知方法声明形参，Spring会将目标方法抛出的异常对象从这里传给我们
@AfterThrowing(
        value = "execution(public int com.atguigu.aop.api.Calculator.add(int,int))",
        throwing = "targetMethodException"
)
public void printLogAfterCoreException(JoinPoint joinPoint, Throwable targetMethodException) {
    
    String methodName = joinPoint.getSignature().getName();
    
    System.out.println("[AOP异常通知] "+methodName+"方法抛异常了，异常类型是：" + targetMethodException.getClass().getName());
}
```



#### 切入点表达式

##### 基本格式

格式：`execution(权限修饰符 函数返回值 包名.类名.方法名(形参类型))` 

**切入点表达式用于绑定通知方法 和 目标类的方法，**例如 

```java
// 该方法应用于 Calculator类add函数的返回通知 
@AfterReturning(value = "execution(public int com.hollis.Calculator.add(int,int))")
public void printLogAfterSuccess() {
    System.out.println("[AOP返回通知] 方法成功返回了");
}
```

切入点表达式支持 `*` 通配符，具体如下：

* 权限修饰符和 返回值：用一个`*` 联合表示权限修饰任意 、返回值任意类型

* 包名：使用`*`表示包名任意，`*.`表示包名任意且层次任意，例如`com.hollis`，层次为2，就可以使用`*.`

* 类名：表示任意字符 ，例如`Service*`，表示以Service开头的任意类名 

* 方法名：同类名 

* 形参列表：（1） int 和 Integer不等 （2）使用`..` 表示任意多参数 

  

```java
// public int 包名任意深度任意 以Service结尾的类名 方法名任意 最后一个形参是int 
execution(public int *..*Service.*(.., int))
```

![image-20220712200540980](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220712200540980.png)



##### 重用表达式 

将一个切入点表达式封装，以后再用到同一个切面表达式时，使用引用的形式，指向该表达式。封装的好处自然是，一处修改，处处修改。 

未重用前 ：在两个通知方法前，使用了相同的切入点表达式

```java
@Aspect
@Component
public class LogAspect {
    @Before(value = "execution(public int com.hollis.Calculator.add(int,int))")
    public void printLogBeforeCore(JoinPoint jp) {
        System.out.println("[AOP前置通知] 方法开始了");
    }

    @AfterReturning(value = "execution(public int com.hollis.Calculator.add(int,int))")
    public void printLogAfterSuccess() {
        System.out.println("[AOP返回通知] 方法成功返回了");
    }

}
```

**重用步骤**：

在一处声明切入点表达式，声明的形式如下 

```java
@Aspect
// @Component注解保证这个切面类能够放入IOC容器
@Component
public class LogAspect {
	
    // @Pointcut 用于声明具体的表达式 
    @Pointcut(value = "execution(public int com.hollis.Calculator.add(int,int))")
    public  void forCalculatorAdd(){}; // 相当于是表达式的别名

    @Before(value = "forCalculatorAdd()") // 使用表达式的名字
    public void printLogBeforeCore() { 
        System.out.println("[AOP前置通知] 方法开始了");
    }

    @AfterReturning(value = "forCalculatorAdd()")
    public void printLogAfterSuccess() {
        System.out.println("[AOP返回通知] 方法成功返回了");
    }
```

上述在一个类内部声明了切入点表达式，并用函数名`forCalculatorAdd`指向了真正目标类的接口方法，然后，在具体的通知方法中，使用了该函数别名。 如果为了更好的封装，可以将这些声明单独地放到一个类里。 



### 对获取bean的影响 

能否正常获取bean，取决于该bean在容器里是否唯一



要分两种情况讨论：

1. 目标类实现了接口，**当被切面类动态代理以后，在容器里真实存在的其实是代理类**，代理类和目标类是兄弟关系，而非直接的目标类 
   1. 依据接口获取：
      1. 实现类唯一：正常 
      2. 实现类不唯一：异常
   2. 依据类获取：异常，原因如上 
2. 目标类没有实现接口，虽**然同样是被切面类代理，但是代理的方式是cglib**，代理类直接继承了目标类，所以容器里依然可以找到该目标类
   1. 依据类获取：正常



## 声明式事务

### 事务管理器 

用于在业务层(Sevice)管理事务的执行，**原则便是“一荣俱荣，一损俱损”。** 

业务层往往会调用多个dao层的方法，来进行数据库的写，其中，若有一个事务执行异常，则此前的所有事务都应该回滚。它的逻辑应该如下：

```java
// 编程式事务管理 事无巨细 需要自己实现 
try{
    // 关闭事务的自动提交
    // dao方法1 
    // dao方法2
    // 提交所有事务
}catcah(){
    // 异常 
    // 回滚事务
}finally{
    // 关闭数据库连接 
}
```

**事务管理器可以直接接管这一套逻辑 ，将这些重复又必须的代码，以注解的形式直接实现，所以也叫做 声明式事务**



spring配置文件

```xml

<!-- 开启基于注解的声明式事务功能 -->
<!-- 使用transaction-manager属性指定当事务管理器的bean -->
<!-- transaction-manager属性的默认值是transactionManager，如果事务管理器bean的id正好就是这个默认值-->
<tx:annotation-driven transaction-manager="transactionManager"/>
<!-- 配置事务管理器 -->
<bean id="transactionManager"
      class="org.springframework.jdbc.datasource.DataSourceTransactionManager">

    <!-- 事务管理器的bean只需要装配数据源，该数据源指向一个已配置的数据池的bean -->
    <property name="dataSource" ref="druidDataSource"/> . 
</bean>
```

在业务层的方法上，或类名（覆盖全方法），使用注解@Transactional。因为业务层才有可能发生一系列数据库操作，符合事务的定义（不可分割的操作序列）。

```java
@Transactional  // 事务管理器接管该类下的所有方法  
@Service
public class EmpService {

    @Autowired
    private EmpDao empDao;

    public void updateTwice(
    ) {
		// 这里会发生多个事务 
    }

}
```

注解@Transactional(value)取值包括：

* `readOnly = true`：接管事务只读，会加速sql执行速度，不允许发生写操作 

* `timeout = int`：事务执行超时，则回滚操作 

* rollbackFor属性：需要回滚的异常，值为一个Class类型的对象

  ```java
  @Transactional(rollbackFor = Exception.class)
  ```

* noRollbackFor：不需要回滚的异常，值同上，类似白名单 



### 用xml声明事务管理器 

依赖如下

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-aspects</artifactId>
    <version>5.3.1</version>
</dependency>
```

配置文件如下

1. 配置事务管理器 `tx:advice`，在事务属性中，接管具体的方法。 
2. 将 事务通知 和 切入点表达式 关联起来，让通知和具体的方法联系到一块

```xml
<!--    用xml配置事务管理器-->
    <aop:config>
        <!-- 配置切入点表达式，将事务功能定位到具体方法上 -->
        <aop:pointcut id="txPoincut" expression="execution(* *..*Service.*(..))"/>

        <!-- 将事务通知和切入点表达式关联起来 -->
        <aop:advisor advice-ref="txAdvice" pointcut-ref="txPoincut"/>

    </aop:config>

    <!-- tx:advice标签：配置事务通知 -->
    <!-- id属性：给事务通知标签设置唯一标识，便于引用 -->
    <!-- transaction-manager属性：关联事务管理器 -->
    <tx:advice id="txAdvice" transaction-manager="transactionManager">
<!--        必须要有事务属性-->
        <tx:attributes>

            <!-- tx:method标签：配置具体的事务方法 -->
            <!-- name属性：指定方法名，可以使用星号代表多个字符 -->
            <tx:method name="get*" read-only="true"/>
            <tx:method name="query*" read-only="true"/>
            <tx:method name="find*" read-only="true"/>

            <!-- read-only属性：设置只读属性 -->
            <!-- rollback-for属性：设置回滚的异常 -->
            <!-- no-rollback-for属性：设置不回滚的异常 -->
            <!-- isolation属性：设置事务的隔离级别 -->
            <!-- timeout属性：设置事务的超时属性 -->
            <!-- propagation属性：设置事务的传播行为 -->
            <tx:method name="save*" read-only="false" rollback-for="java.lang.Exception" propagation="REQUIRES_NEW"/>
            <tx:method name="update*" read-only="false" rollback-for="java.lang.Exception" propagation="REQUIRES_NEW"/>
            <tx:method name="delete*" read-only="false" rollback-for="java.lang.Exception" propagation="REQUIRES_NEW"/>
        </tx:attributes>
    </tx:advice>
```

# Spring MVC

## 准备 

导入依赖

```xml
<dependencies>
    <!-- SpringMVC -->
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-webmvc</artifactId>
        <version>5.3.1</version>
    </dependency>
    
    <!-- 日志 -->
    <dependency>
        <groupId>ch.qos.logback</groupId>
        <artifactId>logback-classic</artifactId>
        <version>1.2.3</version>
    </dependency>
    
    <!-- ServletAPI -->
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>javax.servlet-api</artifactId>
        <version>3.1.0</version>
        <scope>provided</scope>
    </dependency>
    
    <!-- Spring5和Thymeleaf整合包 -->
    <dependency>
        <groupId>org.thymeleaf</groupId>
        <artifactId>thymeleaf-spring5</artifactId>
        <version>3.0.12.RELEASE</version>
    </dependency>
</dependencies>
```



配置web.xml 

1. 创建mvc的 servlet： DispatcherServlet ，修改它的启动顺序为 伴随web应用启动（默认为第一次请求发生时创建）

2. 创建spring配置文件，令DispatcherServlet 的参数`contextConfigLocation` 指向配置文件。配置文件中主要指定加入容器的扫描包

   ```xml
   <!-- 自动扫描包 -->
   <context:component-scan base-package="com.atguigu.mvc.handler"/>
       
   <!-- Thymeleaf视图解析器 -->
   <bean id="viewResolver" class="org.thymeleaf.spring5.view.ThymeleafViewResolver">
       <property name="order" value="1"/>
       <property name="characterEncoding" value="UTF-8"/>
       <property name="templateEngine">
           <bean class="org.thymeleaf.spring5.SpringTemplateEngine">
               <property name="templateResolver">
                   <bean class="org.thymeleaf.spring5.templateresolver.SpringResourceTemplateResolver">
       
                       <!-- 视图前缀 -->
                       <property name="prefix" value="/WEB-INF/templates/"/>
       
                       <!-- 视图后缀 -->
                       <property name="suffix" value=".html"/>
                       <property name="templateMode" value="HTML5"/>
                       <property name="characterEncoding" value="UTF-8" />
                   </bean>
               </property>
           </bean>
       </property>
   </bean>
   ```

   

3. 将所有的url交给DispatcherServlet处理，设置为`/`表示匹配所有 

```xml
<!-- 配置SpringMVC中负责处理请求的核心Servlet，也被称为SpringMVC的前端控制器 -->
<servlet>
    <servlet-name>DispatcherServlet</servlet-name>
    
    <!-- DispatcherServlet的全类名 -->
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    
    <!-- 通过初始化参数指定SpringMVC配置文件位置 -->
    <init-param>
    
        <!-- 如果不记得contextConfigLocation配置项的名称，可以到DispatcherServlet的父类FrameworkServlet中查找 -->
        <param-name>contextConfigLocation</param-name>
    
        <!-- 使用classpath:说明这个路径从类路径的根目录开始才查找 -->
        <param-value>classpath:spring-mvc.xml</param-value>
    </init-param>
    
    <!-- 作为框架的核心组件，在启动过程中有大量的初始化操作要做，这些操作放在第一次请求时才执行非常不恰当 -->
    <!-- 我们应该将DispatcherServlet设置为随Web应用一起启动 -->
    <load-on-startup>1</load-on-startup>
    
</servlet>
    
<servlet-mapping>
    <servlet-name>DispatcherServlet</servlet-name>
    
    <!-- 对DispatcherServlet来说，url-pattern有两种方式配置 -->
    <!-- 方式一：配置“/”，表示匹配整个Web应用范围内所有请求。这里有一个硬性规定：不能写成“/*”。只有这一个地方有这个特殊要求，以后我们再配置Filter还是可以正常写“/*”。 -->
    <!-- 方式二：配置“*.扩展名”，表示匹配整个Web应用范围内部分请求 -->
    <url-pattern>/</url-pattern>
</servlet-mapping>
```



创建控制器，为了能被mvc识别为处理网络请求的控制器（handler），要使用Controller。

一个控制器，负责配置 url映射 与 逻辑处理函数。

```java
@Controller
public class Demo01HelloHandler {
    // @RequestMapping注解在请求地址和Java方法之间建立映射关系
    @RequestMapping("/")
    public String showPortal() {
        return "portal"; // 框架会为我们自动拼接路径 这里表示返回 WEB-INF/templates/portal.html文件
    }
}
```

##  @RequestMapping注解

用于匹配 url 路径 

```java
@RequestMapping("/fruit/*") // 模糊匹配 
@RequestMapping("/fruit/apple") // 精确匹配 
```



在类上和函数上分别使用，用于拼接 

```java
@RequestMapping("/hollis/")
@Controller
public class DemoHandler {

    @GetMapping("/portal") // hollis/portal 真实路径
    public String portal(){
        return "portal";
    }

```



请求方式，GET/POST/DELETE/PUT等 

```java
@RequestMapping(value = "/emp", method = RequestMethod.GET)  // get

// 等效于以下简写 
@GetMapping("/emp")
```

****

**mvc:view-controller**

sping中的一个配置项，用于代替仅仅返回模板的视图函数。

例子:  匹配 `/index.html`，并返回 portal 模板

```java
<mvc:view-controller path="/index.html" view-name="portal"/>
```

它等效于 

```java
@RequestMapping("/index.html")
public String redirectCommand() {
    
    return "portal";
}
```





## 注解驱动和放行

spring 配置文件中加入以下两行：

1. 允许注解驱动 ，即`@RequestMapping`等配置的handler
2. 允许放行没有被requestMapping配置的url，常用于静态资源的请求 。因为静态资源请求在逻辑上，和所谓的逻辑视图 不相关。 

```xml
<mvc:annotation-driven/>
<mvc:default-servlet-handler/>
```





## 页面跳转控制



转发指令 

```java
@RequestMapping("/test/forward/command")
public String forwardCommand() {
    
    // 需求：要转发前往的目标地址不在视图前缀指定的范围内，
    // 通过返回逻辑视图、拼接前缀后缀得到的物理视图无法达到目标地址
    
    // 转发到指定的地址：
    return "forward:/outter.html";
}
```

重定向指令 

```java
@RequestMapping("/test/redirect/command")
public String redirectCommand() {
    
    // 重定向到指定的地址：
    // 框架会自动增加 contextPath 后：/contextPath/outter.html
    return "redirect:/outter.html";
}
```



## 获取数据

### @RequestParam

用于

1. 获取GET方式请求的参数，即`?xx=xxx`这种形式的参数。
2. 以表单形式post提交的数据  

基本使用方法

```java
@RequestMapping("/hollis")
public String oneNameOneValue(
    	// 这里填写url中的参数名 /hollis?userName=jhk 
        @RequestParam("userName") String userName 
) {
    
}
```

参数的可能类型包括：

* 简单字符串： `@RequestParam("userName") String userName` ，直接接收

* 列表：如多选框，` @RequestParam("team") List<String> teamList` ，更改实际接收变量类型即可

* 实体类：post表单的字段对应了一个实体类属性，那么不需要注解，直接用对应的实体类接收，该实体类要提供set方法。 

  提交表单

  ```html
  <form action="emp/save" method="post">
      姓名：<input type="text" name="empName"/><br/>
      年龄：<input type="text" name="empAge"/><br/>
      工资：<input type="text" name="empSalary"/><br/>
      <input type="submit" value="保存"/>
  </form>
  ```

  接收数据

  ```java
  @RequestMapping("/param/form/to/entity")
  public String formToEntity(
          // SpringMVC 会自动调用实体类中的 setXxx() 注入请求参数
          Employee employee) {
  }
  ```

  

该注解支持额外设置 ，如 

```java
// 是否必须 默认值
@RequestParam(value = "userName", required = false, defaultValue = "missing")
```



post提交过程中，数据乱码问题，可以额外配置一个用于字符集处理的过滤器。该过滤器顺序要放在所有过滤器首位

```xml

<!-- 配置过滤器解决 POST 请求的字符乱码问题 -->
<filter>
    <filter-name>CharacterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    
    <!-- encoding参数指定要使用的字符集名称 -->
    <init-param>
        <param-name>encoding</param-name>
        <param-value>UTF-8</param-value>
    </init-param>
    
    <!-- 请求强制编码 -->
    <init-param>
        <param-name>forceRequestEncoding</param-name>
        <param-value>true</param-value>
    </init-param>
        
    <!-- 响应强制编码 -->
    <init-param>
        <param-name>forceResponseEncoding</param-name>
        <param-value>true</param-value>
    </init-param>
</filter>
<filter-mapping>
    <filter-name>CharacterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```





### @PathVariable

url路径本身的一部分，就是作为参数。常见于restful设计的url，例如`/emp/20` 中的20就表示id。 

使用注解` @PathVariable`来获取这部分url

```java

// {}包裹变量名 
@RequestMapping("/emp/{empName}/{empAge}/{empSalary}")
public String queryEmp(
        @PathVariable("empName") String empName, // @PathVariable("url中的变量名")
        @PathVariable("empAge") Integer empAge,
        @PathVariable("empSalary") Double empSalary
) {
    
}
```



restful接口设计风格，简言之，就是让url本身保持简洁和可读性，也不建议使用`？`方式来携带参数，url本身具备这种语义，CRUD操作也使用对应的http协议的method来代替。以下是一个restful设计风格的例子 

查询、删除、修改会带上id，而新增则无，url的字面含义上，表示一个资源。 

| 操作             | 传统风格                | REST 风格                              |
| ---------------- | ----------------------- | -------------------------------------- |
| 保存             | /CRUD/saveEmp           | URL 地址：/CRUD/emp 请求方式：POST     |
| 删除             | /CRUD/removeEmp?empId=2 | URL 地址：/CRUD/emp/2 请求方式：DELETE |
| 更新             | /CRUD/updateEmp         | URL 地址：/CRUD/emp 请求方式：PUT      |
| 查询（表单回显） | /CRUD/editEmp?empId=2   | URL 地址：/CRUD/emp/2 请求方式：GET    |



### @RequestHeader

获取请求头的数据，即header部分。 

用法 

```java
@RequestMapping("/request/header")
public String getRequestHeader(
    
        // 使用 @RequestHeader 注解获取请求消息头信息
        // name 或 value 属性：指定请求消息头名称
        // defaultValue 属性：设置默认值
        @RequestHeader(name = "Accept", defaultValue = "missing") String accept
) {
    
    logger.debug("accept = " +accept);
    
    return "target";
}
```

### @CookieValue

获取cookie部分的数据

```java
@RequestMapping("/request/cookie")
public String getCookie(
    
        // 使用 @CookieValue 注解获取指定名称的 Cookie 数据
        // name 或 value 属性：指定Cookie 名称
        // defaultValue 属性：设置默认值
        @CookieValue(value = "JSESSIONID", defaultValue = "missing") String cookieValue,
    
        // 形参位置声明 HttpSession 类型的参数即可获取 HttpSession 对象
        HttpSession session
) {
    
    logger.debug("cookieValue = " + cookieValue);
    
    return "target";
}
```

## 获取servlet相关对象

包括 reques、response 、session、sevletContext，除了最后一个，前三个都可以在视图函数的形参中获取。

用法如下 

```java

@RequestMapping("/original/api/direct")
public String getOriginalAPIDirect(
        // 有需要使用的 Servlet API 直接在形参位置声明即可。
        HttpServletRequest request,
        HttpServletResponse response,
        HttpSession session
) {
    
    return "target";
}
```

sevletContext 获取:

通过session获取 

```java
@RequestMapping("/original/servlet/context/first/way")
public String originalServletContextFirstWay(HttpSession session) {
    
    // 获取ServletContext对象的方法一：通过HttpSession对象获取
    ServletContext servletContext = session.getServletContext();
    logger.debug(servletContext.toString());
    
    return "target";
}
```

通过IOC容器获取 

```java
// 获取ServletContext对象的方法二：从 IOC 容器中直接注入
@Autowired
private ServletContext servletContext;
    
@RequestMapping("/original/servlet/context/second/way")
public String originalServletContextSecondWay() {
    
    logger.debug(this.servletContext.toString());
    
    return "target";
}
```

两者的关系如下 

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220720193721438.png" alt="image-20220720193721438" style="zoom:67%;" />

## 属性域

### 请求域

即设置request 的参数，可以用于转发或者thymeleaf的模板。



通过model 

```java
@RequestMapping("/attr/request/model")
public String testAttrRequestModel( 
        // 在形参位置声明Model类型变量，用于存储模型数据
        Model model) {
    
    // SpringMVC 会帮我们把模型数据存入请求域
    // 存入请求域这个动作也被称为暴露到请求域
    model.addAttribute("requestScopeMessageModel","i am very happy[model]");
    
    return "target";
}
```

或者使用原生的request对象 

```java
@RequestMapping("/attr/request/original")
public String testAttrOriginalRequest(
    
        // 拿到原生对象，就可以调用原生方法执行各种操作
        HttpServletRequest request) {
    
    request.setAttribute("requestScopeMessageOriginal", "i am very happy[original]");
    
    return "target";
}
```





### 会话域

调用原生的session对象 

```java
@RequestMapping("/attr/session")
public String attrSession(
        // 使用会话域最简单直接的办法就是使用原生的 HttpSession 对象
        HttpSession session) {
    
    session.setAttribute("sessionScopeMessage", "i am haha ...");
    
    return "target";
}
```

### 应用域

应用域指的是servletContext的上下文 

```java
@Autowired
private ServletContext servletContext;

@RequestMapping("/attr/application")
public String attrApplication() {
    
    servletContext.setAttribute("appScopeMsg", "i am hungry...");
    
    return "target";
}
```



## ajax 

前后端分离下的后端数据返回逻辑。

### 普通文本

返回普通文本 ，使用注解 

```java
@ResponseBody // 注解表示 return 后跟着的是 普通文本 告知框架不要 视作模板
@RequestMapping("/ajax/experiment/one")
public String experimentOne(
) {
 
    // 服务器端给Ajax程序的响应数据通过handler方法的返回值提供
    return "message from handler as response[来自服务器的问候]";
}
```

如果类中的每一个方法都是返回 普通文本，则可以使用`@RestController`代替Controller，它是Controller和 ResponseBody 的结合。

### json

导入相关依赖

```xml
<!-- https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-databind -->
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-core</artifactId>
    <version>2.11.3</version>
</dependency>
```



处理post请求的json数据：requestBody注解可以取出请求体数据（整体作为一个字符串）

前端请求部分假设如下 

```js
"experimentTwo":function () {
 
    axios({
        "method":"post",
        "url":"ajax/experiment/two",
 
        // data属性中指定一个 JSON 数据作为请求体
        "data":{
            "stuId": 55,
            "stuName": "tom",
            "subjectList": [
                {
                    "subjectName": "java",
                    "subjectScore": 50.55
                },
                {
                    "subjectName": "php",
                    "subjectScore": 30.26
                }
            ],
            "teacherMap": {
                "one": {
                    "teacherName":"tom",
                    "teacherAge":23
                },
                "two": {
                    "teacherName":"jerry",
                    "teacherAge":31
                },
            },
            "school": {
                "schoolId": 23,
                "schoolName": "atguigu"
            }
        }
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
    });
 
}
```

后端视图函数： 演示了如何 处理json字符串形式的数据请求 和 返回 json字符串形式的 数据 ，设计到实体类的转换

```java
 @ResponseBody
    @RequestMapping(value = "/servlet")
    public String redirect(
            @RequestBody String data,
            HttpServletRequest request,
            HttpServletResponse response,
            HttpSession session
    ){
        System.out.println(data); // json 字符串
        Employee emp = JSON.parseObject(data,Employee.class); // 转为实体类
        System.out.println(emp);

        return JSON.toJSONString(emp); // 实体类 转 字符串 


    }
```



## 拦截器

拦截器的作用和servlet自带的过滤器类似，但是前者仅仅作用在spring mvc框架下，后者的范围是基于tomcat部署下的整个web应用。 



### 实现 

实现接口 

```java
public class Process01Interceptor implements HandlerInterceptor {
 
    Logger logger = LoggerFactory.getLogger(this.getClass());
 
    // 在处理请求的目标 handler 方法前执行
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        
        logger.debug("Process01Interceptor preHandle方法");
         
        // 返回true：放行
        // 返回false：不放行
        return true;
    }
 
    // 在目标 handler 方法之后，渲染视图之前
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
 
        logger.debug("Process01Interceptor postHandle方法");
        
    }
 
    // 渲染视图之后执行
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        
        logger.debug("Process01Interceptor afterCompletion方法");
        
    }
}
```

涉及到拦截器具备的几个函数以及它们的执行顺序（按照从上到下）：

- preHandle() 方法
- 目标 handler 方法
- postHandle() 方法
- 渲染视图
- afterCompletion() 方法



### 注册 

在spring配置文件中配置 

全部拦截 

```xml
<!-- 注册拦截器 -->
<mvc:interceptors>
    
    <!-- 直接通过内部 bean 配置的拦截器默认拦截全部请求（SpringMVC 范围内） -->
    <bean class="com.atguigu.mvc.interceptor.Process01Interceptor"/>
</mvc:interceptors>
```



拦截部分路径：

精确拦截 

```xml
<!-- 具体配置拦截器可以指定拦截的请求地址 -->
<mvc:interceptor>
    <!-- 精确匹配 -->
    <mvc:mapping path="/common/request/one"/>
    <bean class="com.atguigu.mvc.interceptor.Process03Interceptor"/>
</mvc:interceptor>
```

模糊匹配： * 表示匹配一层， ** 表示匹配多层， `mvc:exclude-mapping` 表示拦截白名单 

```xml
<mvc:interceptor>
    <!-- /*匹配路径中的一层 -->
    <mvc:mapping path="/common/request/*"/>
     <!-- 使用 mvc:exclude-mapping 标签配置不拦截的地址 -->
     <mvc:exclude-mapping path="/common/request/two/bbb"/>
    <bean class="com.atguigu.mvc.interceptor.Process04Interceptor"/>
</mvc:interceptor>
```



当有多个拦截器时，拦截器之间是彼此嵌套的，而不是串行 ，所以它们的执行顺序如下 

- reHandle()方法：和配置的顺序一样
- 目标handler方法
- postHandle()方法：和配置的顺序相反
- 渲染视图
- afterCompletion()方法：和配置的顺序相反





## 自定义类型转换器 

前端提交表单时，数据本质上是字符串。mvc 框架在将表单字段封装成实体类时，会为进类型转换，例如常见的 字符串 转 整型。 

如果有必要，可以自定义类型转换器，通过实现接口 ，`org.springframework.core.convert.converter.Converter<S,T>`，s表示源数据类型，一般都是字符串，t表示你的目标转换类型。 



示例：

```java
public class AddressConverter implements Converter<String, Address> {
    @Override
    public Address convert(String source) {
  
        // 1.按照约定的规则拆分源字符串
        String[] split = source.split(",");
         
        String province = split[0];
        String city = split[1];
        String street = split[2];
 
        // 2.根据拆分结果创建 Address 对象
        Address address = new Address(province, city, street);
         
        // 3.返回转换得到的对象
        return address;
    }
}
```

在配置中自定义类型转换器 

```xml

<!-- 在 mvc:annotation-driven 中注册 FormattingConversionServiceFactoryBean -->
<mvc:annotation-driven conversion-service="formattingConversionService"/>
 
<!-- 在 FormattingConversionServiceFactoryBean 中注册自定义类型转换器 -->
<bean id="formattingConversionService"
      class="org.springframework.format.support.FormattingConversionServiceFactoryBean">

    <!-- 在 converters 属性中指定自定义类型转换器 -->
    <property name="converters">
        <set>
            <bean class="com.atguigu.mvc.converter.AddressConverter"/>
        </set>
    </property>
 
</bean>
```



## 数据校验 

通过注解的形式对前端提交的数据进行简单的校验。 

JSR 303 是 Java 为 Bean 数据合法性校验提供的标准框架，它已经包含在 JavaEE 6.0 标准中。

| 注解                       | 规则                                           |
| -------------------------- | ---------------------------------------------- |
| @Null                      | 标注值必须为 null                              |
| @NotNull                   | 标注值不可为 null                              |
| @AssertTrue                | 标注值必须为 true                              |
| @AssertFalse               | 标注值必须为 false                             |
| @Min(value)                | 标注值必须大于或等于 value                     |
| @Max(value)                | 标注值必须小于或等于 value                     |
| @DecimalMin(value)         | 标注值必须大于或等于 value                     |
| @DecimalMax(value)         | 标注值必须小于或等于 value                     |
| @Size(max,min)             | 标注值大小必须在 max 和 min 限定的范围内       |
| @Digits(integer,fratction) | 标注值值必须是一个数字，且必须在可接受的范围内 |
| @Past                      | 标注值只能用于日期型，且必须是过去的日期       |
| @Future                    | 标注值只能用于日期型，且必须是将来的日期       |
| @Pattern(value)            | 标注值必须符合指定的正则表达式                 |



配置 mvc:annotation-driven 后，SpringMVC 会默认装配好一个 LocalValidatorFactoryBean，通过**在处理方法的入参上标注 @Validated 注解**即可让 SpringMVC 在完成数据绑定后执行数据校验的工作。



示例：

导入依赖 

```xml

<!-- https://mvnrepository.com/artifact/org.hibernate.validator/hibernate-validator -->
<dependency>
    <groupId>org.hibernate.validator</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>6.2.0.Final</version>
</dependency>
<!-- https://mvnrepository.com/artifact/org.hibernate.validator/hibernate-validator-annotation-processor -->
<dependency>
    <groupId>org.hibernate.validator</groupId>
    <artifactId>hibernate-validator-annotation-processor</artifactId>
    <version>6.2.0.Final</version>
</dependency>
```

handler方法中 对 需要验证的实体类 添加注解 

```java
@RequestMapping("/save/president")
public String savePresident(@Validated President president,
                            BindingResult bindingResult) {
 	//  BindingResult 用于查看 数据验证是否通过
     if (bindingResult.hasErrors()) { 
        return "error";
    }
     
    logger.debug(president.getEmail());
    return "target";
}
```

实体类内部，对需要的字段添加验证注解 

```java
// 字符串长度：[3,6]
@Size(min = 3, max = 6)

// 字符串必须满足Email格式
@Email
private String email;
```

## 异常映射

将异常也看做可以被视图处理的触发者， 便于统一管理一个项目中的异常处理逻辑。



创建处理异常的类，并将该类添加到扫描包中 

```java
// 异常处理器类需要使用 @ControllerAdvice 注解标记
@ControllerAdvice
public class MyExceptionHandler {
    
    // 声明异常处理的方法 
    // @ExceptionHandler注解：标记异常处理方法
	// value属性：指定匹配的异常类型
	// 异常类型的形参：SpringMVC 捕获到的异常对象
    @ExceptionHandler(value = NullPointerException.class)
    public String resolveNullPointerException(Exception e, Model model) {
        // 我们可以自己手动将异常对象存入模型
        model.addAttribute("atguiguException", e);
        // 返回逻辑视图名称
        return "error-nullpointer";
    }
    
}
```

## 文件上传下载

### 上传

前端请求方式必须是post，且编码方式为` multipart/form-data`，表示利用二进制编码 

```html
<form th:action="@{/atguigu/upload}" method="post" 
      enctype="multipart/form-data">
    <input type="file" name="picture" />
    <button type="submit">上传头像</button>
</form>
```



mvc 导入依赖 

```xml
<!-- https://mvnrepository.com/artifact/commons-fileupload/commons-fileupload -->
<dependency>
    <groupId>commons-fileupload</groupId>
    <artifactId>commons-fileupload</artifactId>
    <version>1.3.1</version>
</dependency>
```

配置文件中 设置解码字符 

```xml

<bean id="multipartResolver" 
      class="org.springframework.web.multipart.commons.CommonsMultipartResolver">
    
    <!-- 由于上传文件的表单请求体编码方式是 multipart/form-data 格式，所以要在解析器中指定字符集 -->
    <property name="defaultEncoding" value="UTF-8"/>
    
</bean>
```

handler 用于接收数据

```java
@RequestMapping("/atguigu/upload")
public String doUpload(
        @RequestParam("userName") String userName,
        @RequestParam("picture") MultipartFile picture  // 该类型形参 就表示 上传的文件 
        ) {
 
    logger.debug("userName = " + userName);
    logger.debug("原始文件名：" + picture.getOriginalFilename());
 
    return "target";
}
```

MultipartFile 接口 中含有对文件描述信息的若干方法：

示例如下

```java
String inputName = picture.getName();
logger.debug("文件上传表单项的 name 属性值：" + inputName);

// 获取这个数据通常都是为了获取文件本身的扩展名
String originalFilename = picture.getOriginalFilename();
logger.debug("文件在用户本地原始的文件名：" + originalFilename);

String contentType = picture.getContentType();
logger.debug("文件的内容类型：" + contentType);

boolean empty = picture.isEmpty();
logger.debug("文件是否为空：" + empty);

long size = picture.getSize();
logger.debug("文件大小：" + size);

byte[] bytes = picture.getBytes();
logger.debug("文件二进制数据的字节数组：" + Arrays.asList(bytes));

InputStream inputStream = picture.getInputStream();
logger.debug("读取文件数据的输入流对象：" + inputStream);

Resource resource = picture.getResource();
logger.debug("代表当前 MultiPartFile 对象的资源对象" + resource);
```





对于前端上传的文件，后端有如下处理方式 

1. 本地转存：实现简单，但是存储的文件变多以后，会拖慢tomcat的运行速度。且项目重新部署后，原先上传的文件（webapp下的）会被清空，不推荐
2. 文件服务器：上传到专门的文件对象存储服务器上 ‘



关于本地转存的例子 。核心要点是：

1. 通过webapp下的虚拟路径来获取在部署时候的真实路径 
2. 通过uuid重命名文件 

```java
……
 
// 1、准备好保存文件的目标目录
// 要根据『不会变的虚拟路径』作为基准动态获取『跨平台的物理路径』
// ③虚拟路径：浏览器通过 Tomcat 服务器访问 Web 应用中的资源时使用的路径
String destFileFolderVirtualPath = "/head-picture";
 
// ④调用 ServletContext 对象的方法将虚拟路径转换为真实物理路径
String destFileFolderRealPath = servletContext.getRealPath(destFileFolderVirtualPath);
 
// 2、生成保存文件的文件名 
String generatedFileName = UUID.randomUUID().toString().replace("-","");
 
// 根据 originalFilename 获取文件的扩展名 找到 . 的位置 
String fileExtname = originalFilename.substring(originalFilename.lastIndexOf("."));
 
// ⑤拼装起来就是我们生成的整体文件名
String destFileName = generatedFileName + "" + fileExtname;
 
// 3、拼接保存文件的路径，由两部分组成
String destFilePath = destFileFolderRealPath + "/" + destFileName;
 
// 4、创建 File 对象，对应文件具体保存的位置
File destFile = new File(destFilePath);
 
// 5、执行转存
picture.transferTo(destFile); // picture就是 MultipartFile  接口 
```



### 下载

下载的demo 

```java
@Autowired
private ServletContext servletContext;

@RequestMapping("/download/file")  // 假设这是下载链接 
public ResponseEntity<byte[]> downloadFile() {

    // 1.获取要下载的文件的输入流对象 以 Web 应用根目录为基准
    InputStream inputStream = servletContext.getResourceAsStream("/images/mi.jpg");

    try {
        int len = inputStream.available(); // 文件大小
        
        byte[] buffer = new byte[len]; // 字节数组 
        inputStream.read(buffer);

        // 封装响应消息头
        MultiValueMap responseHeaderMap = new HttpHeaders();
        responseHeaderMap.add("Content-Disposition", "attachment; filename=mi.jpg");
		
        // 返回 
        ResponseEntity<byte[]> responseEntity = new ResponseEntity<>(buffer, responseHeaderMap, HttpStatus.OK);
        return responseEntity;
    } catch (IOException e) {
        e.printStackTrace();
    } finally {
        if (inputStream != null) {
            try {
                inputStream.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

    }

    return null;
}
```



## 框架整合 

### spring 和 mybatis整合

依赖框架： mybatis-spring  ， [官方介绍](http://mybatis.org/spring/zh/index.html) 

该框架负责整合，spring和mybatis各自需要的包，仍然要引入

```xml
<!-- https://mvnrepository.com/artifact/org.mybatis/mybatis-spring -->
<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis-spring</artifactId>
    <version>2.0.6</version>
</dependency>
```

整合之下的配置文件结构如下：

![image-20220724145519897](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220724145519897.png)

他们的作用为：

* spring-persist：容器相关，指定数据源DataSource、配置SqlSessionFactoryBean、**扫描mappers接口类** 
* mybatis-config： mybatis的相关配置，仅仅保留一些必要的设置 
* jbbc.properties：数据库连接相关信息  



各自的详细信息内容

jbbc.properties 文件

```properties
jdbc.user=root
jdbc.password=atguigu
jdbc.url=jdbc:mysql://192.168.198.100:3306/mybatis-example
jdbc.driver=com.mysql.jdbc.Driver
```

mybatis-config.xml ：对比直接使用[mybatis框架](#Mybatis)可以发现，**mappers.xml文件的装备这些步骤在spring框架整合中，都交给了bean容器的spring配置文件处理**

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>

    <!-- Mybatis全局配置 -->
    <settings>
        <!-- 将数据库表字段映射到驼峰式命名的Java实体类属性中 -->
        <!-- 数据库表字段格式：单词_单词 -->
        <!-- Java实体类属性：首字母小写的驼峰式命名 -->
        <setting name="mapUnderscoreToCamelCase" value="true"/>
    </settings>

</configuration>
```

spring-persist.xml ： 为了使用容器的思想，所以要在spring配置文件中，扫描mappers接口所在包 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd http://www.springframework.org/schema/mvc https://www.springframework.org/schema/mvc/spring-mvc.xsd">


    <!-- 加载外部属性文件 -->
    <context:property-placeholder location="classpath:jdbc.properties"/>

    <!-- 配置数据源  用于获取connection-->
    <bean id="druidDataSource" class="com.alibaba.druid.pool.DruidDataSource">
        <property name="username" value="${jdbc.user}"/>
        <property name="password" value="${jdbc.password}"/>
        <property name="driverClassName" value="${jdbc.driver}"/>
        <property name="url" value="${jdbc.url}"/>
    </bean>

    <!-- 配置 SqlSessionFactoryBean -->
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">

        <!-- 指定 Mybatis 全局配置文件位置 -->
        <property name="configLocation" value="classpath:mybatis-config.xml"/>

        <!-- 指定 Mapper 配置文件位置 -->
        <property name="mapperLocations" value="classpath:mappers/*Mapper.xml"/>

        <!-- 装配数据源 -->
        <property name="dataSource" ref="druidDataSource"/>

    </bean>

    <!-- 配置 Mapper 接口类型的bean的扫描器 -->
    <bean id="mapperScannerConfigurer" class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="basePackage" value="com.hollis.mappers"/>
    </bean>
    

</beans>
```

在配置mapper接口扫描器时，可以简写如下：

```xml
<mybatis-spring:scan base-package="com.hollis.mappers"/>
```

`*Mapper.xml` 文件和Mapper接口类等，依旧遵循mybatis框架的那一套规则。结构和内容如下：

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220724150623050.png" alt="image-20220724150623050" style="zoom:67%;" />



Mapper接口示例：

```java
public interface EmpMapper {
    List<Employee> selectAll();
}
```

与其对应的empMapper.xml 文件 

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.hollis.mappers.EmpMapper">

    <!-- List<Emp> selectAll(); -->
    <select id="selectAll" resultType="com.hollis.Entity.Employee">
        select emp_id,emp_name,emp_salary from t_emp
    </select>

</mapper>
```



### spring 和 spring mvc 整合

当项目中整合多个框架时，例如 spring mvc 、mybatis等，全部配置写在 一个 文件中会显得冗长，需要配置文件的分离。

分离的标准按照每个框架的功能分开：

* 请求url相关：交给DispatcherServlet处理，作为一个单独的 配置文件
* 持久化数据相关：交给mybatis、spring处理，作为一个单独的配置文件 

这就需要使用 `ContextLoaderListener` 。 



1. 创建各自的配置文件 ，mvc表示针对mvc相关的配置文件，persist表示持久层相关的配置文件

   ![image-20220724101946856](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220724101946856.png)

2. 在web.xml配置文件中，创建 ContextLoaderListener

   ```xml
   <!-- 通过全局初始化参数指定 Spring 配置文件的位置 -->
   <context-param>
       <param-name>contextConfigLocation</param-name>
       <param-value>classpath:spring-persist.xml</param-value>
   </context-param>
    
   <listener>
       <!-- 指定全类名，配置监听器 -->
       <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
   </listener>
   ```

3. spring-mvc配置文件中，修改为 仅仅扫描handler包 

   ```xml
   <context:component-scan base-package="com.hollis.handlers"/>
   ```

   

这样一来，在整个项目中，会存在两个ioc容器。**他们的关系是父子关系**，原因如下：

- ContextLoaderListener：初始化时如果检查到有已经存在的根级别 IOC 容器，那么会抛出异常。
- DispatcherServlet：初始化时先检查当前环境下是否存在已经创建好的 IOC 容器。
  - 如果有：则将已存在的这个 IOC 容器设置为自己的父容器
  - 如果没有：则将自己设置为 root 级别的 IOC 容器



两个容器如果扫描的包有重复：

1. 在创建bean对象的时候就会重复创建，浪费空间，所以建议是各自扫描不同的组件包。
2. 尽管会创建两个bean对象，但是它们不完全一样，会有类似二义性的问题。因为它们属于两个不同的容器空间，子容器如果有，就会优先获取子容器的 

所以，正如为什么要分离配置文件一样，**扫描包的侧重点也应该不一样**，mvc配置文件扫描handlers组件包，而persist配置文件则扫描service和dao组件包。**当它们扫描的包是彼此分离的时候，访问的原则是：子容器可以访问父容器的bean，反之，不行**。因为子容器里存在一个`getParent()`方法，可以获取到对父容器的引用。 



