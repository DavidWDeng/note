# -*- coding: utf-8 -*-
import scrapy,re,datetime
from scrapy.http import Request
import urlparse
from ArticleSpider.items import JobBoleArdigitaloceandigitaloceandigitaloceanticleItem
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1,获取文章列表页中的文章url并交给scrapy下载后进行解析
        2，获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        :param response:
        :return:
        '''
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            yield Request(url=urlparse.urljoin(response.url,post_url),meta={'front_image_url':image_url},callback = self.parse_detail)

        #提取下一页并交给scrapy下载
        next_url = response.css('.next.page-numbers::attr(href)').extract_first('')
        if next_url:
            yield Request(url=urlparse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self,response):
        article_item = JobBoleArticleItem()
        #提取文章的具体字段
        front_imgae_url = response.meta.get('front_image_url','')
        title = response.css('.entry-header h1::text').extract()[0]
        create_date = response.css('.entry-meta-hide-on-mobile::text').extract()[0].strip()[0:10]
        praise_nums = int(response.css('.vote-post-up h10::text').extract()[0])
        fav_num = response.css('.btn-bluet-bigger.href-style.bookmark-btn.register-user-only::text').extract()[0]
        match_re = re.match('.*?(\d+).*?', fav_num)
        if match_re:
            fav_num = int(match_re.group(1))
        else:
            fav_num = 0
        com_num = response.css('.btn-bluet-bigger.href-style.hide-on-480 ::text').extract()[0]
        match_re = re.match('.*?(\d+).*?', com_num)
        if match_re:
            com_num = int(match_re.group(1))
        else:
            com_num = 0
        content = response.css('.entry').extract()[0]
        tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        tags = ','.join(tag_list)

        article_item['url_object_id'] = get_md5(response.url)
        article_item['title'] = title
        article_item['url'] = response.url
        try:
            create_date = datetime.datetime.strptime(create_date,'%Y/%m/%d').date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item['create_date'] = create_date
        article_item['front_image_url'] ={front_imgae_url}
        article_item['praise_nums'] = praise_nums
        article_item['comment_nums'] = com_num
        article_item['fav_nums'] = fav_num
        article_item['tags'] = tags
        article_item['content'] = content

        #通过Item Loader加载Item
        item_loader = ItemLoader(item= JobBoleArticleItem(),response=response)
        item_loader.add_css('title','.entry-header h1::text')
        item_loader.add_value('url',response.url)



        yield article_item

        pass
