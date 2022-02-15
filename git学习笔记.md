# 配置

```shell
git config --list # 显示当前配置信息 
git config -e    # 针对当前仓库 
git config -e --global   # 针对系统上所有仓库

# 常见配置 
git config --global user.name "runoob"
git config --global user.email test@runoob.com
```



# 分区

![img](D:\我的坚果云\学习笔记\better\resources\git-command.jpg)



* 工作区：当前工作目录
* 暂存区：`.git`文件夹中的index文件，**保存工作区快照**，又叫做索引区 
* 版本库：隐藏目录`.git`，包含了 暂存区、



![img](D:\我的坚果云\学习笔记\better\resources\1352126739_7909.jpg)

HEAD当前指向master分支，objects表示git对象，存储了各种必要信息。



1. 当执行`git add`时，工作区的文件会被追加到暂存区 
2. 当执行`git commit`时，暂存区的文件就会追加到HEAD所指分支
3. 当执行 `git reset HEAD` 命令时，暂存区的目录树会被重写
4. 当执行` git rm --cached <file>` 命令时，**会直接从暂存区删除文件 ，用于撤销`git add`添加的文件**
5. 当执行 `git checkout .` 或者 `git checkout -- <file>` 命令时，会用暂存区的文件替换工作区的文件。**这个操作很危险，工作区未添加到暂存区的操作将被舍弃** 
6. 当执行 `git checkout HEAD .` 或者` git checkout HEAD <file>` 命令时，**会用 HEAD 指向的 master 分支中的文件同时替换暂存区和以及工作区中的文件。**



```shell
git lf-files # 查看暂存区文件
```



# 基本操作

初始化 

```shell
# init 时 只有在commit一次以后才会真正生成该分支 
git init # 初始化仓库 
git clone # 拷贝 
```

关于克隆：

1. 在本地配置ssh密钥，添加公钥到仓库的可信公钥列表。当本地与仓库通信时，可免去密码连接

2. 使用https服务，每次上传下载都需要密码连接

   ```shell
   # git clone http://userName:password@链接
   git clone https://jiang_hui_kai:xxxx@https://gitee.com/jiang_hui_kai/xxx.git
   ```

   

提交与修改

```shell
gid add # 添加文件到仓库 
git status # 查看当前仓库状态 

git commit # 提交暂存区到本地仓库
git reset # 回退版本  观察上图 只修改暂存区
git rm  # 删除工作区文件 
git mv # 移动或者重命名文件
```



提交时如果改动内容较少，只想修改上一次提交，可以修改为 ，会修改上次提交版本。

```shell
git commit --amend  
```





`.gitignore`只能作用于未被track的文件，对于那些已经被纳入到版本管理的文件，重新编辑`.gitignore`没有作用。做法是

```shell
git rm -r --cached .  # 移除 追踪状态
git add . # 添加 gitignore 文件 此时会自动过滤那些被记录在ignore里的文件 
git commit -m 'update .gitignore' 
```





比较

```shell
git diff # 比较 工作区 和 暂存区 
git diff --HEAD # 比较 工作区 和 local repo
git diff --cached # 比较 暂存区 和 local repo 
git diff branch # 比较分支 
git diff commit-id # 比较版本
```

diff的输出结果中，`---`表示源文件，`+++`表示目标文件（所以可以理解为新增），在源文件与目标文件之间作对比，空格开头的行表示两者都有。





提交日志 

```shell
git log # 查看历史 
git log --oneline # 简略形式 
git log --graph # 树形图形式查看合并记录
git log --oneline --before={3.weeks.ago} --after={2010-04-18} # 时间段查看 


git blame <file> # 以列表形式查看指定文件的历史修改
```



# 分支管理

```shell
git branch (branchname) # 列出分支 /创建分支 
git branch -d (branchname) # 删除分支

# 切换分支的时候 需要先保存分支快照到暂存区 
git checkout (branchname) # 切换分支 / 缺省时为master
git checkout -b (branchname) # 创建并切换到该分支 
git checkout - # 切换上一个分支 

git merge <brachname># 合并分支b到当前分支 
```



合并冲突：当两个分支合并时，未冲突的文件会被自动合并，而那些冲突文件则需要手动解决冲突，然后重新`git add ` 告诉git已经解决冲突。

Git用`<<<<<<<`，`=======`，`>>>>>>>`标记出不同分支的内容，一个冲突的文件格式看起来如下

```
<<<<< branch0,current branch 
something

=======

something 

>>>>>>> branch1 to merge 
```





# 标签

标签，是比commit号更易读的一种指针，同样可以使用tag来恢复快照。

```shell
git tag -a v1.0 # 创建标签 
git tag # 查看已有标签 
git tag -d v1.1 # 查看已有标签
git show v1.0 # 查看版本所发生的修改 
```

# 远程仓库

```shell
ssh-keygen # 本地生成密钥对 公钥放在github上 

git remote -v # 查看当前远程仓库 
git remote add [remote_repo_shortname] [url] # 添加远程仓库 
git remote rm [别名] # 删除远程仓库 
git remote [origin] set-url [url] # 修改远程仓库url


git fetch # 从远程获取代码库 
git pull # 下载远程代码合并 
git pull origin master # 下载origin的master分支
git push # 上传远程代码并合并
git pusb origin master # 上传到远程的master分支
```



[同时关联到github、gitee](https://www.runoob.com/git/git-gitee.html)：关键就是个不同的远程仓库取别名 

​	
