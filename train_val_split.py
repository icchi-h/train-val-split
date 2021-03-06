#!/usr/bin/env python
# coding: utf-8

"""
__doc__
クラス別に分類された画像データを一定の割合でランダムにTraining用とValidation用に分けるスクリプト
"""

__author__ = "Haruyuki Ichino"
__version__ = "1.4"
__date__ = "2017/09/13"

print(__doc__)

import sys
import glob
import os.path
import numpy as np
import random
import shutil
import argparse
import csv


# 入出力ディレクトリ
TRAIN_DIR = "train_images"
VAL_DIR = "val_images"
OUTPUT_CSV_FILE = './output-class-samples.csv'


def output_class_samples_csv(path):
    # ファイル出力の準備
    f = open(OUTPUT_CSV_FILE, 'w')

    # 各クラスディレクトリにアクセス
    classes = np.sort(os.listdir(path))
    for tclass in classes:

        # .DS_Storeのチェック
        if tclass == ".DS_Store":
            continue

        class_path = os.path.join(FLAGS.input_path, tclass)

        # ディレクトリじゃない場合はスキップ
        if not os.path.isdir(class_path):
            continue

        # 書き込み
        files = np.sort(glob.glob(os.path.join(class_path, '*.*[gG]')))
        class_image_count = len(files)
        f.write(tclass + "," + str(class_image_count) + "\n")

    f.close()

def get_csv_dict(csv_path):

    # クラス毎の出力サンプル数
    class_samples = {}

    f = open(csv_path, 'r')
    reader = csv.reader(f)
    for row in reader:
        class_samples[row[0]] = int(row[1]) if not row[1] is '' else 0
    f.close()

    return class_samples


# オプションの設定
parser = argparse.ArgumentParser()
parser.add_argument(
    "--input_path",
    type=str,
    default="./input/",
    help="Input directory path."
)
parser.add_argument(
    "--output_path",
    type=str,
    default="./output/",
    help="Output directory path."
)
parser.add_argument(
    "--train_rate",
    type=float,
    default=0.9,
    help="処理をする最低サンプル数値。このサンプル数以下のクラスは出力しない。"
)
parser.add_argument(
    "--min",
    type=int,
    default=0,
    help="処理をする最低サンプル数値。このサンプル数以下のクラスは出力しない。"
)
parser.add_argument(
    "--sample_num",
    type=int,
    default=0,
    help="出力する各クラスの訓練データサンプル数。"
)
parser.add_argument(
    "--csv",
    type=str,
    default=None,
    help="出力する各クラスの訓練データサンプル数を記述したcsvファイル。"
)
FLAGS, unparsed = parser.parse_known_args()

# csv出力コマンドの処理
if "out" in sys.argv:
    output_class_samples_csv(FLAGS.input_path)
    print("Saved: class samples csv file")
    sys.exit(0)

if FLAGS.sample_num:
    print("訓練サンプル数:", FLAGS.sample_num)
if FLAGS.min:
    print("最低サンプル数:", FLAGS.min)
if FLAGS.csv:
    if os.path.exists(FLAGS.csv):
        print("サンプル数管理csv:", FLAGS.csv)
        class_samples = get_csv_dict(FLAGS.csv)
        print(class_samples)
    else:
        print("Error: Not found specified csv file >", FLAGS.csv)
        sys.exit(0)

# 入出力ディレクトリの存在確認
if not os.path.exists(FLAGS.input_path):
    print("Error: Not found input directory")
    os.mkdir(FLAGS.input_path)
    sys.exit(1)
if not os.path.exists(FLAGS.output_path):
    os.mkdir(FLAGS.output_path)
output_train_path = os.path.join(FLAGS.output_path, TRAIN_DIR)
output_val_path = os.path.join(FLAGS.output_path, VAL_DIR)
if not os.path.exists(output_train_path):
    os.mkdir(output_train_path)
if not os.path.exists(output_val_path):
    os.mkdir(output_val_path)

# 画像カウンター
total_image_count = 0
train_image_count = 0
val_image_count = 0

print()

# 各クラスディレクトリ
classes = np.sort(os.listdir(FLAGS.input_path))
for tclass in classes:

    # .DS_Storeのチェック
    if tclass == ".DS_Store":
        continue

    class_path = os.path.join(FLAGS.input_path, tclass)

    # ディレクトリじゃない場合はスキップ
    if not os.path.isdir(class_path):
        continue

    print("Class: " + tclass + " ---------------------------------")
    files = np.sort(glob.glob(os.path.join(class_path, '*.*[gG]')))
    class_image_count = len(files)
    print("\tFound images:", class_image_count)
    # print(files)
    # print()

    # サンプル数のチェック
    if FLAGS.csv:
        if tclass in class_samples and class_image_count < int(class_samples[tclass] / FLAGS.train_rate):
            print("\tError: サンプル数が指定サンプル数に達していません")
            continue
    if (class_image_count < int(FLAGS.sample_num / FLAGS.train_rate)):
        print("\tError: サンプル数が指定サンプル数に達していません")
        continue
    if class_image_count < FLAGS.min:
        print("\tError: 最低サンプル数に達していません")
        continue

    # 出力用のクラスディレクトリを作成
    output_train_class_path = os.path.join(output_train_path, tclass)
    output_val_class_path = os.path.join(output_val_path, tclass)
    if not os.path.exists(output_train_class_path):
        os.mkdir(output_train_class_path)
    if not os.path.exists(output_val_class_path):
        os.mkdir(output_val_class_path)


    # 画像リストをシャッフル
    random.shuffle(files)

    # 学習用ファイルと検証用ファイルリストの作成
    # csvファイルを使うする場合
    if FLAGS.csv:
        if tclass in class_samples:
            val_sample_num = int(class_samples[tclass] / FLAGS.train_rate) - class_samples[tclass]
            train_images = files[:class_samples[tclass]]
            val_images = files[class_samples[tclass]:class_samples[tclass]+val_sample_num]
    else:
        # 訓練サンプル数が指定されている場合
        if FLAGS.sample_num:
        # 分割Rateにしたがって分割する場合
            val_sample_num = int(FLAGS.sample_num / FLAGS.train_rate) - FLAGS.sample_num
            train_images = files[:FLAGS.sample_num]
            val_images = files[FLAGS.sample_num:FLAGS.sample_num+val_sample_num]
        else:
            split_index = int(class_image_count * FLAGS.train_rate)
            train_images = files[:split_index]
            val_images = files[split_index:]
    print("\tTrain images:", len(train_images))
    # print(train_images)
    print("\tVal images:", len(val_images))
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
print("Total Image Count:", train_image_count + val_image_count)
print("Train Image Count:", train_image_count)
print("Val Image Count:", val_image_count)
