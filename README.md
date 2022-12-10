# acac

競プロ便利 CLI ツール。[AtCoder](https://atcoder.jp/) と [アルゴ式](https://algo-method.com/) に対応。

＊現在 Pre-release のため、挙動やコマンドは変更される場合があります。

## 概要

競技プログラミングの過去問を解くときの（個人的に）典型的なワークフローを CLI として自動化したものです。

過去問だけでなく開催中のコンテストでも使えますが、ログイン機能は実装されていないため、手動で HTML ファイルを取得する必要があります。

## インストール

Python 3.7 以上がインストールされていれば利用可能です。

```sh
pip install acac
```

## 事前準備

作業ディレクトリに移動して、`acac init` を実行します。

```sh
# 例
mkdir kyopro
cd kyopro
acac init
```

`acac.toml` が作成されます。これが設定ファイルです。

## 使用例

1. まず、ブラウザで問題ページ（例えば、[ABC 280 A - Pawn on a Grid](https://atcoder.jp/contests/abc280/tasks/abc280_a)）にアクセスします。

1. URL をコピーします

   - 使用可能な場合、以下のショートカットキーが便利です。
     - Windows: <kbd>Ctrl</kbd>+<kbd>L</kbd>, <kbd>Ctrl</kbd>+<kbd>C</kbd>
     - Mac: <kbd>command</kbd>+<kbd>L</kbd>, <kbd>command</kbd>+<kbd>C</kbd>

1. ターミナルで以下のようなコマンドを実行すると、問題用のフォルダ（以下、問題フォルダ）に環境が自動作成されます。

   ```sh
   acac https://atcoder.jp/contests/abc280/tasks/abc280_a
   ```

   <details><summary>処理の詳細</summary>

   - 問題フォルダを作成します。
   - ソースコードのテンプレートファイルが用意されていれば、そのファイルをコピーします。そうでなければ、ソースコード用の空ファイルを作成します。
   - （`cache.html` が無ければ）問題ページにアクセスし、HTML ファイルを `cache.html` として保存します。
   - `metadata.toml` を作成します。
     - 問題ページのタイトルと URL が格納されます。
   - 問題ページ中からテストケースのサンプルを抽出し、テキストファイルとして保存します。
   - `acac.toml` で設定したコマンドを実行します。
   - `acac.toml` で設定したメッセージをクリップボードにコピーします。
     - 私は Git のコミットメッセージを設定しています。

   </details>

1. コードを書いて問題を解きます。

1. ターミナルで以下のようなコマンドを実行します。

   ```sh
   acac https://atcoder.jp/contests/abc280/tasks/abc280_a -j
   ```

   すると、以下のように処理されます。

   - `acac.toml` で設定したコマンドを実行します（バージョン確認、コンパイル等）。
   - 用意されたテストケースに対してジャッジを行います。
   - `acac.toml` で設定したコマンドを実行します（クリーンアップ等）。
   - すべて AC であれば、ソースコードがクリップボードにコピーされますので、ブラウザに貼り付けて提出してください。
   - 「他の人の提出を確認しますか？」と聞かれるので、`y` と答えれば、同じ言語で AC した提出の一覧ページをブラウザで開きます。
   - `acac.toml` で設定したメッセージをクリップボードにコピーします。

## 設定ファイル

私が実際に使用している設定ファイルは [こちら](https://github.com/seijinrosen/kyopro/blob/main/acac.toml) です。

```toml
# 設定ファイルの例

[create]
# 環境作成後に実行されるコマンドのリスト（以下は git add をして、VSCode でソースコード用のファイルを開いている）
post_create_commands = [
    "git add ${dir_path}/in ${dir_path}/out ${dir_path}/metadata.toml",
    "code . ${dir_path}/${source_file_name}",
]
# 環境作成後にクリップボードにコピーされるメッセージ
clipboard_message = "Create: ${url}"


[judge]
# ジャッジ後にソースコードをクリップボードにコピーするかどうか
copy_source_code_when_ac = true
# ジャッジ後にクリップボードにコピーされるメッセージ
clipboard_message = "AC: ${url} ${source_file_name}"


[language]
# デフォルトの使用言語
default = "cpp"


[language.settings.cpp]
# ソースコードのファイル名
source_file_name = "main.cpp"
# テンプレートファイルのパス
template_file_path = "templates/main.cpp"
[language.settings.cpp.commands]
# ジャッジ前に実行するコマンドのリスト（以下はバージョンを表示し、コンパイルしている）
pre_execute = [
    "g++ --version",
    "g++ ${dir_path}/${source_file_name} -o ${dir_path}/a.out",
]
# 実行コマンド
execute = "${dir_path}/a.out"
# ジャッジ後に実行するコマンドのリスト（以下は `a.out` を削除している）
post_execute = ["rm ${dir_path}/a.out"]


[language.settings.python3]
# ...
```

### `${var}` の置換リスト

| 置換前              | 置換後                                         |
| ------------------- | ---------------------------------------------- |
| ${dir_path}         | 問題フォルダのパス                             |
| ${lang}             | 言語名                                         |
| ${source_file_name} | ソースコードのファイル名（パスではありません） |
| ${url}              | 問題ページの URL                               |

## コマンドオプション

### モード指定

| オプション   | モード                                                                  |
| ------------ | ----------------------------------------------------------------------- |
| -c, --create | 作業環境構築（デフォルト）                                              |
| -j, --judge  | ジャッジ                                                                |
| -m, --manual | URL にアクセスせず、HTML ファイルを手動で配置してテストケースを作成する |

ログインが必要な場合、`acac <url> -m` を実行後、問題フォルダに問題ページの HTML ファイルを配置してください。

### その他

`acac.toml` に指定したデフォルト値を一時的に上書きするような動きをします。イコールは必須です。

| オプション                            | 上書きされるもの         |
| ------------------------------------- | ------------------------ |
| -l, --lang, lang=LANG_NAME            | 使用言語                 |
| -s, --source, source=SOURCE_FILE_NAME | ソースコードのファイル名 |

```sh
# 例
acac https://atcoder.jp/contests/abc280/tasks/abc280_a -l=python3 --source=main2.py
acac https://atcoder.jp/contests/abc280/tasks/abc280_a -s=main2.py lang=python3 --judge
```

## コンセプト

### なぜ `acac create <url>` や `acac judge <url>` のような一般的な CLI の慣例に沿っていないのか

1. `acac <url>` で環境作成
1. コードを書く
1. ターミナルで <kbd>Ctrl</kbd>+<kbd>P</kbd>
1. 末尾に `-j` をつけてジャッジ

という流れを高速で行うためです。基本的に、一つの問題に対し複数のコマンドを実行することが多いので、URL のあとにコマンドやオプションを指定する方式を採っています。

### 問題フォルダ構成が URL そのままで冗長なのはなぜか

開発当初は `AtCoder/ABC/280/A/` のようなフォルダ構成にしていましたが、過去のコンテストの URL 規則との整合性や、未来への拡張性、[ghq](https://github.com/x-motemen/ghq) のような厳密性を保持するため、現在のような形にしました。
