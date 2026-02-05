# 微信公众号排版规范

## 微信编辑器限制

### 支持的CSS属性
微信编辑器支持大部分内联CSS样式，但有以下限制：

1. **外部CSS文件**：不支持，必须使用内联样式
2. **CSS选择器**：不支持class和id选择器，只能使用内联style属性
3. **部分CSS属性被过滤**：如position: fixed, display: none等可能被过滤
4. **字体限制**：只支持部分中文字体，建议使用系统字体栈

### 推荐字体栈
```html
font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue',
             'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei UI',
             'Microsoft YaHei', Arial, sans-serif;
```

### 安全颜色
微信可能会调整颜色显示，建议使用：
- 正文文字：`#333333` 到 `#666666`
- 标题文字：`#000000`
- 辅助文字：`#999999`
- 链接颜色：`#576b95`

## 排版最佳实践

### 段落设置
```html
<p style="margin: 0 0 20px 0; text-align: justify; color: #333;
          font-size: 15px; line-height: 1.75;">
```

### 标题样式
```html
<h2 style="font-size: 18px; font-weight: bold; color: #000;
           margin: 20px 0 10px 0;">
```

### 图片设置
```html
<img src="图片URL" style="display: block; width: 100% !important;
       height: auto !important; margin-bottom: 8px;" alt="描述">
```

### 列表样式
由于微信可能过滤list-style，建议使用自定义列表：
```html
<div style="display: flex; align-items: flex-start; margin-bottom: 10px;">
  <span style="display: block; width: 5px; height: 5px; background: #000;
               margin-top: 10px; margin-right: 10px; flex-shrink: 0;"></span>
  <span style="font-size: 15px; color: #333;">列表项内容</span>
</div>
```

## 注意事项

1. **图片尺寸**：建议宽度不超过1080px，高度自适应
2. **视频插入**：需要在微信编辑器内插入，HTML中只留占位符
3. **代码块**：微信不支持语法高亮，建议使用图片或简单背景色
4. **特殊字符**：避免使用微信可能过滤的特殊符号
5. **链接**：只能使用微信安全域名下的链接或公众号文章链接

## 模板使用指南

### 模板结构
每个模板包含以下基本组件：
1. 标题样式 (H2/H3)
2. 段落样式
3. 引用块
4. 图片容器
5. 列表样式
6. 分隔线
7. 双栏布局（可选）

### 内容替换
将模板中的示例内容替换为实际文章内容，保持样式不变。

### 样式调整
如需调整颜色、间距等，直接修改内联style属性中的值。