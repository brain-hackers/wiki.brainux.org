---
title: Linux のビルド 
tags:
  - Linux
  - 自力ビルド
excerpt: ""
---


# 動作環境

- Debian 10 (Buster)
- Ubuntu 20.04 LTS

本項では上記のいずれかを使用していることを前提で記述します。


# 依存関係のインストール

以下のコマンドで依存関係をインストールします。

```sh
sudo apt install build-essential bison flex libncurses5-dev gcc-arm-linux-gnueabi gcc-arm-linux-gnueabihf libssl-dev bc lzop qemu-user-static debootstrap kpartx
```


# Gitリポジトリのクローン

以下のコマンドでGitリポジトリをクローンして、必要なファイルをダウンロードします。長い時間がかかるので、時間のあるときに行いましょう。

```sh
git clone --recursive https://github.com/brain-hackers/buildbrain.git
```


# Linuxのビルド

1. `cd buildbrain` で `buildbrain` ディレクトリに入ります。

2. `make ldefconfig` を実行して、 `.config` ファイルを作成します。

3. `make lbuild` を実行してLinuxをビルドします。


# Brainuxのビルド

Linuxのカーネルの準備ができたら、カーネルの上で動くアプリケーションを用意して、Linuxディストリビューションを完成させます。

1. バックグラウンドで `make aptcache` を実行します。

   - 新しいウィンドウでターミナルを開き、 `make aptcache` を実行してそのままにしておきます。

2. `make brainux` を実行します。長い時間がかかるので、時間のあるときに行いましょう。


## パッケージの追加方法 (任意)

追加でほしいパッケージを `./os-brainux/setup_brainux.sh` の92行目あたりに追記します。

実際に追記した例を以下に示します。

```diff
    81    apt install -y dialog sudo \
    82               libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev \
    83               xserver-xorg xserver-xorg-video-fbdev xserver-xorg-dev xserver-xorg-input-evdev xinput-calibrator xorg-dev x11-apps x11-ico-dvd xinit \
    84               jwm \
    85               bash tmux vim htop \
    86               midori pcmanfm lxterminal xterm gnome-terminal fbterm uim-fep uim-anthy fonts-noto-cjk \
    87               dbus udev alsa-utils usbutils iw fake-hwclock systemd-timesyncd\
    88               build-essential flex bison pkg-config autotools-dev libtool autoconf automake device-tree-compiler \
    89               python3 python3-dev python3-setuptools python3-wheel python3-pip python3-smbus \
    90               resolvconf net-tools ssh openssh-client avahi-daemon wget git \
    91               network-manager zip neofetch sl python3-numpy ipython3 netsurf-gtk fcitx-anthy
+   92    apt install -y fbterm uim-fep uim-mozc
```

[SD カードへのコピー](/build/copy-sd-card/)に続く…
