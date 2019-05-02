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

    def query(self, term):
        with self.ix.searcher() as searcher:
            results = searcher.search(self.qp.parse(term), limit=None)
            data = {}
            data["total"] = len(results)
            result_list = []
            for result in results:
                item = {}
                for key in result.keys():
                    item[key] = result.get(key)
                import re
                match_class = re.compile('class="match term[0-9]"')
                item['description'] = match_class.sub(" ",str(result.highlights('content')))\
                    .replace(" ", "").replace("\r\n", "").replace("\n", "")
                item['description'] = self.truncate_description(item['description'])
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
                item['description'] = match_class.sub(" ",str(result.highlights('content')))\
                    .replace(" ", "").replace("\r\n", "").replace("\n", "")
                item['description'] = self.truncate_description(item['description'])
                result_list.append(item)
            data["results"] = result_list
            return data
            
if __name__ == '__main__':
    query = Query()
    print(query.recommend_news())
