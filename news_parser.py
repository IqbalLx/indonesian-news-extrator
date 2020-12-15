from urllib.request import urlopen
from lxml import etree

from cleaner import clean_all


class BaseParser:
    def __init__(self, url):
        self._url = url
        self._html_content = urlopen(self._url)
        self._html_parser = etree.HTMLParser()
        self.tree = etree.parse(self._html_content, self._html_parser)
    
    def parse(self):
        pass


class CNNParser(BaseParser):
    def __init__(self, url):
        super().__init__(url)
    
    def parse(self):
        title = self.tree.xpath("//h1[@class='title']/text()")[0]
        title = clean_all(title)

        content = self.tree.xpath("//div[@class='container']/div[@class='l_content']/div[@class='content_detail']/div[@class='detail_wrap']/div[@id='detikdetailtext']/p/text()")
        content = ' '.join(content)
        content = clean_all(content)

        return title+' '+content


class CNBCParser(BaseParser):
    def __init__(self, url):
        super().__init__(url)
    
    def parse(self):
        title = self.tree.xpath("//article/div[@class='jdl__']/div[@class='jdl']/div[@class='container']/h1/text()")[0]
        title = clean_all(title)

        content = self.tree.xpath("//article/div[@class='detail_wrap']/div[@class='detail_text']/p/text()")
        content = ' '.join(content)
        content = clean_all(content)

        return title+' '+content

