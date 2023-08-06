import argparse


class MyParser:

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-q', '--query',
                            help='query you want to check',
                            type=str, default='Global warming')
        parser.add_argument('-u', '--badsites',
                            help='list of unreliable sites',
                            type=str, default='badsites.csv')
        parser.add_argument('-b', '--baits',
                            help='list of baits expressions',
                            type=str, default='baits.csv')
        parser.add_argument('-o', '--opinions',
                            help='list of opinion expressions',
                            type=str, default='opinionwords.csv')

        self.args = parser.parse_args()
