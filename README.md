# Split image data to training and validation
クラス別に分類された画像データを特定の割合でランダムにTraining用とValidation用に分けるスクリプト

オプションで以下の機能を利用可能
- 分割する割合の指定
- 各クラスの出力サンプル数の統一
- 特定サンプル数以上のクラスのみ処理
- 各クラスとそのサンプル数をCSV形式で出力
- CSVファイルをもとにクラスごとに出力サンプル数を指定

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

#### Options
| Option       | Description                        | Default parameter  |
|:-------------|:-----------------------------------|:-------------------|
| --train_rate | 入力データから訓練用に利用する割合 | 0.9                |
| --sample_num | 出力される各クラスのサンプル数     | 0 (無効)           |
| --min        | サンプル数がこの値以下の時処理をスキップ | 0 (無効)     |
| --csv        | クラスごとの出力サンプル数が記述されたCSV | None (無効) |

#### Example
##### すべてのクラスに対して、指定の割合で分割する場合
```bash
python train_val_split.py
```

##### 出力する訓練用サンプル数を300で統一したい場合
```bash
python train_val_split.py --sample_num 300
```

##### サンプル数が200以上のクラスに対して、分割する場合
```bash
python train_val_split.py --min 200
```

##### クラスごとに出力サンプル数を調節する場合

1. クラス毎のサンプル数をCSVに出力

    ```bash
    python train_val_split.py out
    cat output-class-samples.csv
    class1,400
    class2,200
    class3,200
    ```

2. csvファイルを編集

    ```bash
    vim ./output-class-samples.csv
    cat output-class-samples.csv
    class1,150
    class2,100
    class3,100
    ```

3. 実行
    ```
    python train_val_split.py --csv ./output-class-samples.csv
    ```

##### 以下の条件で処理する場合
- CSVで記述した特定クラスは指定の数値でサンプル数を出力
- 記述されていないクラスは指定の数値でサンプル数を統一

上記のように、CSVファイルを用意した後

```bash
python train_val_split.py --csv ./output-class-samples.csv --sample_num 150
```
