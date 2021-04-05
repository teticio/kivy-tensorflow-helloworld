import os
import kivy
import numpy as np
from kivy.app import App
from kivy.uix.label import Label
from model import TensorFlowModel


class MyApp(App):

    def build(self):
        model = TensorFlowModel()
        model.load(os.path.join(os.getcwd(), 'model.tflite'))
        np.random.seed(42)
        x = np.array(np.random.random_sample((1, 28, 28)), np.float32)
        y = model.pred(x)
        # result should be
        # 0.01647118,  1.0278152 , -0.7065112 , -1.0278157 ,  0.12216613,
        # 0.37980393,  0.5839217 , -0.04283606, -0.04240461, -0.58534086
        return Label(text=f'{y}')


if __name__ == '__main__':
    MyApp().run()