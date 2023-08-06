import urllib
from bs4 import BeautifulSoup
from urllib.request import Request
import urllib.request


class Page:
    def __init__(self, url):
        self.url = url
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        self.page = urllib.request.urlopen(req)
        self.soup = BeautifulSoup(self.page, "html5lib")

    def get_title_clickbait_index(self, clickbait_words):
        try:
            title = self.soup.title.string
        except AttributeError:
            return 0
        title = title.split(' ')
        counter = 0
        for t in title:
            if t.lower() in clickbait_words or t.isdigit():
                counter += 1
            if '?' in t or '!' in t:
                counter += 2
        return counter

    def get_opinion_index(self, opinion_words):
        text = self.soup.find_all('p')
        counter = 0
        for line in text:
            words = str(line).split(' ')
            for word in words:
                if word.lower() in opinion_words:
                    counter += 1

        return counter

    def get_links(self, fake_sites):
        s = set()
        print(self.url)

        for tag in self.soup.findAll('a', href=True):
            tag['href'] = urllib.parse.urljoin(self.url, tag['href'])
            if not self.skip_site(self.url, tag['href']):
                s.add(self.get_base_link(tag['href']))
        for site in s:
            if site in fake_sites or (self.get_base_link(self.url)
                                      in fake_sites):
                print('contains link to unreliable site ' + site)

    @staticmethod
    def skip_site(url1, url2):
        s1 = Page.get_base_link(url1)
        s2 = Page.get_base_link(url2)
        return (s1 == s2 or
                'twitter' in url2 or 'facebook' in url2)

    @staticmethod
    def get_base_link(url):
        s1 = url.split('/')

        if 'http:' in s1 or 'https:' in s1:
            return s1[2]

        elif 'www' in s1[0]:
            return s1[0]
        else:
            s1[0] = 'www.' + s1[0]
            return s1[0]
