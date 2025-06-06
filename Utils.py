# import os.path


import os
import numpy as np
import itertools
from parameter import *
from Preprocessing import preprocess
from keras import backend as K

dataset_path_word = '../datasets/iam_words/words_new.txt'
dataset_path_line = '../datasets/IAM_sentences/metadata/sentences.txt'

def decode_label(out):
    out_best = list(np.argmax(out[0, 2:], 1))
    out_best = [k for k, g in itertools.groupby(out_best)]
    outstr = ''
    for c in out_best:
        if c < len(letters):
            outstr += letters[c]
    return outstr

def decode_batch(out):
    ret = []
    for j in range(out.shape[0]):
        out_best = list(np.argmax(out[j, 2:], 1))
        out_best = [k for k, g in itertools.groupby(out_best)]
        outstr = ''
        for c in out_best:
            if c < len(letters):
                outstr += letters[c]
        ret.append(outstr)
    return ret

def get_img_path_and_text(partition_split_file, is_words):
    paths_and_texts = []


    with open(partition_split_file) as f:
        print('partition_split_file:',partition_split_file)
        partition_folder = f.readlines()
    partition_folder = [x.strip() for x in partition_folder]

    if is_words:
        with open(dataset_path_word) as f:
            print('dataset_path_word: ',dataset_path_word)
            for line in f:
                if not line or line.startswith('#'):  # comment in txt file
                    continue
                line_split = line.strip().split(' ')
                assert len(line_split) >= 9
                status = line_split[1]
                if status == 'err':  # er: segmentation of word can be bad
                    continue

                file_name_split = line_split[0].split('-')
                label_dir = file_name_split[0]
                sub_label_dir = '{}-{}'.format(file_name_split[0], file_name_split[1])
                fn = '{}.png'.format(line_split[0])
                img_path = os.path.join('datasets/iam_words/words', label_dir, sub_label_dir, fn)

                gt_text = ' '.join(line_split[8:])
                if len(gt_text) > 16:
                    continue

                if sub_label_dir in partition_folder:
                    paths_and_texts.append([img_path, gt_text])
    else:
        with open(dataset_path_line) as f:
            for line in f:
                if not line or line.startswith('#'):
                    continue
                line_split = line.strip().split(' ')
                assert len(line_split) >= 9
                status = line_split[1]
                if status == 'err':
                    continue
                file_name_split = line_split[0].split('-')
                label_dir = file_name_split[0]
                sub_label_dir = '{}-{}'.format(file_name_split[0], file_name_split[1])
                fn = '{}.png'.format(line_split[0])
                img_path = os.path.join('datasets/IAM_sentences/dataset', label_dir, sub_label_dir, fn)
                gt_text = ' '.join(line_split[8:])
                gt_text = gt_text.replace('|', ' ')
                l = len(gt_text)
                if l < 10 or l > 74:
                    continue
                paths_and_texts.append([img_path, gt_text])
    return paths_and_texts

def predict_image(model_predict, path, is_word):
    if is_word:
        width = word_cfg['img_w']
    else:
        width = line_cfg['img_w']
    img = preprocess(path, width, 64)
    img = img.T
    if K.image_data_format() == 'channels_first':
        img = np.expand_dims(img, 0)
    else:
        img = np.expand_dims(img, -1)
    img = np.expand_dims(img, 0)

    net_out_value = model_predict.predict(img)
    pred_texts = decode_label(net_out_value)
    return pred_texts