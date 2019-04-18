# Chromakey

画像をクロマキー処理する

* Before
<img width=300 src=images/DSC_0530.JPG>

* After
<img width=300 src=airplanes/_test.png>

## Usage
    python chromakey.py [--image][--name][-a,--auto][--backcolor]

* [--image]  
    元画像のファイルを指定
    指定がなければスクリプト実行時にimagesの中のファイルリストから選ぶ仕様  

* [--name]  
    出力ファイル名を指定
    指定しなければスクリプト実行時にファイル名を入力する必要あり
* [-a,--auto]  
    背景色を自動で設定する
    このオプションを付けた場合，backcolor指定は無効

* [--backcolor]  
    数字で指定(0~)
    mask_setting.txtにhsv形式で切り抜く色範囲を指定(任意の数)
    `--backcolor n` でn番目に書き込んだhsvの値を使う

## Dependency Libraries
* numpy
* opencv-python