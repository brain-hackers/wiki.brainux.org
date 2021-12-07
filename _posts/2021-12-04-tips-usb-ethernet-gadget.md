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
2021年2月23日現在ではまだありませんが、コントローラーの動作モードを簡単に切り替えるスクリプトを用意する予定です。

手動で変更するには、Device Tree Compiler を使用します。


# Brain に Ethernet Gadget を喋らせる

1. 以下のスクリプトを vi や nano でホームディレクトリに保存します

   ```
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

   ```
   $ chmod +x gadget.sh
   ```

3. 実行します

   次回起動時からはこのスクリプトを都度実行します。

   ```
   $ ./gadget.sh
   ```


# パソコン側の対応作業

Windows / Mac / Linux すべてで利用可能です。（注: 2021年2月23日現在、上記スクリプトでは Windows と macOS で認識しないことを確認しており、修正予定です）

パソコンを通してインターネットに出るために、ネットワーク接続の共有設定が必要になります。OS ごとに設定方法は異なりますので、別途設定してください。

