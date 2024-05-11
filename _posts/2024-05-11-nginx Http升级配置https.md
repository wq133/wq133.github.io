---
layout: post
title: nginx Http升级配置https
subtitle: 方案、问题踩坑
date: 2024-05-11
author: Wu
header-img: ../article_img/SL_1.jpg
tags:
  - Nginx
  - Https
---
## 1.安装openssl模块

```text
yum -y install openssl openssl-devel
```

![](../../article_img/Pasted%20image%2020240511100506.png)
## 2.Nginx配置文件备份
进入nginx根目录，cd /etc/nginx 对文件备份（常用的配置文件，我这里是/etc/nginx/conf.d/default.conf）

方案1：直接finelshell下载到本地

方案2：linux中用命令备份nginx.conf

```
cp source_file destination_file
```
## 3.证书准备-申请免费证书

1. 开放端口：80和443端口

```shell
systemctl status firewalld.service
systemctl start firewalld.service

firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --permanent --add-port=443/tcp
firewall-cmd --reload

systemctl stop firewalld.service
```

2. 安装 certbot  
使用certbot工具能够很方便的申请和续签let’s encript证书。

```
yum install -y epel-release
yum install -y certbot
```

3. 执行cerbot命令

>  certbot certonly --webroot -w [Web站点目录] -d [站点域名] -m [联系人email地址] --agree-tos

站点目录：html文件保存位置，只需要到文件夹即可。`比如index.html在/www/a/b/index.html，则这里只要取/www/a/b即可`。  
站点域名：购买的域名。  
联系人email地址：填写自己的邮箱即可。

实际我的配置：
`certbot certonly --webroot -w /var/wq133.github.io/_site -d 66dr.cn -m wqh666@vip.qq.com --agree-tos`

执行3的命令后，y确认。

4. 查看证书位置

```shell
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/66dr.cn/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/66dr.cn/privkey.pem
   Your certificate will expire on 2024-08-09. To obtain a new or
   tweaked version of this certificate in the future, simply run
   certbot again. To non-interactively renew *all* of your
   certificates, run "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate

```

/etc/letsencrypt/live/{域名}就是存放当前域名网站证书的路径。

5. 查看证书有效期
`openssl x509 -noout -dates -in /etc/letsencrypt/live/{域名}/cert.pem`
![](../../article_img/Pasted%20image%2020240511103557.png)

## 4.配置Nginx配置文件
原有配置：
```
server {
    listen       80;
    server_name  66dr.cn wqhong.icu www.66dr.cn  www.wqhong.icu;

    #access_log  /var/log/nginx/host.access.log  main;

    location / {
       root   /var/wq133.github.io/_site;
	#proxy_pass http://localhost:4000;
        index  index.html;
    }

    error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
	

}
```

新增配置到server下：
```
# 配置ssl证书
ssl_certificate /etc/letsencrypt/live/66dr.cn/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/66dr.cn/privkey.pem;

# 配置Nginx支持的SSL/TLS协议版本
ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3;

# 配置设定了加密套件（cipher suites）的优先级顺序
ssl_ciphers EECDH+CHACHA20:EECDH+CHACHA20-draft:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;

# Nginx在协商加密套件时优先采用服务器端配置的顺序，而不是客户端提供的偏好。
ssl_prefer_server_ciphers on; 

# 配置了SSL会话缓存，类型为共享缓存，名称为`SSL`，大小为10MB。首次安全连接，之后的连接可以复用之前的会话密钥，减少握手时间。
ssl_session_cache shared:SSL:10m;

# 设置了SSL会话的有效时间为10分钟。这意味着如果客户端在一个会话有效期内重新连接到服务器，它们可以跳过完整的握手过程，从而加快连接速度。
ssl_session_timeout 10m;

# 添加HTTP响应头`Strict-Transport-Security`（简称HSTS），告诉浏览器始终通过HTTPS与该站点通信，有效时间为31536000秒（即1年）。这有助于防止中间人攻击和 cookie劫持，强制客户端将来对该域名的所有请求都使用HTTPS。
add_header Strict-Transport-Security "max-age=31536000";

```

配置完之后实际是：
```
server {
        listen 80;
        server_name 66dr.cn wqhong.icu www.66dr.cn www.wqhong.icu;
        
        # 将所有HTTP流量重定向到HTTPS
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name 66dr.cn wqhong.icu www.66dr.cn www.wqhong.icu;

        # SSL证书配置
        ssl_certificate /etc/letsencrypt/live/66dr.cn/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/66dr.cn/privkey.pem;

        # 其他SSL配置保持不变
        ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3;
        ssl_ciphers EECDH+CHACHA20:EECDH+CHACHA20-draft:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
        add_header Strict-Transport-Security "max-age=31536000";


        location / {
            # 此处无需更改，保持原有配置
		root   /var/wq133.github.io/_site;
		#proxy_pass http://localhost:4000;
		index  index.html;
        }

        # 错误页面配置保持不变
        error_page 404 /404.html;
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
```

因为我的Nginx实际启动conf文件是去载入这个default.conf文件的，所以这里默认启动的conf文件如下：
```

user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/default.conf;
}

```

`include /etc/nginx/conf.d/default.conf `这里就包含了default.conf中配置的ssl证书及其相关配置。

## 5.重启nginx

我这里默认用systemctl 的方式启动。所以执行
> systemctl status nginx.service

> systemctl restart nginx.service

实际上到这里基本完成技术上的配置，由于云服务器的端口是需要在管理端口手动开启，这里我实际测试以https的方式访问博客还是失败。所以再到这个路径开启443端口即可。（阿里云为例子：实例->云服务器 ECS->网络与安全->安全组中，入方向手动添加按钮，添加即可）
![](../../article_img/20240511htpp443conf.png)
## 6.配置 Let'sEncrypt 证书自动续约-TODO-0809

## 参考文章
[全站HTTPS升级系列（三）nginx配置全站HTTPS](https://juejin.cn/post/6844903759764520973?searchId=202405091655379A652FE83C772D955502)
[Nginx 如何配置 Https？](https://www.zhihu.com/question/585631463/answer/3333804746) - 温水煮蛙的回答 - 知乎 
[让网站更安全：使用 Let's Encrypt 轻松获得免费 SSL 证书并自动续签](https://zhuanlan.zhihu.com/p/648603442)
[Nginx 配置 https （Let's Encrypt）](https://juejin.cn/user/3650034333125335/posts)
[Let's Encrypt 自动化续签](https://blog.csdn.net/qq_40579464/article/details/131117495)
[一文搞懂Nginx代理及基础高级配置及跨域(含websocket、http2)](https://juejin.cn/user/4125023358954526/posts)

