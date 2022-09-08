[toc]

# 虚拟环境



虚拟环境管理（windows-cmd）：

* 安装：`pip install virtualenv-win`
* 创建：`mkvirtualenv env_name`，**默认会在用户(User)目录下创建文件夹`Envs`**，创建完成后将自动切换当前路径到虚拟环境目录。如需**更改默认路径**，可以创建系统环境变量（我的电脑，高级）`WORKON_HOME=xxx`来更改
* 切换：`workon env_name`；
* 退出：`deactivate env_name`，
* 删除：`rmvirtualenv env_name`
* 列出：`lsvirtualenv`
* 进入到虚拟环境所在文件目录：`cdvirtualenv env_name` 

# 项目结构

## 创建项目

* 命令行的方式：对应路径下执行`django-admin startproject <project_name>`
* pycharm，创建Django项目

## 创建app

各个app本质是一个python包

* 方法1：pycharm选择创建python package，然后按需手动添加各类py文件（如urls.py）

* 方法2：命令行进入项目路径，执行`python manage.py startapp <app_name>`  



注册APP：在settings.py`INSTALLED_APPS=[]`进行注册，直接添加APP名字即可



**入口app**：和项目名称相同的app，类似于main函数作为入口地址，最先执行，包含项目的配置文件。

下图中，工程名字叫做`url_reflect`，同时存在以下app：`book`、`movie`、`url_reflect`（与项目同名）。

  

![](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/django%E9%A1%B9%E7%9B%AE%E7%BB%93%E6%9E%84.png)

* urls.py：路由文件，匹配url链接 

* settings.py：项目的设置文件文件

* wsgi.py ：项目与 WSGI 协议兼容的 web 服务器入口，部署的时候需要用到的

* manage.py ：终端输入 `python manage.py [子命令] `，可以和项目进行交互。可以输入` python manage.py help `获取帮助 



## 运行项目

* 命令行：`python manage.py runserver 0.0.0.0 port`，0.0.0.0表示本网络的本主机。**若允许以其他IP地址访问**，需要在`setting.py`文件中的`ALLOWED_HOSTS = []`**添加ip端地址**，如`ALLOWED_HOSTS = ['192.168.1.104']`  ，使用`'*'`表示通配所有形式。

* pycharm：在项目运行前设置host端口，然后点击运行。



django的MVT：

![](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/djangoMTV%E6%A8%A1%E5%9E%8B.png)

## 时区设置

### naive time &aware time

**naive time 不带时区属性，而aware time对象包含了时区属性**。 python自带的`datetime.now()`获取的是naive时间。

时区之间的time转换可以调用接口`.astimezone(tz_obj)`。python3.6版本以下时，如果datetime是naive，调用该接口会报错；3.6版本及以后，做了兼容处理，当时间是naive时，转换后的时区会跟随系统。

 下例展示了一个datetime是如何时区转换的（python 3.6版本）。

```python
import pytz
from datetime import datetime

utc=pytz.timezone('utc')	# 这是一个时区对象

now=datetime.now()	# python自带的datetime.now()获取的是naive time 
utc_now=now.astimezone(utc)	# 转UTC时间传入一个tzinfo对象 
local_now=now.astimezone()	# 缺省时区，跟随系统 
print('【{}】\n【 {}】\n【{}】'.format(now,utc_now,local_now))

'''运行结果 可以看到 最后一个时间和第一个时间是相同的
【2020-04-27 09:38:23.684401】
【2020-04-27 01:38:23.684401+00:00】
【2020-04-27 09:38:23.684401+08:00】
'''
```

### USE_TZ

```python
# settings.py
TIME_ZONE = 'Asia/Shanghai'	#当地时区
USE_TZ = True	# 是否启用时区 影响django的时间函数 
```

 django内置的两个获取时间的函数：

* `now`：返回设置的 `TIME_zone`时间，当`USE_TZ`为True时，返回的时间中包含了时区属性
* `localtime`：转换`now()`函数的时区时间为当地时区的时间，涉及到时区转换，**所以要求`USE_TZ = True`**

```python
from django.utils.timezone import now,localtime


# now() 源码 
def now():
    """
    Return an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    if settings.USE_TZ:
        # timeit shows that datetime.now(tz=utc) is 24% slower
        return datetime.utcnow().replace(tzinfo=utc)	#这里补充了时区信息
    else:
        return datetime.now() 
    
# local() 源码 如果是naivetime 直接报错 
# Emulate the behavior of astimezone() on Python < 3.6.
if is_naive(value):
    raise ValueError("localtime() cannot be applied to a naive datetime")
    return value.astimezone(timezone)
```



# 路由配置

## url映射

url格式：`scheme://host:port/path/?query_param=xxx`  



Django在匹配url时，会到`urls.py`寻找一个名为`urlpatterns`的变量，该变量为列表类型，每个元素存储一个path对象，格式为`path('路径/',视图函数地址)` （**存储的是函数地址**）。当匹配到对应的url时，就交由相应的**视图函数**处理。

```python
'''urls.py '''
from django.urls import path,re_path # 后一个是正则路径匹配

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^.*$',admin.site.urls) # 正则 
]
```



## 视图函数

第一个参数为request，是django处理后的浏览器请求。返回是`HttpResponse()`对象、选择重定向、[模板](#模板)渲染等。

```python
from django.http import HttpResponse
from django.shortcuts import redirect,render
def view_func(request,arg):
    #do something
    #return redirect('/index') #重定向跳转
    #return redirect(reverse('index')) #反转url名字跳转 
    #return render(request,'index.html') #模板渲染
    return HttpResponse(arg)
```



## url参数捕获

视图函数如何从url捕获参数

### url及视图函数设置

url设置：

固定字符串形式捕获：

```python
# <type:variable_name>
# 变量名 和 视图函数的形参一致 
urlpatterns=[path('book/<int:page>',pages)]	#page是视图函数接收的变量 
```

以正则表达式的形式捕获：

`re_path(r'(?P<name>匹配规则)',视图函数地址)`，正则会将捕获分组命名name，传给视图函数。

```python
from django.urls import re_path	#re_path要导入 
urlpatterns=[re_path(r'(?P<year>[0-9]{4})/',years)]	 #捕获1个year参数
```





**视图函数如果是默认参数**，需要额外设置一个没有参数的url：

```python
'''默认跳转到第1页'''
from django.http import HttpResponse

def pages(request,page=1):	#Page默认为1
   return HttpResponse("%s" % page)

urlpatterns = [path('book/<int:page>',pages),
               path('book/',pages),  # 额外定义1个没有参数的url 
              ]	
#访问的时候book/将会默认为book/1
```





### 自定义类型转换器 

当类似`<var_type:var>` 这种带参数的url匹配时，向视图函数传递参数的过程发生了：

1. 正则匹配变量部分，捕获并命名为var，此时变量类型为string
2. 进行类型转换，`var_type(var)` ，将其传入视图函数

django默认支持类型可以在`from django.urls import converters`查看。 



自定义类型转换器：这里以编写一个列表类型形式的转换为为例

1. 在app中创建converters文件，并仿照库文件进行编写。

   ```python
   #在converters.py文件
   from django.urls import converters
   class ListConverter:
   	regex=r"\w+(\+\w+)*"  #python+php+... 正则匹配规则 
       def to_python(self,value):	
           return value.split('+')	#转为python的内置列表类型
   
       def to_url(self,value):
           return str(value)	#转为字符串型
       
   # 执行注册 
   converters.register_converter(ListConverters,"List")    
   ```

2. 由于**该文件不会主动运行**，因此，在app的init文件中，写入`from . import converters`，导入的时候自动会执行注册函数

3. 在url参数捕获时，就可以使用自定义的：

```python
#urls文件
urlpatterns=[path("favorite/<List:var>",favorite)]  #使用了自定义的List类型转化器 
```





## 封装映射

将**一些相关的映射规则拆分封装到各自的app**中。



**url匹配是一个路径逐级匹配的过程**：匹配时，会先剥离`主域名:port/`。对于剩下的字符，遍历`urlpatterns`，匹配成功就剥离该段字符串，依次类推。



封装步骤：

1. 在**app中新建一个urls.py映射文件**，创建`urlpatterns`变量，编写该app自己的映射规则，**编写时，只要编写剥离前缀prefix后的url即可**。例如：

   ```python
   #book中的 urls.py 文件
   from . import views #从当前文件夹导入views文件，使用相对路径写法
   
   urlpatterns=[path('',views.index),	#完整路径：prefix/
               path('list/',views.booklist),	#完整路径：prefix/list
               path('detail/',views.bookdetail) ]	#完整路径：prefix/detail         
   ```

   

2. 在根urls.py文件中，使用include函数（要先导入）来封装，前缀在这里定义 

```python
from django.urls import path,re_path,include
urlpatterns=[path('',views.index),
            path('book/',include('book.urls') ) ] # book/xxx前缀开头的url，都会进入book.urls继续匹配
```



## 命名空间 

命名空间的目的：令url反转唯一 

### url 命名 

**以常量字符串的形式将跳转url写死**，例如`redirect('/login/')`，在以后url更名时，**维护不便**。



url命名步骤：

1. 在`path('url',view_func,name='url_name')`**，定义name参数**。

2. 需要重定向的地方，`reverse('url_name')`，该函数输入url名字，返回一个url真正的字符串。



下例中，为`sigup/`url取名为'login'，然后在index视图函数中重定向到该url。

```python
from django.shortcuts import  redirect,reverse

def index(request):
    return redirect(reverse('login')) 	# 反转

urlpatterns = [path('sigup/',index,name='login')]  	# 为signup命名为login
```

### app 应用命名

**仅仅为url命名是不够的**，假设现在一群人在编写各自的app，**那么就很容易出现相同的url命名**。

这时候，就要为app取一个名字，即**应用（app）命名**。



**应用命名步骤：**

1. 在app的`urls.py`文件中创建与`	urlpatterns`同级变量`app_name=xxx`，这就完成了应用的命名，**同时意味着在该app下的所有已经命名的url更名**为`appname:urlname ` 。类似于python的模块命名空间`module.var` 。

   ```python
   appname='xxx'
   urlpatterns=[] 
   ```

2. 反转时，`reverse('appname:urlname')`。

   

### path 实例命名

我们先在根路由定义以`book1/`、`book2/`访问时，都跳转到bookAPP。

```python
urlpatterns=[path('book1/',include('book.urls')),
             path('book2/',include('book.urls'))
            ]
```

然后在book.urls中定义如下路由，`book1/`、`book2/`会进入到views.index视图函数。

```python
#book.urls文件
from . import views
app_name="book"
urlpatterns=[path('',views.index),
    		path('/detail',views.index,name='detail')]
```

book.views定义视图函数，执行一个简单的重定向，跳转到图书详情页。

```python
#book.views 文件
def index(request):
    return redirect(reverse("book:detail"))  

```

我们的预期是，`book1`跳转到了`book1/detail`、`book2`跳转到了`book2/detail`，但实际情况不是，两者都跳到`book1/detail`。原因就是reverse在寻找appname时，在根路由自上而下寻找，进入到了`book1/`中，所以`book2/`在反转的时候就拿到了前缀`book1`。



要想实现我们的预期，就得使用实例命名，所谓的实例，就是`path()`，我们为这样一个具体的path命名。

**创建实例命名：**

1. 在`include('映射文件路径',namespace='xxx')`函数中使用关键字参数`namespace`创建实例命名空间。此时要求**该app必须拥有app_name**。 

   ```python
   #主app, 可以注意到namespace命名和app_name并不需要一样
   urlpatterns=[path('book1/',include('book.urls',namespace="book_first")),
                path('book2/',include('book.urls',namespace="book_second"))
               ]
   ```

   

2. 在reverse时，就不能再写作`appname:urlname`，而是要写作`namespace:urlname`。所以要先获取当前请求的实例名`current_namespace`，再拼接，示例代码：

```python
#book.views 文件
def index(request):
    current_namespace=request.resolve_match.namespace	#获取当前实例命名
    re=reverse("%s:detail"% current_namespace)		#格式为cn:url_name
    print("实例命名空间：%s 反转结果：%s"% (current_namespace,re))
    return redirect(re)
```



从`include`函数的源码`namespace=namespace or app_name`可以发现，当namespace未定义时**，实例命名（`namespace`）就是应用命名空间（`app_name`）。**



实例命名空间、应用命名空间比较：

**应用命名空间是为了让各个url之间命名不重复**，彼此独立，能够正确找到app下的url。**实例命名空间是为了映射到同一个app的不同实例之间彼此独立**，能够正确拼接。实例命名空间定义之后会覆盖应用命名空间，两者都是为了不让reverse混乱。无论应用命名还是实例命名，最终的url都更名为`space_name:urlname` 。



# 静态资源

## Static

### 独立设置

**单独建立一个static文件夹进行管理**。

在 settings.py 中添加变量 `STATICFILES_DIRS=[os.path.join(BASE_DIR, 'static')]` ，表示静态资源查找路径，**该路径优先于APP内的`static`文件夹**。

```python
'''settings.py
BASE_DIR是项目路径 
'''
STATIC_URL = '/static/'	 # 静态资源请求url
STATICFILES_DIRS=[os.path.join(BASE_DIR, 'static')]  # 项目下的static文件夹
```



### app内设置

1. 检查`settings.py`文件

   ```python
   '''settings.py'''
   INSTALLED_APPS = ['django.contrib.staticfiles'] # 开启app
   STATIC_URL = '/static/'		 # 静态资源加载前缀url
   ```

   

2. 创建`static`文件夹：选择一个已经注册了的 某个app 下创建`static`文件夹，建立一层中间目录`app_name`，层级结构如`static/app_name/`。建立中间目录是因为静态资源文件较多时，可能会出现重名的情况。

   

   使用静态资源示例：前半部分的`/static/`是静态资源加载的url，**后面的`img/zhouyu.jpg`是相对于`static`文件夹的路径。**

   ```django
   <img src="/static/img/zhouyu.jpg" alt="图片" width="20%" height="20%">
   ```

   这里的`src="/static/img/zhouyu.jpg"` 是**一个URL**，当浏览器请求该静态资源时，实际发出的请求为`http://host:port/static/img/zhouyu.jpg`。 

   



## MEDIA 

media用于用户上传的图片

1. 在settings.py文件中指定`MEDIA_ROOT`、`MEDIA_URL`，**用于处理媒体文件的上传**。

   ```python
   MEDIA_URL = '/media/' # 请求url 
   MEDIA_ROOT = os.path.join(BASE_DIR,'media') # 上传文件存储位置 
   ```

   MEDIA_URL的作用和STATIC_URL类似，是一个URL前缀，**当请求`/MEDIA_URL/resource`的时候，就会去`MEDIA_ROOT`路径下寻找资源**。当文件上传成功时，通常需要返回该文件的访问url，告知用户。

   ```python
   def upload_file(request):
       import os
       file=request.FILES.get('file')
       name=file.name
       # 写入文件
       with open(os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,name),'wb') \
               as f:
           for chunk in file.chunks():f.write(chunk)
       
       # 返回文件的完整URL, /media/file_name
       file_url=request.build_absolute_uri(settings.MEDIA_URL+name) 
       return restful.result(data={'url':file_url}) #json格式返回
   ```

   

2. 在urls.py文件中添加MEDIA_URL访问路径

   ```python
   from django.urls import path
   from front import views
   from django.conf.urls.static import static	#使用static函数前先导入
   from django.conf import settings
   # static 静态资源加载原理其实也是这个
   # 不过由中间件 'django.contrib.staticfiles' 实现了 
   urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
   ```



# 模板

## 渲染模板

模板：`.html`后缀文件。视图函数不只是可以返回字符串（`Httpresponse("str")`）,也可以返回一个设计好的html文件。

### 模板存放

项目初始化时，会生成一个**固定名为`templates`**的文件夹，该文件夹就用于存放模板。



django搜索`templates`文件夹的顺序可以在入口app的`settings.py`文件中更改。

优先寻找`DIRS`对应的列表，若寻找无果且`APP_DIRS:True`（默认为True）则会在注册的APP下寻找名为`templates`文件夹。

```python
'''settings.py'''
TEMPLATES={"DIRS":[os.path.join(BASE_DIR, 'templates')],
           "APP_DIRS":True}
```





### 返回模板

1. 创建1个字典`context`，**以键值对的形式向渲染模板传入变量**，参数可以是普通变量、函数名、类。模板中以键`key`的形式使用变量
2. 使用render函数（需要导入）渲染模板，语法为`render(request,'html_file',context)` 。

```python
from django.shortcuts import render

def index(request):
    return render(request,'index.html',{'name':'jhk'})
```



***

模板文件使用变量：

在模板文件中，**使用两对花括号`{{var}}`访问变量（这里的var是context中的键），使用`.`运算符来执行变量属性（attribute）访问、方法（method）调用、元素索引（`[]`）等操作。**

若context中传入了函数（地址），虽然在模板文件中可以正常调用，**但该函数不允许有参数**，有很大的局限性。如`{{get}}`将会调用get()函数，django中代而取之的做法是**过滤器**。

```django
<body>
	{{person.keys}} person就是一个变量，keys调用字段方法dict.keys
</body>
```

**注意，django会对模板文件的任意一处DTL语法标签进行渲染，即使是在js脚本中。**利用这一点可以实现js脚本与后台数据的传输。例如

```django
<script>
    // 上下文变量persons 一定是json格式
    // context={"persons":json.dumps()} 
    // safe 过滤器关闭转义作为变量原样输出 
	var nodes ={{ persons|safe }};  //nodes=[{name:'',index:''}]
</script>
```



## DTL语法标签

标签：**DTL标签类python语法中的语句**，**在模板文件中使用**，执行一些特殊操作，使模板文件生成时更加零活。



常用标签：

* 模板导入：`{% include html_name%}`，导入另外的html文件，相当于在此处复制粘贴。当有某个html文件被多次使用时，可以使用include进行导入，优化模板。

  被导入的模板称为”父模板“，父模板可以直接使用子模板的变量`{{var}}`亦或者手动传输。

* if判断：`{% if ...%}`。花括号左右有空格

  ```django
  {%if '鲁班七号' in heros%}
  	<p>鲁班一号正在待命</p>
  {% else %}
  	<p>鲁班一号正在睡觉</p>
  {% endif %}   
  ```

* for循环：`for item in items`，items为可迭代对象。不能使用break、continue语句。

  ```django
  基本的for循环结构
  {%for item items reversed%}  
  	reversed表示反向遍历 
  {{%empty%}}		
  	当迭代对象为空时，进入empty分支
  {%endfor%}
  ```

  DTL在for循环时自定义了一些变量便于判断，如`forloop.counter `表示当前计数（默认从1开始，forloop.counter0可以从0开始），`forloop.first/last`分别表示第一次、最后一次循环。

  下例，循环生成表格的每一行

  ```django
  {%for book in books%}
  <tr>
      <td>序号：{{forloop.count}}</td>
      <td>书名(以索引形式)：{{book.1}}</td>
  </tr>
  {%endfor%}
  ```

  

* with取别名：DTL中**对于复杂变量可以另取一个变量名，方便后文的访问**，该变量名**只能在with语句块中使用**。存在两种写法：（1）`with new_name=old_name`，等号左右不能有空格，否则会无法识别（2）`with old_name as new_name` 

  ```django
  '''.html文件使用with示例，作用域在花括号之内'''
  
  方法1，直接使用=
  {%with name=persons.username%} 
  	<p>{{name}}</p>
  {%endwith%}
  
  #方法2，使用as
  {%with persons.username as name%} 
  	<p>{{name}}</p>
  {%endwith%}
  ```

* url反转：`{%url "url_name" val="value"%}`，url_name为path中url的命名，val表示传递参数，多个参数之间以空格分隔，示例如下。

  ```html
  <a href="{% url 'bookdetail' book_id='1' %}?next=xxx">最火的一篇文章</a>  
  ```
  
* 关闭尖括号自动转义：`{%autoescape=off%} `。DTL会**自动**将context所传变量的尖括号等符号进行**转义**，**以字符串的形式呈现，这会影响HTML标签的插入**。关闭自动转义类似于python的`r""`，所见即所得。

  ```python
  '''view.py'''
  context={'info':"<a href='www.baidu.com'>百度</a>"}	#context定义
  ```

  ```django
  模板文件使用
  <p>  
  {%autoescape off%}  
  关闭自动转义标签，默认开启，块范围内可以关闭转义    
  {{info}}     
  {%endautoescape%} 
  
  这与上面等价
  {{info|safe}}
  </p>
  ```
  
* safe：禁止字符串转义。有两个作用：（1）与autoescae相同，关闭转义（2）与js交互时，作为变量

  ```js
  //persons是上下文的变量 ，使用safe过滤器安全输出
  var nodes={{ persons|safe }};
  ```

  

* 禁止django解析：`{%verbatim%}`，英文意思为“逐字的”。使用该标签，django将不对标签里的内容进行DTL语法解析，仅当做普通字符串处理。在使用art_template模板语法时，可以放在该标签下。

  ```python
  {%verbatim%}
  	这里放art_template的模板语法
  {%endverbatim%}
  ```

* 继承父模板：`{% extends 'base.html'%}` 。与`include`的区别是，继承可以重写父模板开放的`block`接口。

* 标签加载：`{%load label_name%}` 

## 过滤器

**DTL自带的过滤器相当于Python的函数**，负责处理数据。例如`add`、`cut`、`date`过滤器，使用方法为`参数1|过滤器名称:参数2`，**过滤器最多有2个参数**。



### 常用过滤器

* 相加：`val1|add:val2`，首先将两个参数转为整型相加，若不能，则进行该类型本身相加，如列表、字符串拼接
* 拼接：`val1|join:val2`，用参数2作为连接字符连接参数1，类似于python的join函数
* 空格替代：`val1|cut:val2`，将参数1中的val2代之以空格，相当于`str.replace(' ',val2)`
* 时间格式化：`val1|date:"Y-m-d"`，可以**按照指定字符串格式化传入的datetime对象参数**，注意y m d前没有百分号![](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/date%E8%BF%87%E6%BB%A4%E5%99%A8%E6%A0%BC%E5%BC%8F.png)
* 小数保留：`val1|floatformat:val2`，对浮点数参数1保留参数2位小数，若参数2缺省，默认保留1位小数
* 默认值设定：`val1|default:val2`，若参数1为空、None、False等值，将返回参数2作为默认值
* 容器长度计算：`val:length`，计算字典、列表等容器的长度
* 小写转大写：`val:lower/upper`，将字符串转小写、大写
* 随机选取：`val|random`，在参数容器中随机选择一个元素
* 关闭自动转义：`val|safe`，认为字符串是安全的，关闭自动转义。参数可以以html代码的形式插入
* 切片：`val1|slice:"val2::step"`，对容器1从参数2位置开始以步长step切片
* 标签剥夺：`val1|striptags`，剥夺参数1的html标签，以纯文本形式展示。

* `val1|truncatechars:"val2"`：参数1最多能显示val2个字符串，多余部分以...显示。至于`...`被算作3个字符。与之类似的过滤器是`truncatechars_html`，将不会对html标签部分进行字符计数。



### 自定义过滤器

1. 建包：在已注册的APP下新建**固定**名为`templatetags`的python**包** 

2. 编写过滤器：在`templatetags`包中新建py文件，名字任意，于其中编写过滤器函数

3. 注册：编写完后，导入`template`包进行注册。注册的办法有两种（1）使用register装饰器，默认过滤器名称即为函数名字（2）使用`register.filter(filter_name,filer_func)` 。

   ```python
   '''
   在某APP下自定义my_filter.py文件,编写自定义过滤器
   
   '''
   from django import template
   register=template.Library() #新建library类
   
   
   #方法1，可以直接使用装饰器@register来完成映射,
   #默认过滤器名称即为函数名字
   @register.filter  
   def greet(val,word):	#过滤器最多只有两个参数，第一个参数是被过滤的参数
       return val+word   #
   
   #方法2，使用函数进行注册
   register.filter("my_greet",greet)  
   ```

   

4. 加载：在模板文件使用load标签`{% load file_name %}`加载过滤器定义所在文件，加载后可以直接使用文件中的自定义过滤器

```python
'''
在一个html文件中，若需使用自定义过滤器，必先加载其所在py文件
'''
{%load my_filter%}   #加载my_filter.py文件，
{{val|greet:val2}}  #加载后，可以直接使用my_filter中的自定义过滤器
```



## 模板继承

多个网页文档之间存在**公共的html骨架**，可以将该部分提取作为父模板，子模板只需继承父模板并个性化定即可。

继承步骤：

1. 父模板通过`{%block block_name%}`标签**向子模板暴露接口**，

   ```django
   <!base.htmlz作为父模板>
   <head>
       meta="utf-8"
       我是头部
   </head>
   
   <body>
       父模板可以自己写一些东西，子模板继承的时候就会显示这些 
       {%block content%}  
       	命名父模板的block接口为content
       	子模板的内容将会在这里填充   
       {%end block%}    
   </body>
   
   
   <footer>我是脚注</footer>
   ```

   

2. 子模板以`{% extends 'base.html'%}`标签继承父模板，**该继承语句必须写在第一行**。

   子模板使用`block`接口自定义内容，这就好像**父模板决定了基本的结构，子模板来插入数据**。**如果子模板不将数据写在接口内，则所有的数据均被父模板覆盖。**

   子模板在`block`接口编写的内容默认会覆盖父模板，如果不想这么做，可以使用`{{block.super}}`获取父类相关内容，类似于python类继承中的`super()`。

```django
<!index.html子模板继承>

<% extends "base.html"%>   
    
{%block content%}  
   子模板自定义部分，只能写在block区域，默认覆盖父模板的block部分
    {{block.super}}调用父模板的语句
{%end block%}    
 
```







# 数据库

## 数据库配置

django使用Python编写，使用数据库前，应当先安装python数据库驱动，例如`pymysql`（相关内容参考[python学习笔记](python学习笔记.md)）  。



django默认使用的数据库为sqlite3，进入`settings.py`为其更换mysql，并配置相关信息。

```python
'''settings.py 配置数据库 
engine改为mysql 然后配置主机、端口、用户名、密码等相关信息 
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',	
        'NAME': 'book_manager',
        'USER':'root',
        'PASSWORD':'root',
        'HOST':'localhost',
        'PORT':'3306'
    }
}
```



在视图函数中，引入`from django.db import connection`来使用数据库。

```python
'''views.py
展示了如何从数据库获取数据
'''

from django.shortcuts import render
from django.db import connection  # 使用数据库 
# Create your views here.

cursor=connection.cursor()	# 创建句柄

def index(request):
    cursor.execute('select * from book_info')
    #fetchall返回的是元组，每个元素都是表项
    book_info=cursor.fetchall()  #元组((id,book_name,book_author),...)
    #print(book_info)
    #context参数是一个字典
    return  render(request,'index.html',{'book_info':book_info})
```



## ORM创建映射

上述方法使用了原生的sql语句来操作数据库，缺点显而易见，sql语句复杂、重用率不够高。**django对此提供了一个更加灵活高效的解决方案——ORM。**

ORM（object relational mapping），对象关系**映射**。**通过模型类的办法来操作数据库，把表映射成类，把字段映射成类属性，把每一行数据映射成实例**。django底层封装了数据库的实现，支持多个关系型数据库，如mysql、sqlite，这就意味着更换数据库时更少的代码改动。

### 创建模型

在已经安装的app的`models.py`文件中创建类

```python
from django.db import models

'''创建了bookinfo表，有两个字段
1.char(20)类型的btitle
2.date类型的bpub_date 
'''
class BookInfo(models.Model): # 继承模型类 
    btitle=models.CharField(max_length=20)
    bpub_date=models.DateField()
```

**在建表时，如果没有指明主键，django在映射的时候就会默认增加一列自增长int类型的`id`作为主键**。

### 映射模型

在`models.py`文件中编写的模型类，**必须经过映射才可以在数据库发生真正的操作**。

映射的步骤如下：

1. `python manage.py makemigration` ，生成迁移脚本文件，迁移脚本会记录模型的操作， 文件生成在`appname/migrations` 

2. `python manage.py migrate`，进行迁移。该命令会执行1步骤生成的迁移文件，将操作真正写到数据库中。创建的表名为`appname_tabname`，`tab_name`是类名小写。如果是第一次migrate，那么`installed_apps`中内置的模型类也会一并创建。

   ```python
   '''内置模型类，最后1个front是自己创建的app'''
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'front'
   ]
   ```




### 常用字段

在 Django 中，定义了一些 Field（`models.xxxField`） 来与数据库表中的字段类型来进行映射。 

* `BooleanField`：在模型层以`True/False`指定 ，在数据库层是 tinyint 类型（0/1）。如果没有指定默认值，默认值 是 None 

* `CharField(max_length)`：在模型层以`"str"`普通字符串的形式指定，在数据库层是 varchar 类型。在创建时要以`max_length`指定最大的长度

* `IntegerField`：整型

* `DateField`：日期类型，即年月日。在 模型层中是 python的`datetime.date`(from datetime import date) 类型，在映射到数据库中也 是 date 类型。使用这个 Field 可以传递以下几个参数：

  1.  `auto_now`：在每次这个数据保存`(save()`)的时候，都使用当前的时间。
  2.  `auto_now_add` ：在每次数据第一次被添加进去的时候，都使用当前的时间。

  ```python
  class Article(models.Model):
      #默认的时间为UTC时间
      creat_time=models.DateTimeField(auto_now_add=True)  #创建时间
      comment_time=models.DateTimeField(auto_now=True)    #最后修改时间
  ```

* `EmailField`：邮箱格式，无需指定最大长度 



### Field设置

* null：`null=true/false` ，允许字段为空、非空。

* blank：标识这个字段在表单验证的时候是否可以为空。默认是 False 。 这个和 null 是有区别的， null 是一个纯数据库级别的。而 blank 是表单验证级别的
* db_column：这个字段映射到数据库的名字，默认使用模型中属性的名字。
* default：默认值，或者是一个**函数地址**`(default=func)`，不支持 lambda 表达式

* primary_key：是否为主键，如果不设定主键，django底层会生成id作为主键。
* unique：在表中这个字段的值是否唯一，一般是设置手机号码/邮箱等。

### meta设置

**对于一些模型级别的设置**，可以在模型类中定义一个类，叫做`Meta`。然后在这个类中**添加一些 类属性**来控制模型的作用。



[常用类属性](https://docs.djangoproject.com/en/2.0/ref/models/options/)：

* `db_table`：模型类映射时的表名 
* `ordering`：Manager返回数据集时，进行排序。

```python
class Article(models.Model):
    #默认的时间为UTC时间
    creat_time=models.DateTimeField(auto_now_add=True)  #创建时间
    comment_time=models.DateTimeField(auto_now=True)    #最后修改时间

    class Meta:
        db_table='my_article'	# 自定义表名
        ordering=['creat_time','id']	# 字段排序
```



## 模型CURD

### 查询

get：返回1条数据，**若返回结果有多个或不存在，将会报错**。

```python
'''get示例'''
# clsName.objects.get() 
b=BookInfo.objects.get(name='西游记') 	#返回1个bookinfo对象 
b1=BookInfo.objects.get(author='吴承恩')
```

all：返回表中的全部数据，结果是一个列表（QuerySet），支持索引、切片。

```python
'''all示例'''
a=BookInfo.objects.all()	#返回表全部数据
print(a[0])	#索引 
```



filter(key=val)：筛选表中数据，**结果是一个列表，可以为空**。可以在`get`前调用确保数据存在

```python
'''filter示例'''
a=BookInfo.objects.filter(author='鲁迅')[:3]	#返回鲁迅写的书本的前3条数据 
```



### 创建

新建实例，然后执行`.save()`方法。

```python
#方法1：
b=BookInfo(name='西游记',author='吴承恩') 	#新创建1个实例对象,以关键字形式指定字段值
b.save()	#保存

#方法2：当然创建以后，以类属性的形式初始化值也是可以的
b=BookInfo()
b.name='西游记'
b.author='吴承恩' 
b.save()	#保存 

#方法3：queryset-api 底层会调用save
b=BookInfo.objects.create(name='西游记',author='吴承恩')
b.name='西游记1'
b.save() # create 后也可以继续操作实例并保存 
```

### 修改

查询实例，更改属性值，最后save()。

```python
b=BookInfo.objects.get(name='西游记') 
b.author='罗贯中'
b.save() 	#保存修改

# queyset-api，update() 批量更新 
BookInfo.objects.filter(name='西游记').update(author='罗贯中')
```

### 删除

查询到对应对象，然后执行`.delete()`方法即可。

```python
b=BookInfo.objects.get(name='西游记')
b.delete() 	#删除该行 

# queyset-api, delete()
# BookInfo.objects.filter(name='西游记').delete()
```

更多接口请参见[QuerySetAPI](##QuerySetAPI)



## 外键和表

### 创建外键

#### 一对多 

`models.ForeignKey(to=model_class,on_delete)`：

* to ：关联模型名。`self`表示自身
* on_delete ：关联表的数据删除时，这个字段该如何处理。

在一对多的关系中**，外键应当在"多"的那一类定义**，"多—>一"，由多指向1。



`user`、`article`，两者之间是一对多的关系，一个user可以有多个article，但一个article只有1个作者。

```python
class User(models.Model):
    name=models.CharField(max_length=30)


class Article(models.Model):
    a_name=models.CharField(max_length=100)
    # 创建外键字段，指向user模型类
    a_user=models.ForeignKey(User,on_delete=models.CASCADE)  
```

#### 多对多 

`models.ManytoManyField(to,on_delete)`，定义在任意一个“多”中，但不能同时定义在两个“多”中。



`article`、`tags`，文章和标签是多对多的关系。

```python
class Article(models.Model):
    a_name=models.CharField(max_length=100)
    a_user=models.ForeignKey(User,on_delete=models.CASCADE)
    a_tag=models.ManyToManyField('Tag')		# 多对多外键 ，标签  类名也行 不一定要字符串  	

class Tag(models.Model):
    name=models.CharField(max_length=100)
```

模型层面，只需要两个互相关联的模型类即可建立多对多关系。**数据库层面，django实际会创建一张中间表**，分别记录两张表的主键映射关系，形如

| id   | article_id | tag_id |
| ---- | ---------- | ------ |
| null | null       | null   |



多对多使用示例，为文章“三国演义”增加两个标签“四大名著”、“历史文学” 。

```python
#多对多使用示例

#创建图书
article=Article.objects.get(a_name='三国演义')

#创建两个标签
tag=Tag(name='四大名著')
tag.save()
tag1=Tag(name='历史文学')
tag1.save()  

# 添加多对多关系
# 不可以直接为类属性赋值 article.a_tag=[tag,tag1] 是错误的 
article.a_tag.set([tag,tag1])
# article.a_tag.add(tag,tag1) #与上面等效
article.save()
```



#### 一对一 

`models.OnetoOneField(to,on_delete)`，定义在任意一个“一”中，但不能同时在两个类中定义。



### 正反向查询 

当为一个模型创建外键关联字段时，发生了：

1. 数据库层面，外键字段命名为`外键类属性_id`，以上案例中，article表的外键字段名为`a_user_id` 

2. 反向查询：用于**在一对多、多对多的映射中，获取“多”的那个类**。django会为关联类隐式增加一个属性，默认名字为`小写模型名_set`，返回关联对象的`Manager`。例如， `Article`关联到`User`，`User`增加一个关联属性`.article_set`  ，可以通过参数`related_name`更改。因为是隐式增加的，所以叫做 “反向查询”。

   在article类中，创建外键时，指定`releted_name`为`articles`

   ```python
   class User(models.Model):
       name=models.CharField(max_length=30)
   
   class Article(models.Model):
       a_name=models.CharField(max_length=100)
       # 创建外键字段，指向user模型类 
       # User类会隐式增加一个属性 默认为article_set 
       # 由于指定了related_name 所以变更为 articles
       a_user=models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='articles')
       a_tag=models.ManyToManyField('Tag')
   ```
   
   ```python
   #查询示例，一查多
   user=User.objects.get(name='罗贯中')
   for x in user.article_set.all():print(x.a_name)	#遍历打印 
       
   '''运行结果
   三国演义
   三国演义1.0
   '''
   ```
   
3. 正向查询：创建外键的表，可以**用类属性直接得到外键模型类** 

   ```python
   #查询示例，多查一
   article=Article.objects.get(a_name='三国演义')
   print(article.a_user.name) 
   
   '''运行结果 
   罗贯中
   '''
   ```

   

### on_delete 

如果一个模型使用了外键。**那么在对方那个模型被删掉后，该进行什么样的操作**。可以通 过 on_delete 来指定，可以指定的类型如下吗，它们本质是一个函数：

* **CASCADE ：级联操作。如果外键对应的那条数据被删除了，那么这条数据也会被删除。** 
* PROTECT ：受保护。即只要这条数据引用了外键的那条数据，那么就不能删除外键的那条数据。  
* SET_NULL ：设置为空。如果外键的那条数据被删除了，那么在本条数据上就将这个字段设置 为空。如果设置这个选项，前提是要指定这个字段可以为空`null=True`。 
* SET_DEFAULT ：设置默认值。如果外键的那条数据被删除了，那么本条数据上就将这个字段 设置为默认值。如果设置这个选项，前提是要指定这个字段一个默认值`default=xx`。 
* SET(func)：如果外键的那条数据被删除了，那么将会调用 SET()中的func函数的返回值来作为这个外键的 值。 
* **DO_NOTHING ：不采取任何行为。一切全看数据库级别的约束。** 

```python
#示例
from django.dbs import models
author=models.ForeignKey('User',on_delete=models.CASCADE)
```





## 条件查询

语法：`字段名__查询条件`（两个下划线），相当于sql语句中的where部分。

* exact：与使用`=`等效，基本可以省略

    ```python
    article = Article.objects.get(id__exact=14)		#查询id=14
    article = Article.objects.get(id__exact=None)	#查询id=null
    ```

* (i)contains：大小写敏感，判断某个字段是否包含了值。**i=ignore，表示大小写不敏感**，下同

    ```python
    articles = Article.objects.filter(title__contains='hello')	#title字段包含了hello
    #select ... where title like binary '%hello%';	底层的sql语句
    ```

* in：字段值是否包含在指定的容器之中，容器可以列表、元组、**甚至是一个queryset对象**。在筛选的时候比较有用。

  ```python
  articles = Article.objects.filter(id__in=[1,2,3])	#查看id=1，2,3的对象 
  ```
  
  当传递一个queryset对象时，表示查询 queryset的同名字段 
  
  ```python
  inner_qs = Article.objects.filter(title__contains='hello')	#得到字段包含hello的书籍
  categories = Category.objects.filter(article__id__in=inner_qs)	#关联查询
  
  #等效于以下sql语句
  '''
  select ...from category where article.id in (
  	select id from article where title like '%hello%');
  '''
  ```
  
* gt：某个field的值大于给定的值  

    ```python
    articles = Article.objects.filter(id__gt=4)
    ```

    类似的条件还有`gte`（>=）、`lt`（<）、`lte`（<=）。

* (i)startswith：判断某个字段的值是否以某个值开始，i表示大小写不敏感。

    ```python
    articles = Article.objects.filter(title__startswith='hello')
    ```

* endswith：同上，判断结束字符。iendswith，大小写不敏感。

  ```python
  articles = Article.objects.filter(title__endswith='world') 
  ```

* range：判断某个 field 的值是否在给定的区间中

* is_null：根据值是否为空进行查找。

  ```python
  articles = Article.objects.filter(pub_date__isnull=False)	#筛选非空
  articles = Article.objects.filter(pub_date__isnull=True)	#筛选为空
  ```

* (i)regex：正则表达式（i表示大小写不敏感）。

  ```python
  articles = Article.objects.filter(title__regex=r'^hello')	
  ```



### 关联查询

关联查询，**相当于跨表查询。**语法为`关联模型小写__字段名__条件` 

假设现在有两个模型类，user作者，Article文章类

```python
class User(models.Model):	#作者类 
    name=models.CharField(max_length=30)

class Article(models.Model):	#书籍类，指向user
    a_name=models.CharField(max_length=100)
    a_user=models.ForeignKey("User",on_delete=models.CASCADE)
```

其数据库如下

user表

| id   | name   |
| ---- | ------ |
| 1    | 罗贯中 |
| 2    | 施耐庵 |
| 3    | 曹雪芹 |

article表

| id   | a_name   | a_user_id |
| ---- | -------- | --------- |
| 1    | 三国演义 | 1         |
| 2    | 三国机密 | 2         |
| 3    | 红楼梦   | 3         |



```python
# 文章标题中包含 三国的 作者 
# 类名小写article+双下划线+字段名a+双下划线+条件
users=User.objects.filter(article__a_name__contains='三国')	
for user in users:print(user.name)

'''运行结果
罗贯中
施耐庵
'''
```



**是否注意到这和反向查询有些相似？**

**反向查询时，我们使用的是“类名小写__set”**，得到的是一个类似objects的管理器。**关联查询在查询条件时书写**。





## F表达式

**F表达式用于优化ORM的条件查询。** 

看一个例子，假设现在要为公司的每一位员工的薪水增加1000元。未使用F表达式之前，它的操作应该是：遍历，逐个更改。

```python
employees = Employee.objects.all()
for employee in employees:
    employee.salary += 1000
    employee.save()
```

**但是F表达式可以直接执行SQL语句完成这个操作，数据在执行过程中会动态地获取。**语法为`F('字段名')`。

上例可以改写为

```python
from djang.db.models import F
Employee.objects.update(salary=F("salary")+1000)	#注意F的参数 
```



## Q表达式

**Q表达式用于查询时候的多个条件连接，包括与&、或|、非~。**

filter函数中多个参数使用`,`分隔时，默认就是“与”。

```python
#查询图书价格大于等于100 且评分在9分以上的图书
books = Book.objects.filter(price__gte=100,rating__gte=9)
```

但是，若想实现或、非效果，就不得不借助于Q表达式。&|~等符号只能用于两个Q对象之间，filter本身的参数可不支持。

实现或效果

```python
from django.db.models import Q
books = Book.objects.filter(Q(price__lte=10) | Q(rating__lte=9))
#价格小于等于100 或 评分小于等于9分 
```

实现非效果。

```python
# 获取书名包含“记”，但是id不等于3的图书
books = Book.objects.filter(Q(name__contains='记') & ~Q(id=3))
```

## 聚合函数

聚合函数用于统计。聚合函数都是在`.aggregate(cls)`或者`annotate(cls)`方法中执行的。



在使用聚合函数前，先要导入相应的类，`from django.db.models import xxx`

常用聚合函数：

* `Avg(field)`：求平均值

  ```python
  from django.db.models import Avg
  result = Book.objects.aggregate(Avg('price'))	#求取价格平均值
  print(result)
  ```

  上例的result得到的是一个字典，键值对为`{'price_avg':23}`，其中键的格式默认为`field-func`，如果想要修改，可以**以关键字参数的形式为Avg中赋值**。例如

  ```python
  result = Book.objects.aggregate(my_avg=Avg('price'))
  print(result)	#{"my_avg":23}，这里的键变为了 my_avg
  ```

* `Count(field,distinct=False)`：获取指定的对象的个数。distinct参数默认为False，表示会统计重复的表项，设置为True之后，只会统计不重复的表项。

  ```python
  from django.db.models import Count
  result = Book.objects.aggregate(book_num=Count('id'))
  ```

* `Max(field)`、`Min(field)`：获取指定字段的最大值、最小值。

  ```python
  from django.db.models import Max,Min
  result = Author.objects.aggregate(Max('age'),Min('age'))
  print(result)	#{"age__max":88,"age__min":18}
  ```

  注意，`aggregate`函数的参数中写了不止一个类。

* `Sum(field)`：求指定字段的和。

  ```python
  from djang.db.models import Sum
  result = Book.objects.aggregate(total=Sum("price"))
  ```



聚合函数aggregate和annotate的区别：

* aggregate：会对整个字段进行统计，不分组。简单

* annotate：（1）会根**据当前模型的主键进行分组**（sql的group by语句）（2）**会在每个模型添加一个字段**

  ```python
  result = Book.objects.annotate(total=Sum("bookstore__price")).values("name","total"
  )
  ```

  上例中，有两点值得注意。（1）Sum()的参数利用了ORM的关联查询，每本书得到自己在商城的多种售价（2）每个模型对象会新增一个total字段，但是为了便于显示，只提取了name、total两个字段。



更多聚合函数参考[官网](https://docs.djangoproject.com/zh-hans/2.0/ref/models/querysets/)

## QuerySetAPI

在查询操作时，我们通过`model_name.objects`的方式，这个object叫做模型管理器，是一个`django.db.models.manager.Manager`对象**，而`Manager`类是一个空壳类，本身没有任何属性和方法。**它的方法全部从 QuerySet 类（结果集）中拷贝过来的（原理是元类）。

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/Manager%E4%B8%8EQuerySet.png" alt="image-20200511171212935" style="zoom:67%;" />



QuerySet的API调用返回的依旧是QuerySet，执行链式调用会很方便。

QuerySet常用的API：

* **create**：创建1条数据，并且保存到数据库中，结果返回1个实例。这个方法相当于先用指定的模型创建1个对象，赋值，然后保存。

  ```python
  #与上面等效
  article = Article.objects.create(title='abc') # 直接入库 
  ```

  

* **update**：批量更新数据。该方法在底层调用的是sql的update语句，不会执行save()方法，所以不会触发`auto_now`设置的时间字段。注意，这是queryset的api，所以条件筛选时要用filter，而不是get（返回一个model实例）

  ```python
  # 找到符合条件的数据然后批量更新，
  Article.objects.filter(category__isnull=True).update(category_id=3)
  ```

* **delete**：删除所有满足条件的数据，在`filter、get、all`等方法后调用 

  ```python
  Author.objects.filter(id__gte=3).delete() #删除所有id>=3的作者
  ```



* filter：条件查询，返回新的queryset。

* exclude：排除满足条件的数据，返回一个新的queryset。效果上相当于filter后取反。

* annotate：给queryset查询集的每个对象都添加一个使用查询表达式（聚合函数、F表达式、Q表达式等）的新字段。例如

  ```python
  articles = Article.objects.annotate(author_name=F("author__name"))
  ```

  book外键关联作者表，存在属性`author`，上述代码将在articles的所有对象中添加一个字段`author_name`，该字段通过F表达式关联查询（注意看双下划线）动态查询得到。

* order_by：将查询集按照某个字段进行排序，默认升序，如果要倒序排列，在前面加个`-`。

  ```python
  # 根据创建的时间正序排序
  articles = Article.objects.order_by("create_time")
  # 根据创建的时间倒序排序
  articles = Article.objects.order_by("-create_time")
  # 首先根据创建的时间进行排序，如果时间相同，则根据作者的名字进行排序
  articles = Article.objects.order_by("create_time",'author__name')
  # 动态生成1个字段 然后排序 
  books=Book.objects.annotate(order_nums=Count('bookorder__id')).order_by('-order_nums')
  ```

  如果调用了多个order_by，后面的排序将会覆盖前面的。例如会依据name排序而不是create_time。

  ```python
  articles = Article.objects.order_by("create_time").order_by("author__name")
  ```

  

* values：指定提取查询集的哪些字段，默认情况下（参数留空）会把表的所有字段提取。一旦使用`value`方法，返回的查询集（queryset）的元素不再是模型对象，而是字典。可以使用“关键字参数+F表达式”重命名字典的键名。

  ```python
  articles = Article.objects.values("title",'content',author_name=F('author_name'))
  for article in articles:
  	print(article)
      
  #将会打印 {"title":"abc","content":"xxx",'author_name':'xxx'}
  ```

* values_list：类似于values，只不过查询集中存储的不是字典，而是元组。如果指定字段只有1个，可以设置参数`flat=True`使查询集扁平化，也就是查询集的元素就是字段值而不是元组。

  ```python
  articles1 = Article.objects.values_list("title")
  # <QuerySet [("abc",),("xxx",),...]>
  
  #使用参数flat=True
  articles2 = Article.objects.values_list("title",flat=True)
  #<QuerySet ["abc",'xxx',...]>，注意其中的元素
  ```

* all：获模型的所有对象。

* defer：在一些表中，存在多个字段，有一些字段的数据量可能比较庞大，而此时并不需要，这时候就可以使用`defer`来过滤掉该字段。`defer`和`values`的区别是，前者查询集存储的是模型对象（model_object），而不是字典。

  使用defer字段之后，不代表查询集就不能查询过滤掉的字典了，只不过这会重新触发1次查询。

  ```python
  articles = list(Article.objects.defer("title"))	#此处过滤掉title
  for article in articles:
      # 因为在上面提取的时候过滤了title
      # 这个地方重新获取title，将重新向数据库中进行一次查找操作
      print(article.title)
  ```

  

  

* select_related(foreignKey1,)：在提取某个模型的数据的同时，**将相关联的外键模型**从数据库一并取出，存放在内存中。当需要频繁使用外键数据时，这种做法可以减少数据库的查询次数，提升性能。该方法应该在`all()`、`filter()`等数据查询方法前调用。

  ```python
  # article外键关联到作者表中
  #1次sql查询，得到article+author
  article = Article.objects.select_related("author").all()
  article.author.name #不需要重新执行查询语句，相关结果已经存储到内存中
  
  #不用select_related做法
  articles=Article.objects.all() #先得到article的所有字段数据
  for article in articles:
      print(article.author.name)  #author.name又会引起1次sql查询
  ```

* prefetch_related(cls_set)：和select_related类似，也是为了减少数据库的查询次数。但是是为了一对多、多对多的反向查询（得到那个多），可以避免后续[`model_set`](###一对多)属性引起的多次查询。

  ```python
  # 文章 和 标签的关系 是一对多
  # 在使用filter查询数据之前，调用预加载函数，获取它的“多”
  # 过程中会发生两次查询，一次是得到所有的tag_set，一次是得到所有的name（假设这也是一个外键）
  articles = Article.objects.prefetch_related("tag_set__name").\
  			filter(title__contains='hello')	
  #注意下面这段语句 预加载与不预加载的区别
  for article in articles:
      print('title:%s' % article.title)	#打印文章的名字
      #打印该文章的所有标签
      #下面语句的tag_set()会直接从内存中取数据 
      #如果没有预加载，每篇文章都会去数据库查询
      for x in article.tag_set.all():print(x.name)
  ```

  注意，后续的`tag__set`方法只可以使用`all()`，如果使用了类似`.filter`等会返回新的queryset的方法会破坏原先的预加载，重新去数据库中查询，**也就是说prefetxh预加载的数据集是静态的all**。

  

  

* aggregate：使用聚合函数

* 切片：`[i:j]` 

* union(queryset)：类似集合的union，合并两个querySet



## 模型迁移

### 迁移命令

以`python manage.py 'command_here'`执行迁移命令：

* `makemigrations [appname]`：将`models.py`定义的模型生成迁移文件，记录模型变更信息，存储于`app/migrations`文件夹中。**模型所在的app要在settings.py中安装，否则不会检测其变化**。参数appname若不指定，就会默认对所有安装app执行迁移。

* `migrate`：将迁移文件的变更信息映射成实际操作到数据库中常用选项如下：

  * appname：同migrations
  * --fake py_name：将指定的迁移脚本添加到数据库**`django-migrations`表**中，**fake表示伪造的意思，仅在数据库中登记，不会转为SQL语句去执行**
  * --fake-initial：类似于--fake，但是仅将第一次生成的迁移文件`0001_initial.py`登记在`django-migrations`表中。

  

django的`migrations`命令采用增量更新的方式，在模型层作出的改动都会生成一个新的迁移文件，然后再以此映射到数据库中。但是，这不是完美的，**如果我们越过migrations这一层，直接去改动数据库，就会造成迁移文件版本与数据库版本不一致，执行时出现预料之外的偏差。**

例如，手动删除数据库的某些字段，然后再在模型中注释掉该字段（模拟删除字段），迁移文件就会转为SQL语句尝试去数据库中删除该字段，但其实该字段已经不存在了，此时执行`migrate`就会报错。

解决的办法：

1. 查看表的结构，然后以此修改我们的模型类
2. 删除`django-migrations`**指定app**的所有迁移记录。以前的迁移记录此时对我们意义不大
3. 删除`appname/models.py/migations`下所有的迁移脚本，然后执行`makemigrations [your appname]`，就会生成1个新的迁移文件，应该是`0001_initial.py`，表示初始化文件
4. **我们不必去执行`migrate`让迁移文件映射到数据库**，因为表已经存在了。执行`migrate appname --fake-initial`，将初始迁移脚本的执行记录登记在`django-migrations`表中。
5. 至此，**数据库版本和迁移文件版本再次同步**。



### 反向生成模型

数据库在模型创建前已经存在，需要依据旧的数据库来反向创建模型，便于使用django的ORM管理。

反向生成模型的步骤：

1. 配置好项目的数据库信息，进入项目所在路径，终端环境下执行命令`python manage.py inspectdb [your_table]`来自动检测表，参数table可以选择只检测某个表。执行命令后，终端会输出相应的模型类代码。如下

   ```python
   #执行python manage.py inspectdb front_heroinfo 后显示的代码
   class FrontHeroinfo(models.Model):
       hname = models.CharField(max_length=20)
       hgender = models.IntegerField()
       hcomment = models.CharField(max_length=100, blank=True, null=True)
       isdelete = models.IntegerField(db_column='isDelete')  # Field name made lowercase.
       hbook = models.ForeignKey('FrontBookinfo', models.DO_NOTHING)
   
       class Meta:
           managed = False
           db_table = 'front_heroinfo'
   ```

   在表较多的时候，代码生成较多，可以选择重定向到文本`python manage.py inspectdb >file.txt`，然后再复制粘贴相应模型代码到对应的`app/models.py`文件中

2. 修正模型类的相关属性，一般会考虑如下属性：

   * 模型名：默认的模型名是表名的大驼峰命名，可以改成易理解的模型名。只要`class Meta:db_table`是数据库真正的表名即可
   * 外键约束：检查外键指向的模型类，如果不是一个app内的，改成完整路径`app.modelname` 。如果是多对多型的外键，默认生成的模型代码会创建一个外键指向中间表，这在ORM中中是多余的。删除相应代码，然后改成的`ManyToManyField('modelname',db_table='中间表名字')` 。
   * 让django接管模型：删除`class Meta`下的` managed = False` 。如果保留，migrate命令将不再对该模型有效。

3. 执行`python manage.py makemigrations`，为app生成初始迁移文件`0001_initial.py`，然后伪造该映射，`python manage.py migrate appname --fake-initial` 。
4. 除了一些业务所需的表外，django一些核心的表也是需要创建的，例如`django-auth`等。步骤3已经创建了核心表的映射文件（没有指定具体的app），并伪造了业务表的映射，所以接下来执行`python manage.py migrate`会避开业务表的创建，只会生成相应的核心表。至此，django可以完美的使用ORM接管数据库。



# 视图高级

## WSGIRequest对象

**Django在接收到http请求之后，会根据http请求携带的参数以及报文信息创建一个 WSGIRequest对象**，并且作为视图函数第一个参数`request`传给视图函数。



WSGIRequest对象常用属性：

* path：请求路径，不含域名、查询参数部分。例如`/music/`

* **method**：返回一个字符串，代表当前的请求方式，**例如`GET`、`POST`**

* GET：**一个`django.http.request.QueryDict`对象，继承自原生类型`dict`，包含了所有查询参数，以`request.GET.get(key)`的形式访问** 

* **POST：**[QueryDict对象](##QueryDict对象)，包含了POST方式上传的所有参数，以`request.POST.get(key)`的形式访问

* **FILES：**QueryDict对象，**包含了所有上传的文件**，参考官方文档：https://docs.djangoproject.com/en/3.1/ref/files/uploads/ 

* COOKIES：dict类型，包含所有的cookie，键值对都是字符串类型

* session：一个类似dict的对象，用来操作服务器的session

* **META**：**存储客户端请求时所有的头部header信息**

  * CONTENT_LENGTH：请求的正文长度（是一个字符串）

  * CONTENT_TYPE：请求正文的MIME类型

  * HTTP_ACCPET：响应可接收的Content-Type

  * HTTP_ACCEPT_ENCODING ：响应可接收的编码

  * HTTP_ACCEPT_LANGUAGE ： 响应可接收的语言。

  * HTTP_HOST ：客户端发送的HOST值。

  * HTTP_REFERER ：从哪个页面跳转而来，可用于判断爬虫。

  * QUERY_STRING ：单个字符串形式的查询字符串（未解析过的形式）

  * REMOTE_ADDR ：客户端的IP地址。如果服务器使用了 nginx 做反向代理或者负载均衡，那么这个值返回的是 127.0.0.1 ，这时候可以使用 HTTP_X_FORWARDED_FOR 来获取，所以获取 ip 地址的代码片段如下：

    ```python
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
    	ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
    	ip = request.META['REMOTE_ADDR']
    ```

  * REMOTE_HOST ：客户端的主机名。

  * SERVER_NAME ：服务器域名。

  * SERVER_PORT ：服务器端口号，是一个字符串类型。



WSGIRequest对象常用方法：

* is_secure()：是否采用https协议
* is_ajax()：是否采用ajax发送的请求，原理就是判断请求头中是否存在 X-Requested-With:XMLHttpRequest 
* get_host() ：服务器的域名。如果在访问的时候还有端口号，那么会加上端口号。比如 `www.baidu.com:9000 `
* get_full_path() ：返回完整的path。**如果有查询字符串，还会加上查询字符串**，比如 /music/bands/?print=True 。[参考](https://www.cnblogs.com/gcgc/p/10766769.html) 
* build_absolute_uri(path)：将一个相对路径的path构建成完成的url，包含scheme(`http://`)、host(`lo`)等。
* get_raw_uri() ：获取请求的完整 url 。





## HttpResponse对象

**django返回给浏览器的响应必须是HttpResponseBase或者它的子类对象，而HttpResponse是最常用的子类。**



HttpResponse常用属性：

* content：返回的内容。

* status_code：返回的HTTP响应状态码。

* content_type：返回的数据的MIME类型，默认为` text/html `。浏览器会根据这个属性，来渲染数据

  * text/html（默认的，html文件）
  * text/plain（纯文本）
  * text/css（css文件）
  * text/javascript（js文件）
  * **multipart/form-data（文件提交）**
  * **application/json（json数据）**
  * application/xml（xml文件）
  * image/图片格式后缀

* 设置响应头：`response['headername'] = 'value'` 

  ```python
  response = HttpResponse(content_type='text/csv')	#创建response对象
  # 设置响应头
  response['Content-Disposition'] = 'attachment; filename="hdu_transcript.csv"'
  ```

  

HttpResponse常用方法：

* set_cookie：用来设置浏览器的 cookie 信息
* delete_cookie：用来删除cookie信息
* write：HttpResponse 是一个类似于文件的对象，可以调用`.write('content')`到html的数据体（content）中。与`HttpResponse('content')`等效。



***

**JsonResponse**：将python对象序列化成json字符串，然后再封装成一个Response对象返回给浏览器。

使用JsonResponse示例

```python
from django.http import JsonResponse
def index(request):
    # return JsonResponse(persons,safe=False) # 对非字典序列化 指定safe参数 
	return JsonResponse({"username":"zhiliao","age":18},status=200)	#直接丢进去字典 可以返回状态码
```

****



csv返回示例

```python
import csv
from django.http import HttpResponse
def csv_view(request):
    #创建1个response对象
    response = HttpResponse(content_type='text/csv')	#指明内容类型
    # 告诉浏览器 这是一个附件不必显示在页面 ；文件的名字是somefilename.csv
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    
    #创建一个csv句柄 
    writer = csv.writer(response) # 写入response
    writer.writerow(['username', 'age', 'height', 'weight'])	#写入一行
    writer.writerow(['zhiliao', '18', '180', '110'])
    
    return response
```



上述方案在csv数据较大时就会造成页面响应时间过长，造成请求超时。这时候就要使用我们的`StreamingHttpResponse`类，**这个对象是将响应的数据作为一个流返回给客户端，而不是作为一个整体返回。**
StreamingHttpResponse与HttpResponse的区别：

1. 这个类没有content属性，取而代之的是`streaming_content`
2. **这个类的 streaming_content 必须是一个可以迭代的对象。**
3. 这个类没有 write 方法(HttpResponse支持write到content中)，如果给这个类的对象写入数据将会报错
4. StreamingHttpResponse 会另外启动一个进程来和客户端保持长连接，在请求量较大时，会对服务器造成较大压力



使用StreamingHttpResponse来返回1个大csv文件示例。我们使用了一个生成器（一个用圆括号包裹的推导式）来作为`streaming_content`的参数，服务器在生成数据时不必一次全部生成，有利于性能提升。

```python
def get_large_csv(request):
    response=StreamingHttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    
    #一个生成器
    csv_data=('user:{},country:{}\n'.format(i,i+1) for i in range(10**6))
    response.streaming_content=csv_data # 写入response 
    return  response
```





## method装饰器

```python
# 多种method 参数是一个列表 
from django.views.decorators.http import require_http_methods
# 只是一种method
from django.views.decorators.http import require_GET，require_POST,require_safe

@require_http_methods(["GET",'POST'])	
def my_view(request):	#该视图函数只能以GET POST的形式访问
	pass

@require_GET
def my_getview(request):pass

@require_POST
def my_postview(request):pass

@require_safe	#相当于GET HEAD
def my_safeview(request):pass
```



## 类视图

django除了支持函数形式的视图外，**还支持类视图**。**类视图可以灵活使用类的特性，例如封装、继承等，写起来会更优雅。**

### View

`django.views.generic.base.View`是主要的类视图，所有的类视图都继承自它，包括自定义的类视图。

**类视图通过实现不同的函数来支持不同的请求（method）**，一共有`['get','post','put','patch','delete','head','options','trace']`。。

```python
class AddBookView(View):
    def post(self,request,*args,**kwargs):
        return HttpResponse("书籍添加成功！")
    def http_method_not_allowed(self, request, *args, **kwargs):
        # 如果用户访问了视图中没有定义的方法，就会执行这个方法 非必须 可以选择重写        
        return HttpResponse("您当前采用的method是：%s，本视图只支持使用post请求！" % reque
    st.method)
```



**类视图在定义路由时要`.as_view()`转换。**

```python
# urls.py
    urlpatterns = [
		path("xx",views.BookDetailView.as_view(),name='detail')
		]
```



### TemplateView

`django.views.generic.base.TemplateView`，这个类视图专门用于返回模板。

在这个类视图中，有两个属性经常用到：

1.  `template_name `，**这个属性是用来存储模版的路径**，TemplateView 会自动的渲染这个变量指向的模版。
2. `get_context_data()` ，这个方法是用来返回上下文数据的，也就是在给模版传的参数的。



自定义一个类视图继承自TemplateView

```python
from django.views.generic.base import TemplateView
class HomePageView(TemplateView):
	template_name = "home.html"		#要渲染哪个模板
    def get_context_data(self, **kwargs):	#模板需要的上下文数据在这里定义
        context = super().get_context_data(**kwargs)
        context['username'] = "黄勇"
        return context
```

urls.py 中映射代码为

```python
from django.urls import path
urlpatterns = [
	path('', HomePageView.as_view())
]
```



如果模板中不需要任何上下文参数，可以直接使用TemplateView类。 

```python
urlpatterns = [
	path('', TemplateView.as_view(template_name="index.html"))
]
```



## 类视图装饰器

如果进行method限制，只需要定义允许的method函数即可。



这里的装饰器并非限制method。

下例使用装饰器装饰dispatch函数，在进行分发前，判断用户是否登录，若有则显示页面，否则重定向注册页面。

```python
from django.utils.decorators import method_decorator

#定义装饰函数
def login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user:	# 如果用户登录了，返回原视图
            return func(request,*args,**kwargs)
        else:
            return redirect(reverse('login'))	#如果用户没有登录，重定向
    return wrapper
    
@method_decorator(login_required,name='dispatch')	#装饰dispatch方法
class IndexView(View):
    def get(self,request,*args,**kwargs):
        return HttpResponse("index")
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request,*args,**kwargs)
```



## 错误处理

常用错误码：

* 404：没有指定的url（`from django.http import Http404`）
* 403：没有权限访问相关数据 
* 405：请求的Method错误
* 400：bad requet
* 500：服务器内部出错
* 502：：一般部署的时候见得比较多，一般是 nginx 启动了，然后 wsgi 有问题。

在碰到比如404、500错误的时候，可以直接在`templates`文件夹下创建相应错误代码的html文件，如`404.html`，以后发生错误时，就会返回自定义模板文件。如果要看到404页面，记得要设置`settings.py`中的DEBUG=FALSE，否则会直接提示报错。

对于其他错误，可以创建1个app集中处理：
1. 创建app，假设叫做`errors`。然后创建模板文件夹`templates`，定义各种错误的html文件
2. 我们的目的是让其他视图函数出现错误时跳转到我们自定义的errors的视图函数，因此，我们需要编写urls.py 、views.py等文件。

下面是一个定义403错误的示例。
errors/views.py中定义视图函数

```python
def 403_view(request):
	return render(request,'403.html',status=403)	#省略模板，只需知道从此处渲染一个模板回去即可
```
errors/urls.py
```python
app_name='error'
urlpatterns=[path('403.html',403_view,name='403_error')]
```


入口urls.py文件

```python
urlpatterns=[path('error',include('error.urls'))] #
```

在其他需要跳转的app/views.py中

```python
def index(request):
	if request.GET.get('usernamem'):
		return HttpResponse('welcome')
    else:
    	return redirect(reverse('error:403_error'))	#app_name:urlname
```

# 表单

## Form 
django的表单类Form用于**验证前端提交的数据合法性** 

1. 创建一个app/forms.py文件，定义**表单类Form** 
```python
from django import forms
# 自定义表单类
class MessageBoardForm(forms.Form): # 继承Form类 
    # 字段名要和前端表单字段一致 不然 request.POST.get('filed_name') 取不到数据 
    
    # Field字段类型是验证数据的第一步
    # `error_message={'property':'reason'}`是一个字典，用于字段验证失败时返回前端 
    title = forms.CharField(max_length=3,label='标题',min_length=2,
                            error_messages={"min_length":'标题字符段不符合要求！'})
    content = forms.CharField(max_length=100) #字符串
    email = forms.EmailField(label='邮箱') #邮箱格式
    reply = forms.BooleanField(required=False) #require表示非必填
```
2. 视图函数 使用 表单类 。

```python
class FormView(View):
    def get(self,request):
    	#渲染一个模板，然后返回
        return render(request,'myform.html')	

    def post(self,request):  #当用户提交数据过来时，进行验证
        form=MessageBoardForm(request.POST) # 验证表单数据 
        if form.is_valid():    #如果验证通过，就显示 表单数据
            keys=['title','content','email','reply']
            for key in keys:
                # cleaned_data表示验证过的数据，是一个字典
            	# 且会自动转换类型 str-->your_field
                print('{}: {}'.format(key,form.cleaned_data[key]))
            return HttpResponse('success')
        else:
            #errors是一个字典 调用get_json_data可以显示具体的错误信息
            print(form.errors.get_json_data())
            return HttpResponse('failed')

```




表单常用字段：

* CharField：字符串类型
	* max_length、min_length：字段的最大长度、最小长度；
	* required：字段是否是必须的
	* error_messages：字段验证失败的时候的错误信息
 * EmailField：字符串类型，但会验证字符串是否含有@符号
 * FloatField：浮点类型，若验证通过，会自动转化str为float
    * max_value、min_value：最大值、最小值
 * IntegerField：整型；同Float
 * URLField：接收url形式的字符串



## 自定义验证

**一些场合，简单的字段验证无法满足要求，如用户手机号是否已经注册，这种复杂的逻辑就要用到自定义验证。**

自定义验证分两种情况：

1. **仅仅需要对其中几个字段进行验证**，在类中定义方法`clean_fieldname`，后面跟字段名。基本的逻辑是，验证成功，返回该字段，否则抛出异常。

   验证用户手机号是否已经注册示例：

   ```python
   class MyForm(forms.Form):
       #定义字段
       telephone = forms.CharField(max_length=11)
   
       def clean_telephone(self):  #定义字段验证方法
           #已经通过了类型验证，所以直接使用cleaned_data是可以取到的
           telephone = self.cleaned_data.get('telephone')
           #手机号是否已经注册
           exists = User.objects.filter(telephone=telephone).exists()  
           if exists:
               raise forms.ValidationError("手机号码已经存在！")  #抛出异常
           else:
               return telephone    #成功，就返回该字段数据
   ```

2. **验证类中的多个字段，**重写父类的clean()方法，该方法会在所有字段验证通过（字段验证+clean_fieldname）后才执行。比如，注册的时候，验证两次密码输入的是否一致。

   ```python
   class MyForm(forms.Form):
       telephone = forms.CharField(max_length=11)
       pwd1 = forms.CharField(max_length=12)   #密码1
       pwd2 = forms.CharField(max_length=12)   #密码2
       
       def clean(self):        #重写父类clean()方法
           cleaned_data = super().clean()	#先调用父类的方法
           pwd1 = cleaned_data.get('pwd1')
           pwd2 = cleaned_data.get('pwd2')
           if pwd1 != pwd2:
               raise forms.ValidationError('两次密码不一致！')	#抛出异常 
          	else:
               return cleaned_data	#记得最后返回数据，form.is_valid()调用
   ```


## ModelForm

**大部分时候，表单是为了服务于模型Model，其中的字段也往往与模型的字段高度重合**。

这时候我们就可以使用Form类中的`ModelForm`实现表单与模型的绑定。



例如，有模型类Article，定义如下

```python
from django.db import models
from django.core import validators
class Article(models.Model):
    # 模型层的字段
    title = models.CharField(max_length=11)
    content = models.TextField()
    author = models.CharField(max_length=100)
```

定义ModelForm类，该类会从模型类自动生成Form的字段（不包含id）

```python
from django import forms
class MyForm(forms.ModelForm): #继承自ModelForm
    # 也可以添加额外的字段
    # id=forms.IntegerField()
    class Meta:
        model = Article  #模型类
        fields = "__all__"  #所有字段
        # fields=['title','content'] #指定字段
        # exclude=['price']   #排除这些字段  
        
        #自定义字段错误信息
        error_messages = {
            'title': {
                'max_length': '最多不能超过10个字符！',
                'min_length': '最少不能少于3个字符！'
            },
            'content': {
                'required': '必须输入content！',
            }
        }
```



**ModelForm 的` save()`方法，可以在验证完成后调用将数据直接入库。**不过并不常用。

```python
def post(self,request):
    form = MyForm(request.POST)
	if form.is_valid():
		form.save()	#数据入库
		return HttpResponse('success')
	else:
		print('fail')	#错误信息
		return HttpResponse('fail')
```

**save()方法必须要在`is_valid()`验证后使用**，否则会报错。而且既然数据要入库，就要求`form.cleaned_data`包含所有（必填）字段。否则，就需要在save()的时候设置参数`commit=False`。这样子save就只会生成1个model实例，但不会入库。然后手动地再补充缺失字段，调用save()即可。如

```python
form = MyForm(request.POST)
if form.is_valid():
    article = form.save(commit=False)
    article.category = 'Python'	#补充缺失字段
    article.save()	#保存
    return HttpResponse('succes')
else:
    return HttpResponse('fail')
```



## 文件上传

前端实现

[ajax后台文件上传](./html&css&js学习笔记.md)。文件上传要用js的`FormData()`对象，来添加表单的键值对信息。

```js
var submit_btn = $('input[name="submit"]')
submit_btn.click(function (event) {
            event.preventDefault();  //禁止默认行为
            var  form=new FormData();
   			//添加键值对
            form.append('username',$('input[name="username"]').val());
            form.append('file',$('input[name="file"]')[0].files[0]);  // 文件对象
    		//添加csrftoken信息 
            form.append('csrfmiddlewaretoken',
                        $('input[name="csrfmiddlewaretoken"]').val());

            $.ajax({
                'url':'/filerec/',
                'data':form,  //数据
                'type':'post',
                'processData': false, //很重要，告诉jquery不要对form进行编码处理
                'contentType': false, //很重要，指定为false才能形成正确的Content-Type
                'error':function (xhr,status,error) {
                        console.log('状态码：',status);
                        console.log(error);
                },
                'success':function (result,xhr,status) {
                    console.log(result);
                }
            });
        })
```



****

后端实现

在不添加表单类验证的情况下，取文件非常简单，注意用`request.FILES`而不是[`request.POST`](##WSGIRequest对象)

```python
def filerec(request):
    file=request.FILES.get('file') # file是前端input name
    with open(file.name,'wb') as f:
        for chunk in file.chunks():f.write(chunk)

    return HttpResponse('success')
```

当需要表单来验证包含文件上传的控件时，使用`FileField`字段

```python
class MyForm(forms.Form):
    username=forms.CharField(required=False)
    file=forms.FileField()  # 
```

视图函数验证

```python
def filerec(request):
    form=MyForm(request.POST,request.FILES) #验证普通键值对+文件
    if form.is_valid():
        # 存取文件
        file=request.FILES.get('file')
        username=form.cleaned_data['username'] #注意两者的取
    else:
        return HttpResponse('failed')
```






# memcached
memcached 是一个**高性能的分布式的内存对象缓存系统**，可以分担数据库的压力。memcached通过在内存里维护一个统一的巨大的hash表，来存储各种各样的数据。

memcached适合存储不太重要但访问频繁的数据，如验证码、用户的sessionID

## 安装和启动memcached
windows：进入exe所在文件路径（[<1.45版本](https://blog.csdn.net/l1028386804/article/details/61417166)） 
* 安装：memcached.exe -d install
* 启动：memcached.exe -d start





linux(以Ubuntu为例)：

* 安装： sudo apt install memcached

* 启动：进入安装目录下执行，可以设置启动参数

 linux下启动的参数设置：


* -d ：这个参数是让 memcached 在后台运行。

* -m ：指定占用多少内存。以 M 为单位，默认为 64M 。

* -p ：指定占用的端口**。默认端口是 11211** 。

* -l ：别的机器可以通过哪个ip地址连接到我这台服务器。如果是通过 `service memcached start` 的方式，那么只能通过本机连接。如果想要让别的机器连接，就必须设置 `-l 0.0.0.0`

```shell
# 默认的安装目录 
cd /usr/local/memcached/bin
/usr/bin/memcached  -u jianghuikai -p 11222 start	#指定端口、用户执行
```



## telnet操作memcached

* 连接（linux下执行）：`telnent [ip地址] [端口11211]`

* 添加数据：**memcached的数据类似于字典，是以键值对的形式存储**，但可以额外指定过期时间等参数

  * set：如果键已经存在，会覆盖

    ```shell
    set key flas(是否压缩) timeout value_length
    
    #示例 终端执行> 表示回车换行
    > set username 0 60 7
    > zhiliao
    > STORED（提示成功添加）
    ```

  * add：如果键已存在，报错，否则，添加成功

    ```shell
    add key flas(0) timeout value_length
    
    #示例 
    > add username 0 60 7
    > xiaotuo
    ```

* 数据获取、删除：get、delete

  ```shell
  get key
  # get username
  
  delete key
  # delete username
  ```

* 查看当前的memcached状态：stats 

  ```shell
  stats items
  stats cacheddump [items_id] 0	
  #第一步表示查看所有键
  #第二步0表示查看该键（用id表示）下所有的值
  ```

## python操作memcached

* 安装：`pip install python-memcached`

* 建立连接实例：memcache可以集群分布，因此连接的ip是一个列表

  ```python
  import memcache
  mc=memcache.Client(['127.0.0.1:11211','192.168.174.130:11211'],debug=True)
  ```

* 添加数据：set、set_mullti ；和直接使用telnent操作有所区别的是，我们不用再设置var_length。如果连接的有多个ip，添加的数据会依据memcached的算法分配到某一台机器

  ```python
  mc.set('username','hello world',time=60*5)	
  #批量添加数据
  mc.set_multi({'email':'xxx@qq.com','telphone':'111111'},time=60*5)
  ```

* 获取数据、删除数据

  ```python
  #mc是一个实例
  mc.get('key')
  mc.delete('key')
  ```

* 自增长：适用于数字型

  ```python
  mc.incr('read_count',delta=10)	#+10
  mc.decr('read_count',delta=10	#-10
  ```

  

## memcached安全性

memcached的连接不需要用户名密码，只要对方的ip:port即可，因此，需要考虑其安全性。这里有两种解决方案：

1. 启动的时候设置`-l 0.0.0.0`只允许本机访问

2. 使用linux下的防火墙，关闭默认的11211端口，然后开启其余端口。黑客即使攻击的时候也要扫描端口

   ```shell
   #linux 防火墙相关命令
   ufw enable # 开启防火墙
   ufw disable # 关闭防火墙
   ufw default deny # 关闭没有开启的端口
   
   ufw deny 端口号 # 关闭某个端口
   ufw allow 端口号 # 开启某个端口
   ```



## django中使用memcached

1. pip install python-memcached

2. 在settings.py 文件配置 如下

```python
CACHES = {
'default': {
'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
'LOCATION': '127.0.0.1:11211',	#memcached所在机器ip:port
}
}

'''
如果想使用多台机器，LOCATION可以设置成一个列表（分布式）
'LOCATION': [
'172.19.26.240:11211',
'172.19.26.242:11211']
'''

```



使用示例 

```python
from django.core.cache import cache
#也可用于测试本机的memcached服务是否正常
def index(request):
    cache.set('abc','zhiliao',60)   #添加数据，键值对+过期时间
    print(cache.get('abc')) #看看是否已经存储进memcached
    response = HttpResponse('success')
    return response
```

dajngo在底层实际存储键值对的时候会额外给键增加一个前缀、版本号，通过`cache`的api调用可以忽略它。

如果想要更改这个规则，可以在`settings.CACHES`中添加KEY_FUNCTION 键值对，设置处理函数。

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_FUNCTION': lambda key, prefix_key, version: "django:%s" % key
    }
}
```

# cookie 和 session

## cookie

**cookie的出现是为了解决http前后请求无状态的问题。**

客户端第一次和服务器连接成功后，服务器会返回一些数据给浏览器，用于浏览器本地保存。当浏览器发起后续请求时，就会自动地携带上次存储的数据，服务器根据这部分数据来判断当前用户信息。而这部分数据就是cookie。

**cookie的存储量有限，只适合存储小数据**。



在django中操作cookie：

* 设置cookie：cookie是要返回给浏览器的，所以要设置在response中。通过`response.set_cookie(key,value,[max_age,..])`来设置。该函数的各个参数意义如下：

  * key：cookie的键
  * value：cookie的值
  * max_age：cookie的生命周期，单位是秒。默认是None，浏览器关闭时失效 
  * expires：过期时间；需要传递`datetime`格式的日期，如果同时设置了expires和max_age，将以expires为准
  * path：设置的cookie在请求哪个path时有效，默认域名下所有路径有效
  * domain：针对哪个域名有效。默认是针对主域名下都有效，如果只要针对某个子域名才有效，那么可以设置这个属性
  * secure：是否是安全的，如果设置为 True ，那么只能在 https 协议下才可用
  * httponly：默认False。如果为 True ，那么在客户端不能通过 JavaScript 操作cookie

  ```python
  def set_mycookie(request):
      response=HttpResponse('success')
      response.set_cookie('user','jhk',max_age=180) # 设置cookie
      return response
  ```

  

* 删除cookie：`response.delete_cookie(key)` 。实际上，删除cookie就是将指定key的value设置为空，并且立即过期。

  ```python
  def delete_mycookie(request):
      response=HttpResponse('delete cookie!')
      response.delete_cookie('user')
      return response
  ```

* 获取cookie：**服务器获取的cookie是浏览器请求时携带的，所以要从request上获取，注意区分。**`request.COOKIES`也是一个类似于字典的类

  ```python
  cookies = request.COOKIES
  for cookie_key,cookie_value in cookies.items():
  	print(cookie_key,cookie_value)
  ```

  

## session

session的作用和cookie有点类似，都是为了存储用户信息。**不过，cookie是存储在本地浏览器，而session是一个服务器存储的解决方案**，为了解决cookie存储数据不安全的问题。session事实上是一个概念，不同的语言有不同的实现。

在如今的企业中，一般有两种存储方式：

1. 存储在服务端：**cookie仅仅存储一个sessionid**，session的具体数据则是存储在后台的数据库中。这种专业术语叫做`server side session`
2. 存储在客户端：将session数据加密，然后存储在cookie中，这种专业术语叫做`client side session`。flask默认采用的就是这种方式。

无论是上面哪两种方式，都能说明使用session要比使用cookie来的安全。第一种方式，即使黑客攻破cookie，拿到的也只是sessionid，而不能拿到数据，如果说要拿着这个sessionid来伪装请求，这个也是不可能的，可以参见后文的[CSRF攻击](##CSRF攻击)。第2种方式，就意味着黑客要在session过期之前，攻破cookie加密、session数据加密，这个难度并不小。



在django中操作session：django的session数据是存储在服务端的数据库中的。客户端请求时携带cookie，该cookie含有sessionid，django会依据该sessionid从后台取数据。

* 设置session：**在request中设置，和cookie的设置有所区别**。通过`requets.session[key]=value`来设置 

  ```python
  def index(request):
      request.session['username']='jhk'
      return HttpResponse('session ok')
  ```

* **request.session是一个类似字典的对象**，它的其他常用方法：

  * get(key)：从session中获取指定值
  * pop(key)：从session中删除一个值
  * clear：将当前sessionid的数据置空
  * flush：删除该sessionid下的所有数据
  * set_expire(value)：设置过期时间
    * 整型：多少秒后过期，可以为负数，表示立刻过期
    * 0：当浏览器关闭时，session过期
    * None：使用默认的设置，2周过期。可以更改`settings.py/SESSION_COOKIE_AGE`
  * clear_expired：清除过期session。或者在终端，执行p`ython manage.py clearsessions `来清除过期的 session 。



修改session存储机制

session数据默认是存储到数据库中的，不过这可以通过在settings.py文件中增加变量`SESSION_ENGINE`配置，例如
```python
#settings.py 文件
SESSION_ENGINE='django.contrib.sessions.backends.cache'
```
可用配置方案如下：
1. django.contrib.sessions.backends.db ：使用数据库。默认就是这种方案。
2. django.contrib.sessions.backends.file ：使用文件来存储session。
3. django.contrib.sessions.backends.cache ：使用缓存来存储session。想要将数据存储到缓存中，前提是你必须要在 settings.py 中配置好 CACHES ，并且是需要使用 Memcached
4. django.contrib.sessions.backends.cached_db：先使用缓存存储数据，再存储到磁盘。可以保证缓存异常下，也能取到数据
5. django.contrib.sessions.backends.signed_cookies：将 session 信息加密后存储到浏览器的 cookie 中。这种方式要注意安全，建议设置 SESSION_COOKIE_HTTPONLY=True ，那么在浏览器中不能通过 js 来操作 session 数据，并且还需要对 settings.py 中的 SECRET_KEY 进行保密，因为一旦别人知道这个 SECRET_KEY ，那么就可以进行解密。另外还有就是在 cookie 中，存储的数据不能超过 4k 。



# 上下文处理器 中间件
## 上下文处理器

上下文处理器（context_processors）是一个函数，以字典的形式返回数据，**供全局模板文件使用**。就是说，在视图函数中，`render(request,'my.html')`即使不传递任何上下文，该模板文件也可以访问到那些系统内置的上下文 
在`settings.TEMPLATES.OPTIONS.context_processors`中，就有许多内置的上下文处理器，作用如下：

1. `django.template.context_processors.debug` ：为context增加一个 debug 和 sql_queries 变量。在模板中可以通过他来查看到一些数据库查询。

2. `django.template.context_processors.request`：为context增加一个变量request，也就是视图函数接收到的第一个参数

3. `django.contrib.auth.context_processors.auth`：django有内置的用户系统，会为context增加一个user对象。当使用内置函数`django.contrib.auth import login`登录时，contenxt的user会变成该user实例

   ```django
   {%if user.is_authenticated%}
   	用户已经登录，做一些事情
   {%end if}
   ```

4. `django.contrib.messages.context_processors.messages`：增加一个message变量

5. `django.template.context_processors.media`：使得模板可以读取`MEDIA_URL`

   ```django
   <img src="{% MEDIA_URL %} abc.jpg">
   类似于使用static标签，后面直接跟相对于media_root的路径
   实际的http请求src=/media/abc.jpg 
   ```

   

6. `django.template.context_processors.static`：使模板可以读取`STATIC_URL`，**用于静态文件配置**

7. `django.template.context_processors.csrf`：在模板中可以使用csrf_token变量来生成一个`csrf_token` 



另外一方面，从内置的上下文处理器原理出发，我们也可以实现自己的上下文处理器。

比如，用户登录时，在所有的模板文件中传递一个变量`{'user':'user_obj'}`，如果不采用上下文处理器的方式，那么就需要在每个模板文件中手动传入变量，工作量很大。
自定义上下文处理器的步骤：

1. 依据上下文处理器属于哪个app，在该app下创建`context_processors.py` 
2. 在`context_processors.py`中开始编写上下文处理器，它本质就是一个函数，该函数只有1个`request`参数，在逻辑的最后，函数一定要返回一个字典（可以为空）。由于系统内置的上下文处理器已经添加了很多键，自定义键名的时候，注意避开相关名字。

```python
def frontuser(request):
    #判断用户是否登录
    userid = request.session.get("user_name")
    userModel = models.FrontendUser.objects.filter(pk=userid).exists()
    if userModel:
        return {'frontuser':userModel}
    else:
        return {}        
```
3. setting.py中配置自己的上下文处理器
```python
'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',  
  				'myapp.context_process.front_user',	#添加自己的上下文处理器
            ],
            'builtins':['django.templatetags.static']
        },
```

4. 在所有模板中，就可以访问`frontuser` 



## 中间件

中间件是request、response处理过程中的一个插件。**可以在request到达视图函数之前，response返回客户端之前，执行自己的行为**。比如，在request到达视图函数前，判断用户是否登录，从而将一个user对象绑定到request上，response返回客户端前，统一设置一些cookie信息。

**中间件的这种处理逻辑刚好可以用装饰器来实现**，也就是在视图函数执行前做点什么，执行后做点什么。



装饰器一共分为“函数型装饰器”、“类装饰器”，因此，中间件的写法也有两种：

1. 使用函数的中间件示例：
```python
def simple_middleware(get_response):
    # 中间件初始化的代码放这里
    def middleware(request):
        # request到达view的执行代码
        response = get_response(request)
        # response到达浏览器的执行代码
        return response
    return middleware
```
2. 使用类装饰器（initial+call）：
```python
class SimpleMiddleware(object):
    def __init__(self, get_response):
        #绑定函数
        self.get_response = get_response
    # 这个中间件初始化的代码
    def __call__(self, request):
        # request到达view之前执行的代码
        response = self.get_response(request)
        # response到达用户浏览器之前执行的代码
        return response
```

中间件的存放可以依据所属app单独编写在`app/middleware.py`下，也可以在项目目录下建立`middlewares`的package。
编写完成后，若要使用中间件，还需在`settings.py/MIDDLEWARE`下配置：

```python
#要放在系统中间件以后
MIDDLEWARE=[,
'myapp.middleware.my_middlewarefunc']
```
中间件的放置是有顺序的，前后之间可能存在依赖关系，自己写的中间件应当放置在MIDDLEWARE的最后。



**就和上下文处理器一样，中间件也无需显式的调用，在任何自定义的视图函数中，访问request都已经是经中间件过手的reqeust，返回的response也是同理。**

另外。如果同时使用了中间件、视图函数装饰器，中间件是优于装饰器执行的，因为中间件是在request到达视图函数前就被执行了。



django内置中间件：
1. django.middleware.common.CommonMiddleware ：通用中间件。作用如下：

   * 限制 settings.DISALLOWED_USER_AGENTS 中指定的请求头（header）来访问本网，用于反爬虫。DISALLOWED_USER_AGENTS是一个正则表达式的列表，默认是没有的，可以自己定义，如：

     ```python
     import re
     DISALLOWED_USER_AGENTS = [
         re.compile(r'^\s$|^$'),	#以空白、空字符开头
         re.compile(r'.*PhantomJS.*')	#请求头中带有这个的
     ]
     ```

   * 浏览器在访问url的时候，没有带上`/`，该中间件会自动带上

2. django.middleware.gzip.GZipMiddleware：将response的响应数据压缩，超过200字符生效（content-encoding：gzip）

3. django.contrib.messages.middleware.MessageMiddleware ：消息处理相关的中间件

4. django.middleware.security.SecurityMiddleware ：做了一些安全处理的中间件。比如设置 XSS 防御的请求头，比如做了 http 协议转 https 协议的工作等。

5. django.contrib.sessions.middleware.SessionMiddleware ： session 中间件，**会给 request 添加一个处理好的 session 对象**。

6. django.contrib.auth.middleware.AuthenticationMiddleware ：**会给 request 添加一个 user 对象的中间件**，可以在验证授权相关的时候判断。

   ```python
   if request.user:
       pass # 用户登录
   else:
       pass # 未登录 
   ```

   

7. django.middleware.csrf.CsrfViewMiddleware : CSRF 保护的中间件

8. django.middleware.clickjacking.XFrameOptionsMiddleware：做了 clickjacking 攻击的保护。

9. django.middleware.cache.UpdateCacheMiddleware，django.middleware.cache.FetchFromCacheMiddleware：缓存中间件，用来缓存一些页面的。



内置中间件的放置顺序：

1. SecurityMiddleware：最前面，不依赖任何其他的中间件。若一个网站同时支持http、https协议，会自动重定向到后者。放在最前面，执行效率自然最高
2. UpdateCacheMiddleware ：应该在 SessionMiddleware, GZipMiddleware, LocaleMiddleware 之前
3. GZipMiddleware 。
4. ConditionalGetMiddleware 。
5. SessionMiddleware 。
6. LocaleMiddleware 。
7. CommonMiddleware 。
8. CsrfViewMiddleware 。
9. AuthenticationMiddleware 。
10. MessageMiddleware 。
11. FetchFromCacheMiddleware 。
12. FlatpageFallbackMiddleware 。
13. RedirectFallbackMiddleware



# 安全

## CSRF攻击

csrf（Cross Site Request Forgery, 跨站域请求伪造）是一种网络攻击方式。

网站通过cookie实现登录功能，而cookie存储于浏览器。只要浏览器访问cookie的服务器时，就会自动携带cookie。这时候，如果有一个别有用心的病毒网站，通过js代码发起了cookie所在服务器的请求（例如银行的转账），浏览器就会不知道这个请求的真假，从而实现在用户不知情的情况下，**实现隐匿的请求**。

防御csrf攻击的要点是“服务器不知道此次请求的真假”。

解决方案是在用户每次访问表单的时候，在网页源码中添加一串随机字符csrftoken，同时也在cookie中设置该字符串。下一次用户在本网页提交表单的时候，**服务器就会比对cookie的csrftoken和表单的csrftokrn是否一致**，若一致，就认为是用户真正的请求，否则，拒绝。这时候，再假设病毒网站试图伪装用户请求，由于**病毒网站事先不知道csrftoken，且js代码不可以操作非本域名下的cookie**，从而也没有任何途径获取到该随机字符串，因此，csrf攻击就失效了。



在django中，防御csrf攻击的步骤比较简单，需要：

1. 在settings.py中开启csrf中间件

   ```python
   MIDDLEWARE=['django.middleware.csrf.CsrfViewMiddleware']
   ```

   中间件的作用就是在response返回时，在`request`设置csrftoken等信息。因此，我们也要在网页中携带随机字符串

2. 在模板中生成csrftoken ，有两种方式

   ```django
   <form>
   	{% csrf_token%}
       或者像下面这样 
       <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}"/>
   </form>
   ```



## XSS攻击
XSS（Cross Site Script）攻击又叫做跨站脚本攻击。黑客在使用具有 XSS 漏洞的网站的时候，向这个网站提交一些恶意的代码，当其他用户在访问这个网站的某个页面的时候，这个恶意的代码就会被执行，从而破坏网页的结构，获取用户的隐私信息等。

xss的攻击场景：比如 A网站有一个发布帖子的入口，如果用户在提交数据的时候，提交了一段 js 代码，比如：`<script>alert("hello world");</script>` ，然后 A网站在渲染这个帖子的时候，直接把这个代码渲染了，那么这个代码就会执行，会在浏览器的窗口中弹出一个对话框来显示“ hello world ！”，**如果攻击者能成功的运行以上这么一段 js 代码，那他能做的事情就有很多很多了！**



xss攻击防御：

1. 如果网页不需要显示一些富文本，那么在渲染用户提交数据的时候，直接进行转义即可，django默认开启转义。

   ```python
   from django.template.defaultfilters import escape # 加载django自带的转义过滤器
   from .models import Comment 
   from django.http import HttpResponse
   def comment(request):
       content = request.POST.get("content")
       escaped_content = escape(content)   # 转义字符串 
       Comment.objects.create(content=escaped_content)
       return HttpResponse('success')
   ```

2. 如果网页需要显示富文本，那就需要用到一个python的第三方库`bleach(pip install bleach)`。

   bleach库**用来清理包含html格式的字符串，**允许保留用户指定的标签tags或属性attributes 

   ```python
   import bleach
   from bleach.sanitizer import ALLOWED_TAGS,ALLOWED_ATTRIBUTES
   
   @require_http_methods(['POST'])
   def message(request):
       # 从客户端中获取提交的数据
       content = request.POST.get('content')
       
       # 在bleach默认的允许标签中添加 img标签
       tags = ALLOWED_TAGS + ['img']
       # 在bleach默认的允许属性中添加 src属性
       attributes = {**ALLOWED_ATTRIBUTES,'img':['src']}
       
       # 对提交的数据进行过滤 
       cleaned_content=bleach.clean(content,tags=tags,attributes=attributes)
       
       # 保存到数据库中
       Message.objects.create(content=cleaned_content)
       return redirect(reverse('index'))
   ```
   
   

[更多关于bleach的文档](https://bleach.readthedocs.io/en/latest/)



## clickjacking攻击

clickjacking 攻击又称作点击劫持攻击。是一种在网页中将恶意代码等隐藏在看似无害的内容（如按钮）之下，并诱使用户点击的手段。



clickjacking攻击场景：

1. 如用户收到一封包含一段视频的电子邮件，但其中的“播放”按钮并不会真正播放视频，而是链入一个购物网站。这样当用户试图“播放视频”时，实际是被诱骗而进入了一个购物网站。
2. 用户进入到一个网页中，里面包含了一个非常有诱惑力的 按钮A ，但是这个按钮上面浮了一个透明的 iframe 标签，这个 iframe 标签加载了另外一个网页，并且他将这个网页的某个按钮和原网页中的 按钮A 重合，所以你在点击 按钮A 的时候，实际上点的是通过 iframe 加载的另外一个网页的按钮



clickjacking防御：场景1是没有办法避免的，如右下角各种错误引导关闭的小弹窗。但是对于场景2，是可以避免的。只要拒绝网站通过iframe的方式加载即可，我们可以通过在响应（response）头中设置`X-Frame-Options`来设置这种操作，`X-Frame-Options`可以设置以下三个值：

1. DENY：拒绝任何网页使用iframe加载本网页
2. SAMEORIGIN ：同源，只允许在相同域名（也就是我自己的网站）下使用 iframe 加载我这个页面
3. ALLOW-FROM origin ：允许任何网页通过 iframe 加载我这个网页。



django的中间件`django.middleware.clickjacking.XFrameOptionsMiddleware`采用了第2种设置，并且默认开启。



## sql注入攻击

SQL注入：把sql命令插入表单或页面请求的查询字符串中，**欺骗服务器执行SQL命令**。



sql注入攻击场景：假设视图函数中有这样一段sql执行语句：

```python
from django.db import connection
def index(request):
    user_id = request.GET.get('user_id')
    cursor = connection.cursor()
    # 字符串拼接型查询语句
    cursor.execute("select id,username from front_user where id=%s" % user_id)
    rows = cursor.fetchall()
    # 显示所有数据
    for row in rows:
        print(row)
    return HttpResponse('success')
```

浏览器发起GET请求，附带查询参数`user_id`，函数`index`得到响应id后查询用户相关数据。



表面上，这没有什么问题，但是当用户试图传递`1 or 1=1`时，拼接后的sql语句变为

```mysql
select id,username from front_user where id=1 or 1=1
```

由于查询条件永远为真，表中的所有user数据将被查询出来。





sql注入防御：

1. 不要动态拼接sql，使用参数化（execute支持）的sql或者 使用django的ORM

   ```python
   #  cursor.execute("select id,username from front_user where id=%s" % user_id) # 原来的 
   cursor.execute("select id,username from front_user where id=%s",(user_id,))	#后面跟着1个元组
   ```

   

2. **不要使用管理员权限的数据库连接**，为每个应用使用单独权限的有限数据库连接

   




## 跨域请求

前后端分离的项目中，django应当允许跨域请求。

相关设置参考官网： https://pypi.org/project/django-cors-headers/  

1. 安装库：`pip install django-cors-headers`

2. 更改 settings.py 文件 

   ```python
   # 安装 app
   INSTALLED_APPS = [
       ...
       'corsheaders',
       ...
   ]
   
   # 中间件注册 优先级尽量高 
   MIDDLEWARE = [
       ...
       'corsheaders.middleware.CorsMiddleware',
       'django.middleware.common.CommonMiddleware',
       ...
   ]
   
   # 开启允许任何跨域请求
   CORS_ALLOW_ALL_ORIGINS =True 
   ```



# 验证和授权

## User模型类

### 介绍

User是授权系统的核心模型，完整路径是`django.contrib.auth.models.User`。django内置的User模型带有验证、登录等设计，比较强大。 



user类字段：

* username ： 用户名。150个字符以内。可以包含数字和英文字符，以及 _ 、 @ 、 + 、 . 和 - 字符。**不能为空，且必须唯一！**
*  first_name ：歪果仁的 first_name ，在30个字符以内。可以为空。
*  last_name ：歪果仁的 last_name ，在150个字符以内。可以为空。
*  email ：邮箱。可以为空。
*  password ：**经过哈希过后的密码**。
*  groups ：分组。一个用户可以属于多个分组，一个分组可以拥有多个用户。 groups这个字段是跟 Group 的一个多对多的关系。
* user_permissions ：权限。一个用户可以拥有多个权限，一个权限可以被多个用户所有用。
和Permission 属于一种多对多的关系。
* is_staff ：是否可以进入到 admin 的站点。代表是否是员工。
* is_active ：是否是可用的。对于一些想要删除账号的数据，我们设置这个值为 False 就可
  以了，而不是真正的从数据库中删除。
* is_superuser ：是否是超级管理员。如果是超级管理员，那么拥有整个网站的所有权限。
* last_login ：上次登录的时间。
* date_joined ：账号创建的时间。



user模型基本用法：

* 创建user：`create_user(username,password,email)`

  ```python
  from django.contrib.auth.models import User
  user = User.objects.create_user('zhiliao','hynever@zhiliao.com','111111')
  # User.objects.create(username='zhiliao') # 等效于这个 
  # 此时user对象已经存储到数据库中了。当然你还可以继续使用user对象进行一些修改
  user.last_name = 'abc'
  user.save()
  ```

* 创建超级用户：`create_superuser`。**`python manage.py createsuperuser`就是调用的这个接口**

  ```python
  from django.contrib.auth.models import User
  User.objects.create_superuser('admin','admin@163.com','111111')
  ```

* 修改密码：密码并不直接作为关键字参数传入，需要调用`set_password()` 

  ```python
  from django.contrib.auth.models import User
  user = User.objects.get(pk=1)
  user.set_password('密码')
  user.save() 
  ```

* 用户验证：django内置的验证系统提供了一个验证函数，用于用户名、密码验证

  ```python
  from django.contrib.auth import authenticate
  
  user = authenticate(request,username='zhiliao', password='111111')
  # 如果验证通过了，那么就会返回一个user对象。
  if user :
      # 执行验证通过后的代码
      pass
  else:
      # 执行验证没有通过的代码
      pass
  ```



### 扩展

django 自定义用户：https://docs.djangoproject.com/zh-hans/3.2/topics/auth/customizing/ 



**继承自AbstractUser，这种方式相当于魔改Usr，所以必须在第一次migrate前就定义好。**

```python
# 分为两部分 ：定义 Manager 、定义 User
# models.py 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
 
# user.objects 返回的UserManager 
# 在manager中命令行创建 createuser 也会用到
class UserManager(BaseUserManager):
    # 重写 create_user()、create_superuser()方法
    use_in_migrations = True
    def _create_user(self,telephone,password,**extra_fields):
        if not telephone:
            raise ValueError("请填入手机号码！")
        # self.model就是调用时传进来的User类（在下文定义）
        # 查看继承的AbstractUser的__init__方法，model(**kwargs)会为模型设置属性 setattr(model,attr)
        user = self.model(telephone=telephone,*extra_fields)  
        user.set_password(password) #加密后的密码，不会以原文显示
        user.save() # 数据入库
        return user
    
    def create_user(self,telephone,password,**extra_fields):
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(telephone,password,**extra_fields)
    
    def create_superuser(self,telephone,password,**extra_fields):
        extra_fields['is_superuser'] = True
        return self._create_user(telephone,password,**extra_fields) 

class User(AbstractUser):
    telephone = models.CharField(max_length=11,unique=True)
    school = models.CharField(max_length=100)
    is_super=models.BooleanFiedld(default=False)
    # 指定telephone作为USERNAME_FIELD
    # 以后使用authenticate函数验证的时候，就可以根据telephone来验证
    # 而不是原来的username
    USERNAME_FIELD = 'telephone'    #自定义用户表的主键
    REQUIRED_FIELDS = ['school'] # 所有blank=False或未定义的字段 ，在createuser的时候会被要求
    objects = UserManager() # 一个实例化的Manager
```

在settings.py文件中配置`AUTH_USER_MODEL`，指定User模型。

```python
AUTH_USER_MODEL='appname.User' # 不要写成appname.modules.User
```






### 相关函数

#### authenticate() 

用于验证用户，如果用户合法，就会返回一个`user_objet`，否则为None。

```python
from django.contrib.auth import authenticate
def get(request):  
    user=authenticate(request,username=username,# 自己在模型中定义的USERNAME_FIELD 
                      password=password)
```

#### get_user_model()

获取当前项目中的User模型。

```python
# 去settings.py中找 
def get_user_model():
    """
    Return the User model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
        )
```

#### short-uuid

在开发时，经常选uuid作为user的主键 

安装

```shell
pip install django-shortuuidfield
```

使用

```python
from shortuuidfield import ShortUUIDField 

class User(AbstractUser):
    uid=ShortUUIDField(primary_key=True)
```



## 登录注销

### login

 `django.contrib.auth.login `登录函数会额外地设置session

```python
#验证+登录示例
from django.contrib.auth import login,auth
def my_login(request):
    user = authenticate(request,username=username,password=password)
    if user :  #验证成功
        if user.is_active:  
        	login(request, user)	#登录
        else:
            print('账号被冻结')
    else:
        print('用户名或密码错误，验证失败')
```

### logout
`django.contrib.auth.logout`注销函数会清空login保留的session。

```python
from django.contrib.auth import logout
def mylog_out(request):
    logout(request)
    return redirect(reverse('index')) #退出后重定向到首页
```





## 权限增删

在`models.py`中创建完一个模型以后，默认包含3种权限，分别是增删改，在数据库的`auth_permission`表中可以查看。

| id   | content_type_id | codename        | name                             |
| ---- | --------------- | --------------- | -------------------------------- |
| 1    | 7               | add_bookinfo    | Can add book info（可以增加）    |
| 2    | 7               | change_bookinfo | Can change book info（可以修改） |

content_type_id是每个`model`的编号，codename格式为`add/delete/view/change_modelname`，name是对code的解释。



为模型添加权限：

* 通过模型层定义的方式，在`Meta`中添加permissions属性

  ```python
  from django.contrib.auth import get_user_model
  class Article(models.Model):
      title = models.CharField(max_length=100)
      content = models.TextField()
      author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
      class Meta:
          permissions = (
          ('view_article','can view article'),
          )
  ```
  
* 通过代码添加权限：创建`Permission`实例。

  ```python
  from django.contrib.auth.models import Permission,ContentType
  from .models import Article
  
  content_type = ContentType.objects.get_for_model(Article) # 选择模型 
  permission = Permission.objects.create(name='可以编辑的权限',
                                         codename='edit_article',
                                         content_type=content_type)
  ```
  
  

User模型和Permission模型的管理，有以下几种方式：

* `userObj.user_permissions.set(permission_list) `：批量添加权限，元素是permission实例
* `userObj.user_permissions.add(permission,permission,...)` ：一个个添加权限。
* ```````userObj.user_permissions.remove(permission,permission,...)``````` ：一个个删除权限
* `userObj.user_permissions.clear() `：清除权限。
* `userObj.has_perm('<app_name>.<codename>') `：判断是否拥有某个权限。权限参数是一个字符
  串，格式是 `app_name.codename` 。
* `userObj.get_all_permissons() `：获取用户所有的权限。





权限装饰器：

使用` permission_required `可以非常方便的检查用户是否拥有这个权限

```python
from django.contrib.auth.decorators import permission_required
#login_url 用户没有登录时跳转 
@permission_required('front.view_article',login_url='/login',raise_exception=True)
def my_view(request):
	pass
```



## 分组

按组管理用户权限。

`django.contrib.auth.models.Group`模型，对应数据库的`auth_group`。

```python
from django.contrib.auth.models import Group,Permission,ContentType
```

Group是分组模型。

Permission是权限模型，对应数据库的`auth__permission`数据表，记录了每个模型的操作权限。

ContentType模型类对应数据库的`djano_content_type`数据表，记录每个app下的model，以外键的形式被Permission引用。



Permisson的数据示例

| id   | name                 | conent_type_id（app:model  外键） | codename          |
| ---- | -------------------- | --------------------------------- | ----------------- |
| 1    | Can add log entry    | 1                                 | Can add log entry |
| 2    | Can change log entry | 1                                 | change_logentry   |

ContentType数据示例（记录app下创建了什么模型）

| id   | app_label | model   |
| ---- | --------- | ------- |
| 10   | news      | banner  |
| 9    | news      | comment |



分组操作：user类与group类是多对多的关系

1. Group.object.create(group_name) ：创建分组实例
2. groupObj.permissions.add ：添加权限。
3. groupObj.permissions.remove ：移除权限。
4. groupObj.permissions.clear ：清除所有权限。
5. userObj.get_group_permissions() ：获取用户所属组的权限。
6. userObj.groups ：某个用户上的所有分组。多对多的关系





在模板中使用权限：

中间件`django.contrib.auth.context_processors.auth`，会在context中添加一个perms变量，`perms.appname.codename(action_modelname)` ，可以得到用户的所有权限。

```python
{% if perms.front.add_article %}
	<a href='/article/add/'>添加文章</a>
{% endif %}
```



# Redis

Redis是一种nosql（非关系型）数据库，以键值对存储数据。数据既可以保存在内存中，也可以定时将内存的数据同步到磁盘，兼顾速度与持久。而且比memcached支持更多的数据结构，诸如列表、集合，

![](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/redis%E4%B8%8Ememcached%E6%AF%94%E8%BE%83.png)



## 安装与启动（Ubuntu）

* 安装：`sudo apt-get install redis-server` 
* 卸载：`sudo apt-get purge --auto-remove redis-server`。purge会卸载相关的依赖包
* 启动：redis安装后，默认会自动启动，可以查看进程`ps -elf|grep redis`。如果想要手动启动，可以执行`sudo service redis-server start` 
* 停止：`sudo service redis-server stop`  





## redis操作

redis操作有两种方式，一是直接使用redis-cli，二是采用编程语言，如python、java等。



使用redis-cli操作：

* 启动：`sudo service redis-server start`

* 连接：`redis-cli -h [ip] -p [端口]` 。

  redis默认只允许本机连接，即`127.0.0.1`，如果希望其他机器远程访问本机redis，需要进入redis配置文件，修改`bind 127.0.0.1 [your_ip]`，后面添加自己的ip，则其他机器就可以用指定ip访问。

当进入redis服务后

* 添加：`sety key "value" [EX  timeout]`。key存在时会被覆盖。双引号包裹表示为字符串，EX timeout表示设置键值对的超时时间，默认永不过期。
* 删除：`del key` 
* 设置过期时间：`expire key timeout(单位为秒)` 
* 查看某个键的过期时间：`ttl key` 
* 查看redis当前存储的所有键：`keys *` 

***

redis列表操作：下述的key指向一个列表

* 添加元素：分为左添加`lpush key val`、右添加`rpush key val`。当键不存在时，会被创建；当键存在而类型不为列表式，会报错。
* 查看列表所有元素：`lrange key start stop`，如果是查看全部，可以写作`lrange key 0 -1` ，-1表示最后1个
* 获取列表元素个数：`llen key` 
* 移除元素：
  * 左、右移除：`lpop key`、`rpop key`，会分别弹出列表的头、尾元素
  * 移除并返回列表的中间元素：`lrem key count value`，将删除列表中指定count个数的value。count的值可以设为：
    * count>0：从表头搜索，移除count个数的value
    * count=0：移除所有value
    * count<0：从表尾搜索，移除count个数的value
* 索引元素：`lindex key index`

***



redis集合操作：下述的key指向一个集合

* 添加元素：`sadd key value1 value2...`
* 查看元素：`smembers key` 
* 移除元素：`srem set member` 
* 查看元素个数：`scard key` 
* 交集：`sinter key1 key2`
* 并集：`sunion key1 key2`
* 差集：`sdiff key1 key2`

***



redis哈希操作：下述的key指向一个哈希表，filed表示哈希表中的键，value表示哈希表中的值

* 添加：`hset key field val` 
* 获取：`hget  key field` 
* 删除：`hdel key field` 
* 获取所有键值对：`hgetall key`，获取某个哈希中所有的field、value 
* 获取所有键：`hkeys key` 
* 获取所有值：`hvals key` 
* 判断是否存在某个field：`hexists key field` 
* 获取总共键值对：`hlen key` 



***

redis 事务操作：

* 开启事务：`multi`，事务开启后，可以输入若干命名，但不会真正得到执行，相当于添加到事务列表中
* 执行事务：`exec` ，执行自multi开始所有的命令 
* 取消事务：`discard` ，废弃自multi后所有的命令
* 监视一个或者多个key：`watch key` ，如果在事务的执行过程中key发生了变动，事务就不会执行
* 取消监视key：`unwatch key`，key缺省表示取消监视所有key



***

redis发布/订阅操作：

* 给某个频道发布消息：`publish channelname message` ，必须先有人订阅才可以发布
* 订阅某个频道的消息：`subscribe channel` 



## 数据持久化

redis提供了两种数据备份方式，一种是RDB，一种是AOF。

相关配置文件见`/etc/redis/redis.conf` 

|              | RDB                                                          | AOF                                                          |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 开启         | 默认开启                                                     | 配置文件中的`appendonly yes`即是开启                         |
| 关闭         | 注释掉配置文件中所有的save                                   | `appendonly no`                                              |
| 同步机制     | 某个时间段内发生一定数量指令后同步                           | 每秒同步获或者每次发生命令后同步                             |
| 存储内容     | 存储redis的数据                                              | 存储命令                                                     |
| 存储文件位置 | 依据配置文件中的dir+dbfilename                               | 依据配置文件中的dir+appendfilename                           |
| 优点         | 存储数据到文件中会进行压缩，体积要比AOF小；由于直接存储数据，恢复数据也比AOF快，适合备份 | 每秒或者每次发生命令后就同步，即使服务器故障，最多丢失1s的数据；存储的是命令，而不是数据，且以追加（a）的形式写入到存储文件，同步很快 |
| 缺点         | 同步时不是增量同步，而是全盘同步，也就是每次都会全部备份redis的数据，又RDB会额外进行压缩工作，所以每次同步会很慢。这样一个周期中，服务器一旦故障，就会丢失较多数据 | AOF不会压缩，同步文件的体积会比RDB大；并发量很高的时候，AOF的同步机制可能会比较慢（有相当多的命令）；恢复数据的速度不如RDB |



## 密码配置

在配置文件中，取消注释`requirepass password`，password改成自己的密码。修改完配置，记得重启redis服务，`service redis restart` 

此后，客户端连接需要密码

```shell
redis-cli -p 127.0.0.1 -p 6379 -a my_password #连接的时候就输入密码

#或者连接后在输入密码
auth  my_password
```



## python操作redis

* 安装：`pip install redis` ，第三方库 

* 连接：实例化一个对象

  ```python
  # 从redis包中导入Redis类
  from redis import Redis
  # 初始化redis实例变量，如果设置了密码，就要有password参数
  xtredis = Redis(host='192.168.174.130',port=6379,[password=])
  ```

* 字符串操作：

  ```python
  # 添加一个值进去，并且设置过期时间为60秒，如果不设置，则永远不会过期
  xtredis.set('username','xiaotuo',ex=60)
  # 获取一个值
  xtredis.get('username')
  # 删除一个值
  xtredis.delete('username')
  # 给某个值自增1
  xtredis.set('read_count',1)
  xtredis.incr('read_count') # 这时候read_count变为2
  # 给某个值减少1
  xtredis.decr('read_count') # 这时候read_count变为1
  ```

* 对列表操作：

  ```python
  # 给languages这个列表往左边添加一个python
  xtredis.lpush('languages','python')
  # 给languages这个列表往左边添加一个php
  xtredis.lpush('languages','php')
  # 给languages这个列表往左边添加一个javascript
  xtredis.lpush('languages','javascript')
  # 获取languages这个列表中的所有值
  print(xtredis.lrange('languages',0,-1))
  > ['javascript','php','python']
  ```

* 对集合操作：

  ```python
  # 给集合team添加一个元素xiaotuo
  xtredis.sadd('team','xiaotuo')
  # 给集合team添加一个元素datuo
  xtredis.sadd('team','datuo')
  # 给集合team添加一个元素slice
  xtredis.sadd('team','slice')
  # 获取集合中的所有元素
  
  xtredis.smembers('team')
  > ['datuo','xiaotuo','slice'] # 无序的
  ```

* 对哈希（字典）操作：

  ```python
  # 给website这个哈希中添加baidu
  xtredis.hset('website','baidu','baidu.com')
  # 给website这个哈希中添加google
  xtredis.hset('website','google','google.com')
  # 获取website这个哈希中的所有值
  print xtredis.hgetall('website')
  > {"baidu":"baidu.com","google":"google.com"}
  ```

* 事务操作：python操作redis的事务，要先定义一个管道实例 `.pipeline()`

  ```python
  # 定义一个管道实例
  pip = xtredis.pipeline()
  
  #然后以pip对象执行各种命令
  # 做第一步操作，给BankA自增长1
  pip.incr('BankA')
  # 做第二步操作，给BankB自减少1
  pip.desc('BankB')
  
  # 执行事务
  pip.execute()
  ```

* 发布与订阅：

  订阅代码示例，订阅一个频道要先定义一个pubsub对象 

  ```python
  from redis import Redis
  xtredis = Redis(host='192.168.174.130',port=6379)
  
  ps=xtredis.pubsub()	#定义1个pubsub对象 
  ps.subscribe('email')		#订阅email频道
  while True:
      for item im ps.listen():	#listen监听数据，会返回一个生成器
          print(item)
  ```

  发布代码示例

  ```python
  from redis import Redis
  xtredis = Redis(host='192.168.174.130',port=6379)
  
  for i in range(3): xtredis.pubsub('email',i)	#发布到email频道
  ```



## django配置

参考：https://www.cnblogs.com/zpf666/p/10306367.html

# WSGI&uwsgi

参考：

* 简书：https://www.jianshu.com/p/679dee0a4193
* b站：https://www.bilibili.com/video/BV1hE411h7dz?from=search&seid=11858669480138343921



# DRF

## DRF介绍

`DRF`是`Django Rest Framework`单词的简写，是在`Django`框架中实现`Restful API`的一个插件，使用他可以非常方便的实现接口数据的返回。`Django`中也可以使用`JsonResponse`直接返回`json`格式的数据，但是`DRF`相比直接使用`Django`返回`json`数据有以下几个好处：

1. 可以自动生成`API`文档，在前后端分离开发的时候进行沟通比较有用。
2. 授权验证策略比较完整，包含`OAuth1`和`OAuth2`验证。
3. 支持`ORM`模型和非`ORM`数据的序列化。
4. 高度封装了视图，使得返回`json`数据更加的高效。



## 基本使用

### 安装

`drf`目前最新的版本是`3.10`，需要以下依赖：

1. `Python (3.5, 3.6, 3.7)`
2. `Django (1.11, 2.0, 2.1, 2.2)`

准备好以上依赖后，可以通过`pip install djangorestframework`安装最新的版本。

### 注册

安装完后，使用他还需要进行在`settings.INSTALLED_APPS`中进行安装。

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

### 创建app和模型

创建一个名叫`meituan`的`app`，然后在`meituan.models`中创建以下模型：

```python
from django.db import models
from django.contrib.auth.models import User

class Merchant(models.Model):
    """
    商家
    """
    name = models.CharField(max_length=200,verbose_name='商家名称',null=False)
    address = models.CharField(max_length=200,verbose_name='商家',null=False)
    logo = models.CharField(max_length=200,verbose_name='商家logo',null=False)
    notice = models.CharField(max_length=200, verbose_name='商家的公告',null=True,blank=True)
    up_send = models.DecimalField(verbose_name='起送价',default=0,max_digits=6,decimal_places=2)
    lon = models.FloatField(verbose_name='经度')
    lat = models.FloatField(verbose_name='纬度')

    created = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)


class GoodsCategory(models.Model):
    """
    商家商品分类
    """
    name = models.CharField(max_length=20,verbose_name='分类名称')
    merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE,verbose_name='所属商家',related_name='categories')  # 外键关联

class Goods(models.Model):
    """
    商品
    """
    name = models.CharField(max_length=200,verbose_name='商品名称')
    picture = models.CharField(max_length=200,verbose_name='商品图片')
    intro = models.CharField(max_length=200)
    price = models.DecimalField(verbose_name='商品价格',max_digits=6,decimal_places=2) # 最多6位数，2位小数。9999.99
    # 外键关联 
    category = models.ForeignKey(GoodsCategory,on_delete=models.CASCADE,related_name='goods_list')
```



创建完模型后，运行`makemigrations`和`migrate`后把模型映射到`mysql`数据库中。然后在`navicat`中添加测试数据。

### 编写Serializers

在`meituan`这个`app`中新创建一个文件`serializers.py`，然后添加以下代码：

```python
from rest_framework import serializers
from .models import Merchant,GoodsCategory,Goods

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"
```

### 编写视图

使用`drf`我们可以非常方便的创建包含`get/post`等`method`的视图。在`meituan.views`中添加以下代码

```python
# ModelViewSet 绑定模型 + 集成多种method:get/post/delete等 
class MerchantViewSet(ModelViewSet):
    queryset = Merchant.objects.all() # 返回数据    
    serializer_class = MerchantSerializer  # 序列化类
```

### 编写路由

在`meituan.urls`中添加以下代码：

```python
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register('merchant',views.MerchantViewSet,basename='merchant') # prefix/merchant

urlpatterns = [
] + router.urls
```

然后再在项目的`urls.py`中把`meituan`的路由添加进去：

```python
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meituan/',include("meituan.urls"))
]
```

以后我们就可以使用不同的`method`向`/meituan/merchant`发送请求。比如用`get`，那么就会返回`merchant`的列表，比如用`post`，那么就会向`merchant`表添加数据。



## 序列化

**`drf`中的序列化是双向的，主要用于：**

1. 将模型序列化成`JSON`格式的对象，返回给前端
2. 表单验证功能，数据反序列化成实例，进行数据的更新。

### Serializer

虽然restframework存在更高级便捷的封装，但是从最基础的`Serializer`类入手可以更好理解底层原理。

#### 创建Serializer

这里我们以上一节的模型`Merchant`、`GoodsCategory`、`Goods`为例来讲解。

首先我们创建一个`Merchant`的`Serializer`类，**该类必须实现`create`、`update`方法**，示例代码如下：

```python
from rest_framework import serializers
from .models import Merchant,GoodsCategory,Goods

class MerchantSerializer(serializers.Serializer):
    # 需要序列化的字段
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True,max_length=200)
    logo = serializers.CharField(required=True,max_length=200)
    notice = serializers.CharField(max_length=200,required=False)
    up_send = serializers.DecimalField(max_digits=6,decimal_places=2,required=False)
    lon = serializers.FloatField(required=True)
    lat = serializers.FloatField(required=True,error_messages={"required":"必须传入lat！"})

    def create(self, validated_data):
        # create方法实现  
        # validated_data 表示验证过得表单数据 
        # serializer.save()底层会调用该方法 下同 
        # 对应POST 
        return Merchant.objects.create(**validated_data)

    def update(self,instance, validated_data):
        # update方法实现
        # validated_data 表示验证过得表单数据  instance表示数据库实例
        # 相比于create多了一个instance 
        # 对应PUT 
        instance.name = validated_data.get('name',instance.name)
        instance.logo = validated_data.get('logo',instance.logo)
        instance.notice = validated_data.get('notice',instance.notice)
        instance.up_send = validated_data.get('up_send',instance.up_send)
        instance.lon = validated_data.get('lon',instance.lon)
        instance.lat = validated_data.get('lat',instance.lat)
        instance.save()
        return instance
```

**那么以后在视图函数中，可以使用他来对实例数据（instance）进行序列化（服务器向客户端返回），也可以对表单数据（data）进行校验（客户端提交数据到服务器）**，然后存储数据。比如以下在视图函数中使用：

```python
from .models import Merchant
from .serializers import MerchantSerializer
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET','POST'])
def merchant(request):
    if request.method == 'GET':
        merchants = Merchant.objects.all()
        serializer = MerchantSerializer(merchants,many=True)
        return JsonResponse(serializer.data,safe=False) # 序列化实例 传入data
    else:
        serializer = MerchantSerializer(data=request.POST) # data关键字表示对表单数据验证
        if serializer.is_valid():
            serializer.save() # 底层调用create
            # serialzier.save(instance,data) # 如果对应PUT就这么写 会调用update方法 
            return JsonResponse(serializer.data,status=200) # 表单数据 
        return JsonResponse(serializer.errors,status=400)
```



为什么一定要实现`create`、`update`方法？查看`Serializer`的类定义源码可知，这两个函数是为`save()`服务的。

```python
class BaseSerializer(Field):
    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')

    def save(self, **kwargs):
        assert not hasattr(self, 'save_object'), (
            'Serializer `%s.%s` has old-style version 2 `.save_object()` '
            'that is no longer compatible with REST framework 3. '
            'Use the new-style `.create()` and `.update()` methods instead.' %
            (self.__class__.__module__, self.__class__.__name__)
        )

        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )
		
        # 下面是对 create 和 update 的判断
        # validated_data 在 is_valid()后生成 save()函数借助这个技巧来判断
        # 接下来是该调用create还是update
        if self.instance is not None: # 如果instance不为空 表示修改 update
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else: # 否则就是 新增instance 
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance
```





#### data 和 instance 参数

序列化类在实例化时，参数传递有以下几种情况：

1. `MerchantSerializer(instance=queryset,[many=true])`，instance表示是ORM实例，many=True表示前面的queryset实例有多个，用于模型的序列化。通过`se.data`得到序列化后的数据 

2. `MerchantSerializer(data=request.POST)`，data是提交的表单数据，用于验证客户端的提交。当提供data参数时，

   ```python
   '''
   The BaseSerializer class provides a minimal class which may be used
       for writing custom serializer implementations.
   
       Note that we strongly restrict the ordering of operations/properties
       that may be used on the serializer in order to enforce correct usage.
   
       In particular, if a `data=` argument is passed then: 如果提供了data参数
   
       .is_valid() - Available. 验证数据 
       .initial_data - Available.
       .validated_data - Only available after calling `is_valid()` 清洗后的数据 通过了验证+validate_filed+validata() 用于入库的数据 
       .errors - Only available after calling `is_valid()` 验证错误 
       .data - Only available after calling `is_valid()`
   
       If a `data=` argument is not passed then:  如果data参数是省略的 
   
       .is_valid() - Not available.
       .initial_data - Not available.
       .validated_data - Not available.
       .errors - Not available.
       .data - Available. 序列化后的数据 json格式，返回给前端 
   '''
   ```

3. `Merchant([many=True])` ，**在嵌套序列化的时候使用**，用于在序列化类中 显式指定 某个字段的序列化方式。

   ```python
   class GoodsCategorySerializer(serializers.ModelSerializer):
       goods_list=GoodsSerializer(many=True) # 这个字段应该怎么序列化 
       class Meta:
   		model=Goods
           field='__all__'
   ```

   

### ModelSerializer

之前我们在写序列化类的时候，几乎把模型中所有的字段都写了一遍，**我们可以把模型中的字段移植过来即可**。这时候就可以使用`ModelSerializer`类实现。示例代码如下：

```python
class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = "__all__"
        # exclude=[] # 要排除的字段
```



#### `Serializer`嵌套

序列化其中一个模型的时候，涉及到另外一个模型的序列化，即为嵌套。

模型的某个属性为另外一个模型，现实意义就是存在表关联。

* 1对1：定义外键的那个模型，序列化时返回关联模型的id、创建时前端提交id。

* 1对多：例如Goods（多）与Merchant（一）。Merchant在被关联时会创建字段`goods_set`，但是该字段不会被`ModelSerializer`序列化，需要显示指定。

  ```python
  class MerchantSerializer(serializers.ModelSerializer):
      goods_set=GoodsSerializer(many=True) # 多个实例
      class Meta:
          model = Merchant
          fields = "__all__"
  ```

* 多对多：例如Order与Goods，外键关联定义在Order字段。序列化时，会返回Goods的多个id，是列表。前端提交时为列表格式。

  ```python
  class OrderSerializer(ModelSerializer):
      goodsList = serializers.ListField() # 多个goods 返回主键
      class Meta:
          model = Order
          fields=['goodsList','address']
  ```



嵌套序列化就是在一个序列化类中使用另一个序列化类来获取详细信息。

Goods与Merchant是多对一的关系

```js
{id:201,
name:'炸鸡啤酒',
merchant:1} // 只能看到关联到哪个商家id
```

定义序列化类

```python
class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = "__all__"

# 序列化嵌套        
class GoodsCategorySerializer(serializers.ModelSerializer):
    # 显式指定 模型字段merchant 的 序列化方式
    # readonly 表示该字段只会从服务器返回 不会被客户端提交
    merchant = MerchantSerializer(read_only=True,required=False) 
    goods_list = GoodsSerializer(many=True,required=False)
    # 增加merchant_id 是为了应对post方式，便于创建新数据 
    merchant_id = serializers.IntegerField(required=True,write_only=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

    def validate_merchant_id(self,value):
        if not Merchant.objects.filter(pk=value).exists():
            raise serializers.ValidationError("商家不存在！")
        return value

    def create(self, validated_data):
        merchant_id = validated_data.get('merchant_id')
        merchant = Merchant.objects.get(pk=merchant_id)
        category = GoodsCategory.objects.create(name=validated_data.get('name'), merchant=merchant)
        return category
```



#### read_only和write_only：

1. `read_only=True`：这个字段只能读，只有在返回数据的时候会使用。
2. `write_only=True`：这个字段只能被写，只有在新增数据或者更新数据的时候会用到。

### 验证

验证用户上传上来的字段是否满足要求。可以通过以下三种方式来实现。

1. 验证在`Field`中通过参数的形式进行指定。比如`required`等。

2. 通过重写`validate(self,attrs)`方法进行验证。`attrs`中包含了所有字段。**如果验证不通过，那么调用`raise serializer.ValidationError('error')`即可，**

3. 重写`validate_字段名(self,value)`方法进行验证。这个是针对某个字段进行验证的。如果验证不通过，也可以抛出异常。

   ```python
   def validate_id(self,value):
       if xx:return value
       else:serializers.ValidationError("错误原因")

### 更多

更多请参考：

1. `Serializer`：`https://www.django-rest-framework.org/api-guide/serializers/`。
2. `Serializes Fields`及其参数： `https://www.django-rest-framework.org/api-guide/fields/`。





## 类视图

restful的url设计过程中，一个url的想要的操作通过他的`method`区分：

1. get：取数据 ，如`merchant/`（列表数据）、`merchant/31`（id操作）
2. post：创建数据，`merchant/`
3. put：修改数据，`merchant/31`
4. delete：删除数据，`merchant/31` 



### Request和Response对象：

**使用`restframework`的类视图**，在类方法中可以得到拓展加强的`Request`、`Response`对象。

#### Request对象：

`DRF`的`Request`对象是从`HttpRequest`中拓展出来的，但是增加了一些其他的属性。其中最核心的用得最多的属性便是`request.data`：

1. `request.data`：**可以处理任意的数据。可以获取通过`POST`、`PUT`、`PATCH`等方式上传上来的数据。** 
2. `request.query_params`：**查询参数**。比`request.GET`更用起来更直白。 



request在类视图有两处存在：

1. `self.request` ，在被dispatch给相应的method方法前就被构造并存储为对象属性
2. `get(self,requets)`，在相应的method方法中作为第2个参数被传入 ，和步骤1的request相同。



#### Response对象：

**`Response`可以自动的根据返回的数据类型来决定返回什么样的格式**。并且会自动的监听如果是浏览器访问，那么会返回这个路由的信息。



#### 状态码

在`Restful API`中，响应的状态码是很重要的一部分，`DRF`编码了若干状态码，使用起来直观

```python
from rest_framework.response import Response
from rest_framework import status # 可以点进去看详细的状态码 

@api_view(['GET','POST','PUT','DELETE'])
def merchant(request):
    return Response({"username":"zhiliao"},status=status.HTTP_200_OK)
```



### APIView

如果是视图函数，可以使用装饰器`@api_view`限制请求Method

```python
from rest_framework.decorators import api_view

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    pass
```



如果是类视图，可以让类继承自`APIView`，手动实现get\post等请求来完成对应method

```python
from rest_framework.views import APIView

class MerchantView(APIView):
    def get(self,request): # get method
        return Response("你好")
```

### Mixins

`mixins`翻译成中文是混入，组件的意思。在`DRF`中，针对获取列表，检索，创建等操作，都有相应的`mixin`。

相比于上一节的APIView，**`mixins`的各种拔插类封装了数据库操作的相关逻辑**，**继承时增加了类属性`queryset`、`serializer_class`的定义。**

示例代码如下：

```python
from .models import Merchant
from .serializers import MerchantSerializer
from rest_framework import mixins
from rest_framework import generics

class MerchantView(
    generics.GenericAPIView, # 基类 ，提供了一些必要的属性
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin, # get
    mixins.CreateModelMixin, # post
    mixins.UpdateModelMixin, # put
    mixins.DestroyModelMixin # delete
):
    queryset = Merchant.objects.all() # 必要属性：数据集
    serializer_class = MerchantSerializer # 必要属性： 序列化类 
	
    '''
    mixin 提供的各种拔插插件 实现了底层的数据操作，如create对应了post、retrieve对应了get等
    我们 需要实现 method 方法，如下面的get\post\put等
    然后 去 调用 mix类中的方法  
    '''
    def get(self,request,pk=None):
        if pk:
            # 这里的 retrieve 没有传进去 pk 是因为
            # GenericAPIView 里的 dispatch 方法 实现了
            # 从url剥取关键字参数merchant/<int:pk>，并在get_obj、filter等方法里使用 
            # 查找字段 可以更改 lookup_field = 'pk'
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self,request): 
        # 如果有重写的需要 可以点进create函数查看 
        return self.create(request)

    def put(self,request):
        return self.update(request)

    def delete(self,request):
        return self.destroy(request)
```



### Generic：

`mixin`类实现了模型CURD的核心操作，但是操作外还需要套一个method方法调用。generic包有更彻底的封装类：

1. `generics.ListAPIView`：**实现获取列表数据的**。实现`get`方法。
2. `generics.CreateAPIView`：实现创建数据的。实现`post`方法。
3. `generics.UpdateAPIView`：实现更新数据的。实现`put`方法。
4. `generics.DestroyAPIView`：实现删除数据的。实现`delete`方法。
5. `generics.RetrieveAPIView`：**实现检索单个数据的。实现`get`方法**。
6. `generics.ListCreateAPIView`：实现列表和创建数据的。
7. `generics.RetrieveUpdateAPIView`：实现检索和更新数据的。
8. `generics.RetrieveDestroyAPIView`：实现检索和删除数据的。
9. `generics.RetrieveUpdateDestroyAPIView`：实现检索和更新和删除数据的。

用法如下：

```python
class MerchantView(
    generics.CreateAPIView, # 这时候就不用继承自generics.GenericAPIView了 因为它们都是它的子类 
    generics.UpdateAPIView, # 可以点进去看它底层的方法实现 以便自定义修改 
    generics.DestroyAPIView,
    generics.RetrieveAPIView  # 单个查询
):
    '''
    generic 的 方法 相当于帮我们实现了get\post\delete等方法
    所以 只需要 指定 下面两个属性即可 
    '''
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()
```

那么在定义`url`与视图映射的时候，还是按照之前的写法就够了：

```python
urlpatterns = [
    path('merchant/',views.MerchantView.as_view()),
    path('merchant/<int:pk>/',views.MerchantView.as_view())
]
```

请求的`url`和`method`产生的结果如下：

| method | url           | 结果                    |
| :----- | :------------ | :---------------------- |
| get    | /merchant/31/ | 获取id=31的merchant数据 |
| post   | /merchant/    | 添加新的merchant数据    |
| put    | /merchant/31/ | 修改id=31的merchant数据 |
| delete | /merchant/31  | 删除id=31的merchant数据 |



**因为这里`retrieve`占用了`get`方法**，所以如果想要实现获取列表的功能，那么需要再重新定义一个url `merchants/`和视图：

```python
# views.py
class MerchantListView(generics.ListAPIView,):
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()

# urls.py
urlpatterns = [
    path('merchant/',views.MerchantView.as_view()),
    path('merchant/<int:pk>/',views.MerchantView.as_view()),
    path('merchants/',views.MerchantListView.as_view()) # 重新定义一个获取列表数据集的视图 
    ...
]
```

这也是为什么`List`和`Retrieve`不能同时存在一个视图中的原因。可以选择下文的视图集`ModelViewSet` ，更方便。



Generic  、 Mixin、APIView 实现方法对比

| APIView                                                    | Mixin                                                        | GenericApi （底层调用左边的）                           |
| :--------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| 需要手动实现get\post等函数，在函数中实现数据操作的底层逻辑 | **数据操作底层逻辑已经封装，可以直接调用**；**需要手动实现get\post等函数**； | 已经实现了get\post等操作，创建类时继承相应的APIview即可 |
| 类属性定义：none                                           | `qureyset` ；`serializer_class`                              | `qureyset` ；`serializer_class`                         |
|                                                            | `get()`: retrieve，`ListModelMixin`，`RetrieveModelMixin`，可以通过url有无参数的形式区别开 | get，`RetrieveAPIView`，`ListAPIView`，不能共存         |
|                                                            | `pos()`: create（perform_create才是逻辑实现），`CreateModelMixin` | post，`CreateAPIView`                                   |
|                                                            | `delete`: destroy，`DestroyModelMixin`                       | delete，`DestroyAPIView`                                |
|                                                            | `put()`:update，`UpdateModelMixin`                           | put，`UpdateAPIView`                                    |



------

### GenericAPIView 的API 

Mixins 类视图、Generic类视图均继承自 `GenericAPIView `  ，涉及到模型类、序列化类。

#### 属性

queryset：

`queryset`是用来控制视图绑定的数据集

```python
class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer 
```



如果逻辑比较复杂，也可以重写`get_queryset`方法用来返回一个`queryset`对象。如果重写了`get_queryset`，那么以后获取`queryset`的时候就需要通过调用`get_queryset`方法。**因为`queryset` 这个属性只会调用一次，以后所有的请求都是使用他的缓存。** 

```python
def get_queryset(self):
    return self.request.user.addresses  # 返回manager
```

****

serializer_class:

`serializer_class`用来验证和序列化数据的。可以通过直接设置这个属性，也可以通过重写`get_serializer_class`来实现。

### 分页

分页是通过设置`pagination_class`来实现的

1. 自定义一个 分页类，继承PageNumberPagination 

   ```python
   from rest_framework.pagination import PageNumberPagination
   class MerchantPagination(PageNumberPagination):
       page_size = 12  # 每一页大小
       page_query_param = 'page'  # url 请求分页的参数 ?page=xx
   ```

2. 在类视图重写类属性 `pagination_class`  

   ```python
   class MerchantViewSet(ModelViewSet):
       queryset = Merchant.objects.all().order_by('-created_time')
       serializer_class = MerchantSerializer
   
       pagination_class = MerchantPagination
   ```

   也可以在`settings.py`文件中全局配置

   ```python
   REST_FRAMEWORK = {
       'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination'
   }
   ```




在`GET`Merchant的数据时，返回的分页数据格式如下：

```json
{
    "count": 16, // 数据集总共有几条数据 
    "next": "http://222.24.63.60:8000/cms/merchant/?page=2", // 下一页的url 
    "previous": null,  // 上一页的url 
    "results": [] // 里面是一页的数据 
}
```



## ViewSet视图集

`ViewSet`视图集，包含数据增删改查的所有方法，不再需要拔插式的继承。

**在视图集中，不定义`get`和`post`等方法，取而代之的是`list`和`create`。以下分别进行讲解。**

### ViewSet

比如我们想实现一个包含增、删、改、查、列表的视图集。我们可以通过以下代码来实现：

```python
from .models import Merchant
from .serializers import MerchantSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404 # 要么返回数据 要么返回 404Exception

class MerchantViewSet(viewsets.ViewSet):
    '''
    查看 ViewSet 的源码说明，不提供get\post等method
    提供 actions:create,update,retrieve,list,destroy
    最基础的ViewSet 就像 APIView一样 要自己实现CURD逻辑 
    '''
    def list(self,request):
        queryset = Merchant.objects.all()
        serializer = MerchantSerializer(queryset,many=True)
        return Response(data=serializer.data)

    def create(self,request):
        serializer = MerchantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("success")
        else:
            return Response("fail",status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,pk=None):
        queryset = Merchant.objects.all()
        merchant = get_object_or_404(queryset,pk=pk)
        serializer = MerchantSerializer(merchant)
        return Response(serializer.data)

    def update(self,request,pk=None):
        queryset = Merchant.objects.all()
        merchant = get_object_or_404(queryset, pk=pk)
        serializer = MerchantSerializer()
        serializer.update(merchant,request.data)
        return Response('success')

    def destroy(self,request,pk=None):
        queryset = Merchant.objects.all()
        merchant = get_object_or_404(queryset,pk=pk)
        merchant.delete()
        return Response('success')
```

然后在`urls.py`中，通过`rest_framework.routers.DefaultRouter`**注册路由**即可。示例代码如下：

```python
from rest_framework.routers import DefaultRouter

# 只要继承自restframwork.viewsets.GenericViewSet 就可以使用这种路由注册方法 
router = DefaultRouter()
router.register("merchant",MerchantViewSet,basename="merchant") # 要有 basename 参数 

urlpatterns = []+router.urls
```

那么以后通过相应的`method`和`url`即可进行操作。

### ModelViewSet

因为我们一个视图集基本上都是针对一个模型进行操作的，所以我们可以使用`ModelViewSet`简化以上的代码。比如以上代码，我们可以写成：

```python
class MerchantViewSet(viewsets.ModelViewSet):
    '''
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    '''
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
```



## 搜索过滤

自定义搜索类视图 

```python
# GET /定义的url/?search=xxx 
from rest_framework import generics,filters 
class MerchantSearchView(generics.ListAPIView):
    # 默认搜索参数为?search=xx
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    filter_backends = [filters.SearchFilter ] # 搜索的后端逻辑
    # 搜索字段 双下划线是关联模型的字段名 
    search_fields = ['name','categories__name','categories__goods_list__name'] 

```



## 认证和权限

### 认证

#### BasicAuthentication

认证可以简单的理解用户合法性校验。

只要认证通过了，那么在`request`对象（是drf的request对象）上便有两个属性，一个是`request.user`，一个是`request.auth`，**前者就是`django`中的`User`对象，后者根据不同的认证机制有不同的对象**。`DRF`内置了几个认证的模块。以下进行简单了解。

* rest_framework.authentication.BasicAuthentication：基本的授权。每次都要在`Header`中把用户名和密码传给服务器，因此不是很安全，不能在生产环境中使用。
* rest_framework.authentication.SessionAuthentication：基于`django`的`session`机制实现的。如果前端部分是网页，那么用他是可以的，如果前端是`iOS`或者`Android`的`app`，用他就不太方便了
* rest_framework.authentication.TokenAuthentication：基于`token`的认证机制。只要登录完成后便会返回一个`token`，以后请求一些需要登录的`api`，就通过传递这个`token`就可以了，并且这个`token`是存储在服务器的数据库中的。但是这种`token`的方式有一个缺点，就是他没有自动过期机制，一旦登录完成后，这个`token`是永久有效的，这是不安全的。 





BasicAuthentication的验证流程：

1. 从`request.META`中取出`{Authorization:'basic xxx}'`键值对，META存储的是请求头的信息 。如果没有该键值对，则直接返回None。
2. 对xxx进行base64解码，得到`{username:pwd}`键值对 。调用django的`authenticate`对该键值对进行验证 

```python
class MerchantModelView(ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerialzer

    authentication_classes = [BasicAuthentication] # 可以查看源码了解验证流程 
    permission_classes = [IsAuthenticated]
```

```python
import base64
base64.b64encode(b'hollis:root') # 可以得到base64编码 
```

headers需要含有键值对 

![image-20210530183754390](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/image-20210530183754390.png)



BasicAuthentication在类视图中的`Request`参数构造过程中**，会作为一种可能的验证方式被调用，尝试解码请求头，设置`request.user`属性，为后面的可能的权限permission、节流throttle服务。** 

```python
# APIView 部分源码
def initial(self, request, *args, **kwargs):
    ...
    # Ensure that the incoming request is permitted
    self.perform_authentication(request) # 如果验证成功 reques.user 就是一个对象 便于下面的函数判断
    self.check_permissions(request)
    self.check_throttles(request)
```





#### JSON Web Token认证机制

`JSON Web Token`简称`JWT`。在前后端分离的项目中，或者是`app`项目中，推荐使用`JWT`。

`JWT`是在成功后，把用户的相关信息（比如用户id）以及过期时间进行加密，然后生成一个`token`返回给客户端，客户端拿到后可以存储起来，以后每次请求的时候都携带这个`token`，服务器在接收到需要登录的`API`请求候，对这个`token`进行解密，然后获取过期时间和用户信息（比如用户id），如果过期了或者用户信息不对，那么都是认证失败。`JWT`的相关代码如下：

jwt官网编码解码示例 

```python
>>> import jwt
>>> encoded = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
>>> print(encoded)
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U
>>> jwt.decode(encoded, "secret", algorithms=["HS256"])
{'some': 'payload'}
```

实际过程中，加密的是用户信息的键值对，secret是秘钥。



前后端验证的交互流程：

1. **用户第一次登录**，表单提交用户名、密码 
2. 后台验证表单信息，成功后生成token，返回token、除密码信息外的用户信息（前端展示可能会用到）
3. 前端在浏览器保存token、用户信息，下次访问时携带 
4. 后端解密token，得到用户id。数据库检索id，若用户存在，验证成功，否则失败。

```python
import jwt, time
from jwt.exceptions import ExpiredSignatureError
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import BasicAuthentication, get_authorization_header, BaseAuthentication
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import Response
from serializerapp.serilizer import *
from drfLearn.settings import SECRET_KEY # jwt加密使用的密钥


def generate_token(user):
    # {token:,exp:,'user':user_obj}
    exp_time = int(time.time()) + 7 * 24 * 60 * 60
	# 用于用户第一次返回时
    return {'token': jwt.encode({'user': user.telephone, 'exp': exp_time}, key=SECRET_KEY),
            'user':MTUserSerializer(user).data} # 对User也进行序列化

# 验证逻辑 仿照 BaseAuthentication 编写 
class JWTAuthentication(BaseAuthentication):
    """
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: JWT 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'JWT'
    model = get_user_model()

    def authenticate(self, request):
        # from restframework.authentication import get_authorization_header
        auth = get_authorization_header(request).split()  # ['basic','xxx']

        # 没有验证或者验证方式不是jwt
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            '''
            尝试解码
            jwt token中`exp`字段的作用：
            `jwt.decode()`在解码的时候会验证exp字段，检查token是否过期。如果是，就抛出异常。
            '''
            
            token = jwt.decode(auth[1].decode(), key=SECRET_KEY, algorithms=["HS256"]) # 指定算法 

            try:
                user = self.model.objects.get(pk=token.get('user'))
                return  user,token['user'] 
            except Exception:
                # 用户不存在
                msg = "User does't exist"
                raise exceptions.AuthenticationFailed(msg)

        except ExpiredSignatureError:
            # token过期
            msg = 'Invalid token header.Expired Token'
            raise exceptions.AuthenticationFailed(msg)


# 用户第一次登录 请求验证时  不会有token 
# login 视图函数 权限应该为 AllowAny 
class LoginAPIView(APIView):
    def post(self, request):
        # 前端表单 提交 {username,password}
        user=authenticate(telephone=request.data.get('username'),
                          password=request.data.get('password'))
        if user:
            return Response(generate_token(user))
        else:
            return Response('用户名或者密码错误')
            
            
# 当用户登录后 ，jwt验证
class MerchantModelView(ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerialzer
	
    # 增加 jwt 验证
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
```





#### 配置认证

配置认证有两种方式

1. 全局的，在`settings.REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES`中配置。
2. 单个视图，通过`authentication_classes`进行配置。示例代码如下：

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['apps.mtauth.authentications.JWTAuthentication']
}
```

### 权限

**权限在具体层面的增删改查，映射到视图操作，就是post\delete\put\get等操作，因此控制权限，就是限制不同用户对这些method的有无。**

不同的`API`拥有不同的访问权限。比如普通用户有读文章的权限，但是没有删除文章的权限。因此需要用到权限来进行`API`的管理。以下是`DRF`自带的权限。

* permissions.AllowAny：允许所有人访问。
* permissions.IsAuthenticated：登录用户才可以访问（判断条件是`request.user and request.user.is_authenticated`）
* permissions.IsAdminUser：是管理员。（判断条件是`request.user and request.user.is_staff`）
* permissions.IsAuthenticatedOrReadOnly：是登录的用户，并且这个`API`是只能读的（也就是`GET`、`OPTIONS`、`HEAD`）。

#### 自定义权限：

自定义权限要遵循两个条件：

1. 继承自`permissions.BasePermission`。
2. 实现`has_permission(self,request,view)`或者是`has_object_permission(self, request, view, obj)`方法。第一个方法用管理整个视图的访问权限，第二个方法可以用来管理某个对象的访问权限（比如只能修改自己的用户信息）。

```python
from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

#### 配置权限：

权限的使用也是两种方式

1. `settings.REST_FRAMEWORK.DEFAULT_PERMISSION_CLASSES`全局设置
2. 在具体的视图函数中通过`permission_classes`来设置。比如：

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# views.py
class ExampleView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

## 限速节流

使用`drf`可以给我们的网站`API`限速节流。比如一些爬虫，爬你网站的数据，那么我们可以通过设置访问的频率和次数来限制他的行为。

### 配置

限速节流配置也是分成两种：

1. 在`settings.REST_FRAMEWORK`中全局设置，配置分成两个，一个是`throttle_classes`配置不同的节流方式，另外一个是`throttle_rates`配置节流的策略。
2. 针对每个视图函数进行设置。

```python
# settings.py 
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [ # 节流方式 
        'rest_framework.throttling.AnonRateThrottle',  
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': { # 节流策略 会根据 节流类的scope 属性来限制节流
        'anon': '100/day', # 针对AnonRateThrottle 每天访问100次  这里的anon是节流类的标识 scope 
        'user': '1000/day' # 针对UserRateThrottle 
    }
}

# views.py
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

class ExampleView(APIView):
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

### 节流的类

在`drf`中，节流的类总共有以下三个：

#### AnonRateThrottle：

针对那些没有登录的用户进行节流。默认会根据`REMOTE_ADDR`，也就是用户的`IP`地址作为限制的标记。如果用户使用了透明代理（匿名代理没法追踪），那么在`X-Forwarded-For`中会保留所有的代理的`IP`。比如下图：

![img](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/MultipleProxySetup.png)

这时候就要看在`settings.REST_FRAMEWORK.NUM_PROXIES`了，如果这个值设置的是0，那么那么将获取`REMOTE_ADDR`也就是真实的`IP`地址，如果设置的是大于`0`的数，那么将获取代理的最后一个`IP`。

#### UserRateThrottle：

根据用户的`id`来作为节流的标识。

通过继承`UserRateThrottle`类，然后设置`scope`属性，针对不同的`scope`设置不同的节流策略。比如针对管理员`admin`和普通用户`normal`，可以设置不同的策略。代码如下：

```python
class AdminRateThrottle(UserRateThrottle):
    scope = 'admin' # 节流类标识 

class NormalRateThrottle(UserRateThrottle):
    scope = 'normal'
```

然后在`settings.py`中可以如下设置：

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'example.throttles.AdminRateThrottle',
        'example.throttles.NormalRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'normal': '60/day', # 普通用户
        'admin': '1000/day' # 管理员 针对 AdminRateThrottle
    }
}
```

#### ScopedRateThrottle：

根据访问视图`scope`属性来实现节流策略。

在视图中，重写`throttle_scope`属性，指定具体的`scope`，然后在`settings.py`中进行设置。示例代码如下：

```python
# views.py
class ContactListView(APIView):
    throttle_scope = 'contacts' # 为视图标识节流 
    ...

class ContactDetailView(APIView):
    throttle_scope = 'contacts'
    ...

class UploadView(APIView):
    throttle_scope = 'uploads'
    ...

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'contacts': '1000/day',
        'uploads': '20/day'
    }
}
```

### 自定义节流类

自定义节流类

```python
from rest_framework.throttling import SimpleRateThrottle


class SMSRateThrottle(SimpleRateThrottle):  # 继承
     """
    A simple cache implementation, that only requires `.get_cache_key()`
    to be overridden.

    The rate (requests / seconds) is set by a `rate` attribute on the View
    class.  The attribute is a string of the form 'number_of_requests/period'.

    Period should be one of: ('s', 'sec', 'm', 'min', 'h', 'hour', 'd', 'day')

    Previous request information used for throttling is stored in the cache.
    """
        
    scope = 'sms' # 节流类的标识  在settings.py 中会用到 

    def get_cache_key(self, request, view): # 参考  父类的格式 
        if request.user.is_authenticated:
            ident = request.user.pk # 返回用户
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

 
# settings.py 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['apps.mtuser.authentications.JWTAuthentication'],
    'DEFAULT_THROTTLE_RATES': {
        'sms': '2/day',
    }
}
```

# 服务器部署

## django配置

### 环境配置

1. 后端用到的环境导出 `pip freeze >requirements.txt` 
2. 数据库导出sql运行文件 
3. 服务器配置django环境
4. 配置数据库。生成数据库，然后执行django的迁移脚本，创建表结构，执行步骤2的sql文件导入数据。
5. 前端代码更改测试`http://127.0.0.1:8000`为服务器ip ，测试服务器的端口是否正常

### 静态文件处理

如果会用django模板体系生成静态文件，由于后面要使用nginx作为资源代理，所以散落的静态文件需要统一存放

1. 在`settings.py`中配置`STATIC_ROOT=os.path.join(BASE_DIR,'staic_dist')` ，用于存放静态资源
2. 运行`python manage.py collectstatic` 收集静态资源 



如果是用vue等前后端分离的项目，在前端`npm run build`以后就是一个统一的静态资源文件夹了**，可以直接交给nginx配置，或者[参考](https://www.cnblogs.com/lymmurrain/p/13894342.html)将其融合进django的静态资源（不推荐）**。

## uwsgi

WSGI协议：**Python Web Server Gateway Interface**，缩写为WSGI，是为python语言定义的web服务器（以下简称server）与web应用（以下简称app）之间的通用接口，没有官方实现，**是一种协议**。

该协议**包含server、app两部分**，定义了server与app之间的解耦规范，使得遵循规范的Server和App之间可以任意搭配。django、flask等后台框架自带一个简单的WSGI server，**但通常用于开发调试，实际生产环境还需要更可靠的WSGI Server**。 

![](https://gitee.com/jiang_hui_kai/images/raw/master/img/wsgi.png)





<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/http与wsgi.png" style="zoom:50%;" />



**uWSGI正是一个这样可靠的web服务器**，实现了上一节提到的`WSGI`协议、`uwsgi`协议、`http`协议等，旨在为部署分布式集群的网络应用开发一套完整的解决方案。他同时支持静态文件、非静态文件的访问，但后者是他的强项。

uwsgi使用python编写，因此使用`pip install uwsgi`安装即可，然后创建一个叫做uwsgi的配置文件。

```shell
[uwsgi]

# Django相关的配置
# 项目的路径: 必须全部为绝对路径
chdir           = /home/hallen/web/DJSystem
# Django的wsgi文件:项目名.wsgi
module          = DJSystem.wsgi
# Python虚拟环境的路径:通过workon命令查看虚拟环境名称
# 如果是系统python环境 
home            = /root/.virtualenvs/django-env


# 进程相关的设置
# 主进程
master          = true
# 最大数量的工作进程
processes       = 10

http = :8080  # 启动端口
# socket文件路径，绝对路径，项目根目录下即可，在nginx中保持一致
socket          = /home/hallen/web/DJSystem/DJSystem.sock

# 设置socket的权限
chmod-socket    = 666
# 退出的时候是否清理环境
vacuum          = true
#日志路径：随便,如果使用supervisor管理uwsgi，就不能再设置log日志了，在supervisor中已经设置了
#daemonize		= /home/hallen/web/DJSystem/DJSystem_uwsgi.log
```

随后，使用`uwsgi --ini uwsgi.ini`以上述配置启动文件，查看`ps aux|grep uwsgi` 进程是否启动。

## nginx

使用nginx作为web服务器的好处：

1. 相比uwsgi，对静态文件的处理更好
2. 相比uwsgi，暴露在公网上，会更安全一点
3. 运维更加方便，例如黑名单的设置 



安装：`apt install nginx` 



nginx的简单操作：

* 启动/停止/重启：`service nginx start/stop/restart` 
* 测试配置文件：`service nginx configtest` 



nginx配置文件参考。每次修改完配置，需要重启nginx服务。

nginx和uwsgi的协作关系是，如果是静态文件，则由nginx代为处理，反之利用socket通信，交给uwsgi处理非静态文件，uwsgi拉起的正是django服务。

```shell
# upstream后面的名字是可以修改的
upstream DJSystem {
	# uwsgi配置文件中配置的sock路径,两者通过socket通信，会自动创建
    server unix:///home/hallen/web/DJSystem/DJSystem.sock; 
}

# 配置服务器 
# 一段server{}可以配置一个端口 

# http 80
server {
    # 监听的端口号:http
    listen      80;
    # 域名或ip
    server_name 192.168.75.128; 
    charset     utf-8;

    # 最大的文件上传尺寸
    client_max_body_size 75M;  

    # 静态文件
    location /static {
        # 静态文件地址：上面配置的收集静态文件的路径
        # alias表示替换url中的/static 为以下路径
        # root 表示拼接root路径+url路径
        alias /home/hallen/web/DJSystem/static_dist; 
        # root /home/hallen/web/DJSystem/;
        # 以下语句表示 重定向到301服务，$开头的表示nginx预定义的关键字
        # return 301 https://$host$request_uri;
    }

    # 非静态文件，转发请求到django服务
    location / {
    	# 对应upstream的名称
        uwsgi_pass  DJSystem;
        # uwsgi_params文件地址：使用默认的就行
        include     /etc/nginx/uwsgi_params; 
    }
}

# HTTPS 443
server {
        listen       443 ssl;
        # 域名
        server_name  xuptnlp.xyz;
		# 证书名称和密钥，参考https颁发机构
        ssl_certificate      xuptnlp.xyz_bundle.crt;
        ssl_certificate_key  xuptnlp.xyz.key;

        ssl_session_cache    shared:SSL:1m;
        ssl_session_timeout  5m;
		
		ssl_protocols TLSv1.2 TLSv1.3;
	 	ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
        ssl_prefer_server_ciphers  on;

        location / {
    		root   /home/voice_nlp/dist;
            index  index.html index.htm;
        }

    }

```

