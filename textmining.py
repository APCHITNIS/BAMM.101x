import os
import csv
from gensim import corpora
from gensim.parsing.preprocessing import STOPWORDS


# Your code from here
def get_musicians(file):
    import codecs
    from bs4 import BeautifulSoup
    f = codecs.open(file, 'r', 'utf-8')
    soup = BeautifulSoup(f.read(), 'lxml')
    #
    # Question 1
    #
    l = list()
    for a in soup.find_all('a', href=True, title=True, text=True):
        if a['title'] == a.get_text():
            if '_' in a['href']:
                if a['href'].count('_') == 1:
                    l.append("https://en.wikipedia.org" + a['href'])
    return l


def get_text(file):
    import codecs
    from bs4 import BeautifulSoup
    f = codecs.open(file, 'r', 'utf-8')
    #
    # Question 2
    #
    page_soup = BeautifulSoup(f.read(), 'lxml')
    all_text = ""
    for tag in page_soup.find_all('p'):
        all_text += tag.get_text()

    return all_text


def run():
    #
    # Question 3
    #
    # This function can be quite long!
    #
    # Hint: You should create a dataframe df with two columns,
    # TestName, SampleName
    # then dump this dataframe in a csv with the code:
    #
    # df.to_csv('output.csv',index=False)
    doc_list = [entry for entry in os.listdir('samples')]

    documents = [get_text("./samples/" + doc) for doc in doc_list]
    texts = [[word for word in document.lower().split()
              if word not in STOPWORDS and word.isalnum()]
             for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    from gensim import models, similarities
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

    test_list = [entry for entry in os.listdir('test 3')]
    d = []

    d.append(("TestName", "SampleName"))

    for test in test_list:
        vec_bow = dictionary.doc2bow(get_text("./test 3/" + test).lower().split())
        vec_lsi = lsi[vec_bow]
        index = similarities.MatrixSimilarity(lsi[corpus])
        sims = index[vec_lsi]

        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        t = str(test).split('.')[0]
        s = doc_list[sims[0][0]].split('.')[0]
        d.append((t, s))

    return d


# datafile = "boogiewoogie.html"
# data = get_musicians(datafile)
# print(data)

# datafile = "carolinedahl.html"
# data = get_text(datafile)
# print(data)

# all_text = ""
# for entry in os.scandir('samples'):
#     all_text += get_text(entry)
# print(all_text)


d = run()
with open('output.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
    for list in d:
        wr.writerow(list)
