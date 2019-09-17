# -*- coding: utf-8 -*-
import scrapy
from ..items import *
from s3pipeline import Page

class ScrapyRikunabiSpider(scrapy.Spider):
    name = 'scrapy_rikunabi'
    allowed_domains = ['job.rikunabi.com']

    # 企業ページ一覧 今は2021バージョン
    start_urls = ['https://job.rikunabi.com/2021/search/pre/company/result/?isc=r21rcnc00711']

    def parse(self, response):
        # response.css で scrapy デフォルトの css セレクタを利用できる
        for item in response.css('ul.ts-p-search-cassetteList li.ts-p-search-cassetteList-item'):
            # items に定義した Item のオブジェクトを生成して次の処理へ渡す
            company = Company()
            url = response.urljoin(item.css('h2 a::attr(href)').extract_first().strip())
            # company['name'] = item.css('h2').text()
            company['url'] = url
            yield company

        # 再帰的にページングを辿るための処理
        next_link = response.css('a.ts-p-search-pager02-list-item_next::attr(href)').extract_first()

        if next_link is not None:
            # URLが相対パスだった場合に絶対パスに変換する
            next_link = response.urljoin(next_link)

            # 次のページをのリクエストを実行する
            yield scrapy.Request(next_link, callback=self.parse)

