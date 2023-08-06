import sys
import os
from post_truth_checker.my_parser import MyParser
from post_truth_checker.sources_loader import SourcesLoader
from post_truth_checker.page import Page
from urllib import error
try:
    from google import search
except (ImportError, AttributeError):
    sys.exit("You need google library. Run 'pip install google'.")

max_url_length = 60


def searching(query, sources):
    i = 0
    print('searching...')
    for url in search(query, stop=10, pause=5.0):
        if len(url) < max_url_length:
            i += 1
            print('\n', i, ':')
            try:
                pg = Page(url)
                pg.get_links(sources.fake_sites)
                ci = pg.get_title_clickbait_index(sources.clickbait_words)
                if ci > 3:
                    print('Warning! ', end="")

                print('Clickbait title index of this article is: ', ci)
                oi = pg.get_opinion_index(sources.opinion_words)
                if oi > 3:
                    print('Warning! ', end="")
                print('Opinion index of this article is: ', oi)

            except (error.URLError, error.HTTPError):
                print('Skipped site ', url, "because of url/http error")


def run(query):
    info()
    if not query:
        print("No query was entered. "
              "Type some information you want to check out!")
        return
    badsites = os.path.join(os.path.dirname(__file__), 'badsites.csv')
    baits = os.path.join(os.path.dirname(__file__), 'badsites.csv')
    opinions = os.path.join(os.path.dirname(__file__), 'opinionwords.csv')
    sources = SourcesLoader(badsites, baits, opinions)
    searching(query, sources)


def info():
    print("""Program will check reliability of websites searched from input
                query. Returns indexes of specified reliability from zero
                (nothing suspicious was found), upwards(the higher the worse).
                """)


def main():
    p = MyParser()
    query = p.args.query
    info()
    if query:
        query = query.replace('-', ' ')
    else:
        print("No query was entered. "
              "Type some information you want to check out!")
        return

    sources = SourcesLoader(p.args.badsites, p.args.baits, p.args.opinions)
    searching(query, sources)


if __name__ == "__main__":
    main()
