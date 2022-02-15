# 常用包

```python
import torch 
import torch.nn as nn # 神经网络
import torch.nn.functional as F # 常用损失函数
import torch.optim as optim # 优化器相关 
```



# 张量 

### 张量                              

张量，pytorch里的多维矩阵，可以利用GPU进行计算加速。类似numpy里的naarray可以利用CPU。

```python
import torch  
x=torch.rand(5, 3) # 创建随机矩阵 

# 可以使用与numpy相同的shape属性查看
print(x.shape)
# 也可以使用size()函数，返回的结果都是相同的
print(x.size() # torch.Size([2, 3])
```



特殊的，0维矩阵称为标量`scalar`。标量或者1维张量可以使用`.item()`方法取出数据 

```python
scalar =torch.tensor(3.1433223) # 标量
print(scalar.size()) # torch.Size([])
print(scalar.item()) # 3.1433

scalar =torch.tensor([3.1433223]) # 1维 张量 
```

### 初始化

```python
torch.tensor([[1, 2], [3, 4]]) # 指定数值 
torch.randn(2, 2) # 随机初始化 
torch.ones(2, 2) # 初始化，使用1填充
torch.zeros(2,2) # 初始化，使用0填充
torch.eye(2,2)  # 单位矩阵
```

### 常用方法

类似numpy 

```python
torch.max(x, dim=1)  # 沿着行取最大值
torch.sum(x, dim=1) # 沿着行求和
```

正如官方60分钟教程中所说，以_为结尾的，均会改变调用值

```python
# add 完成后x的值改变了
x.add_(y)
print(x)
```

算术运算时，注意 点乘 与 矩阵 乘法 

```python
torch.bmm  # 矩阵广播乘 第一个b表示batch的意思，即支持广播运算
torch.matmul(a,b)  # 矩阵乘 

torch.mul(a,b)  # 点乘，a,b两个矩阵要支持广播运算
a*b # 点乘，两个矩阵形状相同
```





tensor之间比较

* `torch.equal(a,b)` ，比较两个tensor的大小和元素，返回true/false。

* 取最大，`torch.tensor()`

* `a==b`，逐个比较，返回布尔矩阵 

  ```python
  # a和b中相同的个数 accuracy计算
  torch.mean((a==b).float()) # 将bool转为float
  ```








### 数据类型

Tensor的基本数据类型有五种：

- 32位浮点型：**torch.FloatTensor**。 (默认)
- 64位整型：torch.LongTensor。
- 32位整型：torch.IntTensor。
- 16位整型：torch.ShortTensor。
- 64位浮点型：torch.DoubleTensor。



dtype类型：https://pytorch.org/docs/stable/tensor_attributes.html#torch.torch.dtype 





类型声明  

```python
# 指定dtype 
torch.tensor(a,dtype=torch.int8)

# 等同于上面
torch.LongTensor(a)
```



类型切换 

```python
a=torch.LongTensor([1,2,3])
a.float() # 转为 tensor 类型 

# tensor.type() 除了返回张量类型外 
# 还可以用于张量类型转换 
a.type(dtype=torch.uint8)  # 转换为uin8类型 
```







### 与numpy相互转换

我们很容易用`numpy()`和`from_numpy()`将`Tensor`和NumPy中的数组相互转换。需要注意：

1.  这两个函数所产生的的`Tensor`和NumPy中的数组**共享相同的内存**（所以他们之间的转换很快），改变其中一个时另一个也会改变
2. 在CPU中进行



```python
# tensor 转 numpy 
x.numpy() # x是一个tensor 转为numpy  

# numpy 转tensor
b = torch.from_numpy(a) # a是一个ndarray  
```

所有在CPU上的`Tensor`（除了`CharTensor`）都支持与NumPy数组相互转换 。

```python
c = torch.tensor(a) # 初始化 进行拷贝转换
```

### 设备切换

#### cuda支持 

是否安装cuda `torch.cuda.is_available()` 

查看cuda版本 `nvcc --version`

#### cpu gpu

使用`.cpu()`方法将tensor移动到cpu；使用`.cuda()`方法将tensor移动到gpu

```python
cpu_a=torch.rand(4, 3)
gpu_a=cpu_a.cuda() # 移动到gpu
cpu_b=gpu_a.cpu() # 移动到cpu
```



`.to('device')` ，移入指定设备

```python
# torch.cuda.is_available() 返回 True False 
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   # 设备

x = torch.tensor([1, 2, 3], device=device) # x.device 可以查看 数据存在哪里 
```

**当数据存入GPU时，模型也需要存入GPU，这样才可以在GPU上进行计算。**

```python
model.to('cuda') # 模型的所有层丢到GPU 
```



一般来说，在数据送入到模型前、模型初始化的时候，就应该将其移入到GPU。

```python
# train 
model.to('cuda') 
for x,y in train_loader:
	x=x.to('cuda') # to 返回一个新的张量 
	y=y.to('cuda') 
```



#### cuda out of memory

out of memeory一种可能的情况是：pytorch一直存储计算图，未释放。

例如：

```python
'''
loss 在整个训练集遍历完时才反向传播
pytorch就会存储每个batch的计算图 这会导致内存一直被占用
解决的办法是计算每个batch的loss
'''
for x,y in train_loader:
	y_hat=model(x)
    loss+=criterion(y_hat,y) 
loss.backward()


# 正确做法
for x,y in train_loader:
	y_hat=model(x)
    loss=criterion(y_hat,y)
	loss.backward()
```



### 索引 

**索引出来的结果与原数据共享内存。** 

#### 切片 

和python的列表使用一致 `tensor[start:end:step]`，start缺省为0，end缺省为最后。  切片数据和原数据共享内存。 

```python
a= torch.ones(4,3)
b= torch.tensor([[1,2,3],[4,5,6]])
a[::2]=b # 将a的第0行、第2行赋值为b 
```

#### 离散索引

`t[t1]` ，t1是另外一个向量，如`a[[1,2,3]]` 

#### 布尔索引

`tensor.mask_select(mask)` ，mask掩码矩阵，要求为bool型。 mask矩阵不必和tensor相同，但是必须满足广播运算。 函数将会返回 `1*len` 大小的张量，张量的每个元素都是 mask矩阵为true的位置 在 tensor中的元素。

#### gather

把另外一个向量作为索引，在对应维度上，去取另外一个向量   `torch.gather(t1, 1, t2) `  ；`t1`、`t2`的前几个维度需要相同 

官网例子： https://pytorch.org/docs/stable/generated/torch.gather.html?highlight=gather#torch.gather

```python
>>> t = torch.tensor([[1, 2], [3, 4]])
# 在dim1上 按照索引取元素 
# 第一行 取 0 0 
# 第二行 取 1 0 
>>> torch.gather(t, 1, torch.tensor([[0, 0], [1, 0]])) # 第一行的0 0 第二行的1 0
tensor([[ 1,  1],
        [ 4,  3]])
```



### 形状

#### view 

```python
y = x.view(15)  # 一维 
z = x.view(-1, 5)  # -1所指的维度可以根据其他维度的值推出来
```

**`view()`返回的新`Tensor`与源`Tensor`虽然可能有不同的`size`，但是是共享`data`的**，即返回视图

```python
x.clone().view(15) # 克隆后转换形状
```



view 对tensor的内存要求：view只能作用在contiguous（意为内存连续）的variable上，如果在view之前调用了transpose、permute等，就需要调用contiguous()来返回一个contiguous copy。

判断ternsor是否为contiguous，可以调用torch.Tensor.is_contiguous()函数:

```python
import torch 
x = torch.ones(10, 10) 
x.is_contiguous()                                 # True 
x.transpose(0, 1).is_contiguous()                 # False
x.transpose(0, 1).contiguous().is_contiguous()    # True
```

在pytorch的最新版本0.4版本中，**增加了torch.reshape()**，与 numpy.reshape() 的功能类似，大致相当于 tensor.contiguous().view()，这样就省去了对tensor做view()变换前，调用contiguous()的麻烦；

****

#### permute(dim1,dim2）

对tensor的维度重新排列，如`t.permute(1,2,0)` ，原tensor的dim0被移到了最后1个维度，和view的区别在于，view重新改变了tensor的形状，而permute只是换了一个视角看tensor。

****

#### transpose

`torch.transpose(tensor,dim0,dim1)` ，交换指定两个维度



***

#### tensosr.t()

转置

****

#### squeeze/unsqueeze

`tensor.squeeze(dim0)`，在dim0上丢掉维度1（如`a*1*b`） 。`tensor.unsqueeze(dim0)`，在dim0上插入维度1 。

***

#### expand

`tensor.expand()`，将矩阵复制 ，数据并没有填充 

```python
a=torch.tensor([1,2]) # 1*2
b=a.expand(2,2) # 2*2 
b[0,0]=100 # 数据只是复制 

'''
tensor([[50,  2],
        [50,  2]])
'''

# 如果想完成独立的复制 使用clone 
b=a.expand(2,2).clone() 
```



****

#### cat

`torch.cat((a,b),dim)` 在dim上拼接元组里的tensor

#### stack

`torch.stack((t1,t2),dim)` 堆叠 tensor ，新插入一个维度 

***

#### split

`torch.split(tensor,size,dim)` ，在dim维度上切割，size是每一份的大小。 

参考：https://pytorch.org/docs/1.7.1/generated/torch.split.html?highlight=split#torch.split 



# 自动求导

### requires_grad

在张量（Tensor类）上的所有操作，pytorch都能为他们自动提供微分，简化了手动计算导数的复杂过程。

张量属性` requires_grad=True `——来告诉Pytorch需要对该张量进行自动求导，PyTorch会记录该张量的每一步操作历史并自动计算。

```python
x = torch.rand(5, 5, requires_grad=True)
y = torch.rand(5, 5, requires_grad=True)
z=torch.sum(x+y) # z是一个标量
z # tensor(25.6487, grad_fn=<SumBackward0>)
```

在张量进行操作后，grad_fn已经被赋予了一个新的函数——Function对象。Function对象记录了这个Tensor的计算图，直到叶子节点——用户手动创建的tensor。

### backward

```python
z.backward() # 简单的自动求导 
print(x.grad,y.grad) 
```

如果Tensor类表示的是一个标量，则不需要为backward()指定任何参数，上例等价于`z.backward(torch.tensor(1.))`。否则，应该传入一个大小与之匹配的张量。

```python
x = torch.rand(5, 5, requires_grad=True)
y = torch.rand(5, 5, requires_grad=True)
z= x**2+y**3 # z是一个张量 

z.backward(torch.ones_like(x)) # ones_like 返回相同大小的矩阵 元素全为1 
print(x.grad)
```



过程解析：

1. 当我们执行z.backward()的时候。这个操作将调用z里面的grad_fn这个属性，执行求导的操作。
2. 这个操作将遍历grad_fn的next_functions，这部分是一个递归的过程，直到最后类型为叶子节点，也就是反向求导的链式传播。
3. 计算出结果以后，将结果保存到叶子节点的`.grad` 属性上 





backwa调用以后，就会释放从根节点开始的计算图，为了节约内存。这在有些场景需要注意，例如：

```python
loss=0
for x,y in train_loader:
	y_hat=model(x)
    loss+=criterion(y_hat,y)
    optimzer.zero_grad()
    # 在第一次执行的时候是没有问题的，但是第2次的时候 上一个loss已经被释放计算图 这会导致报错 大意为 re_backward 不被允许 
    # Trying to backward through the graph a second time
    loss.backward()  
    optimizer.step()
```







求导的数学原理参考：

* https://www.cnblogs.com/zhouyang209117/p/11023160.html



$y=\begin{bmatrix}y_1\\...\\y_m\end{bmatrix}=f(\begin{bmatrix}x_1\\...\\x_n\end{bmatrix})$ ，完成从输入n维度的x到输出m维度的y变换。

当y是标量时，例如$y'=\sum y_m$ ，对y各个分量累加，则$\overrightarrow{g_x}=\begin{bmatrix}\frac{\partial y'}{\partial x_1}\\...\\\frac{\partial y'}{\partial x_n}\end{bmatrix}$  



当y是张量时，需要传入一个与其同等大小的矩阵，作为权重矩阵，线性加权其雅克比矩阵 $k*Jacobi=\begin{bmatrix}k_1&...&k_m\end{bmatrix}*\begin{bmatrix}\frac{\partial y_1}{\partial x_1}&...&\frac{\partial y_1}{\partial x_n}\\.&.&.\\\frac{\partial y_m}{\partial x_1}&.&\frac{\partial y_m}{\partial x_n}\end{bmatrix}$， 也就是说 y对x的每一个分量都是这样加权，例如$y_1$对$x_1$分量的加权，$\frac{\partial y}{\partial x_1}=\sum_j^m k_j*\frac{\partial y_j}{\partial x_1}$ 



张量求导例子：

```python
import torch 
from torch import tensor 

x=torch.rand(3,3,requires_grad=True)
y=torch.rand(3,3,requires_grad=True)
z=2*x+y

'''
可以拆成
z0=2x0+y0
z1=2x1+y1
...
所以z对x的雅克比矩阵 为
2 0 0 
0 2 0 
0 0 2 

权重系数矩阵
1 0 0 样本1的权重系数 
1 0 1 样本2的权重系数
1 0 2 样本3的权重系数 

最后输出结果 权重系数矩阵*（矩阵乘法）雅克比矩阵 为：
2 0 0
2 0 2
2 0 4

这个例子简化了y对x的函数关系 实际中雅克比矩阵每一行可能都和其他分量有关 
'''
z.backward(torch.Tensor([[1,0,0],[1,0,1],[1,0,2]]))
x.grad
```



### detach

`x.detach()` 返回一个tensor，该tensor与x同享内存，但是`requires_grad=False`，不会参与到后续的计算图中，相当于作为常量固定。此后的方向传播到该节点也将终止，不再继续传播，常见于局部调整网络参数。



例：

```python
y=ANet(x)
z=BNet(y.detach()) 
# 只会对B网络参数梯度更新 因为y是作为叶子节点被送到B的
# 它在A网络的计算图在B中追溯不到 
z.backward() 
```





### 上下文管理器

使用上下文管理器临时关闭对张量的自动求导记录。**在测试集计算准确率的时候会经常用到。**关闭梯度可以免去pytorch对计算图的监控，节省内存消耗，加快速度。

```python
with torch.no_grad():  # 
    print((x +y*2).requires_grad) # false
```

`torch.set_grad_enabled` 同理 ，但是可以灵活控制

```python
x = torch.tensor([1], requires_grad=True)
is_train = False # 是否训练 
with torch.set_grad_enabled(is_train):  
  y = x * 2 # y.requires_grad=False 不可以使用 backward() 

```





**grad在反向传播过程中是累加的(accumulated)，每一次反向传播，梯度都会累加，所以一般在反向传播之前需把梯度清零。**

```python
model.zero_grad()  # 网络所有参数梯度清0
opt.zero_grad() # 只对优化器关注的参数梯度清0 
```



如果我们想要修改`tensor`的数值，但是又不希望被`autograd`记录（即不会影响反向传播），那么我么可以对`tensor.data`进行操作。

```python
x = torch.ones(1,requires_grad=True)

print(x.data) # 还是一个tensor
print(x.data.requires_grad) # 但是已经是独立于计算图之外

y = 2 * x
x.data *= 100 # 只改变了值，不会记录在计算图，所以不会影响梯度传播

y.backward()
```



# 定义网络

`torch.nn`是专门为神经网络设计的模块化接口。

`nn.functional` 这个包包含了神经网络中使用的一些常用函数，这些函数的特点是，不具有可学习的参数(如ReLU，pool，DropOut等)

```python
import torch.nn as nn # 约定俗称
import torch.nn.functional as F # 约定俗成
```

### 定义网络

#### Module

继承`nn.Module`，在初始化中定义网络的各个层，然后实现它的`forward()`方法。

```python
class Net(nn.Module):
    def __init__(self):
        # nn.Module子类的函数必须在构造函数中执行父类的构造函数
        super(Net, self).__init__()
        
        # 卷积层 '1'表示输入图片为单通道， '6'表示输出通道数，'3'表示卷积核为3*3
        self.conv1 = nn.Conv2d(1, 6, 3) 
        #线性层，输入1350个特征，输出10个特征
        self.fc1   = nn.Linear(1350, 10)  #这里的1350是如何计算的呢？这就要看后面的forward函数
    #正向传播 
    def forward(self, x): 
        # x的输入格式：[batch,chanel,width,height]
        print(x.size()) # 结果：[1, 1, 32, 32]
        # 卷积 -> 激活 -> 池化 
        x = F.relu(self.conv1(x)) #根据卷积的尺寸计算公式，计算结果是30 
        print(x.size()) # 结果：[1, 6, 30, 30]
        x = F.relu(F.max_pool2d(x, (2, 2))) #我们使用池化层，计算结果是15
        print(x.size()) # 结果：[1, 6, 15, 15]
        # reshape，‘-1’表示自适应
        #这里做的就是压扁的操作 就是把后面的[1, 6, 15, 15]压扁，变为 [1, 1350]
        x = x.view(1, -1) 
        print(x.size()) # 这里就是fc1层的的输入1350 
        x = self.fc1(x)        
        return x

net = Net()
print(net)
```

net打印结果  含有各层名字和参数

```
Net(
  (conv1): Conv2d(1, 6, kernel_size=(3, 3), stride=(1, 1))
  (fc1): Linear(in_features=1350, out_features=10, bias=True)
)
```

网络的可学习参数通过`net.parameters()`返回

```python
for parameters in net.parameters():
    print(parameters)
```

```
Parameter containing:
tensor([[[[ 0.2745,  0.2594,  0.0171],
          [ 0.0429,  0.3013, -0.0208],
          [ 0.1459, -0.3223,  0.1797]]],
```

`net.named_parameters()` 可以同时返回名称和参数。

```python
for name,parameters in net.named_parameters():
    print(name,':',parameters.size())
```

```
conv1.weight : torch.Size([6, 1, 3, 3])
conv1.bias : torch.Size([6])
```



调用网络实例，传入输入tensor，即可自动调用`forward()`函数，返回输出。

```python
# 最前面的维度表示batch-size 
# torch 支持的最小迭代单位为batch 所以必须人工在单个样本前加一个维度
input = torch.randn(1, 1, 32, 32) # 这里的对应前面forward的输入是32
out = net(input)
print(out.size) #
```

在反向传播前，要将网络的梯度清0，否则会累加。

```
net.zero_grad() 
out.backward(torch.ones(1,10))
```

#### Sequential

当模型的前向计算为**简单串联各个层的计算时**（与之相对的是复用某一些层），`Sequential`类可以通过更加简单的方式定义模型。

```python
# Example of using Sequential
model = nn.Sequential(
          nn.Conv2d(1,20,5),
          nn.ReLU(),
          nn.Conv2d(20,64,5),
          nn.ReLU()
        )

# Example of using Sequential with OrderedDict
# OrderDict 是python的一个有序字典 按照添加顺序创建字典 
model = nn.Sequential(OrderedDict([
          ('conv1', nn.Conv2d(1,20,5)),
          ('relu1', nn.ReLU()),
          ('conv2', nn.Conv2d(20,64,5)),
          ('relu2', nn.ReLU())
        ]))
```



利用sequential 串联复杂的网络（端到端）

```python
# NestMLP、FancyMLP 是两个自定义的网络 
net = nn.Sequential(NestMLP(), nn.Linear(30, 20), FancyMLP())
```



### 激活函数

#### sigmoid

激活函数的作用是对输入施加非线性变化，实现更复杂的函数拟合。因为如果只有很多层线性变换的话，一层层连接，到最后其实也只是一个矩阵相乘。 

sigmoid函数，映射成`(0,1)`  `torch.sigmoid`

<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/image-20210806171258960.png" alt="image-20210806171258960" style="zoom: 67%;" />

#### tanh

tanh 函数 ，映射成`(-1,1)` ，`torch.tanh`

<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/image-20210806171341157.png" alt="image-20210806171341157" style="zoom:67%;" /> 

#### relu

现在最常用的是RELU，简单好用。

relu函数 ，映射成`[0,1)`  ，`torch.relu`

<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/image-20210806171411023.png" alt="image-20210806171411023" style="zoom:67%;" /> 



### 损失函数

nn中还预制了常用的损失函数，下面我们用MSELoss用来计算均方误差

```python
y = torch.arange(0,10).view(1,10).float()
criterion = nn.MSELoss()
loss = criterion(out, y)
#loss是个scalar，我们可以直接用item获取到他的python类型的数值
print(loss.item())
```

#### L1Loss

输入x和目标y之间差的绝对值，要求 x 和 y 的维度要一样（可以是向量或者矩阵），得到的 loss 维度也是对应一样的

![image-20210805154608853](https://gitee.com/jiang_hui_kai/images/raw/master/img/image-20210805154608853.png)

#### nn.NLLLoss

用于多分类的负对数似然损失函数

![image-20210805160729614](https://gitee.com/jiang_hui_kai/images/raw/master/img/image-20210805160729614.png) 

#### MSELoss

<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/image-20210805160804054.png" alt="image-20210805160804054" style="zoom:50%;" />

#### CrossEntropyLoss

多分类用的交叉熵损失函数，LogSoftMax和NLLLoss集成到一个类中，会调用nn.NLLLoss函数，我们可以理解为CrossEntropyLoss()=log_softmax() + NLLLoss()。

<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/image-20210805160846536.png" alt="image-20210805160846536" style="zoom:67%;" />



官网doc：

https://pytorch.org/docs/stable/generated/torch.nn.functional.cross_entropy.html?highlight=cross_entropy#torch.nn.functional.cross_entropy  



`CrossEntropyLoss(input,target)`：

* input：`n*c`大小矩阵，n为batch大小，c是标签数  。物理意义为：每一个样本在c类标签上的概率（会自动进行softmax运算）
* target：`n` 一维矩阵，要求dtype为`torch.long` 



#### loss=nan

loss 出现nan的可能原因：

1. loss函数的计算有问题 
2. 学习率太大，以至于损失函数发散 。更改学习率或者优化器 

### 优化器

#### 优化器

**在反向传播计算完所有参数的梯度后，还需要使用优化方法来更新网络的权重和参数**。以随机梯度下降算法为例：`weight = weight - learning_rate * gradient`

```python
out = net(input) # 这里调用的时候会打印出我们在forword函数中打印的x的大小
criterion = nn.MSELoss()
loss = criterion(out, y)
#新建一个优化器，SGD只需要要调整的参数和学习率
optimizer = torch.optim.SGD(net.parameters(), lr = 0.01)
# 先梯度清零(与net.zero_grad()效果一样)
optimizer.zero_grad() 
loss.backward()

#更新参数
optimizer.step()
```

#### scheduler

`torch.optim.lr_scheduler`类  

```python
# 在 opt.step() 更新参数之后使用 
scheduler = ... # 定义的一个学习率调度器 
for epoch in range(100):
    train(...)
    validate(...)
    scheduler.step()
```

参考：https://blog.csdn.net/qyhaill/article/details/103043637 

## 参数初始化

```python
# 方法带下划线的方法都是原地修改 
# 根据名字
for name,w in model.named_parameters():
    if 'weight' in name:
        # 权重初始化 
         nn.init.normal_(w, mean=0, std=0.01)
    elif 'bias' in name:
        # 偏置初始化 
        nn.init.constant_(w, 0)
    else:
        pass 
```



# 模型保存加载 

网络和优化器有一个属性`.state_dict()`，称作状态字典，记录了各自的状态信息。

网络的`state_dict()`保存了模型的参数值，优化器的状态字典保存了参数的步长、动量等信息。

```python
# 在训练过程中 常见的checkpoint保存
state = {
    'voc': voc, # sth about corpus\data\...
    'embedding': embedding.state_dict(),  # embedding
    'encoder_state': encoder.state_dict(), # module
    'decoder_state': decoder.state_dict(),
    'encoder_opt': encoder_opt.state_dict(),  # optimzer
    'decoder_opt': decoder_opt.state_dict(),
    'epoch': _epoch   # itertion
}

# torch.save 底层调用了python的pickle模块 
torch.save(state, 'save_path')
```



```python
# 加载 
# model是一个模型实例 optimizer同理 
model.load_state_dict('状态字典') # 参数赋值
```







# 数据加载和预处理 

### Dataset

`Datasets()` ，pytorch官网提供的数据集均继承该类。

自定义数据集有两种实现形式

1. `map-style`类型的，需要实现`getitem`、`len`等方法，利于随机取数和提前获取大小。
2. `iterable-style`类型，需要实现`__iter__`方法，当数据集比较大时，可以考虑使用这个方法。

```python
from torch.utils.data import Dataset, DataLoader

# 实现一个数据集
class MyDataset(Dataset):
    def __init__(self):
        super().__init__()
        self.device=torch.device('cuda')
        self.data = [] # 假设这是数据 
        # self.data.append((x,y)) # x是数据 y是标签

    def __getitem__(self, item):
        # dataset[item] 如何返回数据
        # 返回前转为tensor 
        x=torch.tensor(self.data[item][0],dtype=torch.int64).to(self.device)
        y=torch.tensor(self.data[item][1],dtype=torch.int64).to(self.device)
        return x,y # 和pytorch数据格式兼容 <data target> 

    def __len__(self):
        return len(self.data)

    
dataset = MyDataset() # 自定义数据集
loader = DataLoader(dataset=dataset, batch_size=128) # 自定义迭代器 
```







### DataLoader

DataLoader为我们提供了对Dataset的读取操作，返回一个可迭代对象。

```python
# 迭代器
batch_size=64
train_loader=DataLoader(dataset=train_datasets,
                        shuffle=True # 是否随机打乱
                       batch_size=batch_size) # batch大小

# 可迭代对象
i_train_data=iter(train_loader)
next(i_train_data)

# for循环 
# 定义test_loader 同理 
for (data,target) in train_loader:
    # 数据格式：data 是数据 target 是 标签
    pass

```



注意，如果直接对一个dataloader求长度`len(dataloader)`，它返回的是有几个batch。 





Dataloader 还提供了一个钩子函数`collate_fn(batch)`，返回一个batch数据时，如何处理 

```python
def batch_data_process(batch_data):
    for x,y in batch_data:
        pass # 对批量数据做一些处理     
    return x.to(DEVICE),y.to(DEVICE)


DataLoader(batch_size=BATCH_SIZE, 
           dataset=train_data, 
           collate_fn=batch_data_process)
```



### 数据集分割 

随机分割 `random_split` 

```python
from torch.utils.data import random_split 

tain_ratio = int(len(data)*0.95) # 95%数据用于训练 
# 数据集，训练集大小，测试集大小  两者之和为整个数据集大小
# 这里的data可以是 torch.utils 的dataset对象 
train_data,valid_data = random_split(data,[train_ratio,len(data)-train_ratio]) 
```





### torchvision

torchvision 是PyTorch中专门用来处理图像的库。



torchvision提供了一些常用的datasets，可以直接使用。

- MNIST
- COCO
- Captions
- Detection
- LSUN
- ImageFolder
- Imagenet-12
- CIFAR
- STL10
- SVHN

```python
import torchvision.datasets as datasets
trainset = datasets.MNIST(root='./data', # 表示 MNIST 数据的加载的目录
                                      train=True,  # 表示是否加载数据库的训练集，false的时候加载测试集
                                      download=True, # 表示是否自动下载 MNIST 数据集
                                      transform=None) # 表示是否需要对数据进行预处理，none为不进行预处理
```



torchvision.models

torchvision不仅提供了常用图片数据集，还提供了训练好的模型，可以加载之后，直接使用。

- AlexNet
- VGG
- ResNet
- SqueezeNet
- DenseNet



一个使用预训练模型 resetnet18的例子

```python
#我们直接可以使用训练好的模型，当然这个与datasets相同，都是需要从服务器下载的
import torchvision.models as models
model = models.resnet18(pretrained=True) # pretrained=True 表示使用预训练模型 
# 将所有的参数层进行冻结
for param in model.parameters():
    param.requires_grad = False 
# 因为最后的多分类类别数目不同 所以替换全连接层 
fc=nn.Linear(
    in_features=model.fc.in_features,
    out_features=LABELS
)
model.fc=fc # 替换为自定义的全连接层
```

****



torchvision.transforms

```python
from torchvision import transforms as transforms
# transform 接收的输入 是Image对象 在中间过程进行操作时返回的仍然是Image对象
# 最后应当返回一个Tensor 
transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),  # 随机裁剪 先四周填充0，在把图像随机裁剪成32*32
    transforms.RandomHorizontalFlip(),  # 概率水平翻转 
    transforms.RandomRotation((-45,45)), # 概率旋转
    transforms.ToTensor(), # 将Image对象转为tensor
    # R,G,B每层的归一化用到的均值和方差
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.229, 0.224, 0.225)), 
])

# RGB 的均值 和 方差 是imagnet的归一化参数 可以认为是固定值
# 如果是自己的数据集 需要额外设置 
```



transforms例子理解：https://blog.csdn.net/see_you_yu/article/details/106722787



transorm的compose会组合所有操作为一个对象，然后具备对象调用方法`__call__()`

 ```python
 # Compose 源码：
 def __call__(self, img):
     for t in self.transforms: # t是每一个操作 
         img = t(img) # 对Image对象处理 
         return img 
 ```







## 训练框架

一般的训练框架

```python
'''
训练多个epoch 每个epoch分多个batch覆盖一次训练集
loss为整个epoch求和 
'''
import torch 
import torch.nn as nn # 神经网络相关
import torch.optim as optim # 优化器相关

## data preprocess 数据预处理 
# 数据归一化 分割数据集……
# 可以定义dataset dataloader 

## mdoel init
# 定义模型 初始化模型参数 
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        pass
    
    def forward(self,x):
        pass 
    
net=Net()
    
# optimizer and criterion device 
# 定义优化器 和 损失函数  计算设备cpu/gpu

optimzier=opt.Adam(net.parameters())
criterion=nn.CrossEntry()
device='cuda' if torch.cuda.is_available() else 'cpu' 

# train and test
# 训练 一般是每几个epoch就在验证集/测试集上测试
for epoch in range(1,epochs+1):
    loss=0
    for x,y in train_loader:
        out=model(x)
        loss=criterion(out,y) 
        optimizer.zero_grad()
        loss.backward() # 每个batch更新一次
        optimizer.step()
    
    if epoch % print_every == 0:
        # test here
        print('epoch:{} loss:{} acc:{}'.format(epoch,loss,acc))
        
```



# 梯度

## 梯度下降

几何上讲，梯度就是函数变化增加最快的地方，反之，负梯度就是函数下降最快的方向。

梯度确定了损失函数下降的方向，下降幅度取决于步长（学习率 learing rate）。学习率作为超参数，步长过长，迭代容易越过最优点导致发散，步长过小，迭代周期变长。



梯度下降法：现有m个样本点，每一个样本是n维特征向量，欲求取梯度向量：

* 普通梯度下降：计算每一个样本的梯度，求平均，准确但是费时
* 随机梯度：随机取其中一个样本的梯度，计算快速但下降不够平滑 
* 小批量梯度下降：折中上述两种方法，取一个小批量样本的梯度，求平均 



### SGD

随机梯度下降算法，带有动量（momentum）的算法作为一个可选参数可以进行设置，样例如下

```python
#lr参数为学习率，对于SGD来说一般选择0.1 0.01.0.001，如何设置会在后面实战的章节中详细说明
##如果设置了momentum，就是带有动量的SGD，可以不设置
optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
```

### RMSprop

除了以上的带有动量Momentum梯度下降法外，RMSprop（root mean square prop）也是一种可以加快梯度下降的算法，利用RMSprop算法，可以减小某些维度梯度更新波动较大的情况，使其梯度下降的速度变得更快

```python
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01, alpha=0.99)
```

### Adam

Adam 优化算法的基本思想就是将 Momentum 和 RMSprop 结合起来形成的一种适用于不同深度学习结构的优化算法。大多数时候，选用Adam即可。

```python
# 这里的lr，betas，还有eps都是用默认值即可，所以Adam是一个使用起来最简单的优化方法
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-08)
```



## 学习率调度器

调度器`StepLR`的作用，就是每隔一定步长数衰减一次学习率`lr=lr*gamma` ，步长会在每次调用调度器的时候自增。



```python
# Assuming optimizer uses lr = 0.05 for all groups
# lr = 0.05     if epoch < 30
# lr = 0.005    if 30 <= epoch < 60
# lr = 0.0005   if 60 <= epoch < 90
# ...

import torch.optimizer as optim

# 初始化一个调度器 每隔30步 就将学习率衰减为0.1 倍 
optimizer = torch.optim.SGD(model.parameters(), lr=LR) # 优化器 
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1.0, gamma=0.1) # 调度器 
for epoch in range(100):
    train(...)
    validate(...)
    scheduler.step() # 步数+1 
```

## 梯度消失 

在深层神经网络中，反向传播的连乘计算可能会导致梯度消失。 例如，激活函数`sigmoid`的导数图像如下：$|\sigma'|<1$ ，层数增多时，小于1的值不断相乘，最后就导致梯度消失的情况。反之，大于1的值不断相乘，就会导致梯度爆炸。 

<img src="../md_assets/image-20210913164408862.png" alt="image-20210913164408862" style="zoom:50%;" />

梯度消失的典型情况发生在rnn，在循环神经网络中，当前时间步t的隐藏态`ht`依赖于前面`t'<t`的所有时间步，如下：

在`t-T`这几个时间步里，每一个时间步，都会用到隐藏态`ht`，当时间步T变大时，指数效应会导致梯度衰减和爆炸。 

<img src="../md_assets/image-20210913164815564.png" alt="image-20210913164815564" style="zoom:67%;" />





梯度衰减的应对措施：

* 改用其他网络结构：gru/lstm
* 改用relu函数：它在大于0的函数部分导数是常数1 ，因子1不会造成衰减或爆炸 
* batchnorm/laynorm 平滑loss曲面 





## 梯度裁剪/爆炸 

在循环神经网络中，时间步过长时，容易引发梯度爆炸、梯度消失问题，简单理解，可以用公式$W^{length}$ 描述，当length较大时，w<1，容易进入梯度消失区域，w>1，容易进入梯度爆炸区域。



梯度爆炸的应对措施就是梯度裁剪 ，根据L2范数将梯度裁剪到合适的步长。 

```python
loss.backward()

# 梯度裁剪 根据L2范数 
# 裁剪在 反向传播之后 参数更新之前 
clip=50.0
torch.nn.utils.clip_grad_norm_(model.parameters(), clip)

optimizer.step() 
```

<img src="../md_assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0NzY5MTYy,size_16,color_FFFFFF,t_70.png" style="zoom:50%;" />





梯度消失的应对措施是改善网络结构，用gru\lstm代替简单的rnn 

## 丢弃法 

丢弃法，指的是在前向传播过程中，通过将其置0的方法随机丢弃一些隐藏单元，使模型不过分依赖于某几个神经单元，是一种应对过拟合的方法。 

![](../md_assets/3.13_dropout.svg)



假设丢弃概率为p，为了使丢弃后的权重期望值不变，对那些不丢弃的要做相应的比例变化$h=\frac{h}{1-p}$。分子随机变量的期望是 $E=0*p+1*(1-p)=1-p$  

<img src="../md_assets/image-20210906093644935.png" alt="image-20210906093644935" style="zoom:50%;" />



丢弃只应当在训练过程中进行，在测试阶段，应该关闭丢弃法。 

```python
# nn.Droupout(prob) 即可得到一个丢弃层 
# 靠近输入端的丢弃概率应该小 随后变大

net = nn.Sequential(
        nn.Linear(num_inputs, num_hiddens1),
        nn.ReLU(),
        nn.Dropout(0.1),
        nn.Linear(num_hiddens1, num_hiddens2), 
        nn.ReLU(),
        nn.Dropout(0.5),
        nn.Linear(num_hiddens2, 10)
        )

# 模型关闭开启丢弃模式 
model.train() # 训练模式 
model.eval() # 评估模式
```

## Normalization

归一化，即标准化$x=\frac{x-\mu}{\sigma}$ ，对数据进行归一化被证明可以使模型的梯度下降更加平稳 。**归一化操作发生在激活函数前**。 

从归一化的数据集选取来看，可以分为

* batch_norm： 选择同一个batch的数据作为 统计量 计算的范畴
* lay_norm ：选择同一个层的数据 作为 统计量 计算的范畴

所谓，统计量，指的就是上述的均值$\mu$、方差$\sigma$  。



batch_norm：同一个神经元（特征向量的某一个维度）上统计量的计算，参考一个batch中的其他样本。 

<img src="../md_assets/v2-b4818768a18f17a11d5e1b672426b31e_1440w.jpg" alt="img" style="zoom: 50%;" />



batch_norm的问题：

* 当batch过小时，会存在噪声问题，就是刚好噪声掩盖了正常的样本，使得归一化出现偏差  
* 一个batch内样本可能是不等长的，例如rnn的输入就会有填充`PAD`的问题，batch_norm就解决不了，改用laynorm。

****

laynorm：在同一层上的神经元进行归一化，相当于特征向量以自身维度为数据范围，进行归一化。 适用于循环神经网络RNN。

<img src="../md_assets/v2-2d38ab1541713bfc6bdfc95f0bfe09de_1440w.jpg" alt="img" style="zoom: 50%;" />

****

 

# 卷积神经网络

卷积神经网络由一个或多个卷积层和顶端的全连通层组成，可以有效提取数据的局部特征，在图片分类领域取得巨大成功。

## 卷积层

![img](https://gitee.com/jiang_hui_kai/images/raw/master/img/9.gif)

卷积层会定义一个权重矩阵，称为卷积核`kernal`，大小一般为`3*3`、`5*5`。

卷积核在输入上滑动，每滑动一次，就对覆盖区域加权求和，作为输出的一项。

输出大小的矩阵计算如下：$\frac{n-k+2p}{s}+1$ ，n是输入矩阵大小，k是卷积核尺寸，p是padding填充的大小（只算1边），s是卷积核每次移动的步长。

通常，会设置多个卷积核，每个核有不同的权重矩阵，相当于用多种不同的方式提取了特征。 

```python
# out_channels=10 表示进行10个卷积核特征提取
nn.Conv2d(in_channels=1,out_channels=10,kernel_size=5)
```

### 卷积核尺寸与通道

卷积核都是二维的，**默认其中一个维度等于输入通道数`in_channels`**，另外一个维度也就是给定的`kernel_size`。  当卷积核滑动时，每次都会计算所有通道内的数据，然后加权求和该次感受野内的数据，得到一个数。而最后，有多少个`out_channels`，就决定了最终的通道有多少。**简言之，新图像的大小，在滑动方向上，要依靠卷积核大小公式计算，而在通道数上，可以理解为简单映射。**

例如，`227*227*3`的彩色图像，经过一个卷积核大小`11*11*3`、步长为4的计算时，首先在长宽上，卷积核滑动，$\frac{227-11}{4}+1=55$，得到`55*55` 的大小。当卷积核只有1个时，就只进行1次运算，得到大小为`55*55*1`。类推可得，当卷积核个数为`out_channels`时，大小为`55*55*out_channels`。

## 池化层

池化层可以简化卷积层的输出，相当于一个过滤器。池化层不需要padding填充，输出矩阵的大小为$\frac{n-f}{s}+1$  

```python
import torch.nn.functional as F 
F.max_pool2d(x,2,2) # 池化层2*2 输入为x 矩阵 
```



## dropout层

防止过拟合的一种手段。在模型训练过程中，按照一定的概率将部分神经网络暂时丢弃，也就是尝试找到一个更瘦的网络。

## 全连接层

作为最后的输出层。卷积的作用是提取特征，这样得到的特征矩阵是2维的。在传入全连接层之前需要对特征进行展平操作，变成1维的。

```python
x=x.view(-1,chanel*h*w) # 前面-1表示自动计算 ，有时候不足一个batch很好用
x=self.fc(x)
```



## conv1d 

参考：https://blog.csdn.net/sunny_xsc1994/article/details/82969867 

1维卷积核适合词向量运算，词向量维度作为输入通道，序列长度作为卷积核滑动方向。

例如，现有数据`batch,seq_len,embed_dim`，卷积核大小为`m`，则该卷积核实际大小为`m*embed_dim`（第二个维度是通道数目），则新的数据大小为`batch,?,out_channels` ，`?`表示该方向上需要卷积核滑动计算。

**一种特殊情况是，当`m=1;out_chaneels=in_channales`时，退化为一个线性层计算，**`nn.Linear(in_channels,in_channels)`。 



下图中，输入数据为`7*5`，红色的第一个卷积核大小为`4*5`，则滑动的序列变化为$\frac{7-4}{1}+1=4$，  大小为`4*1`，经过最大池化后，变成标量`1*1 `。

<img src="../md_assets/70.jpeg" style="zoom:50%;" />



## 经典模型

经典模型：

* **LeNet-5**，1998年，卷积网络开山之作
* AlexNet，2012年，`torchvision.models.alexnet(pretrained=False)`
* VGG，2015年，`torchvision.models.vgg16(pretrained=False)` 
* GoogLeNet ，2014年 
* ResNet，2015年，残差网络  





![img](https://gitee.com/jiang_hui_kai/images/raw/master/img/cnn.png)

小型图片分类任务，resnet18基本上已经可以了，如果真对准确度要求比较高，再选其他更好的网络架构。



# 循环神经网络

RNN名为循环神经网络，擅长处理序列信息，背后的想法是模拟人的记忆。

循环神经网络的核心思想就是：**当前输出不仅取决于当前输入，还取决于历史信息。** 试想，如果没有后半句，那`<输入-输出>`就是孤立的，和普通的函数拟合没有两样。

输入x之间应当存在前后关系，输出y之间也存在关系。RNN网络在计算时，虽然假设了y是彼此条件独立的，但实际过程中，$y_t$ 同时取决于 $x_t$ 和 $H_{t-1}$ ，所以也可以认为，考虑了y是彼此有关的。

分析两个例子，来理解RNN对输入的处理：

* 语言生成，预测下一个字符 ：用$x_t$来预测$x_{t+1}$ 
* 相同区间上，通过sin预测cos：直觉上，cos和sin是有直接的函数关系的，但是孤立地考虑，用深度神经网络拟合可能要求复杂的结构。如果使用RNN，结合 历史输入$sin(0),...,sin(t-1)$ 和当前输入 $sin(t)$ 无疑是增加了特征信息，能够更好预测$cos(t)$ 。这里，$cos(t)$ 事实上应该和 它自己的过去 $cos(0),...,cos(t-1)$ 有关联，**即y之间存在关系，但前面说过，y被假设为彼此独立**，所以由输入的历史信息（被转为隐藏状态$H_{t-1}=f(sin(0),...,sin(t-1))$）联系。

## RNN

RNN对每个时间步的处理步骤是相同的，接受当前输入、上一个隐藏状态，如此循环，直至处理完所有序列，这就是“循环”的意思。 



每个记忆单元做的事情可以简化为以下公式：

$H_t=\phi(X_tW_{xh}+H_{t-1}W_{hh}+b)$ 





<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/循环神经网络结构.png" alt="image-20210204203138257" style="zoom:50%;" />



循环网络 文本生成-预测字符 示例：

![image-20210215110838378](https://gitee.com/jiang_hui_kai/images/raw/master/img/深度学习语言字符预测模型.pmg)

pytorch 中使用 nn.RNN 类来搭建基于序列的循环神经网络，它的构造函数有以下几个参数：

- input_size：输入数据X的特征值的数目。
- hidden_size：隐藏层的神经元数量，也就是隐藏层的特征数量。
- num_layers：循环神经网络的层数，默认值是 1。
- bias：默认为 True，如果为 false 则表示神经元不使用 bias 偏移参数。
- batch_first：如果设置为 True，则输入数据的维度中第一个维度就是 batch 值，默认为 False。默认情况下第一个维度是序列的长度， 第二个维度才是 - - batch，第三个维度是特征数目。
- dropout：如果不为空，则表示最后跟一个 dropout 层抛弃部分数据，抛弃数据的比例由该参数指定。



```python
rnn = torch.nn.RNN(20,50,2) # input hidden 
input = torch.randn(100 , 32 , 20)
h_0 =torch.randn(2 , 32 , 50)
# rnn 网络会返回两个结果 
# outpout batch seq_len hidden_size_out
# hn 最后一个隐藏状态  direction*lay batch hidden_size_out 
output,hn=rnn(input ,h_0) 
print(output.size(),hn.size())
```



手动实现RNN 

```python
class RNN(object):
    def __init__(self,input_size,hidden_size):
        super().__init__()
        self.W_xh=torch.nn.Linear(input_size,hidden_size) # 输入
        self.W_hh=torch.nn.Linear(hidden_size,hidden_size) # 隐藏层
        
    def __call__(self,x,hidden):
        return self.step(x,hidden) # 计算异步
    
    def step(self, x, hidden):
        #前向传播的一步
        h1=self.W_hh(hidden)
        w1=self.W_xh(x)
        out = torch.tanh( h1+w1) 
        return out, self.W_hh.weight
    
rnn = RNN(20,50)
input = torch.randn( 32 , 20)
h_0 =torch.randn(32 , 50) 
seq_len = input.shape[0]


# 时间步迭代
for i in range(seq_len):
    output,h_0= rnn(output[i, :], h_0) 
print(output.size(),h_0.size())
```




## LSTM

LSTM 是 Long Short Term Memory Networks 的缩写，1997年提出。 

<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/深度学习LSTM.png" alt="image-20210215122012318" style="zoom: 80%;" />



它的核心思想是：选择性地保留上一时间步的信息、选择性地融合当前时间步候选隐藏状态$\widetilde{h_{t}}$与上一时间步隐藏状态$h_t$。 为此LSTM引入了遗忘门f、输入门i、输出门o 三个参数 

<img src="../md_assets/image-20210906091749766.png" alt="image-20210906091749766" style="zoom:50%;" />

首先是候选隐藏层计算 

<img src="../md_assets/image-20210906092350593.png" alt="image-20210906092350593" style="zoom:50%;" />



遗忘门、输入门作为权重系数，施加到 对应时间步隐藏状态

<img src="../md_assets/image-20210906092424574.png" alt="image-20210906092424574" style="zoom:50%;" />



最后通过输出门得到当前时间步的隐藏状态 

<img src="../md_assets/image-20210906092502455.png" alt="image-20210906092502455" style="zoom:50%;" />





```python
lstm = torch.nn.LSTM(10, 20,2)
```



## GRU

<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/深度学习GRU.png" alt="image-20210215112334824" style="zoom:67%;" />



gru 进一步简化了LSTM，仅仅引入了 重置门r、更新门z两个参数。  sigmoid激活函数将两者控制在`(0,1)`范围内。

<img src="../md_assets/image-20210906091029115.png" alt="image-20210906091029115" style="zoom:50%;" />

重置门r，用于控制上一时间步$h_{t-1}$的信息流入 ，点乘可以丢弃与预测无关的历史信息（类似dropout） 

<img src="../md_assets/image-20210906091048688.png" alt="image-20210906091048688" style="zoom:50%;" />



更新门z，用于决定 如何融合 当前时间步的隐藏候选状态 和 上一时间步的隐藏状态 。当z接近1时，当前时间步候选隐藏状态近似被抛弃。 

<img src="../md_assets/image-20210906091219369.png" alt="image-20210906091219369" style="zoom:50%;" />





gru实例

```python
rnn = torch.nn.GRU(10, 20, 2)
```



## 深度循环神经网络

增加了隐藏层H的层数。

![image-20210215122516315](https://gitee.com/jiang_hui_kai/images/raw/master/img/深度循环神经网络.png)

## 双向循环神经网络 

深度双向循环神经网络  ，当前时间步隐藏状态分为前向隐藏状态、后向隐藏状态，最后连接传入输出层 

![image-20210215122715355](https://gitee.com/jiang_hui_kai/images/raw/master/img/深度学习双向循环神经网络.png)









# 自然语言处理

## 分词

### 词典分词

预定义词典，依照算法切割字符串匹配词典：

* 正向最长匹配分词、逆向最长匹配分词、双向最长匹配分词 
* 字典树： 叶节点作为一个词语的结束标记，从根开始遍历，寻找一条路径。



### 二元语法

语言模型：对语言的数学抽象 。



马尔科夫链用概率模型来考虑语言的生成，当前字符出现概率依赖前面出现的若干字符，$p(w_t|w_0...w_{t-1})$，n=1时为二元语法 ，常见的为1元、2元、3元。2元语法下，$p(s)=\Pi_{t=1}^{k+1}p(w_t|w_{t-1})$ 

当n取值过大时，会有以下问题：

* 数据稀疏，$p=\frac{count(w_0...w_t)}{count(w_0...w_{t-1})}$ ，很多片段在语料库根本不会出现。
* 计算量大，当序列变长的时候，每个分子分母计算都非常耗时 



用“平滑策略”来解决数据稀疏的问题，也就是用低阶n元语法来平滑高阶n元语法。以2元语法为例：

$p(w_t|w_{t-1})=\lambda p_{ML}(w_t|w_{t-1})+(1-\lambda)p(w_t)$ ，即使前一项概率为0，也能得到后面一项的概率支撑。lambda为常数平滑因子。



n元语法分词步骤：

1. 给定语料库 统计n元词 词频
2. 给定句子，构建词网
3. 利用维特比算法（也是一种路径算法），计算得到起点sos到终点eos的最长路径（最大可能）。

![image-20210326161134512](https://gitee.com/jiang_hui_kai/images/raw/master/img/image-20210313143643630.png)





## 序列标注

### 词性标注

词典分词的不足：OOV（out-of-bag） ，袋外词语难以召回 。将词语的颗粒度降为字符。分词转为序列标注问题。常见的标注方法为`BEMS`，词语首尾BE、词中Middle、单字词S 。

例如

```
参 观 了 北 京 天 安 门
B  E  S B  E  B M  E
```

单词的数量无穷，而词性有限**。借助词性可以猜测OOV的用法（结合`BEMS`标签）**，而不是将所有的OOV标记为`UNK`，混为一谈。

```
商 B 名词
品 E 名词
和 S 连词
服 B 名词
务 E 连词 
```

### 命名实体识别

命名实体： 描述实体的词汇，比如人名、地名、机构名等，在不同领域各取所需。 

**序列标注要也可以应用在命名实体**（现实存在的实体，人名、地名、机构名）。复杂的命名实体多是由短单位组合成长单位，可以将标注对象从字符扩大为词语，并附着属性标签。例如

```
参观 了 北京 天安门
O    O B-地名 E-地名
```

### 隐马尔可夫

隐马尔可夫模型HMM：两个时序序列联合分布的概率模型

* 观测序列`x` ：字符本身。隐态序列`y`：字符之间的隐藏关联状态 
* 状态转移概率矩阵：从$y_t$到$y_{t+1}$的`N*N`矩阵，N是所有隐藏状态。
* 发射概率矩阵：从$y_t$到$x_{t}$的`N*M`矩阵，N是状态总和，M是x总和。

![image-20210325092302895](https://gitee.com/jiang_hui_kai/images/raw/master/img/HMM)



HMM 假设人们说的话仅仅取决于一个隐藏的状态序列`BEMS`，这个假设不符合语言规律，捕捉到的语言特征有限 。

### 条件随机场



<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/机器学习模型谱系图" alt="1616584511249"  />





**根据建模的究竟是联合概率分布$p(x,y)$还是条件概率分布$p(y|x)$，派生出生成式模型与判别式模型。** 

常见的生成式模型$p(x,y)$：隐马尔可夫模型HMM、朴素贝叶斯模型、高斯混合模型GMM、LDA 

常见的判别式模型$p(y|x)$：线性回归、决策树、支持向量机SVM、k近邻、神经网络 





条件随机场（Condional Random Field，CRF）,给定输入随机变量x，求解条件概率$p(y|x)$的概率无向图。用于序列标注时，化为线性链（linear-chain）。

 相比于HMM，CRF能够提取的特征更加丰富，可以自由定义k个特征函数$f(x_t,y_{t-1},y_t)$ 用以提取特征，对每个特征函数赋予权重$w_k$，整个序列的分数$score(y_i|x)=\Pi_t^T {W*f(x_t,y_{t-1},y_t)}$ ，其中$W$是`k*1`的向量，在训练过程中会迭代更新。

在此基础上，遍历所有可能的标注序列y，对score进行归一化

条件随机场、特征函数通俗理解： https://zhuanlan.zhihu.com/p/104562658 



条件随机场与感知机比较：摘录自《自然语言处理入门》P210

感知机与条件随机场相同点：

* 特征函数相同
* 权重向量相同
* 打分函数相同
* 预测算法相同



**他们最大的不同点在于训练算法**，这是两者准确率差异的唯一原因：

感知机属于在线学习，每次参数更新只使用一个训练实例（`x_i`与`y_hat_i`）。**条件随机场则定义在整个数据集之上，每次参数更新都是全盘考虑。**



在机器学习中，若权重向量的范数太大，意味着模型对自己的判断太过自信，会导致模型过拟合，**丧失泛化能力。常用的手段是正则化——让对数似然函数减去范数**，对那些范数较大的模型施加惩罚。$e=e-\frac{w}{2\sigma^2}$，$\sigma$作为惩罚项控制惩罚力度。



## 信息抽取

### 新词提取

给定一段文本，随机取一个片段，如何判断这个片段是否是一个词语：**互信息、信息熵** 



左右信息熵：**$H(x)=-\sum_x p(x)log{p(x)}$**，衡量片段的左右搭配是否丰富，如果是，那么该片段很有可能就是一个词语

互信息：$I(X,Y)=\sum_{x,y} p(x,y)log{\frac{p(x,y)}{p(x)p(y)}}$，衡量片段内部的搭配是否固定 。互信息越大，两个随机变量的关联就越密切。

统计一个语料库，可以计算某个片段的上述两项指标。例如

> 两只 蝴蝶 飞呀飞
>
> 这些 蝴蝶 飞走了 

“蝴蝶”的左右组合有`{只，些，飞}`，“蝴蝶”两个字的互信息统计整个语料库分别计算“蝴”、“蝶”的字频，同样可以计算。

### 关键词提取

关键词的定义标准不一，很难用有监督学习训练。这里介绍几个无监督学习。

#### 词频统计

关键词通常在文章中反复出现。

词频统计的流程一般是：分词、停用词低频词过滤、按词频取前n个。

#### TF-IDF

词频-倒排文档索引。词频统计的缺陷：出现频次高的不一定是关键词，也有可能是领域的共性词语。

$TF-IDF=\frac{TF(t,d)}{DF(t)}=TF(t,d)*IDF(t)$ ，t代表单词term，d代表文档document。

公式的含义也就是：**一个词的重要程度与它在文章中的频次成正比，与文档包含该词的频次成反比。** 

#### TextRank

TextRank是PageRank在文本上的应用。

pagerank是一种网页排序算法，它的工作原理是将网页看做有向图，网页视作节点，节点之间的链接视作有向边。每个节点的权重都是1，以迭代方式更新，迭代权重更新表达式：

$S(V_i)=(1-d)+d*\sum _{V_j\in In(V_i)}\frac{S(v_j)}{|Out(v_j)|}$ 

$V_i$是节点，d是0-1之间的常数因子，$In(V_i)$表示节点的入边节点集合，$Out(v_j)$表示节点的出边节点集合。

上述公式表示，一个网站给别的网站做的链接越多，每条外链的权重就越低$\frac{1}{Out}$ ，与每条外链本身的权重成正比$S(v_j)$ 。物以类聚，与垃圾网站交换的往往也是垃圾网站。pagerank捕捉到的刚好是这一点。



![image-20210326085401347](https://gitee.com/jiang_hui_kai/images/raw/master/img/image-20210330085731104.png)



## 文本向量化 

将文本表示成向量，作为特征抽取的输入。 

文档的向量表示：

* 词袋模型： 文本由若干词语组成，`[w1,...,wn]`，**出现的词语统计词频**，最后得到`1*voc.nums`大小向量。这种方法简单，但是无词序，损失了部分语义。比方说，“人吃鱼”、“鱼吃人”会得到相同的向量表示。另外，**词频不是唯一指标，可以是tf-idf值，或者词向量本身。** 

  词袋模型中词语的过滤：有些词语没有实际意义，不适合作为特征，如英语的the、汉语的“的”

  * 停用词词典
  * **卡方特征**（有监督 文本分类）：摘录自P309（卡方、期望、置信度）。卡方检验常用与检验两个事件的独立性。将词语的出现与类别的出现作为两个随机事件，**类别独立性越高，越不适合作为特征**。



无监督的文本聚类算法无法学习人类的偏好对文档进行划分，也无法学习每个簇的意义（标签）。 





## 依存句法分析

语法分析：分析句子的语法结构并将其表示为树形结构 。

上下文无关文法（《编译原理》有讲过）：形式化地描述文法产生规则。终结符、非终结符、推导规则。

### 短语结构树

关注如何用语法生成句子  ![image-20210326151418770](../better/resources/image-20210326151418770.png)



### 依存句法树

依存句法树不关注如何产生句子，**而是句子中词语之间的语法联系**，并将其约束为树形结构。



修饰词、支配词：如果一个词语修饰了另外一个词，被修饰的词语称作“支配词”（修饰词语是为它服务的），修饰的词语称作“修饰词”。

![image-20210326153247941](../better/resources/image-20210326153247941.png)





## 深度学习的破局

**通过海量无标注样本的无监督训练自动抽取事物特征**，然后在相对少量的标注样本上进行微调，神经网络展现出强大的迁移学习能力。 

### 传统机器学习的局限

#### 数据稀疏

将离散符号转为向量作为机器学习的输入，一般采用独热编码（one hot）。所谓的独热编码（常见的是按照词典序编码），就是在n维向量中，只有1个维度为1，其余为0，形如`[0,...1,0...]`，彼此正交。**这样的向量维度庞大，数据稀疏，而且，词义上相近的两个词语，在向量上可能完全不搭边。**



**我们希望任意单词都能表示为具有合理相似的向量，那么OOV的问题就不复存在，因为模型看到的这个向量，必定和训练集中的某个向量存在较高的相似度，模型就能将其归为相似单词处理。这种技术在深度学习中被称作“词嵌入”**。



这来源于一个矛盾，**一方面，高级的NLP任务需要复杂的特征。另一方面，特征模板越复杂**，数据就会越稀疏，例如，一个特定单词很常见，两个组合的单词频率就会大幅降低，三个单词的组合更是如此，那些出现概率极低的组合在统计学上没有任何作用。

另外，在某些特定领域，比如电商、医疗，特征模板的抽取需要人们具备一定的专业知识。

#### 误差传播

传统的机器学习在自然语言处理上是一种流水线的作业，分为很多环节，分词、词性标注、停用过滤词、特征筛选（例如卡方检验）、送入分类器分类。

**这种流水线作业会造成严重的误差传播，前一个环节如果出错，后面的环节就会将错就错**。比如，“质量不过关”，错误地被分成“质量 不过 关”。

### 神经网络

**在深度学习中，特征模板抽取被多层感知机代替，这正是深度学习的精髓。** 

简单地理解，**可以将神经网络看做一个多元的非线性函数`f(x1,x2,...)`，输入是特征向量，输出另一个特征向量h，**其中h的每一维都是原始特征的若干次组合重构（从矩阵乘法的角度考虑）。

#### 稠密向量

神经网络输出的新特征h的长度是可以控制的，可以将h设定的较短（稠密向量），**这样子就实现了从高维向量到低维向量的转变，低维向量在空间上会拉近很多，彼此的相似度就容易体现**。

#### 特征自动抽取

神经网络两层之间一般为全连接，不需要根据具体问题来调整连接方式。**网络会自动根据损失函数的梯度来确定隐藏层的权重矩阵，从而自动学习到事物的特征表示。**

#### 端到端的设计

神经网络层之间、网络之间采用的都是统一的向量”语言“，这就很适合多个网络的组合，形成一种端到端的设计。

深度学习兴起之后，传统机器学的每一个环节都可以被（使用同一个损失函数的）神经网络取代，并且在误差传播方面取得更好的效果。

## word2vec

w2c：训练词向量的一种神经网络 



w2c分为跳字模型skip-gram 、连续词袋模型CBOW 

* 跳字模型skip-gram：由中心词$w_c$确定背景词 $w_o$

  ![image-20210131115856638](../better/resources/跳字模型梯度计算公式.png)

* 连续词袋模型CBOW：背景词确定中间词，利用中间词训练背景词。用背景词向量表征词 



跳字模型的梯度计算优化：更改损失函数 

* 初始损失函数计算不足：遍历词典
* 负采样，加入k个噪声词，时间复杂度与k相关

* **二次采样**：对无意义高频词概率丢弃，如the  ；过滤生僻词（出现频率低于阈值）



w2c 词向量的应用：

1. 词嵌入，作为词语表征
2. 词语聚类，利用余弦相似度来寻找近义词，更准确的说法应该是相关词，因为w2c在训练过程中是用上下文训练。一起在上下文出现的词语不一定是近义词，如美丽-丑陋。  



## glove

glove从另一种角度对跳字模型建模 ，表示的损失函数不同。

* 多重集计算需要预先知道语料的全局信息 。**多重集**，一个中心词在文本不同处的背景窗口词语的包含重复词的集合，可以理解为该中心词下可能生出的背景词集合（word2vec是考虑整个词典）
* 每个词的词向量是中间词+背景词向量之和。中间词与背景词等价（多重集对称）。
* glove模型表示词的相似度 
* 求近义词和类比词 b-a=d-c ,b类似于a犹如d类似于c ，`beijing:china :: tokyo:japan `
* glove训练模型命名规范：`模型.数据集(billion十亿).词向量维度（xxdimension）` ，如glove.30b.300d  



## 编码器-解码器 seq2seq

当输入输出是不定长的序列时，如机器翻译、问答聊天等，可以使用seq2seq模型。seq2seq 模型 的架构一般是encoder-decoder两个网络连接起来。

encoder编码器，负责将文本编码成背景向量（context vector），存储上下文语义信息。

decoder解码器，解码背景向量，按时间步迭代，每次解码一个字符。之所以按时间步迭代，是因为解码过程中，当前时间步的解码也需要上一个时间步的解码输出。

它们的计算图（RNN为例）如下：  

![image-20210305152826866](https://gitee.com/jiang_hui_kai/images/raw/master/img/seq2seq) 



 eos、bos作为特殊字符，插入到句子的用意如下：

* eos：end of sentence，表示句子的结束，当解码器解码得到eos时，可以认为已经解码结束了 
* sos/bos：start /begin of sentence，表示句子的开始， 解码器的初始状态需要一个字符来启动解码。 



### 编码器 

在理解编码器前，应该理解torch中`Gru`的一些信息 

`class Gru()` ：

* 初始化：

  * input_size：输入的特征维度 ，一般是 词嵌入维度`embedding_dim`
  * hidden_size：隐藏单元的特征维度 
  * num_layers：层数 
  * batch_first：第一维度是否是batch 
  * dropout：随机丢弃神经单元 
  * bidirectional：是否双向 

* 输入 ：

  * `input`：可以是张量 `seq_len,batch,in_feature`  ，**也可以是一个package对象（用函数打包）。** 
  * `hx`： gru网络的初始隐藏状态  ，如果为`None`  ，默认为0矩阵 ；在按时间步迭代的循环神经网络中，hx参数很有必要 

* 输出 ：

  * out：`seq_len,batch,hidden_size*direction` ，每个时间步的隐藏状态，如果是双向的，会拼接。 **如果要实现相加**，可以手动实现 `out[:,:,:hidden_size]+out[:,:,hidden_size:]` 

    另，当网络输入是`pack`对象时，out 是需要手动解包的。 

    ```python
    # max_len,batch,hidden_size*direction ;第2个返回结果len是我们不需要的
    outputs, _ = nn.utils.rnn.pad_packed_sequence(outputs)

  * hidden：`direction*nlayer,batch,hidden_size` ，最终时间步的详细隐藏状态（各层各个方向），可以用于另一个gru的隐藏状态初始化。 

  





上文中多次提及的`pack`打包，是因为在gru输入时，**并不是句子的所有字符都是有意义的**，有一些会为了长度对齐`max_len`而填充上`<PAD>`填充符

```python
# data：List<str> 若干输入序列 
# zip_longest 和 zip拉链函数相似 都是对多个迭代序列整合 
# 只不过 zip_longest 是取最长序列作为标准 短的用fillvalue填充 
# zip 是取最短序列作为标准 长的截断 
# 另外 zip_longest 将会隐式地将 batch*max_length 转为 max_length*batch 
from itertools import zip_longest
def zero_padding(self, datas, fillvalue=PAD_TOKEN):
    fillvalue = self.voc.stoi[fillvalue]
    return list(zip_longest(*datas, fillvalue=fillvalue))
```

![img](../md_assets/seq2seq_batches.png)



这当中，填充字符`<PAD>`显然无意义，没必要参与计算。 所以一个gru正确的输入输出形式是这样的

```python
x = self.embedding(x)  # max_len,batch ==> max_len,batch,voc_size
pad_x = nn.utils.rnn.pack_padded_sequence(x, length, enforce_sorted=False) # 打包 最后的关键字参数表示无序序列
outputs, hidden = self.gru(pad_x)  # hidden是最后时间步的隐藏态
# max_len,batch,hidden_size*direction ;第2个返回结果len是我们不需要的
outputs, _ = nn.utils.rnn.pad_packed_sequence(outputs) # 解包
```

关于 `pack_padded_sequence` 的详细用法参考官网：https://zhuanlan.zhihu.com/p/34418001  ，简言之，压缩每一个时间步的非填充字符成一维向量。 

官网例子 

```python
>>> from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
>>> seq = torch.tensor([[1,2,0], [3,0,0], [4,5,6]]) # batch,max_len 
>>> lens = [2, 1, 3]
>>> packed = pack_padded_sequence(seq, lens, batch_first=True, enforce_sorted=False)
>>> packed
PackedSequence(data=tensor([4, 1, 3, 5, 2, 6]), batch_sizes=tensor([3, 2, 1]),
               sorted_indices=tensor([2, 0, 1]), unsorted_indices=tensor([1, 2, 0]))
>>> seq_unpacked, lens_unpacked = pad_packed_sequence(packed, batch_first=True) # 恢复信息 
>>> seq_unpacked
tensor([[1, 2, 0],
        [3, 0, 0],
        [4, 5, 6]])
>>> lens_unpacked
tensor([2, 1, 3])
```

 





编码器 

```python
class EncoderRNN(nn.Module):
    def __init__(self, embedding, input_size, hidden_size, nlayers=2, dropout=None):
        super().__init__()
        self.embedding = embedding
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size=input_size, hidden_size=hidden_size, num_layers=nlayers,
                          bidirectional=True,
                          dropout=dropout if dropout else 0)

    def forward(self, x, length):
        x = self.embedding(x)  # max_len,batch ==> max_len,batch,voc_size
        pad_x = nn.utils.rnn.pack_padded_sequence(x, length, enforce_sorted=False)
        outputs, hidden = self.gru(pad_x)  # hidden是最后时间步的隐藏态
        # max_len,batch,hidden_size*direction ;第2个返回结果len是我们不需要的
        outputs, _ = nn.utils.rnn.pad_packed_sequence(outputs)
        outputs = outputs[:, :, :self.hidden_size] + outputs[:, :, self.hidden_size:]  # 拼接前后向
        return outputs.to(DEVICE), hidden.to(DEVICE)
```



### atttention机制 

attention机制即是权重计算机制，$\sum f(q,k)v=\sum \alpha*v$ ，目标就是生成一系列的 权重系数 `alpha` 



用 融入注意力机制的encoder-decoder 模型来解释： 

<img src="../md_assets/image-20210305154438109.png" alt="image-20210305154438109" style="zoom:50%;" />

参与到每个时间步计算的背景向量应该是可变的，这符合直觉。 如何计算可变背景向量？答案是利用 注意力机制。 

令当前解码器的隐藏状态为q 查询向量， 编码器的各个时间步隐藏状态为k 应答向量， 计算它们的相关性（点积），最后进行softmax运算，即可得到一系列`(0,1)`的权重系数 。 



```python
class Attention(nn.Module):
    def __init__(self):
        super().__init__()

    def dot_score(self, hidden, context):
        # context :max_len,batch,hidden_size, hidden:batch*hidden_size
        # broadcast 广播点乘 ==> max_len,batch,hidden_size  在hidden_size维度上求和（点积）
        score = torch.sum(hidden * context, dim=2)  # max_len,batch,hidden_size ==> max_len,batch
        # 在max_len 维度上进行softmax运算 为每个时间步分配不同权重 
        power = F.softmax(score, dim=0).unsqueeze(dim=2)  # max_len,batch,1 ,最后添加1维是为了和context 广播点乘
        # context(max_len,batch,hiddens_size) 得到powr以后 运算如下 
        # weighted_context= torch.sum( context * power,dim=0) # batch*hidden_size 
        return power

    def forward(self, hidden, context):
        return self.dot_score(hidden, context)
```

### 解码器 

解码器的输入 应该包含：

* context ： （可变的）编码器的背景向量  
* y：上一个时间步的输出，是一个概率分布`batch,voc_size`  
* $h_{t-1}$ ：上一个时间步的隐藏状态`direction*layer,batch,hidden`，用于初始化当前时间步的模型隐藏层



```python
class DecoderRNN(nn.Module):
    def __init__(self, embedding, attention_layer, hidden_size, nlayers=2, dropout=None):
        super().__init__()
        self.embedding = embedding
        self.attention_layer = attention_layer
        self.hidden_size = hidden_size

        self.gru = nn.GRU(input_size=embedding.embedding_dim,
                          hidden_size=hidden_size,  # 解码器的隐藏单元大小和编码器相同
                          num_layers=nlayers,
                          dropout=dropout if dropout else 0)
        # 对 gru的输出进行分类 是2个线性层 
        self.concat = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),  # batch,hidden_size*2 ==> batch,hidden_size
            nn.Tanh(),
            nn.Linear(hidden_size, self.embedding.num_embeddings)  # batch,hidden_size ==> batch,voc.size
        )

    def forward(self, x, last_hidden, encoder_out):
        x = self.embedding(x)  # 1,batch ==> 1,batch,embedding_size
        # gru_out:1,batch,hidden_size,hidden:layer*direction*hidden_size
        gru_out, hidden = self.gru(x, last_hidden) 
        # 可变背景向量
        power = self.attention_layer(gru_out, encoder_out)
        # max_len,batch,hidden_size 对时间步求和(dim=0)，==> batch,hidden_size
        weighted_context = torch.sum(power * encoder_out, dim=0)

        # 拼接 分类
        concat_input = torch.cat((weighted_context, gru_out.squeeze(0)), dim=1)  # batch,hidden_size*2
        out = self.concat(concat_input)  # batch,voc_size
        out = F.softmax(out, dim=1)  # batch,voc_size

        return out.to(DEVICE), hidden.to(DEVICE)
```



### 掩码损失 

在计算解码器的解码损失时，要注意，只应该计算 有效字符的交叉熵损失，过滤掉pad字符的计算。这需要借助mask矩阵。 

mask掩码矩阵用0-1保留了 标签的有效字符位置，填充符用0表示 （恰巧在交叉熵运算中此项归为0） 

```python
def mask_loss(predict, target, mask):
    # 计算一个时间步里的平均loss 因为解码器是按照时间步迭代的 
    # predict:batch,voc_size  target:batch  mask:batch
    # loss: batch*1  ;gather运算等同于交叉熵运算 取对应分类位置的 概率 然后log运算
    loss = -torch.log(torch.gather(predict, 1, target.view(-1, 1)).squeeze(1))
    loss = loss.masked_select(mask).mean() # 当前时间步的平均损失  
    return loss
```



按时间步迭代解码 并计算损失 

```python
encoder_out, encoder_hidden = encoder(input_data, length)

# 初始化sos 
decoder_input = torch.LongTensor([voc.stoi[SOS_TOKEN]] * batch_size).view(1, -1).to(DEVICE)  # 1*batch
last_hidden = encoder_hidden[:decoder_layer]  # 这里要考虑encoder 与 decoder 之间结构的差异

loss = 0
for t in range(max_length):  # 解码器一次解码一个时间步 max_length是batch中最长时间步 
    decoder_out, last_hidden = decoder(decoder_input, last_hidden, encoder_out)
    decoder_input = torch.max(decoder_out, dim=1)[1].view(1, -1)  # 1*batch
    # loss 计算 decoder_out:batch,voc_size  target_data:max_len,batch mask_matrix:max_len,batch
    # 索引[t]表示t取时间步的数据 
    loss += mask_loss(decoder_out, target_data[t], mask_matrix[t])
loss.backward()
```



### 贪婪搜索 

在实际使用decoder 模型时，解码器应该按照一定的策略来输出若干字符，作为 解码序列 。最简单的一种策略就是 贪婪搜索 ，所谓 贪婪搜索，就是在每次时间步都选择当下 概率最大的 字符，而忽视整个 序列的连贯可能。 



在贪婪搜索下，解码器的输出如下 ：

```python
for _ in range(max_length):
    # decoder_out: 1*voc_size
    decoder_out, last_hidden = decoder(decoder_input, last_hidden, encoder_out)

    score, token = torch.max(decoder_out, dim=1)  # max得到概率 和 对应位置 索引 
    if token.item == voc.stoi[EOS_TOKEN]: break

        all_scores.append(score)
        all_tokens.append(token)
        decoder_input = token.unsqueeze(0)  # 1*batch 整理成这种格式是为了和下一个时间步输入统一 
        return all_scores, all_tokens
```





### 束搜索

对贪心策略改进的一种候选字符选择算法。

解码器每一步骤输出概率预测，如果选用 贪心策略，虽然每一时间步都输出最大可能字符，但整体概率（条件概率，字符之间并非独立出现）并不一定最大。即贪心策略不能保证得到整体最优输出。

束搜索是对贪心策略的改进，每一次选择概率最大的n个候选词（n是超参数，束宽）送到下一时间步，直到字符中包含eos。

<img src="https://gitee.com/jiang_hui_kai/images/raw/master/img/image-20210305153452558.png" alt="image-20210305153452558" style="zoom:50%;" />



为了避免序列越长得分越高，最终计算分数时，添加一个计算因子，用于抑制序列长。$score=score/L$



## Transfomer

参考：

* 博客：图解transfomer  https://jalammar.github.io/illustrated-transformer/  
* csdn：transofmer源码解读 https://blog.csdn.net/zhaojc1995/article/details/109276945 

transofmer 的整体架构 属于 encoder-decoder 模型  

![image-20210830162139036](../md_assets/image-20210830162139036-16312439400921.png)

### encoder 

encoder 由6层 encoder_layer堆叠  ，每一层`encoder_layer`又由两个子网络构成：

* multi-head attention ：多头注意力机制 
* FFT：两个线性层组成的 前馈神经网络

层与层之间采用残差连接。  

<img src="../md_assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpdWdlMTk4NjA5MjA=,size_16,color_FFFFFF,t_70.png" alt="img" style="zoom:67%;" />

#### pos_embed

transformer改变了rnn网络循环计算的结构，采取并行计算，为了保存token之间的位置信息，设计出了`pos_embedding`。

`pos_embedding `和 输入词向量同维度大小`max_len,dmodel` ，使用正弦函数来保存token的位置信息。   

同一个position，不同维度，有不同频率、不同相位（正余弦差$\pi/2$）的正弦波；同一个维度位置，用position区分。

![image-20210830180352557](../md_assets/image-20210830180352557-16312442324433.png)



位置向量示意图 

<img src="../md_assets/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3poYW9qYzE5OTU=,size_16,color_FFFFFF,t_70#pic_center.png" alt="img" style="zoom:50%;" />



代码实现

```python
class PositionalEncoding(nn.Module):
    def __init__(self,
                 emb_size: int,
                 dropout: float,
                 maxlen: int = 5000):
        super(PositionalEncoding, self).__init__()
        # 换底公式 m**a = exp(a*ln(m)) 
        den = torch.exp( -math.log(10000) * (torch.arange(0, emb_size, 2) / emb_size) ) 
        pos = torch.arange(0, maxlen).reshape(maxlen, 1)  # max_len,1 
        
        pos_embedding = torch.zeros((maxlen, emb_size))
        pos_embedding[:, 0::2] = torch.sin(pos * den)  # 2i,max_len ,embed_siz/2
        pos_embedding[:, 1::2] = torch.cos(pos * den)  # 2i+1 
        pos_embedding = pos_embedding.unsqueeze(-2) # 1,max_len,dmodel

        self.dropout = nn.Dropout(dropout)
        # 注册为buffer 表示不需要在反向传播时更新 但是需要作为状态保存 
        # 同时为模型增加了 self.pos_embedding 属性 
        self.register_buffer('pos_embedding', pos_embedding)  

    def forward(self, token_embedding: Tensor):
        # token + postion 混合
        return self.dropout(token_embedding + self.pos_embedding[:token_embedding.size(0), :])
```



#### self-attn 

使用自注意力机制计算一句话中token之间的相关性，然后累加求和。 

每一个token都对应了`query\key\value`三种向量，query和key用于点乘(dot product)计算注意力机制，然后作用于value上 。 

<img src="../md_assets/self-attention-output.png" alt="img" style="zoom:67%;" />

 



在实际计算时，使用矩阵来加速运算。对于每一次输入`x(seq_len,embed_size)` ，利用投影矩阵一次性得到他们的qkv。投影矩阵是随机初始化的，在训练过程中逐步更新参数。 

<img src="../md_assets/self-attention-matrix-calculation.png" alt="img" style="zoom:50%;" /> 



注意力计算公式$softmax(\frac{QK^T}{\sqrt{d_k}})V$，分母的$\sqrt{d_k}$ 作为比例因子，可以使梯度更新较为稳定。 

<img src="../md_assets/self-attention-matrix-calculation-2.png" alt="img" style="zoom:67%;" />



一次self-attn，如果看做黑箱操作的话，也只是一次特征提取操作`seq_len,dmodel ==> seq_len,dmodel` 。对于每一个特征向量，都考虑了彼此的相关性，作注意力计算然后融合成为新的特征向量。 



#### multihead

multi-head是多头的意思，每一个头进行一次`self-attn`运算。 使用多头的原因类似于CNN中使用多个卷积核，能够关注到输入的不同方面的信息。  为了使输入输出保持相同的维度，多头计算时，每个头的维度等比例变化为`dmodel//h`，拼接后，依旧是`dmodel//h * h=dmodel` 不变。

例句`the animal didn't cross the street because it was too tired` 中，在计算`it`的多头注意力时，有两个头分别注意到了单词`animal` 和 `tired` ，这证明了多头的必要。 

<img src="../md_assets/transformer_self-attention_visualization_2.png" alt="img" style="zoom: 80%;" />





论文中，将头设置为8，每一个头的输出向量维度设置为64 ，最后进行拼接`z=[z0:z1:....:z7]`  

```python
head = 8 
head_size = dmodel/head= 512/8 = 64 
```

每一个头都对应一套自己的$W_Q;W_K;W_V$ 矩阵  ，它们之间不共享一套参数，独立地更新。  

<img src="../md_assets/transformer_attention_heads_qkv.png" alt="img" style="zoom:50%;" />

计算得到8个头的z 

<img src="../md_assets/transformer_attention_heads_z.png" alt="img" style="zoom: 50%;" />

拼接他们，然后再乘一个权重矩阵$W_O$，做一次线性变化  

<img src="../md_assets/transformer_attention_heads_weight_matrix_o.png" alt="img" style="zoom:50%;" />

这是整个 多头注意力 的计算流程

<img src="../md_assets/transformer_multi-headed_self-attention-recap.png" alt="img" style="zoom:50%;" />



```python
class MultiHeadedAttention(nn.Module):
    def __init__(self, h, d_model, dropout):
        """
        实现多头注意力机制
        :param h: 头数
        :param d_model: word embedding维度
        :param dropout: drop out
        """
        super(MultiHeadedAttention, self).__init__()
        assert d_model % h == 0  # 检测word embedding维度是否能被h整除
        # We assume d_v always equals d_k
        self.d_k = d_model // h
        self.h = h  # 头的个数
        # 四个线性变换，前三个为QKV三个变换矩阵，最后一个用于attention后 Wz
        self.linears = clones(nn.Linear(d_model, d_model), 4)  
        self.attn = None
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, query, key, value, mask=None):
        """
        (qk^t/sqrt(k))*v 
        :param query: 输入x，即(word embedding+postional embedding)，size=[batch, L, d_model] tips:编解码器输入的L可能不同
        :param key: 同上，size同上
        :param value: 同上，size同上
        :param mask: 掩码矩阵，编码器mask的size = [batch , 1 , src_L],解码器mask的size = [batch, tgt_L, tgt_L]
        在encoder时 掩码矩阵的作用在于 标记pad位置 令其注意力为0 
        在decoder时 掩码矩阵的作用在于 标价当前时间步之后的位置 令其注意力为0 
        在en-de 时 q是decoder当前的输入 k是encoder编码后的上下文 掩码矩阵的作用在于 标记 
        """
        if mask is not None:
            # 在"头"的位置增加维度1，意为对所有头执行相同的mask操作（广播操作）
            # 编码器mask的size = [batch,1,1,src_L] 
            # 解码器mask的size= = [batch,1,tgt_L,tgt_L]
            mask = mask.unsqueeze(1)  
        nbatches = query.size(0)  # 获取batch的值，nbatches = batch

        # 1) 利用三个全连接算出QKV向量 batch,l,dmodel
        # view维度变换相当于将dmodel切分成h份 每一份是一个头  [batch,L,h,d_model//h] 
        # 这里和原论文稍有不同 是通过view相当于切了h份 qkv 出来 比起初始化h个qkv 这种写法更加简洁 
        # 因为都是线性操作 xw_q=q/xw_k=k... 所以拼接再切割并无不妥 
        # transpose再转置L h 两个维度  , [batch , h , L , d_model//h]
        query, key, value = \
            [l(x).view(nbatches, -1, self.h, self.d_k).transpose(1, 2)  # view中给-1可以推测这个位置的维度
             for l, x in zip(self.linears, (query, key, value))]

        # 2) 实现Scaled Dot-Product Attention
        # 要简化矩阵规模 前面的batch，h 相当于个数 关心后面两个维度
        # x的size = (batch,h,L,d_model//h) ==> (batch,h,L,d_model//h) 
        # 每一行都已经是 注意力融合后 的行 
        # attn的size = (batch,h,L,L) 每一个batch 每一个head 都有一个L*L 的注意力矩阵 
        x, self.attn = attention(query, key, value, mask=mask, dropout=self.dropout)

        # 3) 这步实现拼接 
        # transpose的结果 size = (batch , L , h , d_model//h)
        # view的结果size = (batch , L , d_model)
        x = x.transpose(1, 2).contiguous().view(nbatches, -1, self.h * self.d_k)

        return self.linears[-1](x)  # size = (batch , L , d_model)


def attention(query, key, value, mask=None, dropout=None):
    """
    实现 Scaled Dot-Product Attention
    :param query: 输入与Q矩阵相乘后的结果,size = (batch , h , L , d_model//h)
    :param key: 输入与K矩阵相乘后的结果,size同上
    :param value: 输入与V矩阵相乘后的结果，size同上
    :param mask: 掩码矩阵 batch,1,1,src_l/trg_l 
    中间的两个维度1方便进行广播运算 一种简单的理解就是 在这两个维度上(h,l)执行相同的操作 
    :param dropout: drop out
    """
    d_k = query.size(-1)
    # 计算QK/根号d_k，size=(batch,h,L,L) 这一步已经完成了注意力计算 
    # 但是由于种种原因PAD\时间步遮掩 需要在某些位置上 将其置为负无穷，如此，在softmax后才能使其注意力为0
    # 完成上一步的操作需要mask掩码矩阵 或与scores矩阵同形batch,h,l,l 或可参与广播运算 
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)  
    if mask is not None:
        # 掩码矩阵，编码器mask的size = [batch,1,1,src_L]  
        # 物理意义：对于bacth中每个样本，都有一个 1*src_l的 布尔矩阵与其对应（只是记录pad位置） 
        # 解码器mask的size = [batch,1,tgt_L,tgt_L] 
        # 物理意义：对于batch的每个样本，都有一个 tgt_l*tgt_l的 布尔矩阵与其对应（要记录时间步的位置，是一个下三角）
        scores = scores.masked_fill(mask=mask, value=torch.tensor(-1e9))
    p_attn = F.softmax(scores, dim=-1)  # 以最后一个维度进行softmax(也就是最内层的行),size = (batch,h,L,L)
    if dropout is not None:
        p_attn = dropout(p_attn)
	# score与V相乘 注意力融合  size=(batch,h,L,d_model//h) 
    # 第二个是单纯的注意力矩阵  size = (batch,h,L,L) 
    return torch.matmul(p_attn, value), p_attn  
```

在上述计算注意力的过程中，mask掩码矩阵发挥了重要作用。以下是关于mask掩码矩阵生成的代码：

```python
# mask要掩盖一个什么样的矩阵？ 当然是qK^T 矩阵，也就是得分矩阵 
# 它的大小是 (batch,h,l,dmodel) matmul (batch,h,dmodel,l) ==> batch,h,l,l 
# 然后要考虑mask矩阵应该是什么样的 ？ 怎么才能达到掩盖的目的
# 说结论 详细过程看图 
# 对于encoder而言 mask矩阵应该遮掩相应pad的位置 假设样本的第ij位置是pad 那么在value矩阵中 相应的ij行也是pad
# 对应的注意力应该为0 因此 在得分矩阵中 第ij列应该mask掉（想想矩阵乘法的运算 score*value 是不是刚好作用在那几行） 
# 对于decoder而言 mask矩阵应该遮掩当前时间步及之后的位置 这刚好对应一个不含主对角线的下三角矩阵 

class Batch:
    def __init__(self, src, trg=None, pad=0):
        """
        :param src: 一个batch的输入，size = [batch, src_L]
        :param trg: 一个batch的输出，size = [batch, tgt_L]
        """
        self.src = src
        # 返回一个true/false矩阵，size = [batch , 1 , src_L] 
        # unsqueeze添加的1维度是为了有助于广播运算 
        self.src_mask = (src != pad).unsqueeze(-2)  
        if trg is not None:
            self.trg = trg[:, :-1]  # 用于输入模型，不带末尾的<eos>
            self.trg_y = trg[:, 1:]  # 用于计算损失函数，不带起始的<sos>
            self.trg_mask = self.make_std_mask(self.trg, pad) # 制作出tgt的mask矩阵 
            self.ntokens = (self.trg_y != pad).data.sum()

    @staticmethod  # 静态方法
    def make_std_mask(tgt, pad):
        """
        :param tgt: 一个batch的target，size = [batch, tgt_L]
        :param pad: 用于padding的值,一般为0
        :return: mask, size = [batch, tgt_L, tgt_L]
        """
        tgt_mask = (tgt != pad).unsqueeze(-2)  # 标记pad位置，size = [batch , 1 , tgt_L]
        # typeas 是转换类型 传进去的大小是 tgt_len 
        tgt_mask = tgt_mask & Variable(
            subsequent_mask(tgt.size(-1)).type_as(
                tgt_mask.data))  # 两个mask求和得到最终mask,[batch, 1, L]&[1, L, L]=[batch,tgt_L,tgt_L]
        return tgt_mask  # size = [batch, tgt_L, tgt_L]


def subsequent_mask(size):
    """
    :param size: 输出的序列长度
    :return: 返回下三角矩阵，size = [1, size, size]
    """
    attn_shape = (1, size, size)
    # triu 返回上三角矩阵 k=1 不含主对角线 
    subsequent_mask = np.triu(np.ones(attn_shape), k=1).astype('uint8') 
    # 这一步==0 转换为bool矩阵的同时 返回了一个下三角矩阵 
    return torch.from_numpy(subsequent_mask) == 0 
```



encoder时掩码矩阵的作用示意

带有pad的输入x 以及qkv

<img src="../md_assets/image-20210912091536345.png" alt="image-20210912091536345" style="zoom:67%;" />

掩码矩阵如何作用在score矩阵 

<img src="../md_assets/image-20210911195931346.png" alt="image-20210911195931346" style="zoom:67%;" />



decoder时掩码矩阵的生成 （红色的是False，白色的是True）

`1,tft_l`的用于标记PAD位置，`tgt_L,tgt_L`的用于遮盖时间步信息  

![img](../md_assets/20201206182519180.png)



作用示意图

<img src="../md_assets/image-20210912101045709.png" alt="image-20210912101045709" style="zoom:67%;" />

最关键的地方就是 遮盖后的scores（`l,l`） 矩阵在和 value（`l,dmodel`）矩阵相乘时发生了什么？

在计算Z矩阵的第一行时，只有value的第一行参与了注意力融合；在计算第二行时，value的第一行、第二行参与了注意力融合……以此类推，在计算第i行时，只有`<=i`的前面几行参与了运算，这就达到了遮盖时间步的效果。 





#### residual  & FFT

层与层之间使用残差连接 ，每一层后使用`laynorm`归一化运算  

```python
laynorm( x+network(x) )
```



```python
class LayerNorm(nn.Module):
    def __init__(self, features, eps=1e-6):
        """
        实现层归一化
        """
        super(LayerNorm, self).__init__()
        # 注册为parameter表示系数和偏置都为可训练的量
        self.a_2 = nn.Parameter(torch.ones(features))  # 线性放缩因子 
        self.b_2 = nn.Parameter(torch.zeros(features)) # 偏置
        self.eps = eps # 保证归一化分母不为0

    def forward(self, x):
        """
        :param x: 输入size = (batch , L , d_model)
        :return: 归一化后的结果，size同上
        """
        # laynorm 是在x的特征集上求归一化 
        mean = x.mean(-1, keepdim=True) # 最后一个维度求均值
        std = x.std(-1, keepdim=True)  # 最后一个维度求方差
        return self.a_2 * (x - mean) / (std + self.eps) + self.b_2   #归一化并线性放缩+偏移

class SublayerConnection(nn.Module):
    """
    实现残差连接
    """
    def __init__(self, size, dropout):
        super(SublayerConnection, self).__init__()
        self.norm = LayerNorm(size)   # 读入层归一化函数
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sublayer):
        """
        :param x: 当前子层的输入，size = [batch , L , d_model]
        :param sublayer: 当前子层的前向传播函数，指代多头attention或前馈神经网络
        """
        # 这里把归一化已经封装进来，size = [batch , L , d_model] 
        return self.norm(x + self.dropout(sublayer(x)))
```



在多头注意力后是两层简单的前馈网络

```python
# feed forward network 
# 维度变化： 512--2048--512 
FFN= linear (relu(linear(x)) )
```

<img src="https://jalammar.github.io/images/t/transformer_resideual_layer_norm_2.png" alt="img" style="zoom: 67%;" />



```python
class PositionwiseFeedForward(nn.Module):
    "实现全连接层"
    def __init__(self, d_model, d_ff, dropout):
        super(PositionwiseFeedForward, self).__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        """
        :param x: size = [batch , L , d_model]
        :return:  size同上
        """
        return self.w_2(self.dropout(F.relu(self.w_1(x))))
```

#### stack

采取多层堆叠后的 encoder 是这样的 ，每一层的输出 是 下一层的输入  

<img src="../md_assets/transformer_resideual_layer_norm_3.png" alt="img" style="zoom:67%;" />





```python
# 一个encoder_layer
class EncoderLayer(nn.Module):
    """
    Encoder层整体的封装，由self attention、残差连接、归一化和前馈神经网络组成
    """
    def __init__(self, size, self_attn, feed_forward, dropout):
        super(EncoderLayer, self).__init__()
        self.self_attn = self_attn  #定义多头注意力，即传入一个MultiHeadedAttention类
        self.feed_forward = feed_forward #定义前馈，即传入一个PositionwiseFeedForward类
        self.sublayer = clones(SublayerConnection(size, dropout), 2)   #克隆两个残差连接，一个用于多头attention后，一个用于前馈神经网络后
        self.size = size

    def forward(self, x, mask):
        """
        :param x: 输入x，即(word embedding+postional embedding)，size = [batch, L, d_model]
        :param mask: 掩码矩阵，编码器mask的size = [batch , 1 , src_L],解码器mask的size = [batch, tgt_L, tgt_L]
        :return: size = [batch, L, d_model]
        """
        # sublayer 是两个残差连接 
        # 第2个参数 表示子层网络 函数 
        # 经过 multi-head 后 输入变为 batch,l,dmodel ==> batch,l,dmodel 
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))  
        return self.sublayer[1](x, self.feed_forward)  


# 一个encoder  
# 每一层的输入输出是同形的 batch,l,dmodel ==> batch,l,dmodel 
# 这为多层嵌套提供了极大的方便 
class Encoder(nn.Module):
    """
    Encoder最终封装，由若干个Encoder Layer组成
    """
    def __init__(self, layer, N):
        super(Encoder, self).__init__()
        self.layers = clones(layer, N)  # N层Encoder Layer
        self.norm = LayerNorm(layer.size) # 最终输出进行归一化

    def forward(self, x, mask):
        for layer in self.layers:
            x = layer(x, mask)
        return self.norm(x)
```





### decoder 

decoder 的结构和 encoder 类似，但是 是按照 时间步迭代运行的。 

输入会参与两次注意力计算 ，第1次是输入的self-atten，第2次是encoder-decoder之间的注意力融合。 

<img src="../md_assets/image-20210912085518421.png" alt="image-20210912085518421" style="zoom:50%;" />





self-attn中要额外注意的地方，便是屡次提及的问题——不应让当前时间步看到之后时间步的内容，这个可以用特殊的下三角矩阵来实现，在encoder部分已经提及。 

encoder-decoder的attention部分，q是decoder的输入（已经经过了self-attn），k\v是encoder编码向量，所以mask矩阵应该是encoder用于标记pad位置的mask矩阵（考虑value矩阵）。 

encoder-decoder的attention计算 

<img src="../md_assets/image-20210912090836320.png" alt="image-20210912090836320" style="zoom:67%;" />



decoder时，当前时间步的解码 依赖 编码器的输出向量（上下文向量context）、历史解码字符的拼接。 

注意到，每次输入解码都是 拼接了上一时间步的预测，因为transfomer的self-attn是并行计算的，所以一次输入要包含历史信息，才能做关联的attention计算。而RNN虽然也是按照时间步迭代的，但是每一个时间步都会流出一个隐藏状态给下一时间步使用，故rnn结构的解码器输入上一时间步的单个字符即可，而非拼接。 



![transformer_decoding_2](../md_assets/transformer_decoding_2.gif)



```python
class DecoderLayer(nn.Module):
    "解码器由 self attention、编码解码self-attention、前馈神经网络 组成"
    def __init__(self, size, self_attn, src_attn, feed_forward, dropout):
        super(DecoderLayer, self).__init__()
        self.size = size   # embedding的维度
        self.self_attn = self_attn # self-attn
        self.src_attn = src_attn  # encoder-decoder attn 
        self.feed_forward = feed_forward
        self.sublayer = clones(SublayerConnection(size, dropout), 3) #克隆3个sublayer分别装以上定义的三个部分


    def forward(self, x, memory, src_mask, tgt_mask):
        """
        :param x: target，size = [batch, tgt_L, d_model]
        :param memory: encoder的输出，size = [batch, src_L, d_model]
        :param src_mask: 源数据的mask, size = [batch, 1, src_L]
        :param tgt_mask: 标签的mask，size = [batch, tgt_L, tgt_L]
        """
        m = memory
        #  self-atten、add&norm，和编码器一样, size = [batch, tgt_L, d_model]
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, tgt_mask))
        # 编码解码-attention、add&norm，Q来自target，KV来自encoder的输出，size = [batch, tgt_L, d_model]
        x = self.sublayer[1](x, lambda x: self.src_attn(x, m, m, src_mask)) 
        return self.sublayer[2](x, self.feed_forward) # 前馈+add&norm, size = [batch, tgt_L, d_model]
```



```python
class Decoder(nn.Module):
    "解码器的高层封装，由N个Decoder layer组成"
    def __init__(self, layer, N):
        super(Decoder, self).__init__()
        self.layers = clones(layer, N)
        self.norm = LayerNorm(layer.size)

    def forward(self, x, memory, src_mask, tgt_mask):
        for layer in self.layers:
            x = layer(x, memory, src_mask, tgt_mask)
        return self.norm(x)  # size = [batch, tgt_L, d_model]
```



在解码器输出后，连接一个用于分类的`Linear + softmax`    

<img src="../md_assets/transformer_decoder_output_softmax.png" alt="img" style="zoom:67%;" />



```python
class Generator(nn.Module):
    """
    定义一个全连接层+softmax
    """
    def __init__(self, d_model, vocab):
        super(Generator, self).__init__()
        self.proj = nn.Linear(d_model, vocab)  # vocab为整个词袋的词数

    def forward(self, x):
        """
        :param x: 输入的 size = [batch, tgt_L, d_model]
        """
        return F.log_softmax(self.proj(x), dim=-1)  #dim=-1在最后一维上做softmax
```





****

encoder-decoder 架构 

```python
class EncoderDecoder(nn.Module):
    """
    编码解码架构
    """
    def __init__(self, encoder, decoder, src_embed, tgt_embed, generator):
        super(EncoderDecoder, self).__init__()
        self.encoder = encoder  # 编码器
        self.decoder = decoder  # 解码器
        self.src_embed = src_embed  # 源的embedding
        self.tgt_embed = tgt_embed  # 目标的embedding
        self.generator = generator  # 定义最后的线性变换与softmax

    def forward(self, src, tgt, src_mask, tgt_mask):  # 编码解码过程
        return self.decode(self.encode(src, src_mask), src_mask,
                           tgt, tgt_mask)

    def encode(self, src, src_mask):
        return self.encoder(self.src_embed(src), src_mask)

    def decode(self, memory, src_mask, tgt, tgt_mask):
        return self.decoder(self.tgt_embed(tgt), memory, src_mask, tgt_mask)
```





# torchtext 

torchtext  用于处理自然语言问题。

## 词表建立

首先是分词

`get_tokenizer`返回一个分词器，当使用参数`basic_english`时，分词将包含字符串小写、**unicode标准化**、按照单词形式分割。 

```python
from torchtext.data.utils import get_tokenizer

tokenizer=get_tokenizer('basic_english') # 分词器 

# 分词器输入 句子 ，返回 token序列 
tokenizer("I come from china ") # [i,come,from,china] 
```

关于unicode标准化的必要，因为一个字符在unicode字符集中有多种编码方式，为了统一编码，就需要标准化 

```python
import unicodedata,string 
# 手动标准化 
# 如果使用库提供的分词器 get_tokenizer 就不需要 
# NFD 表示尽可能使用单字符编码 而非 组合编码 combine 

def unicodeToAscii(s):
    all_letters = string.ascii_letters + " .,;'"
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in all_letters
    )

print(unicodeToAscii('Ślusàrski'))
```





使用函数 `build_vocab_from_iterator(tokens_iterator)` 可以很容易建立一个词表，参数如下，最后返回`Vocab` 对象。 

* tokens_iterator：`List[List[str]]`，每个元素是已经分词完毕的tokens列表 
* specials：特殊字符列表 
* min_freq =1：最小词频 



```python
from torchtext.vocab import build_vocab_from_iterator 
# 第一个参数 为每个句子使用分词器分词 每个元素是tokens列表 
# 第二个参数 使用特殊字符 ，列表形式
vocab = build_vocab_from_iterator([tokenizer(s) for s in datas],
                                 specials=['<UNK>'])
vocab.set_default_index(vocab['<UNK>']) # 将OOV索引默认设置为UNK 

```

词表的基本用法 

```python
len(vocab) # 查看词表大小
vocab['a'] # get_item 得到某个字符的索引 
vocab(['an','apple','a','day']) # forward ，返回每个token的index

vocab.get_stoi() # 得到stoi 字典
vocab.get_itos() # 得到itos 列表  
```







# reproducility 

reproducility，意为可再生的。为了每次跑模型的结果基本一致，需要关闭一些随机源

```python
np.random.seed(1) # 设置随机数种子可以确保之后的random函数返回相同结果
torch.manual_seed(1)  # 为GPU设置随机数 
torch.cuda.manual_seed_all(1) # 同上 用于多个GPU情况
```





# 迁移学习

## 迁移学习

迁移学习是指让模型在一个已有的标记数据的领域向未标记数据领域进行迁移，从而训练出适合该领域的模型。 

## 微调

 相似领域下，用被人训练好的模型换成自己的数据，调整参数，重新训练。 

使用微调的好处：

1. 节约时间：使用导出特征向量的方法进行学习
2. 提升模型效果：数据集较小的时候是训练不出一个好的大模型的（模型越大，特征提取能力越强），这时候只能靠微调 
3. 不要重复造轮子



迁移学习和微调大部分时候含义可以交换，严格来说，迁移学习是一种策略，微调是一种调整模型的手段。





微调的方案：

1. fine-tune：冻住模型部分网络层的参数，只训练自己的全连接层（或小型网络），适合小规模数据集。
2. retrain：微调整个网路的所有参数，相当于预训练模型只做了一个初始化的工作，适合大规模数据集。



微调时候的小技巧：

1. 对于不同的层可以设置不同的学习率。原网络的参数学习率要小于（一般可设置小于10倍）初始化的学习率，这样保证已经预训练的层不会扭曲过快，而新层可以快速收敛。



微调示例：1. 修改模型结构，将最后的全连接层替换为自己的全连接层，主要是更改了“输出特征维度” 2. 冻结全连接层之前的网络参数 ，在优化器中仅仅传入全连接层的参数 

```python
def create_model():
    model=resnet50(pretrained=True) # 预训练模型
    for parameter in model.parameters():
        parameter.requires_grad=False # 冻结

    fc=nn.Linear(
        in_features=model.fc.in_features, # 获取之前的输入特征维度 
        out_features=LABELS # LABELS 是自己的多分类总数
    )
    model.fc=fc # 替换为自定义的全连接层
    

# 优化器仅传入fc的参数 
optimzer=optim.Adam(model.fc.parameters())
```
