from googletrans import Translator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
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
            print("Processing {}".format(path))
            parent_dir_name = os.path.basename(os.path.dirname(path))
            file_name = os.path.basename(path)
            target_dir = os.path.join(self.pack_path, parent_dir_name)
            if not os.path.isdir(target_dir):
                os.makedirs(target_dir)

            with open(      ) as fin:
                en_sentences = fin.readlines()
                en_sentences = [sent.strip("\n\t\r ") for sent in en_sentences]
                zh_sentences = self.translate_sentences(en_sentences)

    def gen_package_with_percentage(self, percentage, en_sentences, zh_sentences):
        with open(os.path.join(target_dir, file_name), 'w', encoding='utf8') as fout:
            mixed_sentences = []
            sent_num = len(en_sentences)
            picked_nums = random.sample([i for i in range(0, sent_num)], int(self.percentage * sent_num))
            for i in range(0, sent_num):
                if i in picked_nums:
                    mixed_sentences.append(zh_sentences[i] + "\n")
                else:
                    mixed_sentences.append(en_sentences[i] + "\n")
            fout.writelines(mixed_sentences)

    def gen_package_name(self):
        return "docs-{}%".format(round(self.percentage * 100, 2))

    def translate_sentences(self, en_sentences):
        res = []
        translator = Translator()
        for en_word in en_sentences:
            try:
                ch_sentence = translator.translate(en_word, dest='zh-cn').text
                res.append(ch_sentence)
            except Exception as e:
                print("Error with translating {}, sleep 60s to cool down for google translation".format(en_word))
                sleep(60)
        return res


if __name__ == "__main__":
    percent = 0.0
    for i in range(0, 1):
        percent += 0.1
        print("Processing with {}% mission...".format(percent * 100))
        replace = ChineseReplace(percent)
        replace.process()
        print("finished {}%".format(percent * 100))
    print("finished")
