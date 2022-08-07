---
title: brain-config
categories:
  - Linux
tags:
  - Linux
---

Raspberry Pi OS で馴染み深い raspi-config コマンドをベースとした brain-config コマンドが Brainux にも用意されています。


# 起動方法

`brain-config` コマンドを `sudo` 付きで起動します。

```shell-session
$ sudo brain-config
```


# ルートファイルシステムを拡張する

上下左右キーと Enter キー（決定キー）を使って以下の手順に従って操作します。

1. "Advanced Options" を選択します
2. "Expand Filesystem" を選択します
3. しばらくすると "Root partition has been resized. ..." と表示されるので "Ok" を選択します
4. "Back" を押しトップメニューに戻ります
5. "Finish" を選択すると再起動が促されるため再起動します
6. 再起動したら容量が増えていることを `lsblk` コマンドを使って確認します
