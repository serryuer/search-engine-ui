from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.qparser.dateparse import DateParserPlugin

from whoosh.sorting import FieldFacet

from config import config

from whoosh.classify import Bo1Model

from whoosh.searching import Results
from whoosh.searching import ResultsPage


class Query(object):

    def __init__(self):
        self.ix = index.open_dir(config.index_file_path)

        # Instatiate a query parser
        self.qp = QueryParser("content", self.ix.schema)

        # Add the DateParserPlugin to the parser
        self.qp.add_plugin(DateParserPlugin())

    def _results_todata(self, results):
            data = {}
            if isinstance(results, Results):
                data["total"] = results.estimated_length()
            elif isinstance(results, ResultsPage):
                data['total'] = results.total
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

    def query_page(self, term, page_num, page_len, sort_type):

        with self.ix.searcher() as searcher:
            if sort_type == 1:# default sorted
                results = searcher.search_page(self.qp.parse(
                    term), pagenum=page_num, pagelen=page_len)
            if sort_type == 2:# sorted by publish time
                publish_time = FieldFacet("publish_time", reverse=True)
                results = searcher.search_page(self.qp.parse(
                    term), pagenum=page_num, pagelen=page_len, sortedby=publish_time)
            if sort_type == 3:# sorted by custom hot value
                publish_time = FieldFacet("publish_time", reverse=True)
                results = searcher.search_page(self.qp.parse(
                    term), pagenum=page_num, pagelen=page_len, sortedby=publish_time)
            
            return self._results_todata(results)

    def truncate_description(self, description):
        """
        Truncate description to fit in result format.
        """
        if len(description) <= 160:
            return description
        cut_desc = description[:160]
        i = 160
        letter = description[i]
        length = len(description)
        while i < length - 1 and not (letter == ',' or letter == '，' or letter == '.' or letter == '。'):
            cut_desc += letter
            i = i + 1
            letter = description[i]
        cut_desc += letter
        # print(cut_desc)
        return cut_desc

    def recommend_news(self):
        with self.ix.searcher() as searcher:
            results = searcher.search(self.qp.parse(u"推荐"), limit=None)
            return self._results_todata(results)

    def get_recommend_query(self, term):
        recom_query = []
        with self.ix.searcher() as searcher:
            results = searcher.search_page(
                self.qp.parse(u"推荐"), pagenum=1, pagelen=10)
            for result in results:
                item = {}
                item['term'] = result['title']
                recom_query.append(item)
        return recom_query

    def search_more_like_this(self, url, fieldname, top):
        with self.ix.searcher() as searcher:
            docnum = searcher.document_number(url=url)
            results = searcher.more_like(docnum, fieldname, text=None,
                                top=top, numterms=5, model=Bo1Model,
                                normalize=True, filter=None)

            return self._results_todata(results)



if __name__ == '__main__':
    query = Query()
    # print(query.query("测试", 1, 10))
    # print(query.query_page(u"测试", 1, 10, 1))

    # query.query_page("测试",1,10, 1)
    query.recommend_news()
    # query.get_recommend_query("测试")
