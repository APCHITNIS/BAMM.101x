# Your code from here
import csv



def get_musicians(file):
    import codecs
    from bs4 import BeautifulSoup
    f = codecs.open(file, 'r', 'utf-8')
    soup = BeautifulSoup(f.read(), 'lxml')
    l = list()
    for a in soup.find_all('a', href=True, title=True, text=True):
        if a['title'] == a.get_text():
            if '_' in a['href']:
                if a['href'].count('_') == 1:
                    l.append("https://en.wikipedia.org" + a['href'])
    return l


def get_text(name: object) -> object:
    import codecs
    from bs4 import BeautifulSoup
    f = codecs.open(name, 'r', 'utf-8')
    page_soup = BeautifulSoup(f.read(), 'lxml')
    all_text = ""
    for tag in page_soup.find_all('p'):
        all_text += tag.get_text()

    return all_text


def run():
    import os
    from gensim import corpora
    from gensim.parsing.preprocessing import STOPWORDS

    doc_list = [entry for entry in os.scandir('samples')]

    documents = [get_text(doc) for doc in doc_list]
    texts = [[word for word in document.lower().split()
              if word not in STOPWORDS and word.isalnum()]
             for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    from gensim import models, similarities
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

    test_list = [entry for entry in os.scandir('test 3')]

    for test in test_list:
        vec_bow = dictionary.doc2bow(get_text(test).lower().split())
        vec_lsi = lsi[vec_bow]
        index = similarities.MatrixSimilarity(lsi[corpus])
        sims = index[vec_lsi]
        # print(sims)
        # d.append(test, doc_list[sims])

    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    d = list()
    d.append(("TestName", "SampleName"))
    i = 0

    for sim in sims:
        if i >= len(test_list):
            break
        t = test_list[i].name
        i = i + 1
        t = str(t).split('.')[0]
        s = doc_list[sim[0]].name
        s = str(s).split('.')[0]

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
