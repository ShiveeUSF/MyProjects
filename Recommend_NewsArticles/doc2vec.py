import sys
import re
import string
import os
import numpy as np
import codecs

# From scikit learn that got words from:
# http://ir.dcs.gla.ac.uk/resources/linguistic_utils/stop_words
ENGLISH_STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves"])


def load_glove(filename):
    """
    Reads the indicated Glove file and returns a dictionary
    mapping word:vector where vectors are of numpy `array` type.
    """
    gloves = dict()
    with open(filename) as f:
        for line in f:
            words = line.split(' ')   # get list of word and its features for each word
            feature_list = [float(w) for w in words[1:]] # convert features from str to float
            gloves[words[0]] = np.array(feature_list)  # the first item of list is the word and the rest are features
    return gloves


def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    allfiles = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            allfiles.append(os.path.join(path, name))
    return allfiles


def get_text(filename):
    """
    Loads and returns the text of a text file, assuming latin-1 encoding as that
    is what the BBC corpus uses.
    """
    f = codecs.open(filename, encoding='latin-1', mode='r')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, returns a list of words normalized as follows.
    Split the string to make words. Uses regex compile() function to replace numbers and punctuation
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    Remove English stop words
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    words=[w for w in words if w not in ENGLISH_STOP_WORDS]
    return words



def load_articles(articles_dirname, gloves):
    """
    Loads all .txt files under articles_dirname and returns a list of tuples
    where each record is a list of:

      [filename, title, article-text-minus-title, wordvec-centroid-for-article-text]

    We use gloves parameter to compute the word vectors and centroid.
    """

    articles = list()
    allfiles = filelist(articles_dirname)   #fully qualified list of filenames
    for f in allfiles:
        if f.endswith('.txt'):
            data = get_text(f)
            # extract title and text from article
            title = data.split('\n', 1)[0]
            textminustitle = data.split('\n', 1)[1]
            #get the centroid for text
            articlecentroid=doc2vec(textminustitle,gloves)
            # modify filename
            f_strip=f.replace((articles_dirname+'/'),'')
            #create article tuple
            article=(f_strip,title,textminustitle,articlecentroid)
            # add article to list
            articles.append(article)

    return articles



def doc2vec(text, gloves):
    """
    Returns the word vector centroid for the text.
    Ignoring words not in glove.
    """
    articlecentroid = np.array([0])  # initialise the centroid
    article_words = words(text)  # get list of words in article
    n = 0
    for w in article_words:
        # get the wordvec from gloves for w
        if w in gloves:
            n+=1
            wordvec = gloves[w]
            articlecentroid = np.add(articlecentroid,wordvec)  # add each word vec
    if n!=0: articlecentroid = articlecentroid/n
    return articlecentroid



def distances(article, articles):
    """
    Computes the euclidean distance from article to every other article and returns
    a list of (distance, article) tuples for all articles.
    """
    position = 3
    euc_Distances = list()
    given_centroid = article[position]
    for a in articles:
        if a == article: continue  # not adding the article itself in the returning list
        target_centroid = a[position]
        distance = np.linalg.norm(given_centroid - target_centroid)
        euc_Distances.append((distance,a))
    return euc_Distances


def recommended(article, articles, n):
    """
    Returns a list of top n articles closest to article's word vector centroid.
    """
    eucDistances = distances(article,articles)
    eucDistances.sort(key=lambda x:x[0])
    recommendations = [e[1] for e in eucDistances[:n]]
    return recommendations

