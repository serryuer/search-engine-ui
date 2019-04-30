from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.qparser.dateparse import DateParserPlugin


class Query(object):

    def __init__(self):
        self.ix = index.open_dir("../news-crawler/news/index_files")

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
                result_list.append(item)
            data["results"] = result_list
            return data


if __name__ == '__main__':
    query = Query()
    print(query.query(u'中国'))
