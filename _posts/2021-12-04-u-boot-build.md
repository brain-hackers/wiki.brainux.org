---
title: U-Boot のビルド
categories:
  - U-Boot
tags:
  - U-Boot
  - 自力ビルド
excerpt: ""
---


# 動作環境

- Debian 10 (Buster)
- Ubuntu 20.04 LTS

本項では上記のいずれかを使用していることを前提で記述します。


# 環境の構築

[Linux のビルド](/linux/linux-build/)の頁ですでに構築している場合は飛ばします。


## 依存関係のインストール

以下のコマンドで依存関係をインストールしてください。

```sh
sudo apt install build-essential bison flex libncurses5-dev gcc-arm-linux-gnueabi debootstrap qemu-user-static
```


## Gitリポジトリのクローン

Gitリポジトリをクローンして、必要なファイルをダウンロードします。長い時間がかかるので、時間のある時に実いましょう。

```sh
git clone --recursive https://github.com/brain-hackers/buildbrain.git
```


# U-Bootのビルドとnk.binの作成

1. `cd buildbrain` で `buildbrain` ディレクトリに入ります

2. `make udefconfig-sh*` を実行して、 `.config` ファイルを作成します

    - PW-Sx1のとき： `make udefconfig-sh1`
    - PW-Sx5のとき： `make udefconfig-sh5`

3. `make ubuild` を実行して `u-boot.sb` を生成します

4. `make nkbin_maker` を実行します

5. `make nk.bin` を実行します


[Linux のビルド](/linux/linux-build/)に続く…
