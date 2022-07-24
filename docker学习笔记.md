# 使用



```shell
# 获取镜像
docker pull ubuntu 

# 启动容器
# i表示交互式 t表示终端 ubuntu镜像
# /bin/bash 对于镜像执行的命令
# d表示后台运行 
docker run -itd ubuntu /bin/bash

# 退出 
exit

# 
```



启动停止 容器 

```shell
docker ps -a # 查看所有容器 
docker start b750bbbcfd88  # 容器编号
docker stop <容器 ID>  # 停止容器 
docker restart <容器 ID>  # 重启容器 
```



进入容器 `exec`命令启动的容器，退出时不会停止

```shell
docker exec -it Hollis  /bin/bash
```



导出导入

```shell
# 导出该编号容器 
docker export 1e560fca3906 > ubuntu.tar

# 导入 
cat docker/ubuntu.tar | docker import - test/ubuntu:v1
# 从url导入 
docker import http://example.com/exampleimage.tgz example/imagerepo 
```



删除容器 

```shell
docker rm -f 1e560fca3906  # 删除

# 清除所有处于终止状态的容器 
docker container prune 
```

# DGX

https://www.cnblogs.com/makelu/p/11018212.html 原理介绍



nvidia docker 

https://www.cnblogs.com/wuchangsoft/p/9767074.html

https://www.cnblogs.com/chester-cs/p/14444247.html



* docker start 和 run区别 ： https://www.jianshu.com/p/b3f94f19fd02

* pycharm 连接dcker ： https://zhuanlan.zhihu.com/p/76469329

查看端口是否被占用 

```shell
netstat |grep ssh 

netstat |grep :22 

docker exec -it Hollis  /bin/bash # 可以开启多个终端
```

GPU使用情况

```
nvidia-smi
```



# account

> 在AMAX 数据服务器 222.24.36.241  port 22   username lixiaoge      passwd:123456
> 在DGX nvidia 服务器 222.24.36.240  port 22   username lixiaoge      passwd:123456
