
# 创建一个钩子来在构建期间修改Markdown 中渲染的 HTML 图像标签来解决此问题。
# 本质上，尝试将字符串插入标签的属性 ../article_img替换成 /article_img

Jekyll::Hooks.register :posts, :post_render do |post|
  post.output.gsub!('<img src="../article_img', '<img src="/article_img')
end
