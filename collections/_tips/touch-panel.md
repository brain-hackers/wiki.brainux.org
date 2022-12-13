---
title: タッチパネル
tags:
  - Linux
  - GUI
  - 周辺機器
excerpt: タッチパネルのキャリブレーション（Brainux に同梱されているため手動インストールは不要）
---


# 必要なパッケージのインストール

```sh
apt install xserver-xorg-input-evdev xinput-calibrator
```

を実行して、必要なパッケージをインストールします。


# Xorgとopenboxの起動

```sh
Xorg &
openbox-session &
```

を実行して、Xorgとopenboxを起動します。


# タッチパネル補正ツールの起動

```sh
xinput_calibrator
```

画面上に補正画面が表示されます。

![xinput-calibratorの画面](/assets/images/xinput-calibrator.png)


# 補正する

画面上の 赤い十字 を**丁寧に** 4回タッチすると、補正用の設定項目が端末に出力されます。

```plaintext
         Setting calibration data: 0, 4095, 0, 4095
 Calibrating EVDEV driver for "mxs-lradc-ts" id=6
         current calibration values (from XInput): min_x=0, max_x=4095 and min_y=0, max_y=4095
 
 Doing dynamic recalibration:
         Setting calibration data: 147, 3618, 3826, 350
         --> Making the calibration permanent <--
   copy the snippet below into '/etc/X11/xorg.conf.d/99-calibration.conf' (/usr/share/X11/xorg.conf.d/ in some distro's)
 Section "InputClass"
         Identifier      "calibration"
         MatchProduct    "mxs-lradc-ts"
         Option  "Calibration"   "147 3618 3826 350"
         Option  "SwapAxes"      "0"
 EndSection
```


# 設定ファイルを作成・保存する

`/etc/X11/xorg.conf.d`を作成します。

```sh
mkdir /etx/X11/xorg.conf.d
```

xinput_calibratorの出力に従って、`/etc/X11/xorg.conf.d/99-calibration.conf`に
`Section "InputClass"` から `EndSection`までの行を nano や vi を用いて書き出します。

```plaintext
 Section "InputClass"
         Identifier      "calibration"
         MatchProduct    "mxs-lradc-ts"
         Option  "Calibration"   "147 3618 3826 350"
         Option  "SwapAxes"      "0"
 EndSection
 ```


# Xorgの再起動

```sh
pkill Xorg
Xorg &
openbox-session &
```

でXorgを再起動します。


# 完成

![ちゃんとタッチした場所にカーソルが来ています](/assets/images/calibrator-done.gif)
