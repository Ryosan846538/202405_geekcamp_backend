# 2024 技育キャンプ vol.5 バックエンドリポジトリ

## clone してからやること

- `python -V`でバージョン確認、`.tool-versions`のバージョンと異なっていれば、`asdf install python 3.12.0`をして、`asdf local python 3.12.0`でプロジェクトに適用
- `pip install -r requirements.txt`でパッケージインストール
- `src/`にいろいろ追加していこう

## gitemoji を使うならルールは以下の通りでよろしく

```
# 🐛  :bug: バグ修正
# 👍  :+1: 機能改善
# ✨  :sparkles: 部分的な機能追加
# 🎨  :art: デザイン変更のみ
# 💢  :anger: コンフリクト
# 🚧  :construction: WIP
# 📝  :memo: 文言修正
# ♻️   :recycle: リファクタリング

# 🔥  :fire: 不要な機能・使われなくなった機能の削除
# 💚  :green_heart: テストやCIの修正・改善
# 👕  :shirt: Lintエラーの修正やコードスタイルの修正
# 🚀  :rocket: パフォーマンス改善
# 🆙  :up: 依存パッケージなどのアップデート
# 👮  :cop: セキュリティ関連の改善
# ⚙   :gear: config変更
# 📚  :books: ドキュメント
```
