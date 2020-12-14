from urllib.request import urlopen
from lxml import etree

from cleaner import clean_all


HTML_PARSER = etree.HTMLParser()

class BaseParser:
    def __init__(self, url):
        self._url = url
        self._html_content = urlopen(self._url)
        self.tree = etree.parse( self._html_content, HTML_PARSER)
    
    def parse(self):
        pass


class CNNParser(BaseParser):
    def __init__(self, url):
        super().__init__(url)
    
    def parse(self):
        title = self.tree.xpath('//h1[@class=\'title\']/text()')[0]
        title = clean_all(title)

        content = self.tree.xpath("//div[@class='container']/div[@class='l_content']/div[@class='content_detail']/div[@class='detail_wrap']/div[@id='detikdetailtext']/p/text()")
        content = ' '.join(content)
        content = clean_all(content)

        return title+' '+content
