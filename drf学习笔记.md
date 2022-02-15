# 准备

## DRF介绍

`DRF`是`Django Rest Framework`单词的简写，是在`Django`框架中实现`Restful API`的一个插件，使用他可以非常方便的实现接口数据的返回。`Django`中也可以使用`JsonResponse`直接返回`json`格式的数据，但是`DRF`相比直接使用`Django`返回`json`数据有以下几个好处：

1. 可以自动生成`API`文档，在前后端分离开发的时候进行沟通比较有用。
2. 授权验证策略比较完整，包含`OAuth1`和`OAuth2`验证。
3. 支持`ORM`模型和非`ORM`数据的序列化。
4. 高度封装了视图，使得返回`json`数据更加的高效。

## 安装使用

使用`pip install djangorestframework` 安装，然后在`settings.INSTALLED_APPS`中进行安装。

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

**在一个app（python包）中，新建`serializers.py`文件，在其中书写序列化的详细规则。序列化器作为中间层，夹在了django的ORM数据和返回给客户端的数据之间。**



## 创建模型类

所有的讲解基于以下模型类：

商家、商品、商品分类 

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
    merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE,verbose_name='所属商家',related_name='categories')

class Goods(models.Model):
    """
    商品
    """
    name = models.CharField(max_length=200,verbose_name='商品名称')
    picture = models.CharField(max_length=200,verbose_name='商品图片')
    intro = models.CharField(max_length=200)
    price = models.DecimalField(verbose_name='商品价格',max_digits=6,decimal_places=2) # 最多6位数，2位小数。9999.99
    category = models.ForeignKey(GoodsCategory,on_delete=models.CASCADE,related_name='goods_list')
```



# 序列化

`drf`中的序列化主要是用来将模型序列化成`JSON`格式的对象。**但是除了序列化，它还具有表单验证功能，数据存储和更新功能。**

**drf在设计上，很多地方参考了django的Form类，可以两者对比学习。**



## Serializer类

**Serializer类作为基本的序列化器，使用上可以帮助我们理解序列化的原理。**

这里我们以上一节的模型`Merchant`、`GoodsCategory`、`Goods`为例来讲解。首先我们创建一个`Merchant`的`Serializer`类。必须继承自`Serializer`及其子类。示例代码如下：

```python
from rest_framework import serializers
from .models import Merchant,GoodsCategory,Goods

class MerchantSerializer(serializers.Serializer):
    # 字段与你的模型字段一一对应
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True,max_length=200)
    logo = serializers.CharField(required=True,max_length=200)
    notice = serializers.CharField(max_length=200,required=False)
    up_send = serializers.DecimalField(max_digits=6,decimal_places=2,required=False)
    lon = serializers.FloatField(required=True)
    lat = serializers.FloatField(required=True,error_messages={"required":"必须传入lat！"})
	
    # 如果继承自 Serializer 类
    # 必须实现父类的create和update方法
    
    def create(self, validated_data):
        # create方法实现
        return Merchant.objects.create(**validated_data)

    def update(self,instance, validated_data):
        # update方法实现
        # instance 是模型类实例 validated_data是验证过的数据（dict） 
        instance.name = validated_data.get('name',instance.name)
        instance.logo = validated_data.get('logo',instance.logo)
        instance.notice = validated_data.get('notice',instance.notice)
        instance.up_send = validated_data.get('up_send',instance.up_send)
        instance.lon = validated_data.get('lon',instance.lon)
        instance.lat = validated_data.get('lat',instance.lat)
        instance.save()
        return instance
```

那么以后在视图函数中，可以使用他来对数据进行序列化，也可以对数据进行校验，然后存储数据。比如以下在视图函数中使用：

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
        return JsonResponse(serializer.data,safe=False) # data是一个列表 设置safe参数
    else:
        serializer = MerchantSerializer(data=request.POST) 
        if serializer.is_valid(): # 验证
            serializer.save()
            return JsonResponse(serializer.data,status=200)
        return JsonResponse(serializer.errors,status=400)
```

## ModelSerializer

之前在写基本序列化Serializers类的时候，几乎把模型中所有的字段都写了一遍。**我们可以把模型中的字段移植过来即可，这时候就可以使用`ModelSerializer`类实现**。示例代码如下：

```python
class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = "__all__"
```



## 序列化嵌套

有时候在一个序列化中，我们可能需要其他模型的序列化器。比如我们在`GoodsCategory`中想要获取`Merchant`以及这个分类下的商品`Goods`。他们三者之间的关系为：Merchant创建GoodsCategory，GoodsCategory包含了很多Goods。

序列化嵌套示例代码如下：

```python
class GoodsCategorySerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(read_only=True,required=False) # 返回商家
    goods_list = GoodsSerializer(many=True,required=False)
    merchant_id = serializers.IntegerField(required=True,write_only=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

    def validate_merchant_id(self,value): # 验证字段 
        if not Merchant.objects.filter(pk=value).exists():
            raise serializers.ValidationError("商家不存在！")
        return value

    def create(self, validated_data):
        merchant_id = validated_data.get('merchant_id')
        merchant = Merchant.objects.get(pk=merchant_id) # 创建一个merchant实例
        category = GoodsCategory.objects.create(name=validated_data.get('name'), merchant=merchant) # 再创建一个category实例 
        return category
```

## 关于read_only和write_only

1. `read_only=True`：这个字段只只能读，只有在返回数据的时候会使用。
2. `write_only=True`：这个字段只能被写，只有在新增数据或者更新数据的时候会用到。

## 验证

验证用户上传上来的字段是否满足要求。可以通过以下三种方式来实现。

1. 验证在`Field`中通过参数的形式进行指定。比如`serializers.CharField(max_length=200, required=True)`等。

2. 通过重写`validate(self,attrs)`方法进行验证。`attrs`中包含了所有字段。如果验证不通过，那么调用`raise serializer.ValidationError('error')`即可。

3. 重写`validate_字段名(self,value)`方法进行验证。这个是针对某个字段进行验证的。如果验证不通过，也可以抛出异常。

   ```python
   def validate_merchant_id(self,value):
       if not Merchant.objects.filter(pk=value).exists():
           raise serializers.ValidationError("商家不存在！")
           return value 
   ```



# 请求和响应

## Request对象

`DRF`的`Request`对象是从`HttpRequest`中拓展出来的，但是增加了一些其他的属性。其中最核心的用得最多的属性便是`request.data`。**`request.data`比`request.POST`更加灵活**：

1. `request.POST`：只能处理表单数据，获取通过`POST`方式上传上来的数据。
2. `request.data`：**可以处理任意的数据。可以获取通过`POST`、`PUT`、`PATCH`等方式上传上来的数据。**
3. `request.query_params`：查询参数。比`request.GET`更用起来更直白。

## Response对象

**`Response`可以自动的根据返回的数据类型来决定返回什么样的格式。**并且会自动的监听如果是浏览器访问，那么会返回这个路由的信息。

例如

```python
return Response("你好") # 字符串
return Response(serializer.data) # 序列化数据 
```



## 状态码

在`Restful API`中，响应的状态码是很重要的一部分。比如请求成功是`200`，参数错误是`400`等。但是具体某个状态码是干什么的，`django`是没有做过多的解释（这也不是django所需要解决的问题，因为他只是个web框架），对于一些初学者而言用起来会有点迷糊。**这时候我们可以使用`DRF`提供的状态码（其实就是宏定义）**。比如：

```python
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET','POST','PUT','DELETE'])
def merchant(request):
    return Response({"username":"zhiliao"},status=status.HTTP_200_OK)
```

## 实现`APIView`

以上的`Respone`和`Request`对象都只能在`DRF`的`APIView`中才能使用。如果是视图函数，那么可以使用装饰器`rest_framework.decorators.api_view`进行装饰，这个装饰器中可以传递本视图函数可以使用什么`method`进行请求。示例代码如下（可以看一下Response的用法）：

```python
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

如果是类视图，那么可以让你的类继承自`rest_framework.views.APIView`。示例代码如下：

```python
from rest_framework.views import APIView

class MerchantView(APIView):
    def get(self,request):
        return Response("你好")
```