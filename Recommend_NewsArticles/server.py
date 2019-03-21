# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
from doc2vec import *
import sys

app = Flask(__name__)

@app.route("/")
def articles():
    """Shows a list of article titles"""
    return render_template('articles.html', all_articles=all_articles)

def search(topic, filename, all_artciles):
    f = topic+'/'+filename
    for a in all_artciles:
        if a[0] == f:
            return a


@app.route("/article/<topic>/<filename>")
def article(topic,filename):
    """
    Shows an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    f = topic + '/' + filename
    for a in all_articles:
        if a[0] == f:
            recommend=recommended(a, all_articles, 5)
            return render_template('article.html', the_article=a, recommend=recommend)

# initialization
i = sys.argv.index('server:app')
glove_filename = sys.argv[i+1]
articles_dirname = sys.argv[i+2]

gloves = load_glove(glove_filename)
all_articles = load_articles(articles_dirname, gloves)
#app.run('0.0.0.0')



