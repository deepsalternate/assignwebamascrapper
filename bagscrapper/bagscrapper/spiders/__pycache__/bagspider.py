import scrapy


class BagspiderSpider(scrapy.Spider):
    name = "bagspider"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/s?k=bags"]
    def parse(self, response):
        bags=response.css('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2')
        for bag in bags:
            relative_url= bag.css('h2 a').attrib['href']  # check this first
            bag_url='https://www.amazon.in' + relative_url
        yield scrapy.Request(bag_url,callback=self.parse_bag_page)


        ## next page
        next_page=response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()

        for i in range (19):
            next_page_url='https://www.amazon.in' + next_page
            yield response.follow(next_page_url, callback=self.parse)
        # ANOTHER WAY TO MAKE CRAWL TO PAGES THROUGH THIS BELOW LOGIC 
        # last_page="https:/www.amazon.in/s?k=bags//s?k=bags&page=21"
        # if next_page is not last_page:
        #     next_page_url='https://www.amazon.in/s?k=bags/' + next_page
        #     yield response.follow(next_page_url, callback=self.parse)
        

    def parse_bag_page(self, response):       
        bag = bag=response.css('div#centerCol')
        # table_rows = response.css("table tr")
        detail=response.css("div#detailBullets_feature_div")
        Desc=response.css("div#productDescription")
        yield {
            'url': response.url,
            'title': bag.css('span.a-size-large.product-title-word-break::text').get().strip(),
            'manufacturer': detail.xpath("//*[@id=\"detailBullets_feature_div\"]/ul/li[3]/span/span[2]/text()").get(),
            'ASIN': detail.xpath("//*[@id=\"detailBullets_feature_div\"]/ul/li[4]/span/span[2]/text()").get(),
            # 'price_excl_tax': table_rows[2].css("td ::text").get(),
            # 'price_incl_tax': table_rows[3].css("td ::text").get(),
            # # 'tax': table_rows[4].css("td ::text").get(),
            # # 'availability': table_rows[5].css("td ::text").get(),
            'ratingstars': bag.css("span.a-size-base::text").get(),
            'noofreview': bag.css("span#acrCustomerReviewText::text").get(),
            # 'category': book.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description': Desc.xpath("//*[@id=\"productDescription\"]/p/span/text()").get(),
            'price': bag.css('span.a-price-whole::text').get().strip(),
        }
    




#                SIMPLE VERSION TO TEST TO CHECK IF WORKING PROPERLY .
# import scrapy            testing simple version data on page iteself.
# class BagspiderSpider(scrapy.Spider):
#     name = "bagspider"
#     allowed_domains = ["www.amazon.in"]
#     start_urls = ["https://www.amazon.in/s?k=bags"]


#     def parse(self, response):
#         bags = response.css('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2')
#         for bag in bags:
#             yield{
#                 'name' : bag.css('span.a-size-medium.a-color-base.a-text-normal::text').get(),
#                 'price' : bag.css('span.a-price-whole::text').get(),
#             }
        
#         next_page=response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').get()
#         last_page="https:/www.amazon.in/s?k=bags&page=22"
#         if next_page is not last_page:
#             next_page_url='https://www.amazon.in' + next_page
#             yield response.follow(next_page_url, callback=self.parse)