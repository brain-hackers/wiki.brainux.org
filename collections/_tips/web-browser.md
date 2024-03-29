---
title: Web ブラウザ
tags:
  - Linux
  - GUI
excerpt: Brainux で利用可能な Web ブラウザについて
---


# グラフィカルブラウザ

**グラフィカルブラウザを使うのは困難です！** PW-Sx7 までの Brain が搭載している SoC は初代 Raspberry Pi のクロック周波数の約半分の速度で動作し、メモリ容量も半分以下の 128MB しかありません。つまり、インターネットブラウジングは非現実的です。たとえば、[極めて高速に表示されることで有名な著名人のサイト](http://abehiroshi.la.coocan.jp/)の表示に実測15秒ほどかかります。また、Twitter は表示不可能です。


## NetSurf

バージョン 2022-05-17-020127 にて Web ブラウザに NetSurf を追加しました。以下のコマンドを実行すると NetSurf が起動します。

```sh
netsurf &
```


## Midori

代表的な軽量なブラウザの選択肢に Midori があります。Brainux にはプリインストールされています。Xorg が起動している状態で、以下のコマンドを実行すると Midori が起動します。

```sh
DISPLAY=:0 midori
```


## Surf

[`surf`](https://surf.suckless.org/) も動作することを確認していますが、Midori と速度はほとんど変わりません。


# テキストブラウザ

Lynx や w3m はスムーズに動作します。現実的なスピードで Web サイトを閲覧するにはこれらをお勧めします。

