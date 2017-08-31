# Split image data to training and validation
クラス別に分類された画像データを一定の割合でランダムにTraining用とValidation用に分けるスクリプト


## 使い方

### ディレクトリ構造
以下のようなディレクトリ構造に入力画像をセット
```
.
├── README.md
├── train_val_split.py
└── input
     ├── class1
     │   ├── class1_1.jpg
     │   ├── class1_2.jpg
     │   ├── class1_3.jpg
     │    ...
     ├── class2
     │   ├── class2_1.jpg
     │   ├── class2_2.jpg
     │   ├── class2_3.jpg
     │    ...
     ├── class3
     │   ├── class3_1.jpg
     │   ├── class3_2.jpg
     │   ├── class3_3.jpg
     │    ...
      ...
```

### 実行
```bash
python train_val_split.py
```
