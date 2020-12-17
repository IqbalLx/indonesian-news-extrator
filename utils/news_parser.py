from urllib.request import urlopen
from lxml import etree

from utils.cleaner import clean_all


class BaseParser:
    def __init__(self, date=None):
        """format date: DD-MM-YYYY
        """
        self.date = date
        self._html_parser = etree.HTMLParser()
        self.content = None
    
    def parse_date(self):
        day, month, year = self.date.split('-')
        return day, month, year
    
    def extract_articles_link(self, page_num):
        pass
    
    def extract(self, content_tree):
        pass

    def clean(self):
        return clean_all(self.content)

    def parse(self, url):
        html_content = urlopen(url)
        content_tree = etree.parse(html_content, self._html_parser)

        return self.extract(content_tree)
    

class CNNParser(BaseParser):
    def __init__(self, date=None):
        super().__init__(date)
        self.list_url = "https://www.cnnindonesia.com/indeks?date={}/{}/{}&p={}"
    
    def extract_articles_link(self, page_num):
        day, month, year = self.parse_date()
        articles_html = urlopen(self.list_url.format(year, month, day, page_num))

        articles_tree = etree.parse(articles_html, self._html_parser)
        articles_tree = articles_tree.xpath('//div[@class="list media_rows middle"]/article')
        
        for article_tree in articles_tree:
            yield article_tree.xpath('.//a/@href')[0]

    
    def extract(self, content_tree):
        title = content_tree.xpath("//h1[@class='title']/text()")[0]

        content = content_tree.xpath("//div[@class='container']/div[@class='l_content']/div[@class='content_detail']/div[@class='detail_wrap']/div[@id='detikdetailtext']/p/text()")
        content = ' '.join(content)

        self.content = title+' '+content
        return self


class CNBCParser(BaseParser):
    def __init__(self, date=None):
        super().__init__(date)
    
    # TODO
    # def extract_articles_link(self, page_num):
    #   day, month, year = self.parse_date()
        
    def extract(self, content_tree):
        title = content_tree.xpath("//article/div[@class='jdl__']/div[@class='jdl']/div[@class='container']/h1/text()")[0]

        content = content_tree.xpath("//article/div[@class='detail_wrap']/div[@class='detail_text']/p/text()")
        content = ' '.join(content)

        self.content = title+' '+content
        return self

