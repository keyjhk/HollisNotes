# 机器学习

第三方库： scikit learn 

one-hot编码：https://www.cnblogs.com/shuaishuaidefeizhu/p/11269257.html 



## 分类问题

* 决策树
  * 预处理 one-hot编码
  * 训练集 测试集 train_test_split
  * 准确率 score 判断模型的好坏
* 随机森林
  * 过拟合 欠拟合
  * 网格搜索gridsearchCV  寻找参数 `n_jobs`并行运行的作业数量 

## 回归问题 

预测一个数值

* 线性回归 让点离线的距离尽可能小
  * 正规方程 linearRegression 数据量小 数据比较精确
  * 梯度下降 SGDRegressor 数据量大 
  * 通过均分误差 来判断模型优劣
* 岭回归 解决过拟合 Ridge(alpha=1) 正则化力度 高次项的惩罚系数  alpha越大 theta越小
* 逻辑回归 二分类 sigmoid函数 
  * replace 替换缺失值
  * logistic(C=0.1) C表示正则强度 
  * coef[回归系数](https://baike.baidu.com/item/%E5%9B%9E%E5%BD%92%E7%B3%BB%E6%95%B0/10840879?fr=aladdin)

## 聚类  

* 无监督学习 解决分类问题
* 任意选取3个点 计算所有点离这3个点的距离 归为3类 计算每一个类中的平均值 
* PCA
* KMeans `n_clusters` 代表分为几类 



# 深度学习

深度学习采用矩阵运算 ，gpu可以加速 

多层 通过损失函数来调整每一层的权重 



实战，再回过头看书 

## 张量

一个n维数组，tf的基本数据格式。

keras 