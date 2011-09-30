from scrapy.spider import BaseSpider, Request
from scrapy.selector import HtmlXPathSelector
from parl import items
import re
import sys

# http://www.parlament.ch/ab/frameset/d/n/4820/361145/d_n_4820_361145_361319.htm
# http://www.parlament.ch/ab/toc/d/n/4820/361145/d_n_4820_361145_361319.htm

class ParlSpider(BaseSpider):
    name = "www.parlament.ch"
    allowed_domains = ["www.parlament.ch"]
    base_url = "http://www.parlament.ch" 
    start_urls = [
        "http://www.parlament.ch/ab/toc/d/n/4820/d_n_4820.htm"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sessions = hxs.select('//a[@id="MeetingTitleLink"]/@href').extract()
        for link in sessions:
            yield Request(self.base_url+link, self.parse_subpage)

    def parse_subpage(self, response):
        hxs = HtmlXPathSelector(response)
        subjects = hxs.select("//a[@id='SubjectTitleLink']/@href").extract()
        for link in subjects:
            yield Request(self.base_url+link.replace("/frameset/", "/toc/"), self.parse_detail)
    
    def parse_detail(self, response):
        hxs = HtmlXPathSelector(response)
        #subjects = hxs.select("//a[@id='SubjectTitleLink']/*/span/text()").extract()
        matchSpeakerInfo = re.compile("^([^(]*) \(([^,]*), (.*)\)$")
        subjects = []
        currentSubject = False
        for tr in hxs.select("//tr"):
            id = tr.select('@id').extract()
            if len(id) > 0:
                if id[0] == "SubjectTitleLine":
                    subjectParts = tr.select(".//span/text()").extract()
                    if currentSubject:
                        subjects.append(currentSubject)
                    currentSubject = items.Subject(id=subjectParts[0], title= " ".join(subjectParts[1:]), speakers=[])
                    
                elif id[0] == "SpeachTitleLine":

                    speakerDesc = tr.select(".//a[@id='SpeachTitleLink']//span/text()").extract()
                    speakerDesc = speakerDesc[0]
                    if speakerDesc:

                        name, group, canton = matchSpeakerInfo.match(speakerDesc).groups()

                        speaker = items.Speaker(name=name, group=group, canton=canton, detailPage=tr.select(".//a[@id='SpeachTitleLink']/@href").extract()[0])
                        # @TODO Cannot access speakers like this, find different solution
                        #currentSubject.speakers.append(speaker)
                        print "Speaker", speaker
        if currentSubject:
            subjects.append(currentSubject)
        print subjects
