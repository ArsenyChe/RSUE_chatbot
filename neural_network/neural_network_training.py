import random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import json

import numpy as np

from tensorflow.keras.layers import Dense, LSTM, SpatialDropout1D, Bidirectional, Embedding # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from tensorflow.keras.utils import to_categorical # type: ignore

class NeuralNetworkTraining:
    def __init__(self, file_path):
        self.file_path = file_path
        self.all_patterns = []
        self.element_counter = []
        self.number_intent_patterns = []
        self.Y = None
        self.max_words_count = 10000
        self.max_text_len = 20
        self.tokenizer = Tokenizer(num_words=self.max_words_count, filters='!–"—#$%&amp;()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r«»', lower=True, split=' ', char_level=False)
        self.model = Sequential()

    def read_data(self):
        with open(self.file_path, "r", encoding='utf-8') as my_file:
            data_json = my_file.read()
            data = json.loads(data_json)
            len_json = len(data["intents"])
            self.element_counter = [i for i in range(0, len_json)]
            for i in data["intents"]:
                pattern = i["patterns"]
                self.all_patterns += pattern
                self.number_intent_patterns.append(len(pattern))
            self.Y = np.array([to_categorical(self.element_counter)[0]]*self.number_intent_patterns[0])
            for i in range(1, len_json):
                self.Y = np.append(self.Y, [to_categorical(self.element_counter)[i]]*self.number_intent_patterns[i], axis=0)

    def preprocess_data(self):
        self.tokenizer.fit_on_texts(self.all_patterns)
        data = self.tokenizer.texts_to_sequences(self.all_patterns)
        data_pad = pad_sequences(data, maxlen=self.max_text_len)
        indeces = np.random.choice(data_pad.shape[0], size=data_pad.shape[0], replace=False)
        X = data_pad[indeces]
        self.Y = self.Y[indeces]
        return X, self.Y

    def build_model(self):
        self.model.add(Embedding(self.max_words_count, 64, input_length=self.max_text_len))
        self.model.add(SpatialDropout1D(0.4))
        self.model.add(Bidirectional(LSTM(32, activation='elu', dropout=0.05, recurrent_dropout=0.2)))
        self.model.add(Dense(len(self.element_counter), activation='sigmoid'))  # Добавляем softmax, если классификация на несколько классов

    def train_model(self, X_train, Y_train, train_batch_size, train_epochs):
        self.model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=Adam(0.0001))
        self.model.fit(X_train, Y_train, batch_size=train_batch_size, epochs=train_epochs)
        self.model.export('trained_neural_network')

    def get_sequence_to_text(self,list_of_indices):
        reverse_word_map = dict(map(reversed, self.tokenizer.word_index.items()))
        words = [reverse_word_map.get(letter) for letter in list_of_indices]
        return(words)
    
    def get_answer(self, text):
        data = self.tokenizer.texts_to_sequences([text.lower()])
        data_pad = pad_sequences(data, maxlen=self.max_text_len)
        print( self.get_sequence_to_text(data[0]) )

        result = self.model.predict(data_pad)
        print(result, np.argmax(result), sep='\n')

        with open(self.file_path, "r", encoding='utf-8') as my_file:
            data_json = my_file.read()
            data = json.loads(data_json)
            item = data["intents"][np.argmax(result)]
            print(item['tag'], random.choice(item['responses']))