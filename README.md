
## Problem Set

| Problem | Status|
|---|---|
爬虫 | 于军帅、姜钰宝
索引建立 | 于军帅
基础界面展示 | 于军帅
基础搜索（默认搜索content字段，BM25F排序） | 于军帅
添加新闻来源、时间、类似新闻展示 | 于军帅
首页增加展示热点新闻（需要展示摘要内容） | 于军帅
分页功能 | 于军帅
搜索界面底部（或者右部）显示相关搜索 | 于军帅
界面添加按照时间\热度排序选择框| 于军帅
按照时间排序（读API就可以，尽量不要进行二次搜索） | 于军帅
相似新闻（有类似api） | 于军帅
新闻摘要生成（还不知道怎么从whoosh的索引中得到tfidf数据） | ×
排序函数的重写（Whoosh的默认排序是基于一个字段的BM25F分数，<br>我们想要根据标题和内容的综合检索得分得到排序结果，应该是需要<br>重写whoosh的某些API） | ×
热点新闻（类似于上面的需求，但是要求在所有文档上进行热度排序，<br>不知道有没有类似的API，还可以在给文章建立索引的同时计算它的热度值） | *
相关搜索（whoosh有类似api） | *
通配符索引好像还有点问题 | *

# search-engine-ui
基于 [https://github.com/AnthonySigogne/web-search-engine](https://github.com/AnthonySigogne/web-search-engine)修改

一个简单的搜索引擎界面，基于whoosh全文检索，使用之前需要自行建立索引，可以参考[https://github.com/serryuer/news-crawler-python.git](https://github.com/serryuer/news-crawler-python.git)，爬新闻并建立索引

索引文件夹位置配置在config.py文件：
```
class Config(object):

    index_file_path='**/**'
    
```

## 环境

**Python3.6/Ubuntu18**

- 安装依赖
```
pip install -r requirements.txt
```

## 运行

```
./start.sh
```
<center>
<img src="https://github.com/serryuer/search-engine-ui/raw/master/images/home.png" width=100% height=100%/>"
<center>
<img src="https://github.com/serryuer/search-engine-ui/raw/master/images/search.png" width=100% height=100%/>"

