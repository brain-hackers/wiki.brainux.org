---
title: 初めての方へ ─ とりあえず動かす
categories:
  - For Beginners
tags:
  - For Beginners
  - 沼の入り口
excerpt: ""
---


<img src="/assets/images/happy.png">


# 始めに

このページでは、SHARP Brain で Linux を動かす試みから生まれた Linux ディストリビューション **Brainux** を手軽に起動する方法を紹介します。

Linux ディストリビューションは、カーネルとそれ以外のソフトウェアの組み合わせです。Brain の場合はカーネルを起動するブートローダも SD カード上に必要なため、正確にはカーネル・ソフトウェア・ブートローダのセットが必要になります。

リポジトリ [buildbrain](https://github.com/brain-hackers/buildbrain) では、Raspberry Pi と同様に SD カードに書き込むだけで起動可能にした SD イメージを公開しています。ちなみにカーネル・ソフトウェア・ブートローダはどれも自力で準備することもできます。詳しくは本 Wiki の対応するページを参照してください。

質問がある場合や開発に参加したい場合は、まず [Brain Hackers の Discord](https://github.com/brain-hackers/README) に参加していただき、「雑談」チャンネルでお気軽にご質問ください。


# 対応している機種

2021年2月21日現在、対応している機種とハードウェアは以下の通りです。省略のため、PW-SH1 や PW-SJ1 のような同世代の機種は特記すべき差がない限りは "Sx1" のように省略形で記載します。

内蔵ハードウェアの対応状況や使い方については[内蔵ハードウェア](#内蔵ハードウェア)をご覧ください。キーマップもそちらに掲載しています。

|機種  |Linux 起動        |キーボード        |注釈|
|:-----|:----------------:|:----------------:|:---|
|PW-ACxxx, GCxxx, TC980||||
|PW-G4000, G5000, G5100, A7000, A9000||||
|PW-G4200, G5200 ~ 5300, A7200 ~ 7400, A9100 ~ 9300|:white_check_mark:|:white_check_mark:||
|GX500, GX300|:white_check_mark:|:white_check_mark:|画面が非常に暗くなる|
|PW-Sx1|:white_check_mark:|:white_check_mark:||
|PW-Sx2|:white_check_mark:|:white_check_mark:||
|PW-Sx3|:white_check_mark:|:white_check_mark:||
|PW-Sx4|:white_check_mark:|:white_check_mark:||
|PW-Sx5|:white_check_mark:|:white_check_mark:||
|PW-Sx6|:white_check_mark:|:white_check_mark:||
|PW-Sx7|:white_check_mark:|:white_check_mark:||
|PW-HC4 ~ 6, H7700 ~ H9100|:white_check_mark:|:white_check_mark:||
|PW-SR1 ~ 3|:white_check_mark:|:white_check_mark:||
|PW-AA1 ~ 2|:white_check_mark:|:white_check_mark:||
|PW-AJ1 ~ 2|:white_check_mark:|:white_check_mark:||
|PW-x1, x2, ESxxxx, SR4||||


# SD カードのイメージをダウンロードする

[brain-hackers/buildbrain のリリースページ](https://github.com/brain-hackers/buildbrain/releases)にアクセスし、最新リリースの配布物の中から `sdimage-*.zip` と名のついた ZIP ファイルをダウンロードします。`*` には最新リリースのバージョン名が入ります。


# SD カードに書き込む

書き込むソフトは Windows / macOS / Linux のどれをお使いの場合でも利用可能な balenaEtcher がお勧めです。[公式サイト](https://www.balena.io/etcher/)にアクセスしてダウンロードしてください。

macOS もしくは Linux をお使いの場合は、ZIP を展開して取り出した .img ファイルを `dd` コマンドでそのまま書くことも可能です。


## balenaEtcher を使う場合

今回は macOS で balenaEtcher を使用した際の画像で説明します。どの OS でも同様にして書き込めます。

 1. balenaEtcher を起動します
 2. "Flash from file" をクリックし、ダウンロードした ZIP ファイルを選択します
    - 展開する必要はありません

    <img src="/assets/images/etcher1.png" width=300px>

    <img src="/assets/images/etcher2.png" width=300px>

 3. "Select target" をクリックして書き込み先を選択します
    - 正しい SD カードを選択しているか慎重に確認してください
    - 4GB 以上の SD カードであればなんでも使用可能です
    - SD カードの性能がシステムの使用感に直結するため高速な SD カードを使用することをお勧めします
    - 画像では 8GB の SD カードを選択しています

    <img src="/assets/images/etcher3.png" width=300px>

    <img src="/assets/images/etcher4.png" width=300px>

 4. "Flash!" をクリックして書き込みます
    - あらためて正しい SD カードが選択されているか確認したうえで書き込んでください
    - 書き込みには管理者権限が必要なため管理者パスワードを入力します

    <img src="/assets/images/etcher5.png" width=300px>

    <img src="/assets/images/etcher6.png" width=300px>

    <img src="/assets/images/etcher7.png" width=300px>

 5. 完成！\
    <img src="/assets/images/etcher8.png" width=300px>


## dd を使う場合

macOS もしくは Linux をお使いの場合は、`dd` コマンドでも書き込むことができます。以下にコマンド例を示します。


### macOS の場合

- macOS では `/dev/disk*` に書き込むと非常に遅いため `/dev/rdisk*` を使用します
- どのディスクが SD カードかはディスクユーティリティを使用して確認します

以下に実行例を示します。バージョン番号は適宜読み替えてください。

```sh
cd ~/Downloads
unzip sdimage-2021-02-21-162410.zip
sudo dd if=~/Downloads/sdimage-2021-02-21-162410.img of=/dev/rdisk4 bs=10M
```


### Linux の場合

以下に実行例を示します。バージョン番号は適宜読み替えてください。

```sh
cd ~/Downloads
unzip sdimage-2021-02-21-162410.zip
sudo dd if=~/Downloads/sdimage-2021-02-21-162410.img of=/dev/sdc bs=10M
```


# 実機で起動する

書き込み終わった SD カードを Brain に挿入して Linux を起動しましょう。起動には2つの方法があります。

- アプリメニューからの起動
- SD カードからの直接起動


## アプリメニューからの起動

Windows CE 起動後に "Launch Linux" を追加アプリメニューで選択すると Linux が起動します。


## SD カードからの直接起動

Windows CE の起動シーケンスに割り込み Linux を直接起動する方法です。後述の問題によりこの方法は標準で無効になっています。有効化するには、以下の手順に従ってください。

 1. SD カードの先頭パーティション（ボリューム名が `boot` のパーティション）を開きます
 2. `nk` ディレクトリの中にあるファイルをパーティションのルートディレクトリにすべてコピーします
 3. SD カードを取り外し実機に差し込みます
 4. リセットボタンを押して再起動し Linux が自動で起動することを確認します

直接起動には下記の問題があります。これらを回避したい場合はアプリメニューからの直接起動を使用してください。

- クロック周波数が半減する（修正予定）
- 一部の機種で使えない: PW-G4200, G5200, A7200, A7300, A9200, GX300, GX500


# ログイン

本体の内蔵キーボードに対応している機種では、ログインシェルが表示されたらユーザー名 `user` パスワード `brain` でログインできます。非対応の機種では、電源供給が可能なタイプの OTG ケーブルを使用してキーボードをつなぐと操作できます。root ユーザーは無効になっているのでご注意ください。


# 内蔵ハードウェア

Brain における Linux の動作はまだ初期段階であり、一部のハードウェアしか利用できません。


## キーボード

キーが非常に少ない Brain のキーボードで必要な記号を打つため、キーボードの使用方法は特殊になっています。キートップに記載されたキー以外の文字は、すべて「記号」キーと「シフト」キーを組み合わせて入力します。

Shift キー・Ctrl キー・Alt キーは現実のキーボードに近い配置で対応させています。古い機種は Space キーがないため「Sジャンプ」キーに割り当てています。


### Gxxxx, Axxxx の場合

|特殊キー|対応するキー|備考|
|:-:|:-:|:-:|
|Shift|機能||
|Ctrl|音声||
|Alt|前見出||
|Space|Sジャンプ||


### Sx1 ~ Sx3, HC4 ~ HC6, SR1 の場合

|特殊キー|対応するキー|備考|
|:-:|:-:|:-:|
|Shift|シフト||
|Ctrl|ページアップ|`《` を横に倒した記号|
|Alt|文字切り替え||


### Sx4, H7700, SR2 の場合

|特殊キー|対応するキー|備考|
|:-:|:-:|:-:|
|Shift|シフト||
|Ctrl|音声||
|Alt|ページアップ|`《` を横に倒した記号|


### Sx5 ~ Sx7, H7800 ~ H9100, AAx, AJx, SR3 の場合

|特殊キー|対応するキー|備考|
|:-:|:-:|:-:|
|Shift|シフト||
|Ctrl|ページアップ|`《` を横に倒した記号|
|Alt|音声||


## キーマップ

キーと入力される文字のマップを以下に示します。

<img src="/assets/images/keymap.png" width=640px>

## 電源を切る

リセットボタンを利用して強制的に電源を切るなどの方法で、正常にシャットダウンしなかった場合、SD カード内のデータが破壊される場合があります。

Brainux を正しく終了し電源を切るためには、次のコマンドを入力します。

```sh
sudo shutdown -h now

# こちらでも OK
sudo poweroff
```

また、電源ボタンには一般的な PC の電源ボタンと同じ動作が割り当てられているため、押すとシャットダウンできます。

シャットダウンした後、リセットボタンを押すと Windows CE を起動できます。


# その他

|Q|A|
|:-|:-|
|ファイルシステムを SD カードいっぱいまで拡張したい。|[brain-config](/linux/brain-config/) を使います。|
