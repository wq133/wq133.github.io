---
layout: post
title: 评论插件配置-gittalk
subtitle: 配置、问题踩坑
date: 2024-05-13
author: Wu
header-img: ../article_img/SL_1.jpg
tags:
  - gittalk
  - config
---
## 配置参考
#gitalk  
comments:  
  gitalk: true  
  clientID: ***3liuPVqOOkVJ30*** # 66号dr的disqus  
  secret: ***44a59e70a4bc9a90a9926dfc9b3f3aff07*** # old: 46368790aa221900c7f50d946887fbb447b3c***  
  repo: blog-talk  # ghp_zivwgW2pTxIFQ4WRzOLI0zfLwoWR5d46***  
  owner: wq***  
  admin: wq***  
  distractionFreeMode: true #输入评论内容时，全屏除了输入框，其他位置被屏蔽

## html中引入
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/gitalk@1/dist/gitalk.css">  
<script src="https://cdn.jsdelivr.net/npm/gitalk@1/dist/gitalk.min.js"></script>  
  
<!--引入 JavaScript-MD5-->
<!--
<script src="https://cdn.bootcdn.net/ajax/libs/blueimp-md5/2.10.0/js/md5.min.js"></script> 
-->
```


```html
{% if site.comments.gitalk %}  
  <script>  
    // 测试打印pathName  
    var path = location.pathname;  
    var titleSubstringChars = path.substring(0, 11);  
    // console.log(titleSubstringChars);  
  
    var gitalk = new Gitalk({  
      id: location.pathname,  
      clientID: '{{ site.comments.clientID }}',  //这里其实可以直接填值，但是考虑到页面安全性，还是通过配置的方式添加  
      clientSecret: '{{ site.comments.secret }}',   
repo: '{{ site.comments.repo }}',   
owner: '{{ site.comments.owner }}',  
      admin: '{{ site.comments.admin }}',  
      // id: md5(titleSubstringChars),  
      id: titleSubstringChars,  
      distractionFreeMode: '{{ site.comments.distractionFreeMode }}'  
    })  
  
    gitalk.render('disqus_thread')  
  </script>  
{% endif %}
```

## 参考链接
[gittalk官方文档](https://github.com/gitalk/gitalk/blob/master/readme-cn.md)
[gittalk的使用](https://www.zhwangart.com/2018/12/06/Gitalk/#%E6%8A%A5%E9%94%99%E4%B8%8E%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88)

