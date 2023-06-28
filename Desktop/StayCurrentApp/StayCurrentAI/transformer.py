import logging
import time

import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
import keras


from pickle import dump, load

training_set = '/Users/bennettye/Downloads/cnn/stories'

def positional_encoding(length, depth):
    depth = depth / 2
    positions = np.arrange(length)[:, np.newaxis]
    depths = np.arrange(depth)[np.newaxis, :]/depth
    angle_rates = 1/(10000**depths)
    angle_rads = positions * angle_rates
    pos_encoding = np.concatenate(
        [np.sin(angle_rads), np.cos(angle_rads),],
        axis = -1
    )
    return tf.cast(pos_encoding, dtype = tf.float32)

class PositionalEmbedding(tf.keras.layers.Layer):
    def __init__(self, vocab_size, d_model):
        super().__init__()
        self.d_model = d_model
        self.embedding = tf.keras.layers.Embedding(vocab_size, d_model, mask_zero = True)
        self.pos_encoding = positional_encoding(length = 2048, depth = d_model)

    def compute_mask(self, *args,**kwargs):
        return self.embedding.compute_mask(*args, **kwargs)\
    
    def call(self, x):
        length = tf.shape(x)[1]
        x = self.embedding(x)
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
        x = x + self.pos_encoding[tf.newaxis, :length, :]
        return x

class BaseAttention(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__()
        self.mha = tf.keras.layers.MultiHeadAttention(**kwargs)
        self.layernorm = tf.keras.layers.LayerNormalization()
        self.add = tf.keras.layers.add

class CrossAttention(BaseAttention):
    def call(self, x, context):
        attn_output, attn_scores = self.mha(
            query = x,
            key = context,
            value = context,
            return_attention_scores = True)
        self.attn_scores = attn_scores
        x = self.add([x, attn_output])

        return x

