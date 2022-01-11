---
title: Xorg
categories:
  - Linux
tags:
  - Linux
  - GUI
excerpt: Brain 特有の Xorg の設定について
---


# Brain 特有の Xorg の設定について

PW-Sx7 までは SoC に GPU が載っておらず、framebuffer (fbdev) のみが利用可能です。つまり、お手元の Linux マシンで Xorg が GPU と通信するときに使うしくみ (DRM, DRI) は利用できません。設定ファイルに fbdev を使用するよう明示的に書くことで Xorg が動かせます。


# xorg.conf

設定ファイル xorg.conf の内容を以下に示します。vi か nano を使って以下の内容を `/etc/X11/xorg.conf` に書き込んでください。

<!-- markdownlint-disable fenced-code-language -->
```
Section "Device"
        Identifier "device"
        Driver     "fbdev"
EndSection
Section "Screen"
        Identifier "screen"
        Device     "device"
EndSection
```
<!-- markdownlint-enable fenced-code-language -->


# 起こし方

2021年2月23日現在では、Xorg はブートシークエンスと結合されていません。つまり、手で起動します。

```sh
$ Xorg &
$ openbox-session &
```

以上を実行した後にお好みのソフトを起動してください。

