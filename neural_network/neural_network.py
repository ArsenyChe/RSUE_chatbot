from neural_network.neural_network_training import NeuralNetworkTraining
import random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import json
import numpy as np
from tensorflow.keras.layers import TFSMLayer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore

class NeuralNetwork(NeuralNetworkTraining):
    def __init__(self, file_path):
        super().__init__(file_path)

    def get_answer(self, text):
        model_loaded=TFSMLayer('trained_neural_network', call_endpoint="serve")
        data = self.tokenizer.texts_to_sequences([text.lower()])
        data_pad = pad_sequences(data, maxlen=self.max_text_len)
        print( self.get_sequence_to_text(data[0]))

        result = model_loaded(data_pad)
        print(result, np.argmax(result), sep='\n')

        with open(self.file_path, "r", encoding='utf-8') as my_file:
            data_json = my_file.read()
            data = json.loads(data_json)
            item = data["intents"][np.argmax(result)]
            print(item['tag'], random.choice(item['responses']))
        return random.choice(item['responses'])