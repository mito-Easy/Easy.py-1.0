# 🚀 マスター自作言語エディタ (Master Custom Language Editor)

直感的で楽しいオリジナル自作言語を実行・編集できる、軽量で多言語対応（日本語 / 英語）のGUIコードエディタです。
ファイル1つ（`Easy.py`）で手軽に起動し、スマートフォンの横画面などの小さな画面環境でもすべてのボタンが1画面にピタッと収まるように最適化されています。

---

## ✨ 主な機能と特徴 (Features)

- **オリジナル言語エンジン**: 独自のコマンドを使って、パスワード生成やタイピングアニメーション、効果音、条件に応じた処理などを簡単かつ直感的に記述・実行できます。
- **多言語UI対応**: プルダウンメニューから「日本語」と「English」をいつでも切り替え可能。ボタンやラベルのテキストも文字化けすることなく安全に自動翻訳されます。
- **💾 コードの保存・読み込み**: 編集中の自作コードをワンクリックで外部ファイル（`my_code.txt`）に保存し、いつでも一瞬で読み込んで復元できます。
- **📱 レスポンシブ＆コンパクト設計**: 各テキスト枠の高さや余白を極限まで最適化。スマホやタブレットの横画面環境でもボタンがはみ出さず、スクロール不要で快適に操作可能です。
- **❌ 安全な終了機能**: アプリをエラーなく安全にパッと閉じることができる終了ボタンを搭載。

---

## 🛠️ 動作環境 (Requirements)

- Python 3.x
- `tkinter` (Python標準ライブラリ)

---

## 🚀 使い方 (How to Run)

1. このリポジトリから `Easy.py` をダウンロードします。
2. 以下のコマンドを実行してエディタを起動します：

```bash
python Easy.py
```

### 自作言語のサンプルコード（日本語）
```text
入力 桁 = パスワードは何桁にする？
パスワード 生成結果 = 桁
アニメ 生成したパスワードは以下です：
表示 生成結果
音
警告 完了しました！
```

### Sample Code (English)
```text
ask length = How many digits?
password res = length
type Password is:
print res
beep
alert Done!
```

---

## 📂 ファイル構成 (File Structure)

- `Easy.py` : アプリケーションのメインソースコード
- `my_code.txt` : コード保存時に自動生成されるテキストファイル

---

## 📝 ライセンス (License)

This project is licensed under the MIT License.
⚠️ ライセンスと著作権について / License and Copyright
このプロジェクトは GNU General Public License v3.0 (GPLv3) のもとで公開されています。

無断転載・パクリの禁止: 本プロジェクトのコードをコピー・改変して、自身の成果物として隠蔽・独占配布することはライセンス違反です。
ソースコード公開の義務: 本プロジェクトのコードを一部でも使用または改変して再配布する場合、その成果物のソースコードも完全にGPLv3で公開する義務が発生します。
著作権表示の義務: コードを利用・改変する際は、必ず原作者（minaton）の著作権表示を残す必要があります。
悪質な無断転載やライセンス違反を発見した場合は、GitHubへのDMCAテイクダウン申請（強制削除申し立て）を含めた法的措置を即座に講じます。

This project is licensed under the GNU General Public License v3.0 (GPLv3).

Copyleft: Any derivative work or modifications of this source code must also be open-sourced under the GPLv3.
Attribution: You must retain the original copyright notice and give appropriate credit to the author.
Unauthorized copying, distribution, or plagiarism without complying with the GPLv3 terms will result in an immediate DMCA takedown notice to GitHub.
Copyright (c) 2026 minaton
# Easy.py-1.0
Compared to the previous version, save, load, and exit functions have been added. 
