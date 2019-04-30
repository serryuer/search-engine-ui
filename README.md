
## Problems Set
- 页面添加新闻来源和发布时间（前端相关）
- 首页增加展示热点新闻（前端相关）
- 分页功能（前端相关）
- 新闻摘要生成（还不知道怎么从whoosh的索引中得到tfidf数据）
- 新闻摘要的展示（鼠标悬浮在标题上时展示）
- 排序函数的重写（Whoosh的默认排序是基于一个字段的BM25F分数，我们想要根据标题和内容的综合检索得分得到排序结果，应该是需要重写whoosh的某些API）
- 按照时间排序（读API就可以，尽量不要进行二次搜索）
- 热点新闻（类似于上面的需求，但是要求在所有文档上进行热度排序，不知道有没有类似的API，还可以在给文章建立索引的同时计算它的热度值）

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
conda install --yes --file requirements.txt
```


## 运行

```
./start.sh
```

