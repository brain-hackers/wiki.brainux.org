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


# Ethernet Gadget を有効化する

sysfs のファイル操作により Brain 上で Ethernet Gadget を有効化します。
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


# PC 側の対応作業

Windows / macOS / Linux すべてで利用可能です。


## Windows 10 / 11 の設定

1. USB コントローラの動作モードが `peripheral` に変更された Brain を PC に接続して Gadget を有効化します

2. Windows と Brain を USB ケーブルで接続します

   Brain の Ethernet Gadget が認識されていれば、デバイス マネージャーの「ほかのデバイス」グループに「RNDIS」が列挙されます。

3. 「RNDIS」を右クリックしてコンテキストメニューを表示し「ドライバーの更新」を選択します

   <img src="/assets/images/ether-win1.png" width=300px>

4. 「ドライバーの検索方法」ダイアログで「コンピューターを参照してドライバを検索」を選択します

   <img src="/assets/images/ether-win2.png" width=300px>

5. 「共通ハードウェアの種類」から「ネットワーク アダプター」を選択します

   <img src="/assets/images/ether-win3.png" width=300px>

6. 製造元「Microsoft」からモデル「リモート NDIS 互換デバイス」を選択し「次へ」をクリックします

   以降はセットアップ完了まで画面の指示に従ってください。

   <img src="/assets/images/ether-win4.png" width=300px>

7. 「ネットワーク接続」からアダプターの設定を変更します

   - 設定にて「ネットワークとインターネット」→「ネットワークの詳細設定」→「アダプターのオプションを変更する」を選択します (Windows 10)

      <img src="/assets/images/ether-win5.png" width=300px>

   - 設定にて「ネットワークとインターネット」→「ネットワークの詳細設定」→「ネットワーク アダプター オプションの詳細」を選択します (Windows 11)

      <img src="/assets/images/ether-win6.png" width=300px>

      <img src="/assets/images/ether-win7.png" width=300px>

8. Windows がインターネットの接続に使用しているアダプタ（Wi-Fi / イーサネット）を選択し「プロパティ」を開きます

   <img src="/assets/images/ether-win8.png" width=300px>

9. インターネットの共有設定をします

   「共有」タブから「ネットワークのほかのユーザーに、このコンピューターのインターネット接続を通しての接続を許可する」を選択します。
   加えて、「ホーム ネットワーク接続」プルダウンメニューで Ethernet Gadget に対応するアダプタを選択します。

   <img src="/assets/images/ether-win9.png" width=300px>

10. Brain からインターネットへの疎通を確認します

   Brain からインターネットに `ping` などで到達できるか確認してください。


## macOS の設定

**注意**: 以下に記載する方法で Brain を接続する場合、macOS の システム整合性保護 (SIP) を解除する必要があります。システム整合性保護は、Mac 上の保護されたファイルを改ざんしようとする悪質なソフトウェアからデータを守るセキュリティ技術です。詳しくは、[Mac のシステム整合性保護について - Apple サポート](https://support.apple.com/ja-jp/HT204899) などを参照し、十分に理解してから実行してください。
{: .notice--warning}

1. macOS でカーネル拡張機能 (kext) を利用可能にします

   2023年8月現在 Apple がサポートしている macOS では、kext の読み込みを有効化するために特別な設定が必要です。主な設定内容は以下の通りですが、詳細は macOS のバージョンにより異なるため、お使いの macOS に合わせた手順を検索して設定してください。

   - csrutil による SIP の無効化
   - システム拡張機能のユーザーによる管理の許可
   - システム設定におけるシステム拡張機能の許可

2. HoRNDIS をビルドします

   ビルドに必要な Git や Xcode を事前に適宜インストールしてください。Xcode の初回起動では以下のコマンドが必要な場合があります。

   ```sh
   xcodebuild -license
   xcodebuild -runFirstLaunch
   ```

   ターミナルを使って、以下の手順でビルドします。

   ```sh
   git clone https://github.com/thpryrchn/HoRNDIS.git -b BigSur
   cd HoRNDIS
   make
   ```

3. HoRNDIS をインストールします

   `build/pkg` に `HoRNDIS-kext.pkg` が作成されているので、ダブルクリックして、指示に従いインストールします。

4. USB コントローラの動作モードが `peripheral` に変更された Brain を PC に接続して Gadget を有効化します

5. システム設定で、Brain に対応するネットワークインターフェースに対してインターネット共有を有効化します

6. Brain からインターネットへの疎通を確認します

   Brain からインターネットに `ping` などで到達できるか確認してください。

## Linux の設定

作業手順とスクリーンショットは Ubuntu を例として紹介します。

1. USB コントローラの動作モードが `peripheral` に変更された Brain を PC に接続して Gadget を有効化します

2. Ethernet Gadget のネットワーク設定を開きます

   Ethernet Gadget が認識されていると、トップバー右のシステムメニューに「USB Ethernet」 もしくは 「Ethernet」 という名前の項目で列挙されます。その項目をクリックし、「Wired Settings」 をクリックします。

   <img src="/assets/images/ether-linux1.png" width=300px>

3. 歯車のアイコンをクリックします

   <img src="/assets/images/ether-linux2.png" width=300px>

4. 「IPv4」タブにある「Shared to other computers」を選択します

   <img src="/assets/images/ether-linux3.png" width=300px>

5. Brain からインターネットへの疎通を確認します

   Brain からインターネットに `ping` などで到達できるか確認してください。
