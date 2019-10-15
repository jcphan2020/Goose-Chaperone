#480 x 270
import os
import argparse

import label_image.py

parser = argparse.ArgumentParser(description='Simplify training and testing usage')
parser.add_argument('--test', default=testModel, help='Automatically test model, if available')
parser.add_argument('--train', dest='trainNewModel', help='Create new model from training set')
parser.add_argument('--retrain', dest='retrainModel', help='Retrain existing model')
args = parser.parse_args()

def testModel():
    print('test')
    return

def trainNewModel():
    print('train')
    return

def retrainModel():
    print('retrain')
    return