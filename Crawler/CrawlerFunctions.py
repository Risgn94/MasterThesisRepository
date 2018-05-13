from bs4 import BeautifulSoup
import requests

#Crawler helper class
class Crawler:
    def __init__(self, row=None):
        self.row = row
        self.url = self.row['Link']

        headers = {
            'User-Agent': 'My User Agent 1.0',
            'From': 'youremail@domain.com'  # This is another valid field
        }

        self._page = requests.get(self.url, headers=headers).content
        self.soup = BeautifulSoup(self._page, "lxml")

    def crawl(self, path):
        print(self.row['Link'])
        articleContainer = self.soup.select(path)

        articleArray = []

        for idx, elem in enumerate(articleContainer):
            articleArray.append(elem.decode_contents(formatter="html"))

        if(len(articleArray) < 1):
            articleContainer = self.soup.select(path.replace("div", "p"))

            articleArray = []

            for idx, elem in enumerate(articleContainer):
                articleArray.append(elem.decode_contents(formatter="html"))

            if (len(articleArray) < 1):
                return "None"

        return "".join(articleArray)


#If statement helper function
def domainStatement(row, url):
    return row['Domain'] == url

def runCrawl(row):
    if(domainStatement(row, "http://www.ibtimes.com/")):
        return Crawler(row).crawl(".article-body p")

    elif(domainStatement(row, "http://www.4-traders.com/")):
        return Crawler(row).crawl("#grantexto p")

    elif(domainStatement(row, "http://www.marketwatch.com/")):
        return Crawler(row).crawl("#article-body p")

    elif(domainStatement(row, "http://www.prnewswire.com/")):
        return Crawler(row).crawl(".release-body p[itemprop='articleBody']")

    elif(domainStatement(row, "http://www.business-standard.com/")):
        cResponse = Crawler(row).crawl(".p-content p")

    elif(domainStatement(row, "http://www.ibtimes.co.uk/")):
        return Crawler(row).crawl("#v_main p")

    elif(domainStatement(row, "http://www.reuters.com/")):
        return Crawler(row).crawl(".body_1gnLA p")

    elif(domainStatement(row, "https://www.marketwatch.com/")):
        return Crawler(row).crawl("#article-body p")

    elif(domainStatement(row, "http://www.themalaymailonline.com/")):
        return Crawler(row).crawl(".article-content p")

    elif(domainStatement(row, "https://techcrunch.com/")):
        return Crawler(row).crawl(".article-content p")

    elif(domainStatement(row, "http://www.theage.com.au/")):
        return Crawler(row).crawl("._1665V.undefined p")

    elif(domainStatement(row, "http://www.brisbanetimes.com.au/")):
        return Crawler(row).crawl("article p")

    elif(domainStatement(row, "http://www.thehindu.com/")):
        return Crawler(row).crawl(".article p")

    elif(domainStatement(row, "https://article.wn.com/")):
        return Crawler(row).crawl(".wn-article p")

    elif(domainStatement(row, "http://www.tri-cityherald.com/")):
        return Crawler(row).crawl("#content-body- p")

    elif(domainStatement(row, "http://www.newindianexpress.com/")):
        return Crawler(row).crawl("#storyContent p")

    elif(domainStatement(row, "http://www.businesstimes.com.sg/")):
        return Crawler(row).crawl(".field.field-name-body.field-type-text-with-summary.field-label-hidden p")

    elif(domainStatement(row, "http://wsau.com/")):
        return Crawler(row).crawl(".post-body p")

    elif(domainStatement(row, "http://www.dw.com/")):
        return Crawler(row).crawl(".longText p")

    elif(domainStatement(row, "https://www.yahoo.com/")):
        return Crawler(row).crawl(".canvas-body p")

    elif(domainStatement(row, "http://www.finanznachrichten.de/")):
        return Crawler(row).crawl("#artikelTextPuffer")

    elif(domainStatement(row, "http://www.channelnewsasia.com/")):
        return Crawler(row).crawl(".c-rte--article p")

    elif(domainStatement(row, "http://www.beaumontenterprise.com/")):
        return Crawler(row).crawl(".article-body p")

    elif(domainStatement(row, "http://www.straitstimes.com/")):
        return Crawler(row).crawl(".odd.field-item p")

    elif(domainStatement(row, "http://www.watoday.com.au/")):
        return Crawler(row).crawl(".article__body p")

    elif(domainStatement(row, "http://gulfnews.com/")):
        return Crawler(row).crawl(".wrapper-details p")

    elif(domainStatement(row, "http://www.financialexpress.com/")):
        return Crawler(row).crawl(".main-story-content p")

    elif(domainStatement(row, "http://www.nzherald.co.nz/")):
        return Crawler(row).crawl("#article-content p")

    elif(domainStatement(row, "http://www.theregister.co.uk/")):
        return Crawler(row).crawl("#body p")

    elif(domainStatement(row, "http://www.cnbc.com/")):
        return Crawler(row).crawl("#article_body p")

    elif(domainStatement(row, "https://www.afp.com/")):
        return Crawler(row).crawl(".article-entry p")

    elif(domainStatement(row, "http://www.zdnet.com/")):
        return Crawler(row).crawl(".storyBody p")

    elif(domainStatement(row, "http://www.scmp.com/")):
        return Crawler(row).crawl(" .panel-pane.pane-entity-field.pane-node-body.pane-first.pos-0 .pane-content p")

    elif(domainStatement(row, "https://www.prnewswire.com/")):
        return Crawler(row).crawl(".release-body p")

    elif(domainStatement(row, 'https://www.benzinga.com/')):
        return Crawler(row).crawl('.article-content-body-only p')

    elif(domainStatement(row, 'http://www.hindustantimes.com/')):
        return Crawler(row).crawl('.story-details p')

    elif (domainStatement(row, 'http://www.mirror.co.uk/')):
        return Crawler(row).crawl('.article-body p')

    elif (domainStatement(row, 'http://www.mondovisione.com/')):
        return Crawler(row).crawl('.entry-content p')

    elif(domainStatement(row, 'https://tribune.com.pk/')):
        return Crawler(row).crawl('.clearfix.story-content.read-full p')

    elif(domainStatement(row, 'https://www.khaleejtimes.com/')):
        return Crawler(row).crawl('.articlepage_content_zz p')

    elif(domainStatement(row, 'http://www.newsweek.com/')):
        return Crawler(row).crawl('.article-body p')

    elif(domainStatement(row, 'http://www.taipeitimes.com/')):
        return Crawler(row).crawl('.text p')

    elif(domainStatement(row, 'http://economictimes.indiatimes.com/')):
        return Crawler(row).crawl('.Normal')

    elif(domainStatement(row, 'http://www.euronews.com/')):
        return Crawler(row).crawl('.js-responsive-iframes-container p')

    elif(domainStatement(row, 'http://www.independent.co.uk/')):
        return Crawler(row).crawl('.text-wrapper p')

    elif(domainStatement(row, 'http://newsok.com/')):
        return Crawler(row).crawl('.body.p402_premium p')

    elif(domainStatement(row, 'http://www.firstpost.com/')):
        return Crawler(row).crawl('.article-full-content p')

    elif(domainStatement(row, 'http://www.foxbusiness.com/')):
        return Crawler(row).crawl('.article-content.content.article-body p')

    elif(domainStatement(row, 'http://www.cbc.ca/')):
        return Crawler(row).crawl('.story-content p')

    elif(domainStatement(row, 'http://in.reuters.com/')):
        return Crawler(row).crawl('.body_1gnLA p')

    elif(domainStatement(row, 'http://www.thestar.com.my/')):
        return Crawler(row).crawl('#slcontent_0_sleft_0_storyDiv p')

    elif(domainStatement(row, 'http://www.bbc.co.uk/')):
        return Crawler(row).crawl('.story-body__inner p')

    elif(domainStatement(row, 'https://www.theguardian.com/')):
        return Crawler(row).crawl('.content__article-body.from-content-api.js-article__body p')

    elif(domainStatement(row, 'http://www.bostonherald.com/')):
        return Crawler(row).crawl('.content-body p')

    elif(domainStatement(row, 'http://www.theglobeandmail.com/')):
        return Crawler(row).crawl('.c-article-body.js-c-article-body.u-clearfix p')

    elif(domainStatement(row, 'http://www.wftv.com/')):
        return Crawler(row).crawl('.mod-body.story-body p')

    elif(domainStatement(row, 'http://www.kiro7.com/')):
        return Crawler(row).crawl('.mod-body.story-body p')

    elif(domainStatement(row, 'http://huffingtonpost.com/')):
        return Crawler(row).crawl('.entry__body.js-entry-body p')

    elif(domainStatement(row, 'https://www.siliconrepublic.com/')):
        return Crawler(row).crawl('div[itemprop=articleBody] p')

    elif(domainStatement(row, 'https://www.usatoday.com/')):
        return Crawler(row).crawl('.asset-double-wide.double-wide.p402_premium p')

    elif(domainStatement(row, 'http://www.actionnewsjax.com/')):
        return Crawler(row).crawl('.mod-body.story-body p')

    elif(domainStatement(row, 'https://www.businesslive.co.za/')):
        return Crawler(row).crawl('.text p')

    elif(domainStatement(row, 'https://uk.reuters.com/')):
        return Crawler(row).crawl('.body_1gnLA p')

    elif(domainStatement(row, 'http://www.smh.com.au/')):
        return Crawler(row).crawl('._1665V.undefined p')

    elif(domainStatement(row, 'http://www.miamiherald.com/')):
        return Crawler(row).crawl('.content-body p')

    elif(domainStatement(row, 'http://www.fox13memphis.com/')):
        return Crawler(row).crawl('.mod-body.story-body p')

    elif(domainStatement(row, 'http://www.digitaljournal.com/')):
        return Crawler(row).crawl('.body')

    elif(domainStatement(row, 'https://www.rt.com/')):
        return Crawler(row).crawl('.article__text p')

    elif(domainStatement(row, 'http://www.wsoctv.com/')):
        return Crawler(row).crawl('.mod-body.story-body p')

    elif(domainStatement(row, 'http://www.dailymail.co.uk/')):
        return Crawler(row).crawl('div[itemprop=articleBody] p')

    elif(domainStatement(row, 'https://www.washingtonpost.com/')):
        return Crawler(row).crawl('.paywall p')

    elif(domainStatement(row, 'https://www.technologyreview.com/')):
        return Crawler(row).crawl('.article-body__content p')

    elif(domainStatement(row, 'http://www.ibtimes.co.in/')):
        return Crawler(row).crawl('http://www.ibtimes.co.in/ p')

    elif(domainStatement(row, 'http://www.abc.net.au/')):
        return Crawler(row).crawl('.article.section p')

    elif(domainStatement(row, 'https://www.seattletimes.com/')):
        return Crawler(row).crawl('.article-body.e-content p')

    elif(domainStatement(row, 'http://www.bostonglobe.com/')):
        return Crawler(row).crawl('.article-content p')

    elif(domainStatement(row, 'http://www.theherald.com.au/')):
        return Crawler(row).crawl('.sticky-container p')

    elif(domainStatement(row, 'http://www.radioaustralia.net.au/')):
        return Crawler(row).crawl('.node-inner p')

    elif(domainStatement(row, 'http://news.abs-cbn.com/')):
        return Crawler(row).crawl('.article-content p') #skal være (0)

    elif(domainStatement(row, 'http://www.houstonchronicle.com/')):
        return Crawler(row).crawl('.article-text p')

    elif(domainStatement(row, 'https://investingnews.com/')):
        return Crawler(row).crawl('.entry.blog_entry p')

    elif(domainStatement(row, 'http://nypost.com/')):
        return Crawler(row).crawl('.entry-content.entry-content-read-more p')

    elif(domainStatement(row, 'https://www.wired.com/')):
        return Crawler(row).crawl('.article-body-component p')

    elif(domainStatement(row, 'http://indianexpress.com/')):
        return Crawler(row).crawl('.full-details p')

    elif(domainStatement(row, 'https://www.cnbc.com/')):
        return Crawler(row).crawl('#article_body p')

    elif(domainStatement(row, 'http://money.cnn.com/')):
        return Crawler(row).crawl('#storytext p')

    elif(domainStatement(row, 'http://english.vietnamnet.vn/')):
        return Crawler(row).crawl('.article_content p')

    elif(domainStatement(row, 'http://www.koreatimes.co.kr/')):
        return Crawler(row).crawl('.view_article span')

    elif(domainStatement(row, 'https://www.cnet.com/')):
        return Crawler(row).crawl('.article-main-body p')

    elif(domainStatement(row, 'https://www.dailysabah.com/')):
        return Crawler(row).crawl('.txtInWrapper p')

    elif(domainStatement(row, 'https://betanews.com/')):
        return Crawler(row).crawl('.body.clearfix p')

    elif(domainStatement(row, 'https://www.theepochtimes.com/')):
        return Crawler(row).crawl('.post_content p')

    elif(domainStatement(row, 'https://www.engadget.com/')):
        return Crawler(row).crawl('.article-text p')

    elif(domainStatement(row, 'http://www.bangkokpost.com/')):
        return Crawler(row).crawl('.articleContents p')

    elif(domainStatement(row, 'http://www.seattletimes.com/')):
        return Crawler(row).crawl('.article-content p')

    elif(domainStatement(row, 'http://www.news18.com')):
        return Crawler(row).crawl('#article_body')

    elif(domainStatement(row, 'https://www.thesun.co.uk/')):
        return Crawler(row).crawl('.article')

    elif(domainStatement(row, 'http://www.illawarramercury.com.au/')):
        return Crawler(row).crawl('.article__body.news-article-body')

    elif(domainStatement(row, 'https://www.nytimes.com/')):
        return Crawler(row).crawl('.story-body.story-body-1 p')

    elif(domainStatement(row, 'https://patch.com/')):
        return Crawler(row).crawl('#article-wrapper p')

    elif(domainStatement(row, 'http://investingnews.com/')):
        return Crawler(row).crawl('.entry.blog_entry p')

    elif(domainStatement(row, 'https://www.fnlondon.com/')):
        return Crawler(row).crawl('#fn-article-wrap p')

    elif(domainStatement(row, 'https://www.fnlondon.com/')):
        return Crawler(row).crawl('#fn-article-wrap p')

    elif (domainStatement(row, 'https://www.theregister.co.uk/')):
        return Crawler(row).crawl('#body p')

    elif (domainStatement(row, 'https://www.timesofmalta.com/')):
        return Crawler(row).crawl('#article_body p')

    elif (domainStatement(row, 'http://www.independent.ie/')):
        return Crawler(row).crawl('.body p')

    elif (domainStatement(row, 'http://www.shanghaidaily.com/')):
        return Crawler(row).crawl('.detail_content.detail_content_news p')

    elif (domainStatement(row, 'https://www.geo.tv/')):
        return Crawler(row).crawl('.content-area p')

    elif (domainStatement(row, 'http://techcrunch.com/')):
        return Crawler(row).crawl('.content p')

    elif (domainStatement(row, 'http://www.stuff.co.nz/')):
        return Crawler(row).crawl('#content p')

    elif (domainStatement(row, 'http://english.china.com/')):
        return Crawler(row).crawl('.article-content p')

    elif (domainStatement(row, 'http://www.foxnews.com/')):
        return Crawler(row).crawl('.article-text')

    elif (domainStatement(row, 'https://www.irishtimes.com/')):
        return Crawler(row).crawl('.article_bodycopy p')

    elif (domainStatement(row, 'http://www.thedailystar.net/')):
        return Crawler(row).crawl('.node-content p')

    elif (domainStatement(row, 'http://www.japantimes.co.jp/')):
        return Crawler(row).crawl('.entry:nth-of-type(2) p')

    elif (domainStatement(row, 'http://www.techrepublic.com/')):
        return Crawler(row).crawl('.article-social p')

    elif (domainStatement(row, 'https://www.thestar.com/')):
        return Crawler(row).crawl('.article__body.clearfix article-story-body')

    elif (domainStatement(row, 'https://www.stuff.co.nz/')):
        return Crawler(row).crawl('.story_landing p')

    elif (domainStatement(row, 'https://www.iol.co.za/')):
        return Crawler(row).crawl('.article-body span')

    elif (domainStatement(row, 'https://globalnews.ca/')):
        return Crawler(row).crawl('.story-txt p')

    elif (domainStatement(row, 'https://www.independent.ie/')):
        return Crawler(row).crawl('.body p')

    elif (domainStatement(row, 'http://www.usatoday.com/')):
        return Crawler(row).crawl('.p402_hide:nth-of-type(1) p') #skal være (1)

    elif (domainStatement(row, 'http://www.irishtimes.com/')):
        return Crawler(row).crawl('.article_bodycopy p')

    elif (domainStatement(row, 'http://www.cityam.com/')):
        return Crawler(row).crawl('.article p')

    elif (domainStatement(row, 'http://www.680news.com/')):
        return Crawler(row).crawl('#article-body-content p')

    elif (domainStatement(row, 'http://metro.co.uk/')):
        return Crawler(row).crawl('.article-body p')

    elif (domainStatement(row, 'https://moneyweek.com/')):
        return Crawler(row).crawl('.entry-content.p1 p')

    elif (domainStatement(row, 'http://www.irishexaminer.com/')):
        return Crawler(row).crawl('.ctx_content p')

    elif (domainStatement(row, 'http://wwlp.com/')):
        return Crawler(row).crawl('.entry-content-wrap p')

    elif (domainStatement(row, 'http://www.arkansasonline.com/')):
        return Crawler(row).crawl('#storyBody p')

    elif (domainStatement(row, 'https://www.cbsnews.com/')):
        return Crawler(row).crawl('.entry p')

    elif (domainStatement(row, 'http://www.enca.com/')):
        return Crawler(row).crawl('.article-text p')

    elif (domainStatement(row, 'http://uk.reuters.com/')):
        return Crawler(row).crawl('.StandardArticleBody_body_1gnLA')

    elif (domainStatement(row, 'http://www.washingtontimes.com/')):
        return Crawler(row).crawl('.storyareawrapper p')

    elif (domainStatement(row, 'http://www.manilatimes.net/')):
        return Crawler(row).crawl('.post-content-right p')

    elif (domainStatement(row, 'https://sputniknews.com/')):
        return Crawler(row).crawl('.b-article p')

    elif (domainStatement(row, 'http://www.asiaone.com/')):
        return Crawler(row).crawl('.field.field-name-body p')

    elif (domainStatement(row, 'https://www.thenational.ae/')):
        return Crawler(row).crawl('.article-content.text-content:nth-of-type(1) p') #skal være (1)

    elif (domainStatement(row, 'http://guardian.ng/')):
        return Crawler(row).crawl('.single-article-content p')

    elif (domainStatement(row, 'http://www.ecns.cn/')):
        return Crawler(row).crawl('.content p')

    elif (domainStatement(row, 'http://www.khaleejtimes.com/')):
        return Crawler(row).crawl('.articlepage_content_zz p')

    elif (domainStatement(row, 'http://punchng.com/')):
        return Crawler(row).crawl('.entry-content p')

    elif (domainStatement(row, 'https://www.clickondetroit.com/')):
        return Crawler(row).crawl('.story-content p')

    elif (domainStatement(row, 'https://nypost.com/')):
        return Crawler(row).crawl('.entry-content entry-content-read-more p')

    elif (domainStatement(row, 'http://www.hellenicshippingnews.com/')):
        return Crawler(row).crawl('.entry:nth-of-type(1) p')

    elif (domainStatement(row, 'http://www.dnaindia.com/')):
        return Crawler(row).crawl('.col-md-8 p')

    elif (domainStatement(row, 'http://www.rttnews.com/')):
        return Crawler(row).crawl('#ctl00_CPI_dvBody p')

    elif (domainStatement(row, 'http://www.india.com/')):
        return Crawler(row).crawl('.articleBody p')

    elif (domainStatement(row, 'http://news.trust.org/')):
        return Crawler(row).crawl('.body-text.left p')

    elif (domainStatement(row, 'http://www.atimes.com/')):
        return Crawler(row).crawl('.content-read-more:nth-of-type(0) p') #

    elif (domainStatement(row, 'https://www.bangkokpost.com/')):
        return Crawler(row).crawl('.entry p')

    elif (domainStatement(row, 'http://www.nationmultimedia.com/')):
        return Crawler(row).crawl('.p:nth-of-type(1) p') #skal være (1)

    elif (domainStatement(row, 'https://www.ipe.com/')):
        return Crawler(row).crawl('.storytext p') #skal være (1)

    elif (domainStatement(row, 'https://www.theglobeandmail.com/')):
        return Crawler(row).crawl('.c-article-body p') #skal være (1)

    elif (domainStatement(row, 'https://www.channelnewsasia.com/')):
        return Crawler(row).crawl('.c-article--default:nth-of-type(1) p') #skal være (1)

    elif (domainStatement(row, 'http://www.startribune.com/')):
        return Crawler(row).crawl('.article-body p')

    elif (domainStatement(row, 'https://www.beaumontenterprise.com/')):
        return Crawler(row).crawl('.article-body p')
    #

    else:
        return "None"
    #elif(domainStatement(row, 'https://southfront.org/')):
    #   return Crawler(row).crawl(.123)

