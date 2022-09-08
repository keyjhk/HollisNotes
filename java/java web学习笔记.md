[toc]



# idea

## tomcat 配置 

server 选项卡：配置浏览服务 



on update aciton：当项目修改时，触发的操作

* `-Update resources`：如果发现有更新，而且更新的是资源文件（.jsp，.xml等，不包括java文件） ,就会立刻生
* `-Update classes and resources`：如果发现有更新，这个是同时包含java文件和资源文件的，就会立刻生效;
  在运行模式下，修改java文件时不会立刻生效的。而debug模式下，修改java文件时可以立刻生效的。
* `-Redeploy `：重新打成war包项目部署到服务器，不重启服务器;
* `-Restart` : 重启tomcat服务器

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220521114722315.png" alt="image-20220521114722315" style="zoom:67%;" />



facet：项目描述 。明确web.xml和webapp所在路径，前者作为项目的配置文件，后者作为资源存放路径，未来将要被打包部署到Tomcat的`webapps`目录下。 

![image-20220628110945893](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628110945893.png)





deployment 选项卡 ：有两点值得注意。

一是打包方式。war包和exploded的区别，就是前者是压缩的，后者是未压缩的，相当于直接复制了webapp目录过去。未压缩的情况下，便于修改文件夹，立刻生效。

![image-20220628111353115](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628111353115.png)

部署的上下文路径名：用来标识和访问本web项目的url前缀。 

![image-20220628111635688](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628111635688.png)

context名自然也是打包到tomcat时的包名 

![image-20220628111557825](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220628111557825.png)



## 项目目录结构

工程中的源码分为两类：

1.  `src`文件夹下的源码，项目编译后输出到`WEB-INF/classes`下，得到class文件
2. `lib`库文件，需要放到`WEB-INF`下，部署项目后，tomcat服务器才可以找到 



![image-20220521141658954](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220521141658954.png)



src 为java源码，从作用上可以分为几个文件夹：

* bean：类似django的模型类，**一般一个表对应一个模型** 
* dao： data access object，**用于封装对象访问数据库的sql语句**，完成CURD操作  
* service ：调用DAO层的接口，**实现业务逻辑**相关的代码 
* servlet： 控制层，**处理url访问**，渲染模板、设置请求域等等。 
* utils：其他的工具类





编译后的目录结构：

![image-20220702091415040](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220702091415040.png)



## 封装层次

从层级上来说，bean、dao 是封装数据库的，service是封装对象方法的，使数据库的实体对象展现出类的特征，例如用类方法来实现增删改查，servlet则是处理请求的。

> Servlet ==> Service ==> DAO



bean示例 ：**保留最基本的属性和访问方法（getter/setter）** 

```java
public class User {
    // 对应数据表的列 和列名可以不同 
    private int id;
    private String username;
    private String nickname;
    
    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", nickname='" + nickname + '\'' +
                '}';
    }
	
    // get 和 set 方法
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getNickname() {
        return nickname;
    }

    public void setNickname(String nickname) {
        this.nickname = nickname;
    }
}
```



dao 示例： 封装了user表的CURD操作 

```java
/* 
userDAO 的主要目的是封装 user对象 访问数据库的一些操作 
如 getAllUsers 是查询表所有数据 注意他们返回的数据类型 

getBeanList 、 getBean 等方法则是更进一步的数据库底层操作封装
如创建数据库连接、处理sql语句等 ，也就是BaseDAO 的方法 
BaseDAO 解耦了 sql语句内容 和 处理 
*/

public class UserDAO extends BaseDAO<User>{

    public List<User> getAllUsers(){
        String sql = "select * from user";
        return getBeanList(User.class,sql);
    }

    public User getUserByID(String id){
        String sql = "select * from user where id=?";
        return getBean(User.class,sql,id);
    }

    public int deleteUser(String id){
        return update("delete from user where id=?",id);
    }

    public int addUser(String username,String nickname){
        return update("insert into user(username,nickname) values(?,?)",username,nickname);
    }
}
```



service  示例：注册的逻辑，

```java
public class UserServiceImpl implements UserService{
    private UserDao userDao = new UserDaoImpl(); // 得到它的dao对象 
    @Override
    public void doRegister(User user) throws Exception {
        // 查询用户是否存在 
        // 否则创建它
    }
}
```





# servlet

servlet ，**tomcat为java程序提供的一个接口，用于处理动态资源，响应请求并返回资源**。 

![image-20220518112414447](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220518112414447.png)

 





## 创建servlet

步骤：

1. 继承`HttpServlet`
2. 配置url 映射 ，使用 注解 或者 配置文件`web.xml`

```java
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;


// 创建了url映射 ，访问/webapp/hollis/ 时，交给这个servelet处理
@WebServlet(name = "hollis") // 映射url , /webapp/hollis/ 
public class HollisServlet extends HttpServlet {
	// 创建一个名为 HollisServlet 的 servlet类 
    // GET 请求处理 
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // 设置编码
        request.setCharacterEncoding("UTF-8");
		response.setContentType("text/html;charset=UTF-8");
        
        PrintWriter out = response.getWriter();
        out.write("hello hollis");
    }

}
```



使用idea创建servlet

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220519101414517.png" alt="image-20220519101414517" style="zoom:80%;" />



## url映射

当url被访问时，如何交给对应的serlet处理。

完整的url路径格式：项目部署名+url，`https://host:port/webapp/url_pattern` 

webapp 是部署时，为项目起的别名 。该别名被打包成war包，丢到tomcat下 

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220519102734591.png" alt="image-20220519102734591" style="zoom:67%;" />





方法1：注解

```java
// 如上例 
@WebServlet(name = "hollis") // 映射url , /webapp/hollis/ 
public class HollisServlet extends HttpServlet {
}
```



方法2：配置 `web.xml`中配置 两个属性 `servlet`、`servlet-mapping` 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

    <!-- servlet的路径和别名 -->
    <servlet>
        <!-- 创建的简短名称 -->
        <servlet-name>hollisServlet</servlet-name>
        <!-- 配置Servlet的全类名 -->
        <servlet-class>com.example.demo.HollisServlet</servlet-class>
    </servlet>

    <!-- 处理 servlet和url的映射 -->
    <servlet-mapping>
        <servlet-name>hollisServlet</servlet-name>
        <url-pattern>/hollis</url-pattern>
    </servlet-mapping>

</web-app>
```





当项目部署时，java会对工程文件的目录进行重组，`webapp`下的资源目录相当于根目录



![image-20220519110358116](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220519110358116.png)



## 生命周期

servelet的实例创建销毁流程 

* init方法：实例第一次创建的时候执行，常用于比较耗时的操作，如文件加载 

* service： 每次请求发生，无论method是什么，均执行。
* destroy：实例对象销毁之前执行，用于资源回收、释放、关闭等等操作



```java
public class HollisServlet extends HttpServlet {
    @Override
    public void init() throws ServletException {
        super.init();
    }

    @Override
    public void destroy() {
        super.destroy();
    }

    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 父类的 HttpServlet 在service方法里完成了 按照method分发函数的 工作 
        // 根据 请求方法 执行对应 函数  
        super.service(req, resp);
    }

}
```

## 作用域

### servelet作用域

配置`init-param`属性，对于该servelet的访问均可见

```xml
<!-- 配置Servlet本身 -->
<servlet>
    <!-- 全类名太长，给Servlet设置一个简短名称 -->
    <servlet-name>HelloServlet</servlet-name>

    <!-- 配置Servlet的全类名 -->
    <servlet-class>com.atguigu.servlet.HelloServlet</servlet-class>

    <!-- 配置初始化参数 -->
    <init-param>
        <param-name>goodMan</param-name>
        <param-value>me</param-value>
    </init-param>

    <!-- 配置Servlet启动顺序 如果存在该属性就会提前创建 -->
    <load-on-startup>1</load-on-startup>
</servlet>
```



### context 全局作用域

`servlet context` 归属于整个项目，**所有`servlet`组件都可以访问该上下文变量，相当于全局作用域**。 



获取context对象 

```java
// 1. 直接调用 servlet 的接口
ServletContext ServletContext = getServletContext()
    
// 2. servletConfig 对象 
ServletContext ServletContext = servletConfig.getServletContext();

// 3. HttpServletRequest对象也实现了ServletConfig接口，所以也有getServletContext()方法
ServletContext ServletContext = request.getServletContext();    
```



全局的初始化参数的设置 有如下两种方式：

1. `web.xml` 配置 

   ```xml
   <context-param>
       <param-name>username</param-name>
       <param-value>hahahaha</param-value>
   </context-param>
   ```

2. 通过 context对象读取调用 

   ```java
   ServletContext servletContext = getServletContext()
   String username = servletContext.getInitParameter("username");
   System.out.println("在ServletDemo04中获取全局的初始化参数username=" + username);
   ```



全局参数 动态设置 ，即非初始化参数设置 

```java
servletContext.setAttribute("key",value) // 读
Object value = ServletContext.getAttribute("key"); // 写   
```





## request & response

### request

request，封装的HTTP请求对象

- getMethod()：获取请求方式  

- getContextPath()：获得当前应用上下文路径 ，这个上下文路径指的是部署时命名的webapp 

  <img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220521142044657.png" alt="image-20220521142044657" style="zoom:67%;" />

  ```java
  request.getContextPath() + "pages/index.html"; // 得到完整的路径 /bookstore/pages/index.html
  ```

  

- getRequestURI()：请求地址，省略了主机名    

- getRequestURL()：完整的请求地址，带主机名

- request.setCharacterEncoding("UTF-8") ： 设置编码格式



```java
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        PrintWriter out = response.getWriter();
        System.out.println("get 方法被执行");
        out.write("hello hollis");
		
        /*
        method: GET 
        url: http://localhost:8080/demo/hollis 
        uri: /demo/hollis
        service方法被执行    
        */
        
        String method = request.getMethod();
        String url = request.getRequestURL().toString();
        String uri = request.getRequestURI();
        System.out.println(String.format("method: %s \nurl: %s \nuri: %s",method,url,uri));
    }

```





**HEADER** 

获取请求头的参数：`request.getHeader(String name)` 

```java
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    //根据请求头的name获取value
    //目标:获取name为user-agent的请求头的信息
    //user-agent请求头中包含的是客户端浏览器信息
    String header = request.getHeader("user-agent");
    System.out.println("获取的请求头agent为:" + header);
}
```



**PARAMS**

**获取请求参数** ，请求参数指的是附着在url后面的参数或者请求体的参数 

| 方法名                                           | 返回值类型            | 方法描述                                          |
| ------------------------------------------------ | --------------------- | ------------------------------------------------- |
| **request.getParameterMap()**                    | Map<String, String[]> | 获取当前请求的所有参数，以键值对的方式存储到Map中 |
| **request.getParameter("请求参数的名字")**       | String                | 根据一个参数名获取一个参数值                      |
| **request.getParameterValues("请求参数的名字")** | String []             | 根据一个参数名获取多个参数值                      |
| request.getParameterNames()                      | Enumeration<String>   | 获取当前请求的所有参数的参数名                    |



e.g. `GET http://localhost:8080/demo/hollis?season=spring` ，参数是 season 

```java
public void testGetParamter(HttpServletRequest request){
    	// map 获取参数集 
        Map<String,String[]> paramterMaps = request.getParameterMap();
        Set<String> keyset = paramterMaps.keySet();
        for(String key:keyset){
            String[] values = paramterMaps.get(key);
            System.out.println(key + "=" + Arrays.asList(values));
        }

        //  获取单个参数值
        String season = request.getParameter("season");
        System.out.println("season = " + season);

}
```





**请求转发**

请求转发： `request.getRequestDispatcher("路径").forward(request,response);` 

```java
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    System.out.println("ServletDemo01执行了...")
    //请求转发跳转到ServletDemo02
    request.getRequestDispatcher("/demo02").forward(request, response);
}
```





**请求域**

请求域中读写参数，对于该request生效 

* 往请求域中存入数据：`request.setAttribute(key,value)`
* 从请求域中取出数据：`request.getAttribute(key)` 

```java
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    System.out.println("ServletDemo01执行了...")
    String username = "aobama";

    //将username存储到request域对象中
    request.setAttribute("name",username);
    //请求转发跳转到ServletDemo02
    request.getRequestDispatcher("/demo02").forward(request, response);
}
```





### javaBean

可重用组件，**主要用于存储内存中的数据**，以及提供方法便于使用者获取数据。

**JavaBean的编写要求**

1. 类必须是公有的
2. 必须有无参构造函数
3. 属性私有，使用private修饰，针对所有属性，提供对应的set和get方法
4. 建议重写toString()方法，便于打印对象
5. 基本类型简写使用包装类型



模型类 

```java
public class User {
    private Integer id;
    private String username;

    public User() { // 无参构造
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                '}';
    }
}
```



使用javabean类代替Map类：

1. Map类虽然简单，但是不能直观地了解参数个数的多少，不方维护
2. javabean 类在传参时，编译阶段即可检查，而Map类在sql阶段可以检查 



bean使用，`BeanUtils.populate(map对象,JavaBean.class)` ， populate 方法会按照 属性名匹配的方式 把map对象转为 javabean对象 。

```java

Map<String,Object> m= new HashMap<>();
m.put("ULIId",12343);
m.put("CREATETIME",LocalDateTime.now());
m.put("userMoney",12343.32);

User u=new User();

BeanUtils.populate(u,m);
```

### response

封装响应对象 

```java
//设置编码格式 
response.setContentType("text/html;charset=UTF-8");
//1. 获取字符输出流
PrintWriter writer = response.getWriter();
//2. 输出内容
writer.write("hello world");
```



e.g. 返回文件

```java
public void testWriteFile(HttpServletRequest request, HttpServletResponse response) throws IOException {
    String fpath = getServletContext().getRealPath("statics/img/switch.png"); // 文件的真实路径
    System.out.println(fpath);
    
    // IO流读写文件
    FileInputStream fis = new FileInputStream(fpath);
    byte[] buffer = new byte[1024];
    int eof, len = 0;
    ServletOutputStream ots = response.getOutputStream();
    while ((len=fis.read(buffer)) != -1) {
        ots.write(buffer,0,len);
    }
    ots.close();
    fis.close();
}
```



**重定向**

```java
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    System.out.println("ServletDemo01执行了...")
        //请求转发跳转到ServletDemo02
        response.sendRedirect("/app/demo02");
}
```



重定向和请求转发：

1. 重定向会由浏览器发起新的请求，而请求转发不会发起新的请求（所以它可以使用请求域）
2. 重定向可以访问任意互联网资源，而请求转发只能访问本项目资源





## cookie & session

cookie 和 session 是保存会话状态的不同解决方案。cookie将数据保存在客户端，session将数据保存在服务端。

一次会话的生存周期一般始于浏览器初次创建连接，终于浏览器关闭，但是也可以额外设置。

### cookie

cookie以键值对的形式存储数据。**服务器返回响应时，会要求浏览器创建，而浏览器在发起请求时，会通过设置请求头的方式，携带上cookie。**

要求创建cookie时的响应头 

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220612182802693.png" alt="image-20220612182802693" style="zoom:67%;" />

浏览器携带cookie时的请求头 

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220612182819729.png" alt="image-20220612182819729" style="zoom:67%;" />





**Cookie 对象** 

* 创建 `new Cookie(String key, String Value)` ，会生成一个键值对 

* get 

  ```java
  cookie.getName() ; //返回cookie中设置的key
  cookie.getValue(); //返回cookie中设置的value
  ```

在servlet中应用cookie

```java
response.addCookie(cookie);  // 要求浏览器创建cookie
request.getCookies(); //得到所有的cookie对象 是一个数组 
```

e.g

```java
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    Cookie[] cookies = request.getCookies();
    // 遍历
    for (Cookie cookie : cookies) {
        //匹配cookie的name
        if (cookie.getName().equals("cookie-message")) {
            String value = cookie.getValue();
            System.out.println("在ServletDemo02中获取str的值为：" + value);
        }
    }
}
```





**cookie的时效** 默认就是一次会话的时间，浏览器关闭即消失，但这可以更改。`cookie.setMaxAge(int expiry)`参数单位是秒，表示cookie的持久化时间。如果设置参数为0，表示将浏览器中保存的该cookie删除。



**cookie的Domain 和 Path** 

浏览器会在携带cookie时，会根据cookie的Domain 和 path 过滤筛选，通过`setPath()`和`setDomain()`设置这两个属性

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20220612183208301.png" alt="image-20220612183208301" style="zoom:67%;" />

```java
cookie.setPath(request.getContextPath()); // 设置为当前工程名
```





cookie的path过滤 示例

![img](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5ou_5qOS5qOS57OW55qE54yq54yq5L6g,size_13,color_FFFFFF,t_70,g_se,x_16.png)





### session

存储于服务器内存的数据，cookie中只保存必要的`sessionID`  



 Session的API

- `request.getSession()`：获得session，第一次调用会创建session 
- `Object getAttribute(String name)` ：获取值
- `void setAttribute(String name, Object value) `：设置键值对
- `void removeAttribute(String name)`  ：删除 
- `string getId()`：获取sessionID 



在servlet中应用

```java
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    //1. 获取Session对象
    HttpSession session = request.getSession();
    //2. 往Session对象中存入数据
    String message = (String)session.getAttribute("session-message");
    System.out.println(message);
}
```



`request.getsession()`的工作原理：

- 服务器端没调用request.getSession()方法：什么都不会发生
- 服务器端调用了request.getSession()方法
  - 服务器端检查当前请求中是否携带了JSESSIONID的Cookie
    - 有：根据JSESSIONID在服务器端查找对应的HttpSession对象
      - 能找到：将找到的HttpSession对象作为request.getSession()方法的返回值返回
      - 找不到：服务器端新建一个HttpSession对象返回
    - 无：服务器端新建一个HttpSession对象返回





session的闲置时效，默认1800s 。闲置时效，指的是一次请求到下一次请求的间隔时长。 

```java
// 获取默认的最大闲置时间
int maxInactiveIntervalSecond = session.getMaxInactiveInterval();
System.out.println("maxInactiveIntervalSecond = " + maxInactiveIntervalSecond);

// 设置默认的最大闲置时间
session.setMaxInactiveInterval(15);

// 强制session 立即失效 
session.invalidate(); 
```

# Filter

Filter，一个接口。**运行于servelet前，进行过滤或者放行。**



## 创建

创建Filter：

1. 写一个类实现Filter接口，并且重写方法
2. 在web.xml中配置该过滤器的拦截路径



Filter类

```java
import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;


public class EncodingFilter implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain) throws ServletException, IOException {
        //解决请求参数的乱码
        HttpServletRequest request = (HttpServletRequest) req;
        request.setCharacterEncoding("UTF-8");

        //每次有请求被当前filter接收到的时候，就会执行doFilter进行过滤处理
        System.out.println("EncodingFilter接收到了一个请求...");
		// return; // 如果提前return了 则表示过滤失败 不放行
        //这句代码表示放行 进行下一步的servlet处理
        chain.doFilter(req, resp);
    }


}
```

web.xml 配置 

```xml
<filter>
    <filter-name>encodingFilter</filter-name>
    <filter-class>com.atguigu.filter.EncodingFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>encodingFilter</filter-name>
    <!--url-pattern 可以用*通配符 可以有多个url-pattern-->
    <url-pattern>/demo01</url-pattern>
    <url-pattern>/user/*</url-pattern>
    <url-pattern>*.png</url-pattern>
</filter-mapping>
```



## 生命周期

| 生命周期阶段 | 执行时机         | 生命周期方法                             |
| ------------ | ---------------- | ---------------------------------------- |
| 创建对象     | Web应用启动时    | init方法，通常在该方法中做初始化工作     |
| **拦截请求** | 接收到匹配的请求 | doFilter方法，通常在该方法中执行拦截过滤 |
| 销毁         | Web应用卸载前    | destroy方法，通常在该方法中执行资源释放  |



```java
package com.atguigu.filter;

import javax.servlet.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

/**
 * @author Leevi
 * 日期2021-05-18  10:22
 */
public class IllegalCharFilter implements Filter {
    private List<String> illegalTextList = new ArrayList<>();
    @Override
    public void destroy() {
    }

    @Override
    public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain) throws ServletException, IOException {
    }

    @Override
    public void init(FilterConfig config) throws ServletException {
    }
}

```





## 过滤器链

多个Filter依次过滤请求，称为过滤器链。过滤的顺序取决于xml文件的配置顺序。

示例： 03，02, 01 

```xml
<filter-mapping>
    <filter-name>TargetChain03Filter</filter-name>
    <url-pattern>/Target05Servlet</url-pattern>
</filter-mapping>
<filter-mapping>
    <filter-name>TargetChain02Filter</filter-name>
    <url-pattern>/Target05Servlet</url-pattern>
</filter-mapping>
<filter-mapping>
    <filter-name>TargetChain01Filter</filter-name>
    <url-pattern>/Target05Servlet</url-pattern>
</filter-mapping>
```



# Listener

Servlet监听器，用于监听Web应用程序中的ServletContext，HttpSession 和HttpServletRequest等域对象的创建销毁事件以及对象属性的修改事件。 



## 分类

 ServletContextListener：监听ServletContext对象的创建与销毁

| 方法名                                      | 作用                     |
| ------------------------------------------- | ------------------------ |
| contextInitialized(ServletContextEvent sce) | ServletContext创建时调用 |
| contextDestroyed(ServletContextEvent sce)   | ServletContext销毁时调用 |

```java
// listener示例
public class MyContextListener implements ServletContextListener {
    @Override
    public void contextInitialized(ServletContextEvent sce) {
        System.out.println("服务器启动了...");
    }

    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        System.out.println("服务器关闭了...");
    }
}
```





 HttpSessionListener：监听HttpSession对象的创建与销毁

| 方法名                                 | 作用                      |
| -------------------------------------- | ------------------------- |
| sessionCreated(HttpSessionEvent hse)   | HttpSession对象创建时调用 |
| sessionDestroyed(HttpSessionEvent hse) | HttpSession对象销毁时调用 |



ServletRequestListener：监听ServletRequest对象的创建与销毁

| 方法名                                      | 作用                         |
| ------------------------------------------- | ---------------------------- |
| requestInitialized(ServletRequestEvent sre) | ServletRequest对象创建时调用 |
| requestDestroyed(ServletRequestEvent sre)   | ServletRequest对象销毁时调用 |

ServletRequestEvent对象代表从HttpServletRequest对象身上捕获到的事件，通过这个事件对象我们可以获取到触发事件的HttpServletRequest对象。另外还有一个方法可以获取到当前Web应用的ServletContext对象。



## ServletContextListener

ServletContextListener是监听`ServletContext`对象的创建和销毁。因为ServletContext对象是在服务器启动的时候创建、在服务器关闭的时候销毁，所以ServletContextListener也可以监听服务器的启动和关闭

监听器类创建

```java
package com.atguigu.listener;

import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;

/**
 * 1. contextInitialized()方法可以监听服务器的启动
 * 2. contextDestroyed()方法可以监听服务器的关闭
 */
public class MyContextListener implements ServletContextListener {

    @Override
    public void contextInitialized(ServletContextEvent sce) {
        System.out.println("服务器启动了...");
    }

    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        System.out.println("服务器关闭了...");
    }
}
```

注册监听器 

```xml
<!--配置Listener-->
<listener>
    <listener-class>com.atguigu.listener.MyContextListener</listener-class>
</listener>
```



