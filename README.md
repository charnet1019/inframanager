## 主机信息管理系统

### 使用pipreqs生成requirements.txt
> 进入项目根目录
```
pipreqs --force
```

### 初始化数据库
```
flask db init
flask db migrate
flask db upgrade
```

### 创建管理员用户
```commandline
flask createsuperuser
```
