---
title: Wiki の編集方法とルール
categories:
  - Meta
tags:
  - Wiki
  - メンバー向け
excerpt: ""
---


# 準備

GitHubにログインした状態でWikiをcloneします。

```sh
$ git clone git@github.com:brain-hackers/wiki.brainux.org.git
```

2022/1/8現在、Ubuntu 20.04.3 LTSでは以下のコマンドでRuby 2.7がインストールされます。お使いのディストリビューション標準のパッケージマネージャーでRuby 2.7系がインストールできない場合、rbenvを使うなどして適宜Ruby 2.7系の最新バージョンをインストールしてください。


```sh
$ sudo apt install ruby-full
```

Rubyがインストールできたら、以下のようにしてRuby 2.7が実行されることを確認します。

```sh
$ ruby -v
ruby 2.7.0p0 (2019-12-25 revision 647ee6f091) [x86_64-linux-gnu]
```

次に手元でのビルドに必要な依存関係をインストールします。


```sh
$ cd wiki.brainux.org
$ bundle install
```

ビルドとプレビューができることを確認します。下記のように `bundle exec jekyll serve` を実行すると localhost:4000 でサーバが
起動している旨のメッセージが出るので、メッセージが見え次第ブラウザで `localhost:4000` を開いてプレビューできます。

```sh
$ bundle exec jekyll serve
Configuration file: /Users/takumi/dev/brain/wiki.brainux.org/_config.yml
            Source: /Users/takumi/dev/brain/wiki.brainux.org
       Destination: /Users/takumi/dev/brain/wiki.brainux.org/_site
 Incremental build: disabled. Enable with --incremental
      Generating...
      Remote Theme: Using theme mmistakes/minimal-mistakes
       Jekyll Feed: Generating feed for posts
   GitHub Metadata: No GitHub API authentication could be found. Some fields may be missing or have incorrect data.
                    done in 53.672 seconds.
 Auto-regeneration: enabled for '/Users/takumi/dev/brain/wiki.brainux.org'
    Server address: http://127.0.0.1:4000
  Server running... press ctrl-c to stop.
````

次に、Textlintとmarkdownlintを使うためにNode.jsとパッケージをインストールします。

```sh
$ cd wiki.brainux.org
$ npm install
```

Node.jsのインストール方法とバージョンは動けば何でも良いです。まずはパッケージマネージャーでインストールしたNode.jsを使ってみて、うまく行かなければnodeenv（nodenvではない！）を使う以下の方法を試してください。nodeenvでインストールした場合は、毎回envをactivateするのを忘れないでください。

```sh
$ pip install nodeenv
$ nodeenv -n 16.13.2 env
$ source ./env/bin/activate
(env) $ npm install
```

Textlintを動かして、正常にlintされるか試します。`npm run fix`で発動する自動修正は、誤検知も意図せず修正してしまう可能性があるため事前によくチェックしてから実行してください。

```sh
$ npm run textlint
$ npm run textlint-fix  # お好みで
```

markdownlintを動かして、正常にlintされるか試します。

```sh
$ npm run mdlint
```


# 各種操作


## 1. a. ページを追加・削除する

- 新たにブランチを作成する
  - 後で Pull Request として提出するため、`master` ブランチには直接コミットしないでください
- `_posts` ディレクトリにあるほかのファイルを参考にして md ファイルを追加します
  - 例: `2038-1-19-doomsday.md`
- 記事内容を記述します
- `npm textlint` と `npm mdlint` を実行し、エラーが出ないことを確認します
  - もし誤検知があった場合はルールを修正するかレビュアーと相談してください
  - エラー箇所をどうしても押し通したい場合はそこだけlintを無効化するよう記述してレビュアーに説明してください
- 一通り追加と削除が終わったら `pull -r`, commit, push します


## 1. b. ページを編集する

- 記事内容を記述します
- `npm textlint` と `npm mdlint` を実行し、エラーが出ないことを確認します
  - もし誤検知があった場合はルールを修正するかレビュアーと相談してください
  - エラー箇所をどうしても押し通したい場合はそこだけlintを無効化するよう記述してレビュアーに説明してください
- 一通り編集が終わったら `pull -r`, commit, push します


## 2. 変更を提出する・レビューを受ける・マージしてもらう

文章に対するどのような変更も、必ずPull Requestを提出してドキュメント編集権限のあるメンバー最低1人にレビューを依頼します。
このレビューに通ると変更がマージされ、公開されます。PRのタイトルや文章は丁寧に記述しましょう。詳細はScrapboxの[超説明・開発フロー](https://scrapbox.io/brain-hackers/%E8%B6%85%E8%AA%AC%E6%98%8E%E3%83%BB%E9%96%8B%E7%99%BA%E3%83%95%E3%83%AD%E3%83%BC)を参照してください。

2021年12月現在、編集権限のあるメンバーは以下の通りです。

- @puhitaku
- @tka3320

注意！GitHub の Brain Hackers organization のメンバーでない人はレビューを依頼できないので、
Discord にてメンバー追加依頼をしてメンバーになってから Pull Request を提出しましょう。


# ファイル名のルール

Wiki のページを生成している Jekyll は、md ファイルの名前から記事の日付や URL を生成します。以下のすべての条件を満たすようにしましょう。

- `YYYY-MM-DD-{英字とハイフンでできたタイトル}.md` の形式にする
- URL が冗長になるので日本語は使わない


# 記述ルール

Wiki の体裁に関するルールを列挙します。コミットの前に従っているかチェックしてください。一部のルールはTextlintやmarkdownlintを使って機械的に調べたり修正できます。


## 文体

基本的には、技術文書のルールと同一です。助詞の使いすぎや表記ゆれはtextlintでチェックできますが、機械的に検知できる範囲は限られているためよく心得ておいてください。


### 「ですます」と「だ・である」は統一する

Linterによるチェック: **なし**

Wiki 全体で「ですます」の形で統一します。


### 依頼する時はできるだけ「します」で締める

Linterによるチェック: **なし**

「〇〇してください」は長いので、「します」で極力統一します。不自然に映る場合は「してください」や「しましょう」を使っても OK です。この文書でも実際にどちらも使用しています。


### 繰り返しや冗長な表現をなくす

Linterによるチェック: textlint（部分的）

冗長な表現を組み込んでしまうことは多いので、極限まで削ります。
「など」「いろいろ」「といった」「〇〇できます」は使いがちですので特に気を付けましょう。

:x: 悪い例: このコマンドを使えば、Linux を起動することなどが可能です。

:o: 良い例: このコマンドで、Linux を起動できます。


### 括弧は基本的に使わない

Linterによるチェック: **なし**

どうしても必要な場合は、名詞の別名や補足といった1〜2単語で済む体言を入れるだけにします。

:x: 悪い例: Linux マシン（Ubuntu か Debian が入っていることが望ましい）を用意します。

:o: 良い例: Ubuntu か Debian がインストールされた Linux マシンを用意します。


### 箇条書きには句読点を入れない

Linterによるチェック: **なし**

箇条書きは段落を表現する道具ではありません。よって、内容が極力短くなるようにしつつ、句読点を置かないようにします。


### 感情を排除する

Linterによるチェック: **なし**

極力スムーズに読める文章になるには、感情的表現を取り除く事が必須です。
文章は技術文書（レポート）のような無味乾燥なものにし、感情は Discord で共有しましょう。


### コードブロックや画像と文章の関わりを示す

Linterによるチェック: **なし**

「以下にコマンド例を示します」などのように、文章と以下に連なる要素を関連付けます。


## Markdown

Markdown はリッチなレンダリングがなくとも読めるシンタックスが特徴です。これを念頭に置いて、以下のルールに従ってください。
一部はmarkdownlintによって違反を検知できます。ここにない細かなルールはmarkdownlintの指示に従ってください。


### 必ずプレビューして確認する

ブラウザで文書を編集すると、コミット前に文書を HTML にレンダーするプレビューが利用可能です。ミスがないか確認してからコミットしましょう。

ローカルのコンソールやエディタで書く場合も、Markdown をプレビューできる環境を用意して確認してからコミットしましょう。


### 改行コードは LF に統一する

Windows で特に気を付けましょう。Git は[コミット時に改行コードを LF のみに強制](https://qiita.com/uggds/items/00a1974ec4f115616580)できます。

`git config` で

```sh
git config --global core.autocrlf input
```

と設定すると、コミット時に Unix style でコミットできます。


### 適切な空行を入れる

Linterによるチェック: あり

以下の箇所には1行空行を入れます。

- 段落と段落の間
- プレーンテキストとプレーンテキスト以外の要素の間
  - 節タイトル
  - 箇条書き
  - テーブル
  - 図
  - コードブロック
  - 引用

以下の箇所には2行空行を入れます。

- 節と節の間


### 適切な空白を入れる

Linterによるチェック: **なし**

プレーンテキスト以外の要素の前後には適切な空白を入れ、表示がおかしくなるリスクを減らしましょう。この文書はWikiでの表示に限られるため空白を欠いても大丈夫ですが、エディタでのシンタックスハイライトに失敗することがありますので気を付けましょう。

:x: 悪い例1: `1.あいうえお`

:o: 良い例1: `1. あいうえお`

:x: 悪い例2: `` このコマンドには`-a`という引数を渡します。 ``

:o: 良い例2: `` このコマンドには `-a` という引数を渡します。 ``


### コードスパンとコードブロックを使い分ける

Linterによるチェック: **なし**

コードスパンとは、`` `ident` ``のように行の中に等幅で文字を入れるスパン要素を指します。

コードブロックとは

```sh
echo foo
```

のように新しい段落で等幅に文字を入れるブロック要素を指します。

コードスパンはコードの識別子や短いコマンドの例示に使い、コードブロックは複数行のプログラムや長いコマンドの例示に使用します。

例1: `ls` コマンドには `-l` というオプションがあります。

例2: `ls` コマンドでファイルの詳細情報を表示するには、以下のように実行します。

```sh
ls -l
```


### 明示的改行はバックスラッシュで行う

Linterによるチェック: **なし**

この節でいう明示的改行とは Hard line breaks のことで、空行による段落区切りや単一の LF による Soft line break ではなく確実に改行を入れることを指します。必要でない限りは使わないことが望ましいです。

明示的な改行の入れ方には行末にスペース2つを入れる方法とバックスラッシュを入れる方法がありまず。前者は通常不可視な上に意味合いがわかりづらいため、バックスラッシュを使用します。
