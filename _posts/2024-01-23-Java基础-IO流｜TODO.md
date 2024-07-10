---
layout: post
title: Java-IO流
subtitle: IO模型、NIO...
date: 2024-01-23
author: Wu
header-img: ../article_img/SL_1.jpg
catalog: true
tags:
  - Java
  - 八股文
---

###  I/O 流为什么要分为字节流和字符流呢?

问题本质想问：不管是文件读写还是网络发送接收，信息的最小存储单元都是字节，那为什么 I/O 流操作要分为字节流操作和字符流操作呢？

个人认为主要有两点原因：

- **字符流是由 Java 虚拟机将字节转换得到的**，这个过程还算是比较耗时；
- 如果我们**不知道编码类型**的话，使用**字节流的过程中很容易出现乱码问题**。

### [java-io流中的设计模式有哪些](https://javaguide.cn/java/io/io-design-patterns.html)

###  Java IO 模型详解
操作系统中把一个进程的空间分为用户空间和内核空间，IO操作大致分两种，一种磁盘IO（**读写文件**）和一种网络IO（网络请求和响应）。因此用户进程来执行IO操作的话，实际上是通过系统调用间接访问系统的内核空间，由操作系统的内核完成IO操作。
应用程序发起一次IO操作会经历两个步骤，内核等待I/O设备准备好数据，内核将数据从内核空间拷贝到用户空间。
UNIX 系统下， IO 模型一共有 5 种：**同步阻塞 I/O**、**同步非阻塞 I/O**、**I/O 多路复用**、**信号驱动 I/O** 和**异步 I/O**。
### Java中常见的I/O模型
#### BIO（**同步阻塞 IO 模型｜Blocking I/O** ）
![[../../article_img/BIOModel.png]]
在应用程序发起read之后，直到内核把数据拷贝到用户空间之前都会一直阻塞。
在客户端连接数量不高的情况下，是没问题的。
但是，当面对十万甚至百万级连接的时候，传统的 BIO 模型是无能为力的。因此，我们需要一种更高效的 I/O 处理模型来应对更高的并发量。

#### NIO（ I/O 多路复用模型｜Non-blocking/New I/O）

同步非阻塞IO模型：同步非阻塞 IO 模型确实有了很大改进。通过轮询操作，避免了一直阻塞。
缺点：应用程序不断进行 I/O 系统调用轮询数据是否已经准备好的过程是十分消耗 CPU 资源的。

同步非阻塞IO模型 不等于 I/O 多路复用模型

NIO它是支持面向缓冲的，基于通道的 I/O 操作方法。 


I/O多路复用模型，其实就是应用程序先向内核发起一次查询，如果要拷贝的资源准备好就直接拷贝，没准备就等数据准备好，再做read进行阻塞拷贝。
优点：IO 多路复用模型，通过减少无效的系统调用，减少了对 CPU 资源的消耗。
场景：对于高负载、高并发的（网络）应用，应使用 NIO 。
![[../../article_img/NIO_IO_Model.png]]

Java 中的 NIO 于 Java 1.4 中引入，对应 `java.nio` 包，提供了 `Channel` , `Selector`，`Buffer` 等抽象。Java 中的 NIO ，有一个非常重要的选择器 ( Selector ) 的概念，也可以被称为 多路复用器。通过它，只需要一个线程便可以管理多个客户端连接。当客户端数据到了之后，才会为其服务。
![[../../article_img/NIO_Buffer_Channel_Selector_relation.png]]

#### AIO（Asynchronous I/O）

 NIO 2。Java 7 中引入了 NIO 的改进版 NIO 2,它是异步 IO 模型。

其实异步 IO 是基于事件和回调机制实现的，也就是应用操作之后会直接返回，不会堵塞在那里，当后台处理完成，操作系统会通知相应的线程进行后续的操作。
![[../../article_img/AIO-ASync_IOModel.png]]

总结场景类型IO的区别：
![[../../article_img/BIOandNIOandAIOCompare.png]]


### [ NIO详解](https://javaguide.cn/java/io/nio-basis.html#nio-%E7%AE%80%E4%BB%8B)｜TODO
#### Buffer

#### Channel

#### Selector