import bs4 as bs
import urllib.request
import re
from flask import Flask, render_template, request
import nltk as nltk
import heapq

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('question',
                                      'https://teamtreehouse.com/community/takes-0-positional-arguments-but-1-was-given')
        scraped_data = urllib.request.urlopen(user_input)
        article = scraped_data.read()

        parsed_article = bs.BeautifulSoup(article, 'lxml')

        paragraphs = parsed_article.find_all('p')

        article_text = ""

        for p in paragraphs:
            article_text += p.text

        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        sentence_list = nltk.sent_tokenize(article_text)
        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(6, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        return (summary)

    else:
        return render_template('index.html')


@app.route('/txt', methods=['POST', 'GET'])
def txt():
    if request.method == 'POST':
        paragraphs = request.form.get('question_txt')
        print(paragraphs)
        article_text = ""

        for p in paragraphs:
            article_text += p

        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        sentence_list = nltk.sent_tokenize(article_text)
        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        import heapq
        summary_sentences = heapq.nlargest(6, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        return(summary)

    else:
        return render_template('text.html')


if __name__ == '__main__':
    app.run(debug=True)
