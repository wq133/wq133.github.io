---
layout: post
title: 开发总结（二）
subtitle: Mybatis、Mybatis-plus...
date: 2024-05-16
author: Wu
header-img: ../article_img/SL_1.jpg
tags:
  - Java
  - Mybatis
  - 开发总结
---

Mybatis

## 注解
@TableName
@TableId
@TableField
@EnumValue
@Value
@TableLogic
## 动态SQL

1. 常用标签
```xml
<select></select>
<update></update>
<insert></insert>
<delete></delete>

<foreach></foreach>
<if></if>
```
2. [动态foreach使用](https://link.juejin.cn/?target=https%3A%2F%2Fwww.hxstrive.com%2Farticle%2F359.htm "https://www.hxstrive.com/article/359.htm")
```xml
<select id="getUserInfo" parameterType="hashmap" resultType="hashmap">SELECT N_USERID, C_NAME, C_SEX, N_AGE FROM T_USER  
    WHERE N_USERID IN     <foreach item="myItem" index="index" collection="myList" open="(" separator="," close=")">  
        #{myItem}  
    </foreach>  
</select> 
<insert>  
insert into purchase_record (id,product_name,trigger_time,username,type,record_template_id) values <foreach  
        collection="list" separator="," item="item">(  
    #{item.id},#{item.productName},#{item.triggerTime},#{item.username},#{item.type},#{item.recordTemplateId})  
</foreach> ....  
</insert>
```

3. [CASE THEN WHEN用法](https://link.juejin.cn/?target=https%3A%2F%2Fzhuanlan.zhihu.com%2Fp%2F550518885 "https://zhuanlan.zhihu.com/p/550518885")
```xml
<select id="getOutStockApply" parameterType="com.boot.reservation.entity.domain.qo.OutStockQO"
            resultType="com.boot.reservation.entity.outstock.OutStockApplyDTO">
            select
            *,
            ( CASE
                            WHEN STATUS = '00' THEN '已保存'
                            WHEN STATUS = '01' THEN '待审核'
                            WHEN STATUS = '02' THEN '已通过'
                            WHEN STATUS = '03' THEN '已驳回'
                          END ) status,
            file_id fileId,
            pic_id picId
            from
            storage_out_stock_apply
            where
            apply_out_stock_serial_num = #{applyOutStockSerialNum}
```
两种写法
```
# 简洁写法
CASE sex  
WHEN ‘1’ THEN ‘男’  
WHEN ‘2’ THEN ‘女’  
ELSE ‘其他’ END
```

```
# 搜索函数写法
CASE 
WHEN sex = ‘1’ THEN ‘男’  
WHEN sex = ‘2’ THEN ‘女’  
ELSE ‘其他’ END
```

4. resultMap和resultType

  resultType 用于返回值只有一个字段的类型，resultMap 用于返回值有多个字段的类型。
```xml
<!-- resultMap --> <resultMap id="BaseResultMap" type="cn.scpro.model.UserInfo">         <id column="id" property="id" jdbcType="INTEGER"/>         <result column="name" property="name" jdbcType="VARCHAR"/>         <result column="doccode" property="doccode" jdbcType="VARCHAR"/>         <result column="telno" property="telno" jdbcType="VARCHAR"/> </resultMap>
```

```xml
<!-- resultType -->  
<select id="getAge" resultType="java.lang.Integer">
SELECT age FROM USER WHERE id = 1   
</select>
```

```xml
<select id="select" resultType="Person">
SELECT * FROM Person WHERE state = ‘ACTIVE’
	<choose>         
		<when test="title != null">
				   AND title like #{title}
		</when>         
		<when test="sex != null">
				   AND sex = #{sex}
		</when>
		<otherwise>
				  AND height = 170         
		</otherwise>
   </choose>
</select>
```

5. 实体类查询条件

实体查询条件一般是指提取出公共的搜索条件，以便多次复用。
```xml
<!-- 实体类查询条件 -->     
<sql id="conditionExample">
	<where>             
		<if test="example.id != null">
		AND id = #{example.id}             
		</if>             
		<if test="example.name != null">
		AND name = #{example.name}             
		</if>            
		<if test="example.doccode != null">
		AND doccode = #{example.doccode}             
		</if>             
		<if test="example.telno != null">
		AND telno = #{example.telno}             
		</if>         
	</where>
</sql>
```

6. 查询字段名

查询字段名，需要返回的字段信息，提取出来复用，包含基本的和指定字段。一般是使用指定字段，以提高查询效率。
```xml
<!-- 查询字段名 --> 
<sql id="Base_Column_List">
	id,
	name,
	doccode,
	telno	 
</sql>
```
7. 主键查询

主键查询，根据主键查询相关对象信息。
```xml
<!-- 主键查询 --> 
<select id="selectByPrimaryKey" resultMap="BaseResultMap"             parameterType="java.lang.Integer">
	select <include refid="Base_Column_List"/>
	from user_info         
	where id = #{id}     
</select>
```

8. 插入数据 返回主键

  新增数据，并返回主键信息，方式一：使用useGeneratedKeys="true" 和keyProperty="id"。
```xml
<!-- 插入数据 返回主键--> 
<insert id="insertSelective" parameterType="cn.scpro.model.UserInfo" useGeneratedKeys="true" keyProperty="id">insert  
    into user_info  
    <trim prefix="(" suffix=")" suffixOverrides=",">  
        <if test="id != null">id,</if>  
        <if test="name != null">name,</if>  
        <if test="doccode != null">doccode,</if>  
        <if test="telno != null">telno,</if>  
    </trim>    <trim prefix="values (" suffix=")" suffixOverrides=",">  
        <if test="id != null">#{id},</if>  
        <if test="name != null">#{name,jdbcType=VARCHAR},</if>  
        <if test="doccode != null">#{doccode},</if>  
        <if test="telno != null">#{telno,jdbcType=VARCHAR},</if>  
    </trim></insert>
```

9. 插入数据返回主键

  新增数据，并返回主键信息，方式二：使用selectKey。
```xml
<!--插入数据返回主键2 -->  
<insert id="insertTaskHistory" parameterType="cn.scpro.model.UserInfo">insert into user_info  
    <trim prefix="(" suffix=")" suffixOverrides=",">  
        <if test="userinfo.name != null">name,</if>  
        <if test="userinfo.doccode != null">doccode,</if>  
        <if test="userinfo.telno != null">telno,</if>  
    </trim>    <trim prefix="values (" suffix=")" suffixOverrides=",">  
        <if test="userinfo.name != null">#{userinfo.name,jdbcType=VARCHAR},</if>  
        <if test="userinfo.doccode != null">#{userinfo.doccode,jdbcType=VARCHAR},</if>  
        <if test="userinfo.telno != null">#{userinfo.telno,jdbcType=VARCHAR},</if>  
    </trim>    <selectKey resultType="java.lang.Integer" order="AFTER" keyProperty="userinfo.id">SELECT id FROM user_info ORDER BY  
        id DESC LIMIT 0,1  
    </selectKey>  
</insert>
```

10. 更新数据

  根据对象更新数据信息
```xml
<!-- 更新数据 -->  
<update id="updateByPrimaryKeySelective" parameterType="cn.scpro.model.UserInfo">update user_info  
    <set>  
        <if test="name != null">name = #{userinfo.name,jdbcType=VARCHAR},</if>  
        <if test="doccode != null">doccode = #{userinfo.doccode},</if>  
        <if test="telno != null">telno = #{userinfo.telno,jdbcType=VARCHAR},</if>  
    </set>    where id = #{userinfo.id}  
</update>
```

11. 批量新增数据

  批量插入数据，以List为例。
```xml
<!-- 插入list -->  
<insert id="insertNotifylist" parameterType="java.util.List" useGeneratedKeys="true">insert into user_info values  
    <foreach  
            collection="userlist" item="item" index="index" separator=",">  
        (#{item.name,jdbcType=VARCHAR},#{item.doccode,jdbcType=VARCHAR}, #{item.telno,jdbcType=VARCHAR})  
    </foreach>  
</insert>
```
12. 批量更新数据

  批量更新数据，以List为例。
```xml
<!-- 更新list-->  
<update id="UpdateById">update user_info set name= null where id in  
    <foreach collection="list" item="id"  
             separator="," open="(" close=")">  
        #{id}  
    </foreach>  
</update>
```
13. 批量删除数据

  批量删除数据，以List为例。
```xml
<!-- 删除list -->  
<delete id="DeleteById" parameterType="java.util.List">delete from user_info where id in  
    <foreach  
            collection="list" item="id" separator="," open="(" close=")">#{id}  
    </foreach>  
</delete>
```

14. 查多个对象
  继承map，可查多项个实体
```xml
<!-- 继承map，可查多项个实体 -->  
<resultMap id="BaseResultMapForMore" type="com.test.model.User" extends="BaseResultMap">  
    <collection property="score" ofType="com.test.model.Score" column="userid" javaType="com.test.model.Score"  
                select="com.test.mapper.ScoreMapper.findByuserid"></collection>  
    <collection property="teacherlist" ofType="com.test.model.Teacher" column="teacherid"  
                javaType="com.test.model.Teacher"  
                select="com.test.model.TeacherMapper.findById"></collection>  
    <collection property="homeinfo"  
                ofType="com.test.model.Home" column="homeid"  
                javaType="com.test.model.Home"  
                select="com.test.mapper.HomeMapper.findById">  
    </collection></resultMap>
```
15. if条件查询
if标签：`<if test="dto.isSend == null or dto.isSend == false"></if>`

16.  set 元素来实现类似于 where 元素的功能。在如下的示例中，set 元素确保了 SQL 语句中的 SET 永远是合法的，它能自动处理 SET 为空、结尾多逗号，并自动拼接 SET 字符串。
```xml
<update id="update">update Person  
    <set>  
        <if test="title != null">title=#{title},</if>  
        <if test="sex != null">sex=#{sex},</if>  
    </set>    where id=#{id}  
</update>
```
17. trim标签:动态地处理字符串前缀、后缀以及空格问题，常用于构建`WHERE`子句时去除不必要的`AND`或`OR`。
```xml
<select id="selectUsers" parameterType="map" resultType="User">  
    SELECT * FROM user  
    <where>  
        <!-- 使用trim去除多余的AND -->  
        <trim prefix="AND" prefixOverrides="AND">  
            <if test="username != null and username != ''">  
                username = #{username}  
            </if>  
            <if test="email != null and email != ''">  
                AND email = #{email}  
            </if>  
            <if test="age != null">  
                AND age = #{age}  
            </if>  
        </trim>    </where></select>
```
## mybatis-plus函数

`.eq().like() 三个参数`
- 第一个参数：**condition标识表条件，条件在if中成立才会拼接sql**,hi
- 第二个参数：**条件字段（Employee::getId）**,
- 第三个参数：**值**

`.selectPage(new page<1,2>,wrapper)` 分页返回Ipage 对象
wrappers创建方式:
2.X版本
`new Condition();`
`new EntityWrapper();`
3.X版本
`LambdaQueryWrapper<YourEntity> lambdaQuery = Wrappers.lambdaQuery();`
`QueryWrapper<YourEntity> query = new QueryWrapper<>();`

版本差异：
- selectOne 变更为： getOne
- insert 变更为： save
- EntityWrapper 变更为： QueryWrapper

`.saveBatch(Collection<T> entryList)`批量插入
`.apply()` 应用查询条件
`.last("limit 1")` 无视规则拼接到sql的最后，有sql注入的风险。只能调用一次，多次调用以最后一次为准。

`.select()`
作用
- 查询多个字段。 
- 指定字段,断言查询。
- 方法带有一个@SafeVarargs，意味安全的可变长的字符。

`.groupBy("order_id")`

`ne()`就是 not equal不等于

`gt()` 就是 greater than大于

`lt()` 就是 less than小于

`ge()` 就是 greater than or equal 大于等于

`le()` 就是 less than or equal 小于等于

`in()` 就是 in 包含（数组）

`isNull()` 就是 等于null

`between()` 就是 在2个条件之间(**包括边界值**)

`like()` 模糊查询 `like CONCAT('%',#{dto.customerName},'%' ))`



## 参考链接
- [Mybatis参考文档](https://github.com/zwwhnly/mybatis-action?tab=readme-ov-file)
- [MyBatis 常用语法汇总](https://juejin.cn/user/2040300414187416/posts)
- [caseWhen用法](https://zhuanlan.zhihu.com/p/550518885)
- [Mybatis-Demo参考](https://juejin.cn/user/3245414056985831/posts)
- [Mybatis常用注解](https://juejin.cn/post/7317278802727256075?searchId=2024051417310161DB1178CC603F14A0CC#heading-6)
- [Mybatis版本差异问题](https://blog.csdn.net/lxy13122589680/article/details/104552654)
- [2.1.9的mybatis-plus-boot-starter,无法使用QueryWrapper](https://www.imooc.com/qadetail/325262 )




