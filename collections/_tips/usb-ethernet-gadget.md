---
title: USB Ethernet Gadget
tags:
  - Linux
  - USB
  - 周辺機器
excerpt: PC と USB ケーブル1本で接続できる便利な仕組みとその導入方法
---


# USB Gadget とは？

コンピュータがあたかも USB デバイスであるかのように振る舞うしくみです。


# Why USB Gadget?

インターネットに接続可能なPCと Brain を接続するだけで Brain からインターネットに出たり、PCと Brain で双方向に SSH したりできます。電池切れの心配もありません。


# USB コントローラの動作モードを変更する

初期状態では Brain の USB コントローラはホストとして動作するため、このままではデバイスになることができません。
コントローラの動作モードを切り替える方法には、brain-config というツールを使う方法と手動でデバイスツリーを書き換える方法があります。


## 方法A. brain-config で変更する

`brain-config` による動作モードの切り替え方法については [brain-config](/linux/brain-config) のページを参照してください。


## 方法B. 手動で変更する

手動で変更するには、以下の手順に従ってください。

1. SDカードの第1パーティションを`/boot`にマウントします

   ```sh
   sudo mount /dev/mmcblk1p1 /boot
   ```

2. 元のdtsをバックアップします

   `{デバイスツリー名}`の箇所は、[対応機種の表](/beginners/get-started/#対応している機種)でお使いの機種を探して、対応する「デバイスツリー名」列の文字列で置き換えてください。（例:PW-SH5→imx28-pwsh5.dtb）

   ```sh
   sudo cp /boot/{デバイスツリー名}.dtb /boot/{デバイスツリー名}.dtb.orig
   ```

3. dtbファイルをテキスト形式に変換します

   ```sh
   dtc -I dtb -O dts /boot/{デバイスツリー名}.dtb > dts 2> /dev/null
   ```

4. 設定を書き換えます

   ```sh
   nano dts
   ```

   `usb@80080000`ノードの中から`dr_mode = "host"`の箇所を探し、`dr_mode = "peripheral"`に書き換えます。スペルに注意しましょう。

   書き換え後は以下のようになります。

   ```diff
   usb@80080000 {
           compatible = "fsl,imx28-usb\0fsl,imx27-usb";
           reg = < 0x80080000 0x10000 >;
           interrupts = < 0x5d >;
           clocks = < 0x03 0x3c >;
           fsl,usbphy = < 0x1f >;
           status = "okay";
           pinctrl-names = "default";
           pinctrl-0 = < 0x20 >;
           vbus-supply = < 0x21 >;
   -       dr_mode = "host";
   +       dr_mode = "peripheral";
   };
   ```

   書き換えたら保存してエディタを終了します。`Ctrl+O`の次に`Enter`を押して保存して、`Ctrl+X`で終了します。

5. 編集したものをバイナリ形式に変換します

   ```sh
   dtc -I dts -O dtb dts > dtb 2> /dev/null
   ```

   ```sh
   sudo mv dtb /boot/{デバイスツリー名}.dtb
   ```

6. SDカードの第1パーティションアンマウントします

   ```sh
   sudo umount /boot
   ```

7. 再起動します

   ```sh
   sudo reboot
   ```

1〜3の手順をまとめると以下のようになります。

```sh
sudo mount /dev/mmcblk1p1 /boot
sudo cp /boot/{デバイスツリー名}.dtb /boot/{デバイスツリー名}.dtb.orig
dtc -I dtb -O dts /boot/{デバイスツリー名}.dtb > dts 2> /dev/null
```

5〜7の手順をまとめると以下のようになります。

```sh
dtc -I dts -O dtb dts > dtb 2> /dev/null
sudo mv dtb /boot/{デバイスツリー名}.dtb
sudo umount /boot
sudo reboot
```


# Brain に Ethernet Gadget を喋らせる

sysfs のファイル操作により Ethernet Gadget を有効化します。
Brainux バージョン 2023-07-29-024604 以降では有効化処理が起動時に自動で実行されます。もし手動で有効化したい場合は以下の手順を参照してください。

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
   sudo ./gadget.sh
   ```


# PC側の対応作業

Windows / Mac / Linux すべてで利用可能です。（注: 2021年2月23日現在、上記スクリプトでは Windows と macOS で認識しないことを確認しており、修正予定です）

PCを通してインターネットへ出るために、ネットワーク接続の共有設定が必要になります。OS ごとに設定方法は異なりますので、別途設定してください。

