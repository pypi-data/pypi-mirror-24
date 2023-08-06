from post_truth_checker.page import Page


def get_base_link_test_http():
    url = 'http//www.wikipedia.com'
    assert Page.get_base_link(url) == 'www.wikipedia.com'


def get_base_link_test_www():
    url = 'www.wikipedia.com'
    assert Page.get_base_link(url) == 'www.wikipedia.com'


def get_base_link_test():
    url = 'wikipedia.com'
    assert Page.get_base_link(url) == 'www.wikipedia.com'


def skip_site_test():
    assert Page.skip_site('google.com', 'facebook.com')
