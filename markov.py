import pandas as pd
import numpy as np
import numpy.random as nr
import random as r
import re

letters = list("abcdefghijklmnñopqrstuvwxyz ")

def clean_tildes(text):
    """En el caso del español, tenemos las tildes que no importan en este contexto, por lo tanto
    son quitadas."""
    special_chars = { 'á': 'a',
            'é': 'e',
            'í': 'i',
            'ó': 'o',
            'ú': 'u' }

    for char in special_chars:
        text = text.replace(char, special_chars[char])

    return text

class Markov:
    """
    This is a class that have a main matrix called main_dataframe that will contain the entire
    alphabet in the rows and columns.
    Basically will calculate the probability of the next char depending on the current char.
    """

    # actual variable that will contain mostly all the information.
    main_dataframe = None

    def __init__(self):
        temp_dict = dict()
        for letter in letters:
            # we create every letter with zeroes.
            temp_dict[letter] = [0 for _ in range(len(letters))]

        self.main_dataframe = pd.DataFrame(data=temp_dict, index=letters)

    def __str__(self):
        return self.main_dataframe.__str__()

    def prepare_line(self, line):
        """Do some stuff with the line, not intended to be used out of the
        class"""

        # we need to delete all the points and commas
        separators_regex = re.compile(r"\.|,|¿|\?|_|-|\(|\)|=|\[|\]")

        line = line.lower()
        line = line.strip()
        # we clean!
        line = clean_tildes(line)
        line = separators_regex.sub("", line)

        return line

    def train(self, source):
        """Trains the model with a source, currently can support just one source.
        args:
            source: the name of the file (including path)
        """

        with open(source, 'r') as main_file:
            for line in main_file:
                line = self.prepare_line(line)

                if len(line) == 1:
                    continue

                for i in range(len(line) - 1):
                    curr_char = line[i]
                    next_char = line[i + 1]

                    if curr_char not in letters or next_char not in letters:
                        continue

                    self.main_dataframe.loc[curr_char][next_char] += 1

                # count the last char as space
                if curr_char in letters:
                    self.main_dataframe.loc[curr_char][' '] += 1

        for index in self.main_dataframe.index:
            # we have to ask the case when it's zero!
            total = self.main_dataframe.loc[index].sum()
            if total:
                self.main_dataframe.loc[index] = \
                     self.main_dataframe.loc[index]/total

    def generate_words(self, quantity, min_len=0):
        """Once is trained, this function can generate words,
            args:

            quantity: the quantity of words that you want
            min_len=0: the minimum length of a word.
        """
        i = 0
        while i < quantity:
            word = ''
            selected_char = ' '
            ready = False

            while not ready:

                selected_char = nr.choice(self.main_dataframe.columns,
                        p=self.main_dataframe.loc[selected_char])
                word += selected_char

                if selected_char == ' ':
                    ready = True
            if len(word) > min_len + 1:
                i += 1
                print(word)

if __name__ == '__main__':
    spanish = Markov()
    spanish.train('test.txt')
    spanish.generate_words(100)
