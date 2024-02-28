
### 查看日志

tail -fn 200 info.log 

/error 查看关键词 n下一个
:set number 显示行数


### 查找文件｜模糊查找
find /etc --name *wq133

### 解除端口占用
netstat -nlp | grep "80"
fuser -k 80/tcp
kill -9 PID

参考链接
https://juejin.cn/post/7249586142990532645
https://www.cnblogs.com/cainiao-Shun666/p/16220713.html
https://www.cnblogs.com/yaradish/p/10481215.html


