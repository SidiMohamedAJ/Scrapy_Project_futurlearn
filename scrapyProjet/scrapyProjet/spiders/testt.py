import scrapy
from urllib.parse import urljoin


class FuturlearnSpiderSpider(scrapy.Spider):
    allowed_domains = ["www.futurelearn.com"]
    start_urls = ["https://www.futurelearn.com/subjects"]

    def parse(self, response):

        subjects = response.xpath('//p[@class="subjectCard-title_q-L51"]/text()').extract()
        decs = response.xpath('//p[@class="text-module_wrapper__Dg6SG text-module_white__-TrpJ '
                              'text-module_sBreakpointSizesmall__6hBFg text-module_sBreakpointAlignmentleft__NFsd7 '
                              'text-module_isRegular__cAvX9"]/text()').extract()
        linksub = response.xpath('//a[@class="subjectCard-wrapper_jAKp9 subjectCard-navy_8kIz0"]/@href').extract()

        for subject, link, dec in zip(subjects, linksub, decs):
            url = urljoin(self.start_urls[0], link)
            yield {
                'subject': subjects,
                'description': dec,
                'link': url,
            }
            yield scrapy.Request(
                url,
                callback=self.parse_subSubject,
                meta=dict(
                    categorie=subject,
                )
            )

    def parse_subSubject(self, response):
        sub_subjects = response.xpath(
            '//div[@class="RelatedLinks-links_REr4B"]//span[@class="index-module_content__pkuA-"]/span/text()').extract()
        links = response.xpath('//div[@class="RelatedLinks-links_REr4B"]//a/@href').extract()
        decs = response.xpath('//p[@class="Show-displayFromMediumBreakpoint_KMZFt"]/text()').extract()

        for sub_subject, link, dec in zip(sub_subjects, links, decs):
            url = urljoin(response.url, link)
            yield {
                'subject': response.meta['categorie'],
                'sub-subject': sub_subject,
                'description': dec,
                'link': url,

            }

            yield scrapy.Request(
                url,
                callback=self.parse_formation,
                meta=dict(
                    categorie_sub_subject=sub_subject,
                )
            )

    def parse_formation(self, response):
        titles = response.xpath('//div[@class="Title-wrapper_5eSVQ"]/h3/text()').extract()
        links = response.xpath('//div[@class="Body-wrapper_0gskP"]//a[@class="link-wrapper_djqc+ link-inBody_fdO+k '
                               'link-withFlexGrow_8Xelm"]/@href').extract()


        for title, link in zip(titles, links):
            url = urljoin(response.url, link)
            yield {
                'sub-subject': response.meta['categorie_sub_subject'],
                'title': title,
                'link': url,

            }



