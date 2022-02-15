# Sass介绍

众所周知，`css`不是一门编程语言。他没法像`js`和`python`那样拥有逻辑处理的能力，甚至导入其他的`css`文件中的样式都做不到。**而`Sass`就是为了解决`css`的这些问题。他它允许你使用变量、嵌套规则、 `mixins`、导入等众多功能**，并且完全兼容`css`语法。`Sass`文件不能直接被网页所识别，写完`Sass`后，还需要专门的工具转化为`css`才能使用。

## Sass文件的后缀名：

`Sass`文件有两种后缀名，一个是`scss`，一个是`sass`。不同的后缀名，相应的语法也不一样。**这里我们使用`scss`的后缀名。包括后面讲到的`Sass`语法，也都是`scss`的后缀名的语法。**

## Sass基本语法：

### 注释：

支持`/* comment */`和`// 注释`两种方式。

### 嵌套：

`Sass`语法允许嵌套。比如`#main`下有一个类为`.header`，那么我们可以写成以下的形式：

```sass
#main{
    background: #ccc;
    .header{
        width: 20px;
        height: 20px;
    }
}
```

这样写起来更加的直观。一看就知道`.header`是在`#main`下的。

### 引用父选择器（`&`）：

有时候，在嵌套的子选择器中，需要使用父选择器，那么这时候可以通过`&`来表示。示例代码如下：

```sass
a{
    font-weight: bold;
    text-decoration: none;
    &:hover{
        color: #888;
    }
}
```

### 定义变量：

是的，你没听错。在`Sass`中可以定义变量。对于一些比较常用的值，我们可以通过变量存储起来，以后想要使用的时候就直接用就可以了。定义变量使用`$`符号。示例代码如下：

```sass
$mainWidth: 980px;
#main{
    width: $mainWidth;
}
```

### 运算：

在`Sass`中支持运算。比如现在有一个容器总宽度是`900`，要在里面平均放三个盒子，那么我们可以通过变量来设置他们的宽度。示例代码如下：

```sass
$mainWidth: 900px;
.box{
    width: $mainWidth/3;
}
```

### @import语法：

**将指定文件的代码拷贝到导入的地方**。示例代码如下：

```sass
@import "init.scss";
```

这就支持了css以import的形式导入，免去了在`<header>`中定义。

### @extend语法：

有时候我们一个选择器中，可能会需要另外一个选择器的样式，那么我们就可以通过`extend`来直接将指定选择器的样式加入进来。**extend适合样式间的拷贝，import是文件的导入**。示例代码如下：

```scss
.error{
    background-color: #fdd;
    border: 1px solid #f00;
}
.serious-error{
    @extend .error;
    border-width: 3px;
}
```

### @mixin语法：

有时候一段样式代码。我们可能很多地方要用到。那么我们可以把他定义成`mixin`。需要用的时候就直接引用就可以了。示例代码如下：

```scss
@mixin large-text {
  font: {
    family: Arial;
    size: 20px;
    weight: bold;
  }
  color: #ff0000;
}
```

如果其他地方想要使用这个`mixin`的时候，可以通过`@include`来包含进来。示例代码如下：

```scss
.page-title {
  @include large-text;
  padding: 4px;
  margin-top: 10px;
}
```

`@mixin`也可以使用参数。示例代码如下：

```scss
@mixin sexy-border($color, $width) {
  border: {
    color: $color;
    width: $width;
    style: dashed;
  }
}
```

那么以后在`include`的时候，就需要传递参数了。示例代码如下：

```scss
p { 
    @include sexy-border(blue, 1px); 
}
```

### 更详细的教程：

更详细的教程可以参考：`http://sass.bootcss.com/docs/sass-reference/`。     

# gulp 

前端我们使用`gulp`来自动化开发流程。配置好`gulp`后，可以自动给我们处理好一些工作。比如写完`css`后，要压缩成`.min.css`，写完`js`后，要做混淆和压缩，图片压缩等。这些工作都可以让`gulp`帮我们完成。

## 安装gulp：

### 1. 创建本地包管理环境：

使用`npm init`命令在本地生成一个`package.json`文件。

### 2. 安装gulp：

`gulp`的安装非常简单，只要使用`npm`命令安装即可。但是因为`gulp`需要作为命令行的方式运行，因此需要在安装在系统级别的目录中。

```shell
npm install gulp -g
```

因为在本地需要使用`require`的方式`gulp`。因此也需要在本地安装一份：

```shell
npm install gulp --save-dev
```

以上的`--save-dev`是将安装的包的添加到`package.json`下的`devDependencies`依赖中。以后通过`npm install`即可自动安装。`devDependencies`这个是用来记录开发环境下使用的包，如果想要记录生产环境下使用的包，那么在安装包的时候使用`npm install xx --save`就会记录到`package.json`下的`dependencies`中，`dependencies`是专门用来记录生产环境下的依赖包的！

### 3. 创建gulp任务：

要使用`gulp`来流程化我们的开发工作。**首先需要在项目的根目录下创建一个`gulpfile.js`文件。**然后在`gulpfile.js`中填入以下代码：

```javascript
var gulp = require("gulp")

gulp.task("greet",function () {
    console.log('hello world');
});
```

这里对代码进行一一解释：

1. 通过`require`语句引用已经安装的第三方依赖包。这个`require`只能是引用当前项目的，不能引用全局下的。`require`语法是`node.js`独有的，只能在`node.js`环境下使用。
2. `gulp.task`是用来创建一个任务。`gulp.task`的第一个参数是命令的名字，**第二个参数是一个函数，就是执行这个命令的时候会做什么事情，都是写在这个里面的。**
3. 写完以上代码后，以后如果想要执行`greet`命令，那么只需要进入到项目所在的路径，然后在终端（terminal）使用`gulp greet`即可执行。

### 4. 创建处理css文件的任务：

**`gulp`只是提供一个框架给我们。如果我们想要实现一些更加复杂的功能**，比如`css`压缩，那么我们还需要安装一下`gulp-cssnano`插件。`gulp`相关的插件安装也是通过`npm`命令安装，安装方式跟其他包是一模一样的（gulp插件本身就是一个普通的包）。
对`css`文件的处理，需要做的事情就是压缩，然后再将压缩后的文件放到指定目录下（不要和原来css文件重合了）！这里我们使用`gulp-cssnano`来处理这个工作：

```shell
npm install gulp-cssnano --save-dev
```

然后在`gulpfile.js`中写入以下代码：

```javascript
var gulp = require("gulp")
var cssnano = require("gulp-cssnano")

// 定义一个处理css文件改动的任务
gulp.task("css",function () {
    gulp.src("./css/*.css")
    .pipe(cssnano())
    .pipe(gulp.dest("./css/dist/"))
});
```

以上对代码进行详细解释：

1. `gulp.task`：创建一个`css`处理的任务。
2. `gulp.src`：找到当前`css`目录下所有以`.css`结尾的`css`文件。
3. `pipe`：管道方法。**将上一个方法的返回结果传给另外一个处理器。比如以上的`cssnano`。**
4. `gulp.dest`：将处理完后的文件，放到指定的目录下。不要放在和原文件相同的目录，以免产生冲突，也不方便管理。

### 5. 修改文件名：

像以上任务，压缩完`css`文件后，最好是给他添加一个`.min.css`的后缀，这样一眼就能知道这个是经过压缩后的文件。这时候我们就需要使用`gulp-rename`来修改了。当然首先也需要安装`npm install gulp-rename --save-dev`。示例代码如下：

```javascript
var gulp = require("gulp")
var cssnano = require("gulp-cssnano")
var rename = require("gulp-rename")
gulp.task("css",function () {
    gulp.src("./css/*.css")
    .pipe(cssnano())
    .pipe(rename({"suffix":".min"}))
    .pipe(gulp.dest("./css/dist/"))
});
```

在上述代码中，我们增加了一行`.pipe(rename({"suffix":".min"}))`，这个我们就是使用`rename`方法，并且传递一个对象参数，指定修改名字的规则为添加一个`.min`后缀名。这个`gulp-rename`还有其他的指定文件名的方式，比如可以在文件名前加个前缀等。更多的教程可以看这个：`https://www.npmjs.com/package/gulp-rename`。

### 6. 创建处理js文件的任务：

处理`js`文件，我们需要使用到`gulp-uglify`插件。安装命令如下：

```shell
npm install gulp-uglify --save-dev
```

安装完后，我们就可以对`js`文件进行处理了。示例代码如下：

```js
var gulp = require("gulp")
var rename = require("gulp-rename")
var uglify = require('gulp-uglify');
gulp.task('script',function(){
    gulp.src(path.js + '*.js')
    .pipe(uglify())
    .pipe(rename({suffix:'.min'}))
    .pipe(gulp.dest('js/'));
});
```

这里就是增加了一个`.pipe(uglify())`的处理，对`js`文件进行压缩和丑化（修改变量名）等处理。更多关于`gulp-uglify`的教程。请看：`https://github.com/mishoo/UglifyJS2#minify-options`。

### 7. 合并多个文件：

在网页开发中，为了加快网页的渲染速度，有时候我们会将多个文件压缩成一个文件，从而减少请求的次数。要拼接文件，我们需要用到`gulp-concat`插件。安装命令如下：

```shell
npm install gulp-concat --save-dev
```

比如我们现在有一个`nav.js`文件用来控制导航条的。有一个`index.js`文件用来控制首页整体内容的。那么我们可以使用以下代码将这两个文件合并成一个文件：

```js
var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
gulp.task('vendorjs',function(){
    gulp.src([
        './js/nav.js',
        './js/index.js'
    ])
    .pipe(concat('index.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest('dist/js/'));
});
```

### 8. 压缩图片：

图片是限制网站加载速度的一个主要原因。图片越大，从网站上下载所花费的时间越长。因此对于一些图片，我们可以采取无损压缩，即在不改变图片质量的基础之上进行压缩。在`gulp`中我们可以通过`gulp-imagemin`来帮我们实现。安装命令如下：

```shell
npm install gulp-imagemin --save-dev
```

压缩图片也是一个比较大的工作量，对于一些已经压缩过的图片，我们就没必要再重复压缩了。这时候我们可以使用`gulp-cache`来缓存那些压缩过的图片。安装命令如下：

```shell
npm install gulp-cache --save-dev
```

两个插件结合使用的代码如下：

```js
var imagemin = require('gulp-imagemin');
var cache = require('gulp-cache');
gulp.task('image',function(){
    gulp.src("./images/*.*")
    .pipe(cache(imagemin()))
    .pipe(gulp.dest('dist/images/'));
});
```

### 9. 检测代码修改，自动刷新浏览器：

以上所有的任务，我们都是需要手动的在终端去执行。这样很不方便我们开发。最好的方式就是我修改了代码后，`gulp`会自动的执行相应的任务。这个工作我们可以使用`gulp`内置的`watch`方法帮我们完成：

```js
var gulp = require("gulp")
var cssnano = require("gulp-cssnano")
var rename = require("gulp-rename")

// 定义一个处理css文件改动的任务
gulp.task("css",function () {
    gulp.src("./css/*.css")
    .pipe(cssnano())
    .pipe(rename({"suffix":".min"}))
    .pipe(gulp.dest("./css/dist/"))
    .pipe(connect.reload())
});

// 定义一个监听的任务
gulp.task("watch",function () {
    // 监听所有的css文件，然后执行css这个任务
    gulp.watch("./css/*.css",['css'])
});
```

以后只要在终端执行`gulp watch`命令即可自动监听所有的`css`文件，然后自动执行`css`的任务，完成相应的工作。

### 10. 更改文件后，自动刷新浏览器：

以上我们实现了更改一些`css`文件后，可以自动执行处理`css`的任务。但是我们还是需要手动的去刷新浏览器，才能看到修改后的效果。有什么办法能在修改完代码后，自动的刷新浏览器呢。答案是使用`browser-sync`。`browser-sync`安装的命令如下：

```shell
npm install browser-sync --save-dev
```

`browser-sync`使用的示例代码如下：

```js
var gulp = require("gulp")
var cssnano = require("gulp-cssnano")
var rename = require("gulp-rename")
var bs = require("browser-sync").create()

gulp.task("bs",function () {
    bs.init({
        'server': {
            'baseDir': './'
        }
    });
});

// 定义一个处理css文件改动的任务
gulp.task("css",function () {
    gulp.src("./css/*.css")
    .pipe(cssnano())
    .pipe(rename({"suffix":".min"}))
    .pipe(gulp.dest("./css/dist/"))
    .pipe(bs.stream())
});

// 定义一个监听的任务
gulp.task("watch",function () {
    gulp.watch("./css/*.css",['css'])
});

// 执行gulp server开启服务器
gulp.task("server",['bs','watch'])
```

以上我们创建了一个`bs`的任务，这个任务会开启一个`3000`端口，以后我们在访问`html`页面的时候，就需要通过`http://127.0.0.1:3000`的方式来访问了。然后接下来我们还定义了一个`server`任务。这个任务会去执行`bs`和`watch`任务，只要修改了`css`文件，那么就会执行`css`的任务，然后就会自动刷新浏览器。
`browser-sync`更多的教程请参考：`http://www.browsersync.cn/docs/gulp/`。



## gulp文件示例

[package.json地址](.\resources) 

```js
var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var concat = require('gulp-concat');
var bs = require('browser-sync').create();
var sass = require('gulp-sass');
var util = require('gulp-util');
var sourcemaps= require('gulp-sourcemaps');

//定义路径
var path={
    'html':'templates/**/',
    'css':'src/css/',
    'js':'src/js/',
    'image':'src/image/',
    'css_dist':'dist/css/',
    'js_dist':'dist/js/',
    'image_dist':'dist/image/'
};

//测试gulp框架
gulp.task('hello',function () {
    console.log('hello world');
});


//处理html gulp.task('task_name',function)
gulp.task('html',function (done) {
    gulp.src(path['html']+'*.html')
        .pipe(bs.stream());
    done();
});

//处理scss
gulp.task('scss',function (done) {
    //处理scss 文件
    gulp.src(path['css']+'**/*.scss')
        .pipe(sass().on('error',sass.logError)) //处理scss语法
        // .pipe(cssnano()) //压缩css文件
        .pipe(rename({'suffix':'.min'})) //重命名添加后缀.min
        .pipe(gulp.dest(path['css_dist'])) //移到到目标路径 css_dist
        .pipe(bs.stream());

    done();
});

//处理css
gulp.task('css',function (done) {
    gulp.src(path['css']+'**/*.css')
        // .pipe(cssnano()) //压缩css文件
        .pipe(rename({'suffix':'.min'})) //重命名添加后缀.min
        .pipe(gulp.dest(path['css_dist'])) //移到到目标路径 css_dist
        .pipe(bs.stream());

    done();
});

//处理js
gulp.task('js',function (done) {
    gulp.src(path['js']+'*.js') //源文件
        // .pipe(sourcemaps.init())
        // .pipe(uglify().on('error',util.log)) // 简化
        // .pipe(sourcemaps.write())
        .pipe(rename({'suffix':'.min'})) //重命名添加后缀.min
        .pipe(gulp.dest(path['js_dist'])) //目标路径存放
        .pipe(bs.stream()); //浏览器刷新
    done();
});

//处理image
gulp.task('image',function (done) {
    gulp.src(path['image']+'*.*')
        .pipe(gulp.dest(path['image_dist']))
        .pipe(bs.stream());
    done();
});

//监听
gulp.task('watch',function (done) {
    //监听的是整个文件夹，具体的文件位置则由每个任务去配置
    gulp.watch(path['css'],gulp.series('css'));
    gulp.watch(path['css'],gulp.series('scss'));
    gulp.watch(path['js'],gulp.series('js'));
    gulp.watch(path['image'],gulp.series('image'));
    gulp.watch(path['html']+'*.html',gulp.series('html'));
    done();
});

//浏览器实时同步
gulp.task('bs',function (done) {
    bs.init({
        'server':{
            'basedir':'./templates/'
        }
    });
    done();
});

gulp.task('default',gulp.parallel('bs','watch')); //开启浏览器自动刷新
// gulp.task('default',gulp.series('watch'));
```

