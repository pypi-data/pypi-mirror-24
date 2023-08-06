This program was created in order to help distinguish fake news/clickbait article from reliable one. It is based on:
  - blacklist sites which have poor reputation
  - title expressions generally considered as clickbaits
  - opinion expressions, which is non-neutral and creates a special view on issue

It won't clearly show you forbidden sites, but as a result it returns top websites links with indexes of untrust.
Indexes starts at 0 which means that in the article was not found any suspected expressions.
The higher returned index is, the more untrusted site it is. You should think twice before you click on them.

## How to use
1. Run python and then:
 >>> from post_truth_checker import main
 >>> main.run('expression')
where <expression> is a phrase you want to test out. The phrase have to be in quotation signs.
