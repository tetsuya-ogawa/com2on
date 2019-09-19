# -*- coding: utf-8 -*-
import scrapy
from ..items import *
from s3pipeline import Page

class ScrapyRikunabiSpider(scrapy.Spider):
    name = 'scrapy_rikunabi'
    allowed_domains = ['job.rikunabi.com']

    # 企業ページ一覧 今は2020バージョン
    start_urls = ['https://job.rikunabi.com/2020/s/']

    def parse(self, response):

        # 各セレクターを定義。css変わっちゃったらここを変更すればok
        list_item_selector = 'ul.ts-h-search-cassetteWrapper li.ts-h-search-cassette'
        a_tag_selector = '.ts-h-search-cassetteTitle a::attr(href)'
        next_link_selector = 'a.ts-h-search-pagerBtn_next::attr(href)'

        # response.css で scrapy デフォルトの css セレクタを利用できる
        for item in response.css(list_item_selector):
            # items に定義した Item のオブジェクトを生成して次の処理へ渡す
            company = Company()
            url = response.urljoin(item.css(a_tag_selector).extract_first().strip())
            # company['name'] = item.css('h2').text()
            company['url'] = url
            yield company

        # 再帰的にページングを辿るための処理
        next_link = response.css(next_link_selector).extract_first()

        if next_link is not None:
            # URLが相対パスだった場合に絶対パスに変換する
            next_link = response.urljoin(next_link)

            # 次のページをのリクエストを実行する
            yield scrapy.Request(next_link, callback=self.parse)

