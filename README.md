# selenium爬取京东商品+MongoDB保存

## 环境

	* PYTHON
	* 已安装MongoDB数据库
	* Chrome浏览器 / chromedriver
	* selenium库
	* pymongo库
	* time库

## 实现思路

	* 定位商品搜索框/提交按钮
	* 模拟输入和搜索
	* 京东商品的展示是先加载一部分，等滑到一半再加载剩下的，这里我直接将滑块拉到最底部
	* 智能等待页面渲染完成
	* 信息提取加保存，自动翻页

## 函数说明

	* get_page()  提交搜索，返回页面
	* get_data()   提取所需信息
	* click_next()  点击下一页
	* save_mongodb()   保存到MongoDB
	* save_excel()   保存成csv文件

## 文件结构

	* data文件夹存放爬取数据

## 闲聊

#### selenium虽然简单方便，但是速度太慢了，要是网页有许多图片又有很多异步加载，那凉凉。但是用selenium来做辅助操作，配合别的库一起使用却有意想不到的效果。

