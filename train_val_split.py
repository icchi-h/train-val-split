#!/usr/bin/env python
# coding: utf-8

"""
__doc__
クラス別に分類された画像データを一定の割合でランダムにTraining用とValidation用に分けるスクリプト
"""

__author__ = "Haruyuki Ichino"
__version__ = "1.0"
__date__ = "2017/09/01"

print(__doc__)

import sys
import glob
import os.path
import numpy as np
import random
import shutil


# 学習用に使うデータの割合
TRAIN_RATE = 0.9
# 入出力ディレクトリ
INPUT_DIR = "./input/"
OUTPUT_DIR = "./output/"
TRAIN_DIR = "train_images"
VAL_DIR = "val_images"


# 入出力ディレクトリの存在確認
if not os.path.exists(INPUT_DIR):
    print("Error: Not found input directory")
    os.mkdir(INPUT_DIR)
    sys.exit(1)
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
output_train_path = os.path.join(OUTPUT_DIR, TRAIN_DIR)
output_val_path = os.path.join(OUTPUT_DIR, VAL_DIR)
if not os.path.exists(output_train_path):
    os.mkdir(output_train_path)
if not os.path.exists(output_val_path):
    os.mkdir(output_val_path)

# 画像カウンター
total_image_count = 0
train_image_count = 0
val_image_count = 0

# 各クラスディレクトリ
classes = np.sort(os.listdir(INPUT_DIR))
for tclass in classes:

    # .DS_Storeのチェック
    if tclass == ".DS_Store":
        continue

    class_path = os.path.join(INPUT_DIR, tclass)

    # ディレクトリじゃない場合はスキップ
    if not os.path.isdir(class_path):
        continue

    # 出力用のクラスディレクトリを作成
    output_train_class_path = os.path.join(output_train_path, tclass)
    output_val_class_path = os.path.join(output_val_path, tclass)
    if not os.path.exists(output_train_class_path):
        os.mkdir(output_train_class_path)
    if not os.path.exists(output_val_class_path):
        os.mkdir(output_val_class_path)

    print("Class: " + tclass + " ---------------------------------")
    files = np.sort(glob.glob(os.path.join(class_path, '*.*g')))

    # 画像リストをシャッフル
    random.shuffle(files)
    print("\tAll images:", end=' ')
    print(len(files))
    # print(files)
    # print()

    # 学習用ファイルと検証用ファイルリスト
    class_image_count = len(files)
    split_index = int(class_image_count * TRAIN_RATE)
    train_images = files[:split_index]
    val_images = files[split_index:]
    print("\tTrain images:", end=' ')
    print(len(train_images))
    # print(train_images)
    print("\tVal images:", end=' ')
    print(len(val_images))
    # print(val_images)

    # カウンターに追加
    total_image_count += class_image_count
    train_image_count += len(train_images)
    val_image_count += len(val_images)

    # ファイルリストを元にコピー
    for train_image in train_images:
        filename = os.path.basename(train_image)
        shutil.copyfile(train_image, os.path.join(output_train_class_path, filename))
    for val_image in val_images:
        filename = os.path.basename(val_image)
        shutil.copyfile(val_image, os.path.join(output_val_class_path, filename))


print()
print("Completed")
print("Total Image Count:", total_image_count)
print("Train Image Count:", train_image_count)
print("Val Image Count:", val_image_count)
