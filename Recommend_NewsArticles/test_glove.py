import sys

from doc2vec import *

def search(topic, filename, all_artciles):
    f = topic + '/' + filename
    print(f)
    for a in all_artciles:
        print(a[0])
        if a[0]==f:
            return a


if __name__ == '__main__':
    glove_filename = sys.argv[1]
    articles_dirname = sys.argv[2]

    gloves = load_glove(glove_filename)
    articles = load_articles(articles_dirname, gloves)
    #print(articles[:1])

    #print(gloves['dog'])

    #f='/Users/shivee/data/bbc/business/0030.txt'

    article=search('business','030.txt',articles)
    print(article)
    recommend=recommended(article,articles,5)
    for i in recommend:
        print(recommend[1])




