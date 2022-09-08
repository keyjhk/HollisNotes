[toc]



# vscode配置 

## 插件安装

1. `jshint`：`js`代码规范检查。
2. `Beautify`：一键美化代码的插件。
3. `Vetur`：`.vue`文件识别插件。 
4. `Javascript(ES6) code snippets`：`ES6`语法提示。
5. `Auto Rename Tag`：自动重命名标签。html标签都是成对出现的，开始标签修改了，结束标签也会跟着修改。
6. `Auto Close Tag`：自动闭合标签。针对一些非标准的标签，这个插件还是很有用的。
7. `vue helper`：一些`Vue`代码的快捷代码。
8. `vscode-icons`：可选。提供了很多类型的文件夹`icon`，不同类型的文件夹使用不同的`icon`，会让文件查找更直观。
9. `open in browser`：可选。右键可以选择在默认浏览器中打开当前网页。

## 自定义代码模板 

vsCode自定义代码片段：

1. crtl+shift+p ，打开命令行窗口

2. 搜索snippet 关键字，选择`prefrence:configure user snippets`

3. 选择对应模板，例如，`html.json` 。

4. 在每一个模板上，都会有相应的提示。其自定义模板如下

   ```json
   "print to console 是自定义模板名
   prefix 是启动模板的快捷键 
   body 是模板实体 每一行都是一个字符串 
   如果字符串含有双引号 ，要改为单引号（因为json最外面的字符串使用了“”）
   $1 $2 表示光标停留处 按一下tab 光标会移到下一处 
   "
   
   "Print to console": {
       "prefix": "log",
       "body": [
           "console.log('$1');",
           "$2"
       ],
       "description": "Log output to console"
   }
   ```

   

## 快捷键

vue的快捷键查看方式：按下`crtl+k`然后迅速按下`crtl+s`就能打开快捷窗口，查看所有快捷键。

# vue

## 引入

用外部脚本的方式引入 

```html
<script src="https://cdn.staticfile.org/vue/2.2.2/vue.min.js"></script>
```

在`script`部分就可以使用vue

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>vue模板</title>
  <script src="https://cdn.jsdelivr.net/npm/vue"></script>

</head>

<body>
  <div id="app">
	
  </div>
    
  <script>
    let vm = new Vue({
      el: '#app',
      data: {
		// 属性
      },
      methods: {
		// 方法
      }

    });
  </script>

</body>

</html>
```



## 基本使用

创建一个`Vue`对象，并且在这个对象中传递`el`参数（element）。

el元素作为`Vue`实例渲染的根元素，根元素及其子元素才可以访问vue对象里的数据和方法。

```html
<div id="app">
</div>

<script>
  let vm=new Vue({
    el:'#app',
    data:{},
    methods:{}
  });
</script>
```

## 模板语法 

数据如何与html标签交互。

### 文本&属性

通过`{{ variable }}`（双大括号）中插入Vue对象中的数据到文本

```html
<p>{{name}}</p>
```

花括号的形式默认会转为字符串，如果数据是html标签，并且想正常渲染，使用`v-html`属性。

```html
<div id="app">
    <div v-html="code"></div>
</div>
<script>
    let vm = new Vue({
        el: "#app",
        data: {
            "code": "<a href='https://www.baidu.com/'>百度一下，你就知道！</a>"
        }
    });
</script>
```





通过`:attr=""`  冒号使用vue对象的数据作为标签属性，冒号是简化后的指令`v-bind:attr=""` 。

```vue
<img :src="this.img.src">
```



使用`{{}}` 的文本 或者 `:` 的属性中可以使用js表达式

```vue
{{username.split("").reverse().join("")}}
```





### class&style

设置class的方式有两种

1. 利用数组的形式，`:class="[c1,c2]"`，**其中c1、c2是vue对象的data数据**
2. 直接使用`<style>`标签中定义的样式名，后跟布尔值，表示是否应用该样式。这种手段可以作为开关控制样式的应用。`:class="{'style1':true,style_2:false}"` 。**style加引号不是必须的，但若命名不符合js对象规范（例如含有横杆-）就一定要加引号。**

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>vue模板</title>
  <script src="https://cdn.jsdelivr.net/npm/vue"></script>

  <style>
    .title {
      color: red;
      font-size: 20px;
    }

    .funny-style {
      font-style: italic;
    }
  </style>

</head>

<body>
  <div id="app">
    <!-- class1 是vue里的数据  -->
    <p :class="[class1,class2]">hello hollis</p>

    <!-- 每一个键直接使用style的样式名 利用js对象的形式设置class  -->
    <!-- 如果样式里带了- 应该要用引号包裹 -->
    <!-- 键被理解为js的对象，只允许字母、数字、下划线 -->
    <p :class="{'title':true,'funny-style':false}">hello hollis</p>
  </div>
  <script>
    let vm = new Vue({
      el: '#app',
      data: {
        class1: 'title',
        class2: 'funny-style'
      },
      methods: {

      }

    });
  </script>

</body>

</html>
```



style属性: 创建对象，键值对形式

1. 单样式：`:style=""`
2. 多样式：`:style=[...]` 

```html
<div id='app'>
    <p :style="[mystyle1,mystyle2]">hello hollis</p>
    <p :style="mystyle1">hello hollis</p>
</div>
<script>
    let vm = new Vue({
        el: '#app',
        data: {
            // key:val 
            mystyle1:{
                "background-color":"blue",
                "color":"white"
            },
            mystyle2:{
                "border":"5px solid gold"
            }
        },
        methods: {

        }
    });
</script>
```



### 条件判断

#### v-if

if-else-if 判断

```html
<div id="app">
    <p v-if="weather == 'sun'">判断p标签！</p>
    <p v-else-if="weather == 'rain'">今天去看电影！</p>
    <p v-else>今天哪儿也不去！</p>
  </div>
<script>
    let vm = new Vue({
        el: "#app",
        data: {
            weather: 'rain'
        }
    });
</script>
```



在使用 v-if 切换组件的时候，**vue会惰性渲染，重用组件节省资源**。例如，同样的input组件在视图切换的时候会保存上一个input的历史输入。为元素增加`key`属性作为标识，可以解决此问题。

```vue
<input type="text" id="username" key="username"> 
```



#### v-show



`v-if`是“真正”的条件渲染，**它会确保在切换过程中条件块内的事件监听器和子组件适当地被销毁和重建**。同时，它也是惰性的：如果在初始渲染时条件为假，则什么也不做。如果条件变为真了，就会销毁前者的组件，然后重新渲染。

相比之下，`v-show`就简单得多，**它是基于css样式控制的**——不管初始条件是什么，**元素总是会被渲染**，但是会给那些不显示的元素增加属性`display:none`。这就表示使用`v-show`控制的组件不会有留存历史记录的问题（因为它们是不同的组件）。

 一般来说，`v-if`有更高的切换开销，而`v-show`有更高的初始渲染开销。因此，如果需要非常频繁地切换，则使用`v-show`较好；如果在运行时条件很少改变，则使用`v-if`较好，例如后台人员的超级管理员、普通用户登录页面。



**v-show只能在普通的html上标签使用，template无法使用，可以用`div`标签代替**。

```vue
 <div v-show="loginType=='email'">
</div>
```



### for循环

v-for的写法

```js
// 对象
v-for="(value, name) in object" // val key 
v-for="value in object"  // val of object

// 数组
v-for="item of/in items" // item of items
v-for="(item, index) in items" // item indx 
```

**在 `v-for` 块中，我们可以访问所有父作用域的 property**。 

```html
<div v-for="item in items" v-bind:key="item.id">
  <!-- 内容 -->
</div>
```

 



2.2+的版本中，使用`v-for`时，key属性是必须的。

key属性的添加，方便vue能跟踪每个节点的身份，从而重用和重新排序现有元素。

![img](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/3973616-25f6c171772b50b6.jpg) 



关于key属性的有无：

* 简书例子：https://www.jianshu.com/p/4bd5e745ce95  
* 官网：https://cn.vuejs.org/v2/guide/list.html#维护状态 





## ref属性

设置属性`ref="ref_name"`  

```html
<div class="category-group" ref="category"></div>
```

获取元素

```js
this.$refs.category 
```



## 事件绑定

通过`v-on`绑定事件的，可以简写成`@`，例如`@click`等价于`v-on:click` 。

```vue
<button v-on:click="count+=1">直接执行js代码</button>
<button v-on:click="subtract(10)">调用method里的函数</button>
```





事件修饰符用来装饰事件发生时的动作，格式为`事件.修饰符` 。

`$event$` 参数是原生DOM 的event事件。



下例，禁止了a标签默认的跳转点击事件，改为跳转到360。

```html
<div id="app">
    <a href="https://www.baidu.com/" @click="gotoWebsite($event)">百度</a>
</div>
<script>
    let vm = new Vue({
        el: "#app",
        data: {
            count: 0
        },
        methods: {
            gotoWebsite: function(event){
                event.preventDefault();
                window.location = "https://www.360.cn/"
            }
        }
    });
</script>
```



vue为一些常用的事件提供了修饰符：

1. `.prevent`，阻止默认事件 
2. `.stop`：`event.stopPropagation`，**阻止事件冒泡（内层元素的点击事件会逐层冒泡到外层节点）**
3. `.capture`：事件捕获，获取事件的优先级最高。
4. `.once`：这个事件只执行一次。
5. `.self`：代表当前这个被点击的元素自身。
6. `.passive`：在页面滚动的时候告诉浏览器不会阻止默认的行为，从而让滚动更加顺畅。

```vue
<div id="innerDiv" @click.stop="clickInnerDiv"></div>
```





## 计算属性

v-model 获取控件数据到 data 属性 

**有些属性不是静态的，需要依赖逻辑计算才可以得到**，比方说”矩形面积“依赖输入的长和宽。

计算属性声明：

```js
computed:{  //计算属性 
    prop:function(){
        // prop是计算属性名 默认是GET
        // 不可递归调用 如 this.prop
        // return val;
    }
},
```

计算属性需要修改赋值时，提供一个SET函数。

```js
computed:{  //计算属性 
    prop:{
        get:function(){
            // 获取 
    },
        set:function(){
            // 设置相关属性
        }
    }
},
```

访问形式同data数据无异，不用加括号

```vue
{{ prop }}
```



## 监听器

监听对象属性，如果发生了变化，就执行一些动作。

创建监听器的步骤：

1. 在控件上使用`v-model` 实现双向数据绑定，这样子用户的输入才能更改data里的数据

   ```html
   <input type="text" name="search" v-model="keyword">
   ```

   

2. 创建`watch:{}`，如下所示。**函数名即为监听属性名**，`watched_data(new,old)` ，第一个参数是新值，后一个参数是旧值。

```js
watch:{
    keyword(new_keyword, old_keyword)
    {
        // 监听keyword值
        // 第一个参数是最新的value 第二个参数是之前的value 
        this.result = old_keyword + '==>' + new_keyword;
    }
}
```

## v-model

**`v-model`实现数据的双向绑定**。

如果用于表单，能够自动依据控件类型（input、checkbox等）读取不同的属性。



```html
<input v-model="message" placeholder="请输入...">
<p>输入的内容是：{{ message }}</p>
```



**修饰符**：用于控制表单控件元素更改对象数据的动作，类似于django的过滤器

* `.lazy`：在默认情况下，`v-model`在每次`input`事件触发后将输入框的值与数据进行同步 。你可以添加`lazy`修饰符，那么只有当焦点消失时，才会发生同步

  ```html
  <!-- 在“change”时而非“input”时更新 -->
  <input v-model.lazy="msg" >
  ```

* `.number`：如果想自动将用户的输入值转为数值类型，可以给`v-model`添加`number`修饰符。

  ```html
  <input v-model.number="age" type="number">
  ```

* `.trim`：自动过滤用户输入的首尾空白字符，可以给 v-model 添加 trim 修饰符。

  ```html
  <input v-model.trim="msg">
  ```



## 自定义组件

**每个组件本质上是一个vue实例。**

自定义组件：

1. **data要求是一个函数，该函数返回一个对象** 。函数形式的data，可以保证每个组件对应一份独立的data副本
2. **template包含单一根元素。**

全局定义组件：

```js
// 全局注册 
// 命名风格：组件名推荐使用kebab风格，短横线隔开多个单词 因为HTML对大小写不敏感
// 存储风格：存储该组件文件时，推荐以大驼峰命名vue文件，`MyComponet.vue`
Vue.component('my-component', {
    data: function(){
        return {
            count: 0, // data的键值对 
        }
    },
    template: '<span>这里写标签</span>'
});
```

使用组件

```html
<my-component></my-component>
```



定义组件名的方式有两种：

使用 kebab-case

```js
Vue.component('my-component-name', { /* ... */ })
```

当使用 kebab-case (短横线分隔命名) 定义一个组件时，你也必须在引用这个自定义元素时使用 kebab-case，例如 `<my-component-name>`。

使用 PascalCase

```js
Vue.component('MyComponentName', { /* ... */ })
```

当使用 PascalCase (首字母大写命名) 定义一个组件时，你在引用这个自定义元素时两种命名法都可以使用。也就是说 `<my-component-name>` 和 `<MyComponentName>` 都是可接受的。注意，尽管如此，直接在 DOM (即非字符串的模板) 中使用时只有 kebab-case 是有效的。





### 组件注册

全局注册 ，可以随意使用

```js
// 全局注册 
Vue.component('组件名', {
});
```



局部注册 ，在需要使用的组件中定义`components`属性。

```js
var ComponentA = { 
    name:'',
    data:function(){}，
}; // 变量形式保存对象 

var ComponentB = {
  components: {
    'component-a': ComponentA ,// 组件B局部注册组件a 在组件B中可以使用 
  },
  // ...
}
```

### 组件属性 

`props`，作为组件对外暴露的属性attr

props创建有2种形式 

```js
// 可以是一个简单的数组 原型开发时使用 不推荐 
props:[attr1,..]

props:{
    // 详细定义 类型、是否必要等
    books:{
        type:Array,
        required:true,
            default:function(){
                // default 的形式有多种
                // default:0 
                // 如果type是object 要求default是函数 
            }
    }
}
```

**props里定义的属性和自定义组件里的data拥有同等地位，template里可以同样访问。**



示例：

属性创建：

```js
props: {
  greetingText: String // html同样可以使用kecab-case 
}
```

给组件属性赋值

```html
<WelcomeMessage greeting-text="hi"/>
```



###   组件通信

1. 子组件的事件函数向外抛出自定义事件 

   ```js
   // 这会向它的父组件抛出一个事件，名字就是自定义事件名
   // html属性不区分大消息，所以自定义事件名一般使用 - 分隔 ，如inner-click
   click(){
      this.$emit('子组件定义事件',参数1,..) 
   }
   ```

2. 父组件捕捉子组件抛出的事件，写在最外层的 `methods`里。 

   ```
   @child-event="function"



示例：

```js
// 全局注册一个组件 
Vue.component('mycheckbox', {
    props: ['man'],
    methods: {
        inner_click: function () {
            // 向外抛出事件 叫做 mylick 
            this.$emit('myclick', this.man); 
        }
    },
    // 模板里包含了一个input 子组件 
    template: `
      <div>
          <span>{{man}}</span>
          <input type="checkbox"  @click="inner_click">范端权
      </div>
      `
})

// 根组件 
let vm = new Vue({
    el: '#app',
    data: {
        man: 'hollis'
    },
    methods: {
        outterclick: function (man) {  // man 将会是子组件上传的数据 
            console.log('ouuter click function', man);
        }
    }
```

父组件捕捉的事件名字叫做 `myclick` 

```html
<div id='app'>
    <!-- 用类似于传参的形式往自定义组件里传递属性 -->
    <mycheckbox :man='man' @myclick='outterclick'></mycheckbox>
</div>
```



### 组件v-model 

父组件赋值给子组件的prop如何同步 



**子组件内部不能修改父组件传递的值**，只能向外传递：

1. 增加组件属性`model`  

```js
props:['属性x'],
model:{
    prop:'属性x',    // 绑定属性  
    event:'事件名', // 当该事件触发时 组件向外抛出新的值 
}
```

2. 在事件函数中中抛出触发事件  

```js
function(){
    this.$emit('触发事件名',属性值)  
}
```



计步器示例

```js
Vue.component('haojunyu', {
      props: ['count'], 
      // v-model 相关的配置 
      model: {
        prop: 'count', // v-model 数据传入时绑定哪个属性
        event: 'count-changed' //当该事件触发时向外传出count 
      },
      methods: {
        substract: function () {
          // 标准写法 抛出事件+新的count值
          this.$emit('count-changed', this.count - 1>=0?this.count-1:0);
        },
        add: function () {
          // 与 substract 同理
          this.$emit('count-changed', this.count + 1);
        }
      }
}
)
```

父组件赋值，接收从子组件传过来的新值 

```vue
<haojunyu v-model="good_count"></haojunyu>
```



### 插槽

#### 单插槽

在没有使用插槽的情况下，我们的自定义组件不允许在标签之间嵌入文本

```html
<mybtn>这里写自己的东西</mybtn>
```

使用插槽`slot`可以实现这个效果。



模板里的插槽允许写上默认值，这些默认值会在实际传入值时被覆盖。**可以是普通文字、标签、另外一个自定义模板。**

```js
Vue.component('my-btn', {
    template: `       
      <button>
      <slot>确认</slot>
    </button>
        `
})
```

使用插槽

```vue
 <my-btn>取消</my-btn>
```

#### 命名插槽

当模板里存在多个插槽时，可以为插槽命名。

* 为插槽命名`<slot name=""></slot>`   

  ```js
  Vue.component('my-page', {
      template: `
        <div>
          <p style="background-color: sandybrown;">
             <slot name='header'></slot>
          </p>
      	<p style="background-color:seagreen">
        		<slot name='body'></slot>
      	</p>    	
        </div>      
        `
  });
  ```

  

* 在使用到插槽的地方，` <template v-slot:插槽名>插入的内容</template>`   ,`v-slot:`可以简写为`#` 

```html
 <my-page>
      <template v-slot:header>header</template>
      <template #body>body</template>
</my-page>
```





### css样式

在自定义组件样式时，`<style scoped>`，表示局部样式。

vue在模板编译时，**就会为该模板里的样式自动加上哈希**，使其仅作用于当前组件。

```scss
// 类选择器[属性选择器]
// 这个属性是用来标识该组件的 vue自动生成
.title[data-v-211e4c4a] {
    color: #ff0;
}
```

所以正常情况下，父组件即使出现了和子组件同名的样式，也不对对其造成影响。



但如果确实想在父组件中更改子组件的样式，使用`>>>`或`/deep/` 。

```css
<style scoped>
	 // 子组件的 title属性也会受到影响 
     /deep/ .title{
        color: #ff0;
    }
</style>
```

或者在scss语法下 使用`::v-deep`

```scss
<style scoped lang="scss">
  ::v-deep .el-collapse-item__header {
    background: #1f2f3d;
    color: pink;
  }
  
</style>
```



## 生命周期函数



<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/vue_lifecycle.png" alt="img" style="zoom: 50%;" />





### 创建期间

#### beforeCreate

`Vue`或者组件刚刚**实例化**，**`data`、`methods`都还没有被创建**。

#### created

**此时`data`和`methods`已经被创建**，可以使用了。**模板还没有被编译。**

#### beforeMount

`created`的下一阶段。此时模板被编译，静态的data数据被渲染到模板了，**但是只是存在于内存中，还没有被挂在到网页中，进行DOM操作只能得到旧的数据**

#### mounted

模板代码已经被加载到网页中了。此时创建期间所有事情都已经准备好了，网页开始运行了。 

**mounted函数中发生的数据变动也可以被vue捕捉。** 

### 运行期间

#### beforeUpdate

在网页网页运行期间，`data`中的数据可能会进行更新。在这个阶段，数据只是在`data`中更新了，但是并没有在模板中进行更新，因此网页中显示的还是之前的。

#### updated

数据在`data`中更新了，也在网页中更新了。

### 销毁期间

#### beforeDestroy

`Vue`实例或者是组件在被销毁之前执行的函数。在这一个函数中`Vue`或者组件中所有的属性都是可以使用的。

#### destroyed

`Vue`实例或者是组件被销毁后执行的。此时`Vue`实例上所有东西都会解绑，所有事件都会被移除，所有子元素都会被销毁。

## 过滤器

本质是一个函数，类似于django的过滤器。

过滤器的使用

```html
<!-- 在双花括号中 -->
{{ message|capitalize }}
<!-- 在 `v-bind` 中 -->
<div v-bind:id="rawId|formatId"></div>
```



定义过滤器的方式有两种：

1. `Vue.filter('过滤器名称',function(参数1){})`  全局过滤器 

   ```js
   Vue.filter('capitalize', function (value) {
     if (!value) return ''
       
     value = value.toString()
     return value.charAt(0).toUpperCase() + value.slice(1)
   })
   ```

2. 当然也可以在组件中，自定义过滤器（`filters`多了一个s） 。这就只能在组件本身上使用 

   ```js
   filters: {
     capitalize: function (value) {
       if (!value) return ''
       value = value.toString()
       return value.charAt(0).toUpperCase() + value.slice(1)
     }
   }
   ```

   

过滤器其他：

* 串联

  ```js
  {{ message | filterA | filterB }}
  ```

* 传递多个参数。其中，`arg1`是第二个参数 

  ```js
  {{ message | filterA('arg1', arg2) }}
  ```



## 深入响应式原理

官网参考：https://cn.vuejs.org/v2/guide/reactivity.html#如何追踪变化  

归纳整理如下：



**当把普通的js对象作为vue的data时，vue将遍历对象的property，将其转为`getter/setter`，追踪其变化，通知watcher，重新渲染。**

<img src="https://hollis-md.oss-cn-beijing.aliyuncs.com/img/data.png" alt="img" style="zoom:50%;" /> 

### 对象

对于对象，vue不能响应式地检测到property的增加删除，**数据变动后vue不会在dom更新周期里主动地重新渲染组件**。只有当视图销毁再创建（比如网页重新加载）需要重新获取数据时，才会体现这部分变动。

**vue要求data在创建之时就为必要的property声明，哪怕为空`''`** 

```js
var vm = new Vue({
  data:{
    a:1
  }
})

// `vm.a` 是响应式的

vm.b = 2
// `vm.b` 是非响应式的
```

**对于这种情况，vue使用`$set`解决。**

```js
this.$set(this.someObject,'b',2) //可以纳入监听
```

如果同时增加多属性

```js
// 代替 `Object.assign(this.someObject, { a: 1, b: 2 })
// 表示原对象与新增加的属性 混合为 一个新对象 
this.someObject = Object.assign({}, this.someObject, { a: 1, b: 2 })
```

### 数组

Vue 不能检测以下数组的变动：

1. 当你利用索引直接设置一个数组项时，例如：`vm.items[indexOfItem] = newValue`
2. 当你修改数组的长度时，例如：`vm.items.length = newLength`

```js
var vm = new Vue({
  data: {
    items: ['a', 'b', 'c']
  }
})
vm.items[1] = 'x' // 不是响应性的
vm.items.length = 2 // 不是响应性的
```

对于问题1，使用

```js
vm.$set(vm.items, indexOfItem, newValue)
```

对于问题2，使用

```js
vm.items.splice(newLength)
```



****

还要一种情况是，数据更改过程中，触发了响应式数据的setter，setter会通知watcher在下一轮的时候进行dom更新。这时候，那些非响应的数据也会一并更新。 参考：https://www.cnblogs.com/zhaotq/p/9392520.html 



```vue
<div id="app">
    <div>{{test[0].name}}</div>
    <div>{{test[1]}}</div>
    <div>{{items[0]}}</div>
    <button @click="change">点击更改</button>

</div>

<script>
    let vm = new Vue({
        el: '#app',
        data: {
            // 属性
            test:[
                {name:'jhk'},
                'jhh'
            ],
            items:['a','b','c']
        },
        methods: {
            // 方法
            change(){
                
                this.$set(this.test,0,{name:'蒋慧凯'})  // 这会触发setter，通知watcher

                // 下面两个非响应式更新地 也会在下一轮dom更新时跟着变
                // 但是注释掉第一行的响应式更新后 这两句变化就不会更新视图
                this.test[1]='蒋慧海';
                this.items[0]='z也会跟着变呀';
                
            }
        }

    });
</script>
```





### 异步更新

**Vue 在更新 DOM 时是异步执行的**。只要侦听到数据变化，Vue 将开启一个队列，并缓冲在同一事件循环中发生的所有数据变更。**如果同一个 watcher 被多次触发，只会被推入到队列中一次**。这种在缓冲时去除重复数据对于避免不必要的计算和 DOM 操作是非常重要的。然后，在下一个的事件循环“tick”中，Vue 刷新队列并执行实际 (已去重的) 工作。

例如，当你设置 `vm.someData = 'new value'`，该组件不会立即重新渲染。当刷新队列时，组件会在下一个事件循环“tick”中更新。

**为了在数据变化之后等待 Vue 完成更新 DOM，可以在数据变化之后立即使用 `Vue.nextTick(callback)`**，vue中一个tick是一个dom更新周期。这样回调函数将在 DOM 更新完成后被调用。例如

```html
<div id="example">{{message}}</div>
```

```js
var vm = new Vue({
  el: '#example',
  data: {
    message: '123'
  }
})
vm.message = 'new message' // 更改数据
vm.$el.textContent === 'new message' // false,数据已经更改，但是dom并未重新渲染
// 全局方法 nexttick
Vue.nextTick(function () {
  vm.$el.textContent === 'new message' // true，dom已经重新渲染
})
```



组件内使用`nexttick`示例

```js
Vue.component('example', {
  template: '<span>{{ message }}</span>',
  data: function () {
    return {
      message: '未更新',// 模板显示的数据 
    }
  },
  methods: {
    updateMessage: function () {
      this.message = '已更新'
      console.log(this.$el.textContent) // => '未更新'
      this.$nextTick(function () {
        // 钩子函数
        console.log(this.$el.textContent) // => '已更新'
      })
    }
  }
})
```



## 插件

插件通常用来为 Vue 添加全局功能。**插件的功能范围**没有严格的限制——一般有下面几种：

1. 添加全局方法或者 property。如：[vue-custom-element](https://github.com/karol-f/vue-custom-element)
2. 添加全局资源：指令/过滤器/过渡等。如 [vue-touch](https://github.com/vuejs/vue-touch)
3. 通过全局混入来添加一些组件选项。如 [vue-router](https://github.com/vuejs/vue-router)
4. 添加 Vue 实例方法，通过把它们添加到 `Vue.prototype` 上实现。
5. 一个库，提供自己的 API，同时提供上面提到的一个或多个功能。如 [vue-router](https://github.com/vuejs/vue-router)



使用插件

通过全局方法 `Vue.use()` 使用插件。**它需要在你调用 `new Vue()` 启动应用之前完成**

```js
// 调用 `MyPlugin.install(Vue)`
// Vue.use 是否使用取决于插件的install方法 
Vue.use(MyPlugin)
```

`Vue.use` 会自动阻止多次注册相同插件，届时即使多次调用也只会注册一次该插件。 



`vue.use`的原理（源码）以及调用时机：https://m.html.cn/qa/vue-js/20932.html 

vue引入第三方库：https://www.cnblogs.com/sxz2008/p/8245282.html 

***

插件应该暴露一个install 方法，在 `use`的时候会被调用。
```js
MyPlugin.install = function (Vue, options) {
  // 第一个参数 是 Vue构造器 （Vue类）
  // 1. 添加全局方法或 property
  Vue.myGlobalMethod = function () {
    // 逻辑...
  }

  // 2. 添加全局资源
  Vue.directive('my-directive', {
    bind (el, binding, vnode, oldVnode) {
      // 逻辑...
    }
    ...
  })

  // 3. 注入组件选项
  Vue.mixin({
    created: function () {
      // 逻辑...
    }
    ...
  })

  // 4. 添加实例方法
  Vue.prototype.$myMethod = function (methodOptions) {
    // 逻辑...
  }
}
```



## 引入

### 全局变量引入

```js
// main.js 文件中
import Vue from 'vue'
import globale from "./utils/globalVariables"
import auth from "./utils/auth"

Vue.prototype.$auth = auth; // 全局变量 使用的时候 this.$auth
Vue.prototype.$global = global;
```

### 外部css引入

* 使用scss的`@import`语法，直接引入是全局样式，局部使用使用`scoped`关键字 
* 在`index.html`中的`link`标签引入，将作为全局样式

### 外部js引入

* 在index.html中的`script`标签中引入，全局可用
* `在main.js`中import导入

# Vue-router

## 安装

vue引入

* cdn：`<script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>` 

* 下载到本地：`<script src="../../lib/vue-router.js"></script>` 

* 使用`npm`安装：`npm install vue-router`。详细使用：https://www.cnblogs.com/flywong/p/10904449.html

## 使用

1. 新建`routes.js`文件 ，编写路由信息

```js
import Vue from 'vue'
import VueRouter from 'vue-router'

//申明使用插件
Vue.use(VueRouter)

// 定义顶层路由对象 
const routes=[
  {
    path: "/",
    component: Home,
    name:"home"
  }
]


const router=new VueRouter({
  routes:routes
});

export default router
```

2. main.js 引入路由对象 

```js
import Vue from 'vue'
import App from './App.vue'

import router from './routes' // 引入模块


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router // 注册 
}).$mount('#app') // 第一层的路由对象会被渲染到app节点上

```

3. 在html中，**用vue封装的`router-link`标签来实现页面的点击跳转。它在最后渲染时，会成为`a`标签。`router-link`的`to`属性指定跳转路径，组件会在`<router-view>`被渲染。**





vue在生成链接的时候使用hash模式，会带上`/#/`，如果手动在浏览器输入链接使vue跳转，为`/#/`、`/#/find`、`/#/friend` 。

（关于vue页面的hash模式和history模式：https://blog.csdn.net/qq_35630674/article/details/100697604 ）





## route和router

`this.$router`表示`VueRouter`对象，包含了所有的路由信息。在`router.js`中创建导出，并在`main.js`中注册到全局的vue对象中。



`this.$route`表示当前的路由对象，包含了查询参数对象query（GET参数`）、传递参数params对象（解析url得到的参数）、path(`/foo/bar/`，总是解析为绝对路径)、fullPath(得到完整的url，包含query等信息)等信息。



## 动态路由

动态路由：将url的部分路径作为参数捕获，例如`{path:'/profile/:userid'}` ，userid部分会被捕捉为变量，使用`this.$route.params`访问。

路由跳转

```html
<router-link to='/profile/123'>个人中心</router-link>
```



## 路由嵌套

路由的逐级匹配，子路由嵌套在父路由下面。

```js
// routes.js 中的路由配置 
export default new VueRouter({
    routes: [
        {
            path: "/",
            component: Frame,
            children:[
                // 不以 / 开头 表示是相对于当前路径 而不是重新从根路径开始 
                {path:'',component:Index,name:'index'},
                {path:'order/',component:Order,name:'order'},
                {path:'merchant/',component:Merchant,name:'merchant'},
                {path:'user/',component:User,name:'user'},
            ]
        },
        {
            path: '/login',
            component: LogIn
        }
    ]
})
```



**嵌套的子组件会去父路由的`<router-view>` 处渲染，例如上面的`Index` 组件就会在`Frame`下的路由出口被渲染。** 



## 编程式导航

`<router-link>`可以在用户点击的情况下进行页面更新。但有时候我们**想要在`js`中用函数的形式修改页面的跳转**，这时候就需要使用编程式导航了。

### push

`$router.push`跳转：导航到不同的`URL`，会向`history`栈添加一个新的记录。当用户点击浏览器后退按钮时，则回到之前的`URL`。

当点击`<router-link>`时，这个方法会在内部调用。

| 声明式                    | 编程式             |
| ------------------------- | ------------------ |
| `<router-link :to="...">` | `router.push(...)` |

```javascript
// 字符串
router.push('home')

// route对象
router.push({ path: 'home' })

// 命名的路由 带参数  params 是url参数 
router.push({ name: 'user', params: { userId: '123' }})

// 带查询参数，变成 /register?plan=private
router.push({ path: 'register', query: { plan: 'private' }})
```

### replace

`router.replace(location, onComplete?, onAbort?)`：

类似 router.push ，直接替换掉当前的 history 记录，不会向 history 添加新记录

### go

`router.go(n)`：

这个方法的参数是一个整数，意思是在`history`记录中向前或者后退多少步，类似 `window.history.go(n)`。

```javascript
// 在浏览器记录中前进一步，等同于 history.forward()
router.go(1)

// 后退一步记录，等同于 history.back()
router.go(-1)

// 前进 3 步记录
router.go(3)

// 如果 history 记录不够用，那就默默地失败呗
router.go(-100)
router.go(100)
```

 

## 命名路由

通过`name`标识一个路由，

```javascript
const router = new VueRouter({
  routes: [
    {
      path: '/user/:userId',
      name: 'user',		// 为路由命名 	
      component: User
    }
  ]
})
```

跳转的时候传入对象`{name:'route_name'}`

```html
<router-link :to="{ name: 'user', params: { userId: 123 }}">User</router-link>
<router-link :to="/user/123/">User</router-link>
```

```javascript
// router.push 
router.push({ name: 'user', params: { userId: 123 }})
router.push('/user/123/')
```

##  命名视图

在一个组件中拥有多个路由出口`router-view`，定义`name`属性为其命名。

```html
<router-view class="view one"></router-view>
<router-view class="view two" name="a"></router-view>
```

路由定义：

```javascript
const router = new VueRouter({
  routes: [
    {
      path: '/',
      components: {
          // 多个组件 名字变为 components 
          // view-name:Component
        default: Foo, // 默认组件
        a: Bar,
      }
    }
  ]
})
```

## 重定向和别名 

1. 重定向：在定义路由的时候，可以增加一个`redirect`参数，用来重定向到另外一个页面 
2. 别名：在定义路由的时候，增加一个`alias`参数，表示这个url的别名



```js
let vm = new Vue({
      el: '#app',
      router: new VueRouter({
        routes: [{
            path: '/',
            redirect: '/article',
            alias: '/index'
          },
          {
            path: '/article',
            component: articles
          }
        ]
      }),
    });
```



## 导航守卫

导航守卫，就是路由导航过程中各个阶段的钩子函数。分为**全局导航守卫**、**路由导航守卫**、**组件导航守卫**。

### 全局导航守卫

**全局导航守卫，就是在整个网页中，只要发生了路由的变化，都会触发。**全局导航守卫主要包括两个函数，分别为：`beforeEach`、`afterEach`。

#### beforeEach

**在路由发生了改变，但是还没有成功跳转的时候会调用。**在整个`Router`对象上调用该函数的方法如下

```js
// router 是一个 VueRouter对象 
router.beforeEach(function(to,from,next){
    // next() 按照正常的流程走 
    // next('/') 重新跳转到/ 另外一个网页
    // next(false) 或者不写 ，什么事情也不会做
    
    // to 是目标跳转路由 from是跳转前路由 
      
})
```



**借助`beforeEach` 来实现一个权限登录模拟**。在用户登录的状态下，所有页面都可访问，在未登录的状态下，访问权限页面要求跳转登录页面。下例中，使用`logined`变量来模拟这个登录状态。

```js
// 路由定义部分

const routes=[
  {
    path: "/",
    component: Home,
    name:"home",
    meta:{  
      // 用这个属性来表示路由是否要认证 
      requireAuthed:true // meta表示一些额外属性 
    }
  }

   
// beforeEach 
// 定义路由对象
const router=new VueRouter({
  routes:routes
});

router.beforeEach((to,from,next)=>{
  // console.log(to,from); 
  // auth.token 是表示用户登录的一个变量 
  if(to.meta.requireAuthed&&!auth.token){
    // 目标路由要求用户登录
    console.log('目标网页要求登录',to,from)
    // to.path 存储url路径 跳转到登录页
    next({name:'login','from':to.path}) 
  }
  else
  {
    next() // 正常跳转
  }
})
export default router
```

#### afterEach

路由已经改变完成后的函数。这个函数没有`next`参数。因为页面已经完成了跳转。

```js
router.afterEach(function(to,from){
  console.log('to:',to);
  console.log('from:',from);
})
```



### 路由导航守卫

路由导航守卫是局部的，定义在单个路由对象上(`{path:,component}`)。其使用方法如下：

```js
{path:'',component:COM_obj,beforeEnter:function(to,from,next)()}
```



路由导航示例 ：针对`/login`这个路由，检测登录状态。如果已经登录，直接跳转到首页，否则正常跳转。

```js
{
    path: '/login',
        component: login,
            name: 'login',
                beforeEnter:function(to,from,next){
                    if(logined){
                        next('/');
                    }
                    else{
                        next(); 
                    }
                }
}
```



### 组件导航守卫

组件导航守卫，存在于组件中，包括

* `beforeRouteEnter`：组件在渲染前被调用
* `beforeRouteUpdate` ：组件复用时被调用
* `beforeRouteLeave`：组件失活时调用 



### 导航解析流程

1. 导航被触发。
2. 在失活的组件里调用离开守卫  `beforeRouteLeave`
3. 调用全局的 `beforeEach` 守卫 
4. 在重用的组件里调用 beforeRouteUpdate 守卫 (2.2+)。
5. 在路由配置里调用 beforeEnter。
6. 解析异步路由组件。
7. 在被激活的组件里调用 beforeRouteEnter。
8. 调用全局的 beforeResolve 守卫 (2.5+)。
9. 导航被确认。
10. 调用全局的 afterEach 钩子。
11. 触发 DOM 更新。
12. 用创建好的实例调用 beforeRouteEnter 守卫中传给 next 的回调函数。 



# vue-cli

vue-cli [介绍](###vue-cli 安装)

## node 介绍

**node是一种执行js的运行环境**，可以让js脱离浏览器运行在服务端，像其他后端语言如python、java一样实现后端功能。 

node的优势：

1. 基于js语法开发，没有学习成本小
2. 更小的并发成本带来的超强并发能力
3. 高性能，针对js优化编译，接近c的执行效率

## webpack

参考：https://www.runoob.com/w3cnote/webpack-tutorial.html 

Webpack 是一个前端资源加载/打包工具。它将根据模块的依赖关系进行静态分析，然后将这些模块按照指定的规则生成对应的静态资源。



## node 环境配置

### nvm安装

**`nvm（Node Version Manager）`是一个用来管理`node`版本的工具**。 我们之所以需要使用`node`，是因为我们需要使用`node`中的`npm(Node Package Manager)`，使用`npm`的目的是为了能够方便的管理一些前端开发的包！

`nvm`的安装步骤如下：

1. 到这个链接下载`nvm`的安装包：`https://github.com/coreybutler/nvm-windows/releases`。
2. 然后点击下一步，安装即可！
3. 安装完成后，还需要配置环境变量。在`我的电脑->属性->高级系统设置->环境变量->系统环境变量->Path`下新建一个，把`nvm`所处的路径填入进去即可！
4. 打开`cmd`，然后输入`nvm`，如果没有提示没有找不到这个命令。说明已经安装成功！
5. `Mac`或者`Linux`安装`nvm`请看这里：`https://github.com/creationix/nvm`。也要记得配置环境变量。



`nvm`常用命令：

1. `nvm install [version]`：安装指定版本的`node.js` 。
2. `nvm use [version]`：使用某个版本的`node`。
3. `nvm list`：列出当前安装了哪些版本的`node`。
4. `nvm uninstall [version]`：卸载指定版本的`node`。
5. `nvm node_mirror [url]`：设置`nvm`的镜像。
6. `nvm npm_mirror [url]`：设置`npm`的镜像。

### node安装

安装完`nvm`后，我们就可以通过`nvm`来安装`node`了。这里我们安装`10.16.0`版本的的`node.js。`安装命令如下：

```shell
nvm install 10.16.0
```

如果你的网络够快，那以上命令在稍等片刻之后会安装成功。如果你的网速很慢，那以上命令可能会发生超时。因为`node`的服务器地址是`https://nodejs.org/dist/`，这个域名的服务器是在国外。因此会比较慢。**因此我们可以设置一下`nvm`的源**。

```shell
nvm node_mirror https://npm.taobao.org/mirrors/node/
nvm npm_mirror https://npm.taobao.org/mirrors/npm/
```

### npm

`npm(Node Package Manager)`在安装`node`的时候就会自动的安装了。当时前提条件是你需要设置当前的`node`的版本：`nvm use 10.16.0`。然后就可以使用`npm`了.
关于`npm`常用命令以及用法，请看下文。

#### 初始化

**在新的项目中，需要先进入项目路径执行`npm init`初始化，**根据提示完成一些信息填写，结束后创建一个`package.json`文件用来保存本项目中用到的包。**`package.json`是用来记录当前项目依赖了哪些包，以后别人拿到你这个项目后，不需要你的`node_modules`文件夹（因为node_moduels中的包实在太庞大了）。只需要执行`npm install`命令，即会自动安装`package.json`下`devDependencies`中指定的依赖包。**

#### 安装包	

安装包分为全局安装和本地安装。全局安装是安装在当前`node`环境中，可以在cmd中当作命令使用。而本地安装是安装在当前项目中，只有当前这个项目能使用，并且需要通过require引用。安装的方式只有`-g`参数的区别：

```shell
npm install vue   # 本地安装
npm install vue --save   # 本地安装，并且保存到package.json的dependice中
npm install vue --save-dev # 本地安装，并且保存到package.json的dependice-dev中 开发者依赖 
npm install vue -g   #全局安装
npm install -g @vue/cli  #全局安装vue-cli
```

##### 本地与全局

本地安装

1. 将安装包放在`./node_modules`下（运行 npm 命令时所在的目录），如果没有`node_modules`目录，会在当前执行`npm`命令的目录下生成`node_modules`目录。
2. 可以通过`require()`来引入本地安装的包。

全局安装

1. 将安装包放在`/usr/local`下或者你`node`的安装目录。
2. 可以直接在命令行里使用。

##### --save 

`--save-dev`后缀是将安装的包的添加到`package.json`下的`devDependencies`依赖中。以后通过`npm install`即可自动安装。**`devDependencies`这个是用来记录开发环境下使用的包**。

如果想要记录生产环境下使用的包，那么在安装包的时候使用`npm install xx --save`就会记录到`package.json`下的`dependencies`中，**`dependencies`是专门用来记录生产环境下的依赖包的。**

尽管生产环境所用的包是开发环境所用的包的子集，**但上述两个命令的输出只会输出到一个依赖中。**

#### 卸载包

```shell
npm uninstall [package]
```

#### 更新包

```shell
npm update [package]
```

#### 搜索包

```shell
npm search [package]
```

#### 使用淘宝镜像

`npm`的服务器在国外。那么可以安装一下`cnpm`，并且指定镜像为淘宝的镜像：

```shell
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

那么以后就可以使用cnpm来安装包了！ 

```shell
cnpm install 
```

#### 手动安装npm

有时候使用`nvm`安装完`node`后，`npm`没有跟着安装，这时候可以到`https://github.com/npm/cli/releases`下载`6.10.1`的版本。然后下载完成后，解压开来，放到`v10.16.0/node_modules`下，然后修改名字为`npm`，并且把`npm/bin`中的`npm`和`npm.cmd`两个文件放到`v10.16.0`根目录下



## vue-cli 安装

`vue-cli`是和`vue`进行深度组合的工具，可以快速帮我们创建`vue`项目，并且把一些脚手架相关的代码给我们创建好。

### 安装

**`Vue CLI`需要`Node.js 8.9`或更高版本 (推荐`8.11.0+`)。**`node`环境安装后，直接通过`npm install -g @vue/cli`即可安装。安装完成后，输入`vue --version`，如果出现了版本号，说明已经下载完成。 



版本查看 

**查看Vue版本：**

1.npm list vue

2.进入项目中package.json文件直接查看



**查看Vue/cli版本：**

vue -V 或者 vue --version



### 创建启动项目

1. 在指定路径下使用`vue create [项目名称]`创建项目。
2. 会让你选择要安装哪些包（默认是`Babel`和`ESLint`），也可以手动选择。
3. 如果在安装的时候比较慢，可以在安装的时候使用淘宝的链接：`vue create -r https://registry.npm.taobao.org [项目名称]`。
4. 如果不想在创建项目的时候都每次指定淘宝链接，可以在当前用户目录下，找到`.npmrc`，然后设置`registry=https://registry.npm.taobao.org`。



项目创建完毕后，进入项目所在目录，执行`npm run serve`即可启动vue项目。

### 项目结构介绍

![img](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/vue-cli%E7%BB%93%E6%9E%84%E5%9B%BE.png)

1. `node_modules`：本地安装的包的文件夹。
2. `public`：项目出口文件。
3. src项目源文件
   - `assets`：资源文件，包括字体，图片等。
   - `components`：组件文件。
   - `App.vue`：入口组件。
   - `main.js`：`webpack`在打包的时候的入口文件。
4. `babel.config.js`：`es`转低级`js`语言的配置文件。一些浏览器可能不支持es的高级语法。
5. `package.json`：项目包管理文件。



`main.js`、`App.vue`、`index.html`三者之间的关系：`main.js`控制`App.vue`挂载到`index.html`中 

1. main.js入口文件 ：实例化vue组件，确定要挂载的组件。

   ```js
   import App from './App.vue' 
   
   new Vue({
     el: '#app',  // 挂载节点id
     components: {App }, 
     template: '<App/>', // 模板
   })
   ```

   

2. `App.vue`根组件，被用来挂载到`index.html` 

   ```vue
   <template>
       <div>
          
       </div>
   
   </template>
   
   <script>
       export default {
           name: 'App',
           data() {
               return {
                   
               }
           },
           components: {
           }
       }
   </script>
   
   <style lang='scss'>
     
   </style>  
   
   ```

   

3. `index.html`，body部分为空，实际内容被挂载为`App.vue` 

   ```html
   <div id="app">来自index.html正文中的内容 实际会显示为app.vue中的内容</div>
   ```

   

**main.js的作用包括：**

1. 实例化vue
2. 放置项目中经常会用到的插件和CSS样式
3. **存储全局变量** 

```js
import Vue from 'vue'
import App from './App'
import router from './router' 

Vue.use(router) // 安装插件 


// 公共css
import './assets/css/common.css'
import './assets/css/public.css'


new Vue({// 页面入口
  el: '#app',
  router,  // 全局属性 各个组件可以通过this.$property的形式访问 
  components: { App },
  template: '<App/>'
})
```

# Vuex

Vuex 有点像多线程之间的共享变量，方便组件之间的数据传递和读写，有严格的读写机制。

## 数据传递

整理Vue组件之间的数据交换方式：

1. 同一个组件模板中：使用实例属性`data`  

   ```js
   {
   	data:function(){
           return {
               // 因为是在一个实例中 
               // data 可以共享访问
           }
       }
   }
   ```

2. [组件](## 自定义组件)属性 `prop`，父组件传入属性，子组件使用事件向外抛出实现同步
3. url携带请求参数，组件解析url
4. vuex 实现的数据池变量 



## 安装

官网： https://vuex.vuejs.org/zh/installation.html

1. `npm install vuex --save`
2. 如果你的网站想要支持那些不支持Promise的浏览器：`npm install es6-promise --save`  



## 使用

使用：https://vuex.vuejs.org/zh/guide/ 

1. `Vue.use(Vuex)`，全局安装插件

   ```js
   // main.js 文件
   import Vue from 'vue'
   import Vuex from 'vuex'
   
   Vue.use(Vuex) // 在new Vue之前
   ```

2. 创建Store对象 

  ```js
const store = new Vuex.Store({
  state: {
    count: 10
  },
  mutations: {
    increment(state){
      state.count++
    },
    substract(state){
      state.count--
    }
  },
  getters: {
    currentCount(state){
      return "当前的count为："+state.count
    }
  }
})
  ```

3. 在main.js中，需要把store放到`Vue`对象中，作为一个全局属性。这样以后在其他的组件中才能通过`this.$store`的方式方便的访问到。

   ```js
   new Vue({
     el: '#app',
     store
   })
   ```

   

   

## 数据的操作

1. 如果是直接获取，那么可以通过`this.$store.state.xxx`来访问。
2. 如果想要修改，那么建议通过`mutation`的形式来操作。可以在`Store`中定义一些`mutations`，以`$store.commit("函数名")`来调用修改。
3. getters：**非常类似于组件中的计算属性**，可以进行一些操作再把值给返回回去。在组件中调用是通过`$store.getters.xxx`来调用。
4. **store里的数据要想被vue实时更新视图，应当设置为计算属性`computed`。**



# 常用开发依赖

## sass语法

1. 安装`loader`：`webpack`在解析`scss`文件的时候，会去加载`sass-loader`以及`node-loader`，因此我们首先需要通过`npm`来安装一下：

   ```shel
   npm install node-sass@4.12.0 --save-dev
   npm install sass-loader@7.0.3 --save-dev
   ```

2. 指定`sass`语言：在指定`style`的时候，添加`lang="scss"`属性，这样就会将`style`中的代码识别为`scss`语法。

3. 将vscode中的右下角的语言模式改成vue

   ![image-20201029171945898](https://hollis-md.oss-cn-beijing.aliyuncs.com/img/vue%E6%9B%B4%E6%94%B9%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%BC%8F.png)

 

## axios 异步请求

axios是通过promise实现对ajax技术的一种封装，就像jQuery实现ajax封装一样。

axios官网：http://www.axios-js.com/zh-cn/docs/#安装 

### vue使用

vue使用axios：

1. 安装 ：`cnpm install axios --save`

2. main.js 引入 axios变量

   ```js
   import axios from "axios";
   Vue.prototype.$axios=axios;  
   ```

3. 组件中使用 axios 请求

   ```js
   this.$axios.post(url,data).then(res=>{
       // data:返回的请求体数据
       // status_code : 返回的状态码 2xx 
       console.log(res); // 请求成功 取数据调用属性 res.data
   }).catch(err=>{
       // catch 捕获的异常章状态码都不是2开头的
       console.log(err); // 请求失败 
   })
   ```

### 常用API

可设置的请求参数 

```js
{
   // `url` 是用于请求的服务器 URL
  url: '/user',

  // `method` 是创建请求时使用的方法
  method: 'get', // default

  // `baseURL` 将自动加在 `url` 前面，除非 `url` 是一个绝对 URL。
  // 它可以通过设置一个 `baseURL` 便于为 axios 实例的方法传递相对 URL
  baseURL: 'https://some-domain.com/api/',

  // `transformRequest` 允许在向服务器发送前，修改请求数据
  // 只能用在 'PUT', 'POST' 和 'PATCH' 这几个请求方法
  // 后面数组中的函数必须返回一个字符串，或 ArrayBuffer，或 Stream
  transformRequest: [function (data, headers) {
    // 对 data 进行任意转换处理
    return data;
  }],

  // `transformResponse` 在传递给 then/catch 前，允许修改响应数据
  transformResponse: [function (data) {
    // 对 data 进行任意转换处理
    return data;
  }],

  // `headers` 是即将被发送的自定义请求头
  headers: {'X-Requested-With': 'XMLHttpRequest'},

  // `params` 是即将与请求一起发送的 URL 参数
  // 必须是一个无格式对象(plain object)或 URLSearchParams 对象
  params: {
    ID: 12345
  },

   // `paramsSerializer` 是一个负责 `params` 序列化的函数
  // (e.g. https://www.npmjs.com/package/qs, http://api.jquery.com/jquery.param/)
  paramsSerializer: function(params) {
    return Qs.stringify(params, {arrayFormat: 'brackets'})
  },

  // `data` 是作为请求主体被发送的数据
  // 只适用于这些请求方法 'PUT', 'POST', 和 'PATCH'
  // 在没有设置 `transformRequest` 时，必须是以下类型之一：
  // - string, plain object, ArrayBuffer, ArrayBufferView, URLSearchParams
  // - 浏览器专属：FormData, File, Blob
  // - Node 专属： Stream
  data: {
    firstName: 'Fred'
  },

  // `timeout` 指定请求超时的毫秒数(0 表示无超时时间)
  // 如果请求话费了超过 `timeout` 的时间，请求将被中断
  timeout: 1000,

   // `withCredentials` 表示跨域请求时是否需要使用凭证
  withCredentials: false, // default

  // `adapter` 允许自定义处理请求，以使测试更轻松
  // 返回一个 promise 并应用一个有效的响应 (查阅 [response docs](#response-api)).
  adapter: function (config) {
    /* ... */
  },

 // `auth` 表示应该使用 HTTP 基础验证，并提供凭据
  // 这将设置一个 `Authorization` 头，覆写掉现有的任意使用 `headers` 设置的自定义 `Authorization`头
  auth: {
    username: 'janedoe',
    password: 's00pers3cret'
  },

   // `responseType` 表示服务器响应的数据类型，可以是 'arraybuffer', 'blob', 'document', 'json', 'text', 'stream'
  responseType: 'json', // default

  // `responseEncoding` indicates encoding to use for decoding responses
  // Note: Ignored for `responseType` of 'stream' or client-side requests
  responseEncoding: 'utf8', // default

   // `xsrfCookieName` 是用作 xsrf token 的值的cookie的名称
  xsrfCookieName: 'XSRF-TOKEN', // default

  // `xsrfHeaderName` is the name of the http header that carries the xsrf token value
  xsrfHeaderName: 'X-XSRF-TOKEN', // default

   // `onUploadProgress` 允许为上传处理进度事件
  onUploadProgress: function (progressEvent) {
    // Do whatever you want with the native progress event
  },

  // `onDownloadProgress` 允许为下载处理进度事件
  onDownloadProgress: function (progressEvent) {
    // 对原生进度事件的处理
  },

   // `maxContentLength` 定义允许的响应内容的最大尺寸
  maxContentLength: 2000,

  // `validateStatus` 定义对于给定的HTTP 响应状态码是 resolve 或 reject  promise 。如果 `validateStatus` 返回 `true` (或者设置为 `null` 或 `undefined`)，promise 将被 resolve; 否则，promise 将被 rejecte
  validateStatus: function (status) {
    return status >= 200 && status < 300; // default
  },

  // `maxRedirects` 定义在 node.js 中 follow 的最大重定向数目
  // 如果设置为0，将不会 follow 任何重定向
  maxRedirects: 5, // default

  // `socketPath` defines a UNIX Socket to be used in node.js.
  // e.g. '/var/run/docker.sock' to send requests to the docker daemon.
  // Only either `socketPath` or `proxy` can be specified.
  // If both are specified, `socketPath` is used.
  socketPath: null, // default

  // `httpAgent` 和 `httpsAgent` 分别在 node.js 中用于定义在执行 http 和 https 时使用的自定义代理。允许像这样配置选项：
  // `keepAlive` 默认没有启用
  httpAgent: new http.Agent({ keepAlive: true }),
  httpsAgent: new https.Agent({ keepAlive: true }),

  // 'proxy' 定义代理服务器的主机名称和端口
  // `auth` 表示 HTTP 基础验证应当用于连接代理，并提供凭据
  // 这将会设置一个 `Proxy-Authorization` 头，覆写掉已有的通过使用 `header` 设置的自定义 `Proxy-Authorization` 头。
  proxy: {
    host: '127.0.0.1',
    port: 9000,
    auth: {
      username: 'mikeymike',
      password: 'rapunz3l'
    }
  },

  // `cancelToken` 指定用于取消请求的 cancel token
  // （查看后面的 Cancellation 这节了解更多）
  cancelToken: new CancelToken(function (cancel) {
  })
}
```

响应体数据res

```js
{
  // `data` 由服务器提供的响应
  data: {},

  // `status` 来自服务器响应的 HTTP 状态码
  status: 200,

  // `statusText` 来自服务器响应的 HTTP 状态信息
  statusText: 'OK',

  // `headers` 服务器响应的头
  headers: {},

   // `config` 是为请求提供的配置信息
  config: {},
 // 'request'
  // `request` is the request that generated this response
  // It is the last ClientRequest instance in node.js (in redirects)
  // and an XMLHttpRequest instance the browser
  request: {}
}
```



创建一个axios对象

```js
this.axios = axios.create(
    {
        baseURL:'https://some-domain.com/api/', // 此后该对象发起的所有请求url都会拼接在这个url后面
        timeout: 1000,
    }
);
```

get/post/put/delete

```js
// this.axios 实际是 上一步创建的axios对象 下同 
// data ：{}
this.axios.get(url); 
this.axios.post(url, data);
this.axios.put(url, data);
this.axios.delete(url); 
```



请求拦截 

```js

this.axios.interceptors.request.use(config => {
    // 拦截请求 添加响应头 参考官网
    if (this.auth.token) {
        // 为请求头+token
        config.headers.common['Authorization'] = 'jwt ' + this.auth.token
    }
    return config; // 一定要返回 
});
```

响应拦截 

```js
this.axios.interceptors.response.use(res => {
    return res;  // 第一个钩子函数是正常的时候怎么做
}, error => {
    // 第二个钩子函数是异常的时候怎么做 也就是不是2xx状态码的时候
    console.log('请求失败：', error)
    if (error.status == 401) {
        this.auth.clearToken();
        router.replace('login/')
    }
    return Promise.reject(error); // 官网格式 
});
```

## rem移动端适配

**如果想要写完一套代码，能够在所有移动设备上都正常运行，那么采用原生的`px`单位来设置是不行的，因为各个设备的尺寸不同。**这时候我们可以通过`rem`来解决这个问题。



### rem是什么

* em：当前元素字体大小相对于父标签的字体大小。比如：

  ```html
   <div style="font-size:16px;">
       <span style="font-size:2em">你好</span>
   </div>
  ```

  在`div`中字体大小是`16px`，而在`span`标签中因为用的是`2em`，因此是2倍的父标签字体的大小，也就是`32px`。

* `rem`：跟`em`类似，只不过此时的参照元素不是父元素**，而是根元素，也就是`html`元素的大小**。比如：

  ```html
   <html style="font-size:14px">
       <div style="font-size:16px;">
           <span style="font-size:2rem">你好</span>
       </div>
   </html>
  ```

  此时的`span`标签字体大小为`html`标签字体大小的2倍，也就是`28px`。

  

### rem适配原理

rem的适配原理是**等比缩放。**

假如设计师按照`750px`的尺寸来设计，我们设置`font-size=100px`，当需要实现一个32px元素大小时，可以写作`0.32rem`，换算下来0.32*100px=32px。

| 设备尺寸 | html 根尺寸（修改） | element             |
| -------- | ------------------- | ------------------- |
| 750px    | 100px               | **32px（0.32rem）** |

当用户设备是375px时，我们的元素应该实现等比缩放，也就是16px。

保持在0.32rem的比例不动，这时候修改 html 的`font_size=100*(375/750)=50px`即可。

| 设备尺寸 | html 根尺寸（修改） | element             |
| -------- | ------------------- | ------------------- |
| 375px    | *50px*              | **16px（0.32rem）** |

以后，再切换到不同设备时，**只需要按照计算规则`比例=设备缩放比*html_font_size`，重新 定义 html 的根尺寸 即可**。



### vue-cli的rem布局

1. 安装两个包，分别是：`postcss-pxtorem`、`lib-flexible`。`postcss-pxtorem`会自动的将我们写的`px`转化成`rem`，而`lib-flexible`会根据当前的尺寸，来调整`html`上的`font-size`进行适配。安装命令通过`npm install --save-dev postcss-pxtorem lib-flexible`安装即可。

2. 配置`package.json`

   ```json
   "postcss": {
        "plugins": {
          "autoprefixer": {},
          "postcss-pxtorem": {
            "rootValue": 37.5, // 设计师的尺寸/100 计算得到
            "propList": [
              "*"
            ],
            "selectorBlackList": [ // 黑名单 不需要自动转换计算
              "van-*"
            ]
          }
        }
      }
   ```

3. 配置`main.js` 

   ```js
   import "lib-flexible"
   ```



## vant组件库

vant库是有赞公司前端团队开源的一款针对`vue`库的组件库。里面集成了很多移动端用到的组件，包括按钮、图片、Icon图标等。而且因为有赞是一个做微商城的公司，所以有很多微商城的组件比如地址列表、商品卡片、优惠券等组件。

### 安装

```shell
npm install vant --save
```

### 引入组件

`babel-plugin-import`是一款`babel`插件，它会在编译过程中将`import`的写法自动转换为按需引入的方式

```js
// npm intall安装上述插件后 找到项目的 babel.config.js 文件
// 添加以下键值对 
module.exports = {
  plugins: [
    ['import', {
      libraryName: 'vant',
      libraryDirectory: 'es',
      style: true
    }, 'vant']
  ]
};

// 接着你可以在代码中直接引入 Vant 组件
// 插件会自动将代码转化为方式二中的按需引入形式
// {{}}用来包裹对象中的变量 
import { Button } from 'vant';
```

更多请参考：`https://youzan.github.io/vant/#/zh-CN/quickstart`。

## Element UI组件库

`element ui`组件库是由饿了么前端团队专门针对`vue`框架开发的组件库，专门用于电脑端网页的。

### 安装

```shell
npm install element-ui@2.12.0 --save
```

### 引入

需要借助`babel-plugin-component`这个库，才能实现按需引入。安装的命令为：`npm install babel-plugin-component --save-dev`。

### 配置

在`babel.config.js`中**添加如下配置（重新exports一个）**

```js
module.exports = {
  "presets": [
    "@vue/app"
  ],
  "plugins": [
    [
      "component",
      {
        "libraryName": "element-ui",
        "styleLibraryName": "theme-chalk"
      }
    ]
  ]
}
```

### 使用

```vue
<template>
  <div id="app">
    <el-button type="primary">这是一个按钮</el-button>
  </div>
</template>

<script>
import {Button} from 'element-ui'

export default {
  name: 'app',
  components: {
    [Button.name]: Button
  }
}
</script>
```

## 支付宝组件

* 沙箱账号配置 、公私钥设置 
* 第三方的python sdk ：https://github.com/fzlee/alipay/blob/master/README.zh-hans.md 。如果要设置回调url，需要公网服务器







 
