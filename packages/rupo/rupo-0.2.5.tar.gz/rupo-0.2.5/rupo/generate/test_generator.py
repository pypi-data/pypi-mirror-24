# # -*- coding: utf-8 -*-
# # Автор: Гусев Илья
# # Описание: Тесты генератора.

import os
import pickle
from rupo.settings import DATA_DIR, GENERATOR_LSTM_MODEL_PATH
from rupo.generate.grammeme_vectorizer import GrammemeVectorizer
from rupo.generate.word_form_vocabulary import WordFormVocabulary
from rupo.generate.lstm import LSTMGenerator

# if __name__ == "__main__":
#     # filename1 = "/media/data/PoetryMorph.txt"
#     # filename2 = "/media/data/ru-ud-train.txt"
#     dir_name = "/media/data/Datasets/Morpho/clean"
#
#     # vectorizer = GrammemeVectorizer()
#     # vectorizer.collect_grammemes(filename)
#     # print(vectorizer.get_ordered_grammemes())
#     # vectorizer.collect_possible_vectors(filename)
#     # print(vectorizer.vectors)
#     #
#     # vocab = WordFormVocabulary()
#     # vocab.load_from_corpus(filename, grammeme_vectorizer=vectorizer)
#     # print(vocab.word_forms)
#
#     lstm = LSTMGenerator(nn_batch_size=256, embedding_size=5000, recalculate_softmax=True)
#     lstm.prepare([os.path.join(dir_name, filename) for filename in os.listdir(dir_name)])
#     # lstm.build()
#     lstm.load(GENERATOR_LSTM_MODEL_PATH)
#     print(lstm.model.summary())
#     lstm.train([os.path.join(dir_name, filename) for filename in os.listdir(dir_name)], validation_size=1,
#                validation_verbosity=5, dump_model_freq=5)