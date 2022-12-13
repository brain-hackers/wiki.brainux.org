---
title: Swap 領域
categories:
  - Tips
  - Linux
tags:
  - Linux
excerpt: ""
---


# スワップの作成を推奨します

Brain の DRAM は 128MB しかないので、簡単にメモリが食いつぶされます。OOM Killer により重要なプロセスを終了される危険があるため、スワップを作成することをお勧めします。

2021年2月23日現在のリリースではまだスワップ領域を標準で設定していません。Brain Hackers では将来のリリースで最初からスワップを設定することを検討しています。


# 作成方法

 1. 以下のコマンドを実行して、スワップのための領域を確保します

    今回の例では、256MB（これ以上を推奨）の領域を確保しています。ほかの容量にしたい場合は適宜 `bs` や `count` の値を変えてください。

    ```sh
    dd if=/dev/zero of=/swapfile bs=1M count=256
    chmod 0600 /swapfile
    ```

 2. スワップ領域を初期化します

    ```sh
    mkswap /swapfile
    ```

 3. スワップ領域を有効にします

    ```sh
    swapon /swapfile
    ```
