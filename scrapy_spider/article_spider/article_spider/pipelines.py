# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs,json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class ArticleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipleine(object):
    #自定义json文件导出
    def __init__(self):
        self.file = codecs.open("article.json","w",encoding="utf-8")

    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()

class JsonExporterPipeline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open("articleexport.json","wb")
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii = False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect("172.16.5.250","root","root","article",charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql ="""
            insert into article(title,url,create_date,fav_nums)
            VALUEs (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["title"],item["url"],item["create_date"],item["fav_nums"]))
        self.conn.commit()

class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_setting(cls,settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            charset ="utf-8",
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )


        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def procss_item(self,item,spider):
        #使用twisted将mysql插入变成异步执行
        self.dbpool.runInteraction(self.do_insert,item)

    def do_insert(self,cursor,item):
        insert_sql = """
                    insert into article(title,url,create_date,fav_nums)
                    VALUEs (%s,%s,%s,%s)
                """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))


class ArticleImagePipeline(ImagesPipeline):
    '''
    下载图片的pipline
    '''
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item