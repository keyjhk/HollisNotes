教程地址：https://www.runoob.com/bootstrap/bootstrap-tutorial.html 

# 模板

```html
<!DOCTYPE html>
<html>
<head>
    <title>Bootstrap 模板</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 引入 Bootstrap -->
    <link href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <!-- HTML5 Shiv 和 Respond.js 用于让 IE8 支持 HTML5元素和媒体查询 -->
    <!-- 注意： 如果通过 file://  引入 Respond.js 文件，则该文件无法起效果 -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
    <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
</head>
<body>
<h1>Hello, world!</h1>


<!-- jQuery (Bootstrap 的 JavaScript 插件需要引入 jQuery) -->
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<!-- 包括所有已编译的插件 -->
<script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
</body>
</html>
```



# css库

## 网格系统

bs的网格系统（grid system）是一个响应式的、移动设备优先的系统，**可以随着设备的尺寸变化自动伸缩**，最多扩展为12列。

![image-20201005160956478](D:/我的坚果云/学习笔记/python/pictures/bs网格扩展.png)

bs中对屏幕尺寸大小的缩写

| 缩写            | 屏幕尺寸          |
| --------------- | ----------------- |
| xs(extra small) | 超小设备 <768px   |
| sm(small)       | 小型设备 >=768px  |
| md(middle)      | 中型设备 >=992px  |
| lg(large)       | 大型设备 >=1200px |


网格系统**通过一系列包含内容的行和列来创建页面布局**，要求：

* `container`表示容器，容器不可嵌套。`row`是行，`col-*-*`是列。
* 行必须放置在 `.container` 样式内
* 列作为直接子元素放置在行中，而内容放在列中。列与列之间由内边距padding分隔，如果包裹在`row`内，则首尾两列内边距会被一个负的`margin`取消。



基本的网格结构如下

```html
<div class="container">
   <div class="row">
      <div class="col-*-*"></div>
      <div class="col-*-*"></div>      
   </div>
   <div class="row">...</div>
</div>
<div class="container">....
```

**样式`col-<屏幕尺寸型号>-<列数>`会自适应设备分辨率，当设备分辨率满足尺寸型号时，就自动扩展为指定列数。** 

下例，按照格式创建了一个容器，当设备满足超小尺寸时，每一列就占据6个宽度，一行2列，占据2行。当设备满足小尺寸时，，每一列就占据3个宽度，一行之内就能容纳4列。可以缩放浏览器窗口以观察。

```html
<div class="container">
    <div class="row">
        <div class="col-xs-6 col-sm-3"
             style="background-color: #dedef8;
            box-shadow: inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
            <p>人生若只如初见，何事秋风悲画扇</p>
        </div>
        <div class="col-xs-6 col-sm-3"
             style="background-color: #dedef8;box-shadow:
        inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
            <p>等闲变却故人心，却道故人心易变</p>
        </div>

        <div class="clearfix visible-xs">
        </div>

        <div class="col-xs-6 col-sm-3"
             style="background-color: #dedef8;
        box-shadow:inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
            <p>骊山语罢清宵半，泪雨霖铃终不怨</p>

        </div>
        <div class="col-xs-6 col-sm-3"
             style="background-color: #dedef8;box-shadow:
        inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
            <p>何如薄幸锦衣郎，比翼连枝当日愿</p>
        </div>
    </div>
</div>
```



col的其余样式：

* 列偏移，`col-md-offset-<偏移大小>`，表示列的开始位置偏移指定大小。正数表示向右偏移。

  ```html
  
  <div class="col-md-6 col-md-offset-3" >
  <p>
      借助偏移 上面的列实现了居中效果3+6+3
      </p>
  </div>
  ```

* 列排序，` .col-md-push-` 和` .col-md-pull-` 分别实现列的右向拉扯和左向拉扯。可以使列的显示顺序不拘泥于书写顺序 

* 嵌套，列可以嵌套新的行 。按照格式构造row、col即可，**而且col依旧会被划分为12列（尽管这12列是父列的大小）**

  下列所示，在第2列中，又重新开辟了新的2行（row），每行的列（col）加起来依旧为12。

  ```html
  <div class="container">
      <h1>Hello, world!</h1>
      
      <div class="row">
          <div class="col-md-3"
               style="background-color: #dedef8;box-shadow: inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
              <h4>第一列</h4>
              <p>
                  君不见黄河之水天上来，奔流到海不复回
              </p>
          </div>
          <div class="col-md-9"
               style="background-color: #dedef8;box-shadow: inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
              <h4>第二列 - 分为四个盒子</h4>
              
              <div class="row">
                  <div class="col-md-6"
                       style="background-color: #B18904; box-shadow: inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
                      <p>
                          君不见高堂明镜悲白发，朝如青丝暮成雪
                      </p>
                  </div>
                  <div class="col-md-6"
                       style="background-color: #B18904; box-shadow: inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
                      <p>
                          人生得意须尽欢⑷，莫使金樽空对月
                      </p>
                  </div>
              </div>
              
              <div class="row">
                  <div class="col-md-6"
                       style="background-color: #B18904; box-shadow: inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
                      <p>
                          天生我材必有用，千金散尽还复来
                      </p>
                  </div>
                  <div class="col-md-6"
                       style="background-color: #B18904; box-shadow: inset 1px -1px 1px #444, inset -1px 1px 1px #444;">
                      <p>
                          烹羊宰牛且为乐，会须一饮三百杯
                      </p>
                  </div>
              </div>
          </div>
      </div>
  </div>
  ```




## 表单

创建表单的基本步骤：

1. 为`form`元素设置`role="form"` ，默认为垂直表单，也就是各个表单控件垂直分布。

   * 内联表单，表单控件水平分布在一个div里

     ```html
     <form class="form-inline" role="form"></form>
     ```

   * 水平表单，通过列宽设置，将label和控件放在了一行。label要添加`control-label`样式 

     ````html
     <form class="form-horizontal" role="form">
     	<div class="form-group">    
         	<label for="lastname" class="col-sm-2 control-label">姓</label>
         	<div class="col-sm-10">
           		<input type="text" class="form-control" id="lastname" placeholder="请输入姓">
         	</div>
         </div>
     </form>
     ````

     

2. 把标签和控件放在`<div class="form-group">`容器中，这将获得最佳间距

3. 为表单控件元素设置样式`class="form-control"`，如input、select



表单样式使用示例 

下例中整体使用垂直分布，然后在最后一个div中使用水平分布表单，设置了籍贯、性别等选项。

```html
<form role="form">
    <div class="form-group">
        <label for="xing">姓</label>
        <input type="text" class="form-control" id="xing">
    </div>
    <div class="form-group">
        <label for="ming">名</label>
        <input type="text" class="form-control" id="ming">
    </div>
    <div class=" form-inline">
        <div class="form-group">
            <label for="sex">性别</label>
            <select class="form-control" name="sex" id="sex">
                <option value="男">男</option>
                <option value="女">女</option>
            </select>
        </div>

        <div class="form-group">
            <label for="birth">籍贯</label>
            <select class="form-control" name="birth" id="birth">
                <option value="浙江">浙江</option>
                <option value="陕西">陕西</option>
            </select>
        </div>
    </div>

</form>
```

## 按钮

按钮标签的[设置较为简单](https://www.runoob.com/bootstrap/bootstrap-buttons.html)，可以分为

* 按钮类别：default 、danger、  primary  、info，以不同颜色区分按钮类型。 也可以选择为链接添加样式 。

* 按钮大小：btn-lg 、btn-sm、 btn-xs、 btn-block（占据父元素的100%宽度）

* 按钮状态：active，给按钮设置凹陷状态；` disabled="disabled" ` 给按钮设置禁用状态 

* 按钮组 `btn-group`（btn-group-vertical btn-group-lg）、`btn-toolbar` （包含多个group）

  ```html
  <div class="btn_toolbar">
      <div class="btn-group">
          <button class="btn btn-default">点我</button>
          <button class="btn btn-default">点我</button>
      </div>
      <div class="btn-group">
          <button class="btn btn-info">点我</button>
          <button class="btn btn-danger">点我</button>
      </div>
  </div>
  ```

  

# 布局组件

## 导航

**导航元素使用相同的基类`class="nav"`。**

* 标签页导航，`<ul class="nav nav-tabs">` 
* 胶囊式导航 ，`<ul class="nav nav-pills">`
* 垂直分布导航 ， `<ul class="nav nav-pills nav-stacked">` 
* 面包屑导航，`<ul class="breadcrumb">  `



导航栏示例

```html
<ul class="nav nav-tabs">
  <li class="active"><a href="#">Home</a></li>
  <li><a href="#">SVN</a></li>
  <li><a href="#">iOS</a></li>
  <li><a href="#">VB.Net</a></li>
  <li><a href="#">Java</a></li>
  <li><a href="#">PHP</a></li>
</ul>
```

导航栏包含下拉列表

```html
<ul class="nav nav-tabs">
        <li class="active"><a href="#">Home</a></li>
        <li><a href="#">SVN</a></li>
        <li><a href="#">iOS</a></li>
        <li><a href="#">VB.Net</a></li>
        <li class="dropdown">
            <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                Java <span class="caret"></span>
            </a>
            <ul class="dropdown-menu">
                <li><a href="#">Swing</a></li>
                <li><a href="#">jMeter</a></li>
                <li><a href="#">EJB</a></li>
                <li class="divider"></li>
                <li><a href="#">分离的链接</a></li>
            </ul>
        </li>
        <li><a href="#">PHP</a></li>
</ul>
```

## 导航栏

**导航栏是全局的 ，而上一节的导航是局部的，比如说侧边导航栏。**

创建一个默认导航栏的步骤：

1. 创建如下的nav标签，作为容器，包含所有导航元素

   ```html
   <nav class="navbar navbar-default" role="navigation"></nav>
   ```

2. **对于导航标题**，使用样式`navbar-header`，会使相应文字变大一号；**对于普通导航元素**，使用样式`navbar-nav` 



默认导航栏示例 

```html
<nav class="navbar navbar-default" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <a class="navbar-brand" href="#">Header</a>
        </div>

        <ul class="nav navbar-nav">
            <li class="active"><a href="#">iOS</a></li>
            <li><a href="#">SVN</a></li>
            <li><a href="#">hollis</a></li>
        </ul>
    </div>
</nav>
```

![image-20201015094104980](D:/我的坚果云/学习笔记/python/pictures/bs导航栏示例.png)



导航栏中的按钮（表单元素），要求使用样式`navbar-form`。

`navbar-left`、`navbar-right`用于设置元素的左右浮动。

`.navbar-btn` 使按钮元素能够垂直居中在导航栏。

```html
<nav class="navbar navbar-default" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <a class="navbar-brand" href="#">菜鸟教程</a>
        </div>

        <form class="navbar-form navbar-left" role="search">
            <div class="form-group">
                <input type="text" class="form-control" placeholder="Search">
                <button type="submit" class="btn btn-default">提交按钮</button>
            </div>
        </form>
        <button type="button" class="btn btn-default navbar-btn navbar-right">
            导航栏按钮
        </button>
    </div>
</nav>
```



## 输入框组

输入框组（input-group）扩展自 [表单控件](https://www.runoob.com/bootstrap/bootstrap-forms.html)。使用输入框组，一般用于向输入框添加前（后）缀文字。

输入框组示例

```html
<form role="form">
    <p>一个前后缀示例</p>
    <div class="input-group">
        <span class="input-group-addon">$</span>
        <input type="text" class="form-control">
        <span class="input-group-addon">.00</span>
    </div>
</form>
```

## 分页与翻页

链接：https://www.runoob.com/bootstrap/bootstrap-pagination.html 

## 标签 徽章

带有修饰效果的文字标签。同样，分为`default`、`primary`等效果。

```html
<span class="label label-success">成功标签</span>
```

![image-20201015111657790](D:/我的坚果云/学习笔记/python/pictures/bs标签.png)

徽章与标签类似，只是边角更加圆滑，可以实现“点赞”、"消息提醒"等效果。

```html
<span class="badge">50</span>
```

![image-20201015111625817](D:/我的坚果云/学习笔记/python/pictures/bs徽章.png)

## 超大屏幕

可以用于登录页面的设计

```html
<div class="jumbotron">
    <div class="container">
        <h1>欢迎登陆页面！</h1>
        <p>这是一个超大屏幕（Jumbotron）的实例。</p>
        <p><a class="btn btn-primary btn-lg" role="button">
         学习更多</a>
        </p>
    </div>
</div>
```

![image-20201015111538947](D:/我的坚果云/学习笔记/python/pictures/bs超大屏幕.png)

## 缩略图

```html
<div class="container">
    <div class="row">
        <div class="col-md-2">
            
            <a href="#" class="thumbnail">
                <img src="https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3581292644,1396534104&fm=26&gp=0.jpg"
                     alt="通用的占位符缩略图">
            </a>
        </div>

    </div>
</div>

```

![image-20201015112119013](D:/我的坚果云/学习笔记/python/pictures/bs缩略图.png)

## alert警告框

alert同样有success、info、warning等类型。

```html
<div style="width: 500px">
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
                aria-hidden="true">
            &times;
        </button>
        <a href="" class="alert-link">这是一个可以关闭的警告框；button必须如上设置</a>
    </div>

    <div class="alert alert-info">这是一个不可以关闭的提示框</div>
</div>
```



![image-20201015142048105](D:/我的坚果云/学习笔记/python/pictures/bs警告框.png)

## 进度条

创建百分比进度条

* progress设置最外层的进度框。progress-striped条纹进度，为条纹进度添加`active`样式可以支持动画效果。
* progress-bar（`progress-bar-*`，设置不同样式进度，如info、success等）设置内层进度
* style的width属性用来设置进度百分比。

```html
<div class="progress">
    <div class="progress-bar" role="progressbar" aria-valuenow="60" 
        aria-valuemin="0" aria-valuemax="100" style="width: 40%;">
        <span class="sr-only">40% 完成</span>
    </div>
</div>
```

![image-20201015142552771](D:/我的坚果云/学习笔记/python/pictures/bs普通进度条.png)

## 列表组

`list-group`+`list-group-item` 。item中如果带有active效果，会显示为蓝色。

```html
<div class="container well">
    <div class="row">
        <div class="col-md-4">
            <div class="list-group">
                <a href="#" class="list-group-item active">
                    免费域名注册
                </a>
                <a href="#" class="list-group-item">24*7 支持</a>
                <a href="#" class="list-group-item">免费 Window 空间托管</a>
                <a href="#" class="list-group-item">图像的数量</a>
                <a href="#" class="list-group-item">每年更新成本</a>
            </div>
        </div>
    </div>
</div>
```

## 面板

为div设置`panel`样式

```html
<div class="panel panel-default">
    <div class="panel-heading">
        <h3 class="panel-title">
            面板标题
        </h3>
    </div>
    <div class="panel-body">
        面板内容
    </div>
    <div class="panel-footer">
        面板脚注
    </div>
</div>
```

![image-20201015144948481](D:/我的坚果云/学习笔记/python/pictures/bs面板样式.png)

## glyphicon图标





# tmp

![image-20201031112934821](C:/Users/hollis/AppData/Roaming/Typora/typora-user-images/image-20201031112934821.png)



container 与 row  

section 标签？

![image-20201031113048812](C:/Users/hollis/AppData/Roaming/Typora/typora-user-images/image-20201031113048812.png) 



栅格系统是对父元素的划分 



先布局再样式 



文字居中 

text-align:center 作用在下面的行内元素上 



wow+amimate.css 