class SourcesLoader:
    def __init__(self, unreliable_sites, clickbait, opinion):
        self.fake_sites = {line.rstrip()
                           for line in open(unreliable_sites, "r")}
        self.clickbait_words = {line.rstrip().lower()
                                for line in open(clickbait, "r")}
        self.opinion_words = {line.rstrip().lower()
                              for line in open(opinion, "r")}
