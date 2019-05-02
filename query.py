from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.qparser.dateparse import DateParserPlugin

from config import config


class Query(object):

    def __init__(self):
        self.ix = index.open_dir(config.index_file_path)

        # Instatiate a query parser
        self.qp = QueryParser("content", self.ix.schema)

        # Add the DateParserPlugin to the parser
        self.qp.add_plugin(DateParserPlugin())

    def query_page(self, term, page_num, page_len, sort_type):
        with self.ix.searcher() as searcher:
            results = searcher.search_page(self.qp.parse(
                term), pagenum=page_num, pagelen=page_len)
            data = {}
            data["total"] = results.total
            result_list = []
            for result in results:
                item = {}
                for key in result.keys():
                    item[key] = result.get(key)
                import re
                match_class = re.compile('class="match term[0-9]"')
                item['description'] = match_class.sub(" ", str(result.highlights('content')))\
                    .replace(" ", "").replace("\r\n", "").replace("\n", "")
                item['description'] = self.truncate_description(
                    item['description'])
                result_list.append(item)
            data["results"] = result_list
            return data

    def truncate_description(self, description):
        """
        Truncate description to fit in result format.
        """
        if len(description) <= 160:
            return description
        cut_desc = description[:160]
        i = 160
        letter = description[i]
        while not (letter == ',' or letter == '，' or letter == '.' or letter == '。'):
            cut_desc += letter
            i = i + 1
            letter = description[i]
        cut_desc += letter
        # print(cut_desc)
        return cut_desc

    def recommend_news(self):
        with self.ix.searcher() as searcher:
            results = searcher.search(self.qp.parse(u"推荐"), limit=None)
            data = {}
            data["total"] = len(results)
            result_list = []
            for result in results:
                item = {}
                for key in result.keys():
                    item[key] = result.get(key)
                import re
                match_class = re.compile('class="match term[0-9]"')
                item['description'] = match_class.sub(" ", str(result.highlights('content')))\
                    .replace(" ", "").replace("\r\n", "").replace("\n", "")
                item['description'] = self.truncate_description(
                    item['description'])
                result_list.append(item)
            data["results"] = result_list
            return data

    def get_recommend_query(self, term):
        recom_query = []
        with self.ix.searcher() as searcher:
            results = searcher.search_page(self.qp.parse(u"推荐"), pagenum=1, pagelen=10)
            for result in results:
                item = {}
                item['term'] = result['title']
                recom_query.append(item)
        return recom_query


if __name__ == '__main__':
    query = Query()
    # print(query.query("测试", 1, 10))
    print(query.get_recommend_query("测试"))
