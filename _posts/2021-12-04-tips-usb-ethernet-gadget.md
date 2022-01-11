---
title: USB Ethernet Gadget
categories:
  - Tips
  - Linux
tags:
  - Linux
  - USB
  - 周辺機器
excerpt: PC と USB ケーブル1本で接続できる便利な仕組みとその導入方法
---


# USB Gadget とは？

コンピューターがあたかも USB デバイスであるかのように振る舞う仕組みです。


# Why USB Gadget?

インターネットに接続可能なパソコンに USB で Brain を接続するだけで Brain からインターネットに出たり、パソコンと Brain で双方向に SSH したりできるようになります。電池切れの心配もありません。


# USB コントローラーの動作モードを変更する

初期状態では Brain の USB コントローラーはホストとして動作するため、このままではデバイスになることができません。
2022年1月8日現在ではまだありませんが、コントローラーの動作モードを簡単に切り替えるスクリプトを用意する予定です。

手動で変更するには、以下の手順に従ってください。

1. SDカードの第1パーティションを`/boot`にマウントします

   ```sh
   sudo mount /dev/mmcblk1p1 /boot
   ```

2. 元のdtsをバックアップします

   {機種名の数字}は適宜置き換えてください。（例:PW-SH5→imx28-pwsh5.dtb）

   ```sh
   sudo cp /boot/imx28-pwsh{機種名の数字}.dtb /boot/imx28-pwsh{機種名の数字}.dtb.orig
   ```

3. dtbファイルをテキスト形式に変換します

   ```sh
   dtc -I dtb -O dts /boot/imx28-pwsh{機種名の数字}.dtb > dts 2> /dev/null
   ```

4. 設定を書き換えます

   ```sh
   nano dts
   ```

   `usb@80080000`ノードの中から`dr_mode = "host"`の箇所を探し、`dr_mode = "peripheral"`に書き換えます。スペルに注意しましょう。

   書き換え後は以下のようになります。

   ```diff
   ahb@80080000 {
           usb0: usb@80080000 {
                   pinctrl-names = "default";
                   pinctrl-0 = <&usb0_id_pins_a>;
                   vbus-supply = <&reg_usb0_vbus>;
   -               dr_mode = "host";
   +               dr_mode = "peripheral";
                   status = "okay";
           };
   };
   ```

   書き換えられたら保存してエディタを終了します。`Ctrl+O`の次に`Enter`を押して保存して、`Ctrl+X`で終了します。

5. 編集したものをバイナリ形式に変換します

   ```sh
   dtc -I dts -O dtb dts > dtb 2> /dev/null
   ```

   ```sh
   sudo mv dtb /boot/imx28-pwsh{機種名の数字}.dtb
   ```

6. SDカードの第1パーティションアンマウントします

   ```sh
   sudo umount /boot
   ```

7. 再起動します

   ```sh
   sudo reboot
   ```


## コピペ用

1〜3の手順をまとめると以下のようになります。

```sh
sudo mount /dev/mmcblk1p1 /boot
sudo cp /boot/imx28-pwsh{機種名の数字}.dtb /boot/imx28-pwsh{機種名の数字}.dtb.orig
dtc -I dtb -O dts /boot/imx28-pwsh{機種名の数字}.dtb > dts 2> /dev/null
```

5〜7の手順をまとめると以下のようになります。

```sh
dtc -I dts -O dtb dts > dtb 2> /dev/null
sudo mv dtb /boot/imx28-pwsh{機種名の数字}.dtb
sudo umount /boot
sudo reboot
```


# Brain に Ethernet Gadget を喋らせる

1. 以下のスクリプトを vi や nano でホームディレクトリに保存します

    ```sh
    #!/bin/sh

    g=/sys/kernel/config/usb_gadget/eth

    mkdir ${g}

    mkdir ${g}/functions/rndis.rn0
    echo "8a:15:8b:44:3a:02" > ${g}/functions/rndis.rn0/dev_addr
    echo "8a:15:8b:44:3a:01" > ${g}/functions/rndis.rn0/host_addr

    mkdir ${g}/configs/c.1
    ln -s ${g}/functions/rndis.rn0 ${g}/configs/c.1/

    echo "ci_hdrc.0" > ${g}/UDC

    sleep 1
    ifconfig usb0 up
    sleep 1
    dhclient
    ```

2. スクリプトに実行属性を付けます

   ここではスクリプト名を `gadget.sh` としています。1. で保存した名前に置き換えてください。

   ```sh
   chmod +x gadget.sh
   ```

3. 実行します

   次回起動時からはこのスクリプトを都度実行します。

   ```sh
   ./gadget.sh
   ```


# パソコン側の対応作業

Windows / Mac / Linux すべてで利用可能です。（注: 2021年2月23日現在、上記スクリプトでは Windows と macOS で認識しないことを確認しており、修正予定です）

パソコンを通してインターネットに出るために、ネットワーク接続の共有設定が必要になります。OS ごとに設定方法は異なりますので、別途設定してください。

