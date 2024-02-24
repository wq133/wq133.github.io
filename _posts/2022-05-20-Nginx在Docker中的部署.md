---
layout: post
title: "Nginx在Docker中的使用"
subtitle: "了解Nginx和使用Docker部署"
date: 2022-05-20
author: "Wu"
header-img: "/article_img/SL_1.jpg"
catalog: true
tags: 
 - Nginx
 - Docker
---

## Nginx 在Docker的部署

### 1.Nginx的历史和安装

#### 1.1Nginx的起源



#### 1. 2Nginx的初始化安装和测试

```yml

# : 指定版本 不加默认 latest版本 参考镜像hub.docker.com/_/nginx
docker pull nginx:1.7.8
# --name 指定dockers容器名称
# -p 映射端口号 9091前置位映射的是容器外部（也就是映射的服务器端口） 80映射容器内部(也就是docker中的端口)
docker run --name nginx -p 9091:80 -d nginx

# windows主机访问 http://192.168.230.99:9091  虚拟机ip:服务器映射端口 出现welcome即为成功


```

#### 1.3出现的问题

```yml
# 推测：80端口未开启？
参考链接[https://blog.csdn.net/zhaofuqiangmycomm/article/details/128183305]

# 开启防火墙

systemctl start firewall 

# 打开80端口

firewall-cmd --zone=public --add-port=80/tcp --permanent 

# 重载防火墙

firewall-cmd reload

# 查看80端口开放状况

firewall-cmd --zone=public --query-port=80

# 开机禁用防火墙

systemctl disable firewall
# 重启docker
systemctl restart docker
# 这时候启动nginx 会报错 ...
docker rm nginx 
# docker rm name/container Id  
# 解释：rm 容器名/持久化容器id ，id在docker ps -a 中查看
docker run --name nginx -p 9091:80 -d nginx 
#  http://192.168.230.99:9091  成功运行
```

### 2.Nginx的配置和部署

#### 2.1容器部署

​	创建挂载目录

```shell
# 创建页面目录
mkdir -p /server/nginx/html
# 创建日志目录
mkdir -p /server/nginx/logs
# 创建配置目录
mkdir -p /server/nginx/conf
```

#### 2.2创建容器指定挂载目录

```shell
# 拷贝配置文件到宿主机创建的挂载目录
docker cp nginx:/etc/nginx/nginx.conf /server/nginx/conf/nginx.conf

# 拷贝完 停止、删除容器
docker stop nginx
docker rm nginx

# 挂载到对应目录且创建并启动容器 |		不指定版本直接nginx |		指定版本nginx:xxx
docker run -d -p 9091:80 --name nginx -v /server/nginx/html:/usr/share/nginx/html -v /server/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /server/nginx/logs:/var/log/nginx --privileged=true nginx:xxx

docker run -d -p 9091:90 --name nginx -v /server/nginx/html:/usr/share/nginx/html nginx



```



2.3配置hosts文件

2.4配置文件

2.5重启服务

2.6常规配置 

2.7配置中的问题

```shell
# 挂载 拷贝配置文件的权限问题

[root@localhost nginx]# docker run -d -p 9091:80 --name nginx -v /server/nginx/html:/usr/share/nginx/html -v /server/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /server/nginx/logs:/var/log/nginx nginx:1.17.8
949f5d7cdebff5de5edc4d204f73d88da9e663eae75059295ea80c39138df0b0
docker: Error response from daemon: OCI runtime create failed: container_linux.go:346: starting container process caused "process_linux.go:449: container init caused \"rootfs_linux.go:58: mounting \\\"/server/nginx/conf/nginx.conf\\\" to rootfs \\\"/var/lib/docker/overlay2/7c94763f88d871bb4d80d41fecbac8d6595b17cfc6e636c81744ddcb21a42270/merged\\\" at \\\"/var/lib/docker/overlay2/7c94763f88d871bb4d80d41fecbac8d6595b17cfc6e636c81744ddcb21a42270/merged/etc/nginx/nginx.conf\\\" caused \\\"not a directory\\\"\"": unknown: Are you trying to mount a directory onto a file (or vice-versa)? Check if the specified host path exists and is the expected type.




```



### 3.Nginx的正向代理和反向代理的区别

