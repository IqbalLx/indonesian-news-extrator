import scrapy

from cnn_indonesia import cleaner

DATE = "2020-11-18"
year, month, date = DATE.split('-')

class CnnindonesiaSpider(scrapy.Spider):
    name = 'cnnIndonesia'
    allowed_domains = ['cnnindonesia.com']

    n_pages = 2
    page = 1 
    start_urls = [f'https://cnnindonesia.com/indeks?date={year}/{month}/{date}&p={page}']


    def parse(self, response):
        articles = response.xpath('//div[@class="list media_rows middle"]/article')
        print(articles)
        for article in articles:
            article_link = article.xpath('./a/@href').extract_first()
            yield scrapy.Request(article_link, callback=self.parse_article)


        if self.page < self.n_pages:
            self.page += 1
            yield scrapy.Request(f'https://cnnindonesia.com/indeks?date={year}/{month}/{date}&p={self.page}', callback=self.parse)
    

    def parse_article(self, response):
        title = response.xpath('//h1[@class=\'title\']/text()').extract_first()
        title = cleaner.clean_punc(title)

        content = response.xpath("//div[@class='container']/div[@class='l_content']/div[@class='content_detail']/div[@class='detail_wrap']/div[@id='detikdetailtext']/p").extract()
        content = ' '.join(content)
        content = cleaner.clean_all(content)

        if not content == "":
            yield {
                "date": DATE,
                "title": title,
                "content": content
            }
