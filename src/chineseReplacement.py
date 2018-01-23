from googletrans import Translator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from common import *
import os
import random
from time import sleep


class ChineseReplace:
    def __init__(self, percentage):
        self.percentage = percentage
        self.paths = []
        for root, dirs, files in os.walk(EASY_CLINIC_ENG):
            for _file in files:
                self.paths.append(os.path.join(root, _file))
        self.pack_path = os.path.join(DATA_DIR, self.gen_package_name())
        if not os.path.isdir(self.pack_path):
            os.makedirs(self.pack_path)
        self.stopwords_set = set(stopwords.words('english'))

    def process(self):
        """
        Replace the given percent of english(exclude stopwords) vocabulary into chinese
        :return:
        """

        for path in self.paths:
            word_set = set()
            parent_dir_name = os.path.basename(os.path.dirname(path))
            file_name = os.path.basename(path)
            target_dir = os.path.join(self.pack_path, parent_dir_name)
            if not os.path.isdir(target_dir):
                os.makedirs(target_dir)

            with open(path) as fin, open(os.path.join(target_dir, file_name), 'w', encoding='utf8') as fout:
                text = fin.read().lower()
                tokens = word_tokenize(text)
                word_set.update(tokens)
                self.remove_invalid_tokens(word_set)
                word_sampels = random.sample(word_set, int(len(word_set) * self.percentage))
                trans_dict = self.get_chinese_word_set(word_sampels)
                mixed_tokens = []
                for tk in tokens:
                    if tk in trans_dict:
                        mixed_tokens.append(trans_dict[tk])
                    else:
                        mixed_tokens.append(tk)
                fout.write(" ".join(mixed_tokens))

    def remove_invalid_tokens(self, word_set):
        for stopword in self.stopwords_set:
            word_set.discard(stopword)
        word_copy = list(word_set)
        for word in word_copy:
            if not word.isalpha():
                word_set.remove(word)
        return word_set

    def gen_package_name(self):
        return "docs-{}%".format(round(self.percentage * 100, 2))

    def get_chinese_word_set(self, en_words):
        en_zh = dict()
        translator = Translator()
        for en_word in en_words:
            try:
                ch_wd = translator.translate(en_word, dest='zh-cn').text
                en_zh[en_word] = ch_wd
            except Exception as e:
                print("Error with translating {}, sleep 60s to cool down for google translation".format(en_word))
                sleep(60)
        return en_zh


if __name__ == "__main__":
    percent = 0.2
    for i in range(0, 10):
        percent += 0.1
        print("Processing with {}% mission...".format(percent * 100))
        replace = ChineseReplace(percent)
        replace.process()
        print("finished {}%".format(percent * 100))
    print("finished")
