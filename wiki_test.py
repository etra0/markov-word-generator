from markov import Markov
import wikipedia as w

"""This file will download the article "Amor" from wikipedia and will train
the markov chain with that article. """

def get_article():
    w.set_lang('es')
    curr_article = w.page(title="Amor")

    with open("temp.txt", "w") as f:
        f.write(curr_article.content)

# get_article()
spanish = Markov()
spanish.train('temp.txt')
spanish.generate_words(100, min_len=3)
