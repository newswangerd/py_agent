import nltk
from newspaper import Article

def parse_url(url):
    article = Article(url)

    article.download()
    article.parse()

    # 1 time download of the sentence tokenizer
    nltk.download('punkt')
    article.nlp()

    return article
