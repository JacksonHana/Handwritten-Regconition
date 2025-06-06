from parameter import *
from ImageGenerator import TextImageGenerator
from CRNN import word_model, line_model
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.optimizers import Adam
# from keras.src.optimizers.adam import Adam
from Utils import *
import tensorflow as tf


def train(train_data, val_data, is_word_model):
    with tf.device('/gpu:0'):
        print("Using GPU")

        if is_word_model:
            model, _ = word_model()
            cfg = word_cfg
        else:
            model, _ = line_model()
            cfg = line_cfg

        input_length = cfg['input_length']
        model_name = cfg['model_name']
        max_text_len = cfg['max_text_len']
        img_w = cfg['img_w']
        img_h = cfg['img_h']
        batch_size = cfg['batch_size']
        train_set = TextImageGenerator(train_data, img_w, img_h, batch_size, input_length, max_text_len)
        print('Loading data for train ...')
        train_set.build_data()
        print('Loading data for validation ...')
        val_set = TextImageGenerator(val_data, img_w, img_h, batch_size, input_length, max_text_len)
        val_set.build_data()
        print('Done')

        print("Number train samples: ", train_set.n)
        print("Number val samples: ", val_set.n)

        model.compile(loss=lambda y_true, y_pred: y_pred, optimizer='adam')

        ckp = ModelCheckpoint(
            filepath='Resource/' + model_name + '--{epoch:02d}--{val_loss:.3f}.weights.h5', monitor='val_loss',
            verbose=1, save_best_only=True, save_weights_only=True
        )
        earlystop = EarlyStopping(
            monitor='val_loss', min_delta=0, patience=10, verbose=0, mode='min'
        )

        model.fit(train_set.next_batch(),
                    steps_per_epoch=train_set.n // batch_size,
                    epochs=32,
                    validation_data=val_set.next_batch(),
                    validation_steps=val_set.n // batch_size,
                    callbacks=[ckp, earlystop])

    return model


if __name__ == '__main__':
    path = '..' + '/datasets/splits/train.uttlist'
    train_data = get_img_path_and_text(path, is_words=False)
    val_data = get_img_path_and_text(path, is_words=False)
    print('number of train image: ', len(train_data))
    print('number of valid image: ', len(val_data))

    model = train(train_data, val_data, False)