# Content based recommendation engine.

This is a recommendation engine that shows a list of BBC news articles to the user. When the user clicks on a particular article, the article content is displayed and system recommends similar articles to the user to make the system more engaging.

I used Glove pretrained word embeddings to find similar articles to the one user is reading. Used Flask to create UI. The recommendation engine is designed to run as a Web service on AWS server.

GloVe is an unsupervised learning algorithm for obtaining vector representations for words. Training is performed on aggregated global word-word co-occurrence statistics from a corpus, and the resulting representations showcase interesting linear substructures of the word vector space.

