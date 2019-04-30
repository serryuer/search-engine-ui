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
