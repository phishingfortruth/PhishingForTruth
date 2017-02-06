import requests
import shutil
from bs4 import BeautifulSoup
from subprocess import call

newbanner = 'file://~/phishingfortruth/newheader.png'

# assume url starts with http://
fakeurl = 'http://www.breitbart.com/big-journalism/2017/02/04/tancredo-the-disgusting-media-double-standard-between-obama-and-trump/'

shutil.rmtree('test')
call(["httrack", fakeurl, "-O", "test", "--depth=4"])

real = requests.get ('http://www.politifact.com/truth-o-meter/article/2017/feb/01/politifact-sheet-national-security-council-shakeup/')
with open('test/' + fakeurl[6:] + 'index.html', 'r+') as f:
    faketext = f.read()
    f.seek(0)
    f.truncate()

    realsoup = BeautifulSoup(real.text, 'html.parser')
    fakesoup = BeautifulSoup(faketext, 'html.parser')

    # first figure tag is always class='art-block'
    realsoup.find('figure').extract()

    new_tag = fakesoup.new_tag("img", src=newbanner)
    fakesoup.find('div', id='BBStoreFullDesk').replace_with(new_tag)

    realarticle = realsoup.find('article')
    fakearticle = fakesoup.find('article')

    realarticle.attrs = fakearticle.attrs

    fakesoup.find('article').replace_with(realarticle)
    f.write(fakesoup.prettify())
