OpenATS
=======

Open AI Training Station

TODO:
-----

※開発後削除

-  Trainer for Keras\_cnn\_audio.Trainer
-  Manager for Keras\_cnn\_audio.manage.py

Install
-------

https://pypi.python.org/pypi/OpenATS

::

    pip install OpenATS

ルール
------

-  r1. 1 Stationに 1 Dataset
-  r2. 1 Stationに n Model
-  r3. 1 Stationに n Setting

つまり、1StationにつきNxNパターンの学習を実施する.

Usage
-----

-  Init 初期ディレクトリツリーを作成する ``openATS init``
-  Create Dataset データセットを作り直す ``openATS makeDataset``
-  Run あるモデルと設定ファイルの組みで学習を開始する
   ``openATS run -m model001.py -s 01-setting.conf``
-  Run All モデル数x設定ファイルパターンの学習を開始する
   ``openATS runAll``
-  Test 少ないサンプルとエポック数で、正常に学習可能かテストする
   ``openATS run --test -m model001.py -s 01-settings.conf  openATS runALL --test``

Feature
-------

-  **テストモード** : epoch1, datasize100,
   batch\_size10,　計算ができるか実行する機能.
-  **モデル保存** :
-  (1)**BestAcc-Model** : 最大Acc時の重みを保存.
-  (2)**LastAcc-Model** : 最終Accを保存

Version1.x
~~~~~~~~~~

-  **Datasource** : 信号データのみ対応
-  **Dataset** : mspec、mfccに対応
-  **Model.py** : Modelファイルはpyファイルのみ対応
-  **Setting.conf** : .confのみ対応

Version2.x
~~~~~~~~~~

-  **Datasource** : 画像データの入力に対応
-  **Model.json** : Modelファイルのjsonインポートに対応
-  **Setting.conf** : json対応
-  **HTTP Access** : 指定したWebサーバーにログを送信する機能

dataset.conf
------------

.. code:: conf

    [Datasource]
    datasource_dirfullpath = /home/ubuntu/datasource/mp3/
    allow_subdirs = True
    datasource_ext = mp3

    [Dataset]
    max_duration_ms = 3000 # max duration. Zero padding if shorter.
    error_if_shorter = True # error_if_shorter_than_max_duration
    pipeline = "mspec" # "mfcc", "mspec"
    nfft = 4096
    nmel = 128

setting.conf
------------

::

    [model]
    optimizer = "adam" # Keras opt. sgd,rmsprop,Adagrad,Adadelta,Adam,Adamax,Nadam
    # loss = "categorical_crossentropy" # binary_crossentropy
    metrics = 'accutuary'

    [train]
    epoch = 2
    batch_size = 32
    sample_size = 500

基本ディレクトリ構成
--------------------

initコマンドでコマンドを実行したディレクトリに初期構成を展開

::

    $ openATS init
    Create default directory tree ..

    .gitignore
    Stationfile
    /dataset/
        default-dataset.conf 
        /train/
        /test/
    /models/
        001_cnn_4layer_a0.py
        002_cnn_4layer_a0.py
    /settings/
        default-setting.conf
        argmentation.conf
        non-argumentation.conf
    /results/
        /001_cnn_4layer_a0-_sample-settings/
            /tflogs/
            training.csv
            validate.csv
            classification_report.csv
            acc_vs_epoch.json
            loss_vs_epoch.jon
            model.png
            model-bestepoch-200.model
            model-lastepoch-1200.model
            acc_vs_epoch.png
            loss_vs_epoch.png

.gitignore
----------

::

    *.pyc
    __pycache__/
    dataset/

Resultディレクトリ
------------------

-  結果ファイルの格納方法
   解析中にはテンポラリディレクトリに結果ファイルを保存する。解析が完了後Resultディレクトリに移動
