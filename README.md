# Github name finder
Github上で使用されていないユニークネーム(userId)を検索することができます。

You can find the names that Github users havn't used yet.

## 環境変数
[.env.example](.env.example)を参考にして.envを作成して下さい。

```python
NAME_LENGTH= # 検索する名前の長さ 
TARGET_COUNT= # 検索する名前の個数
MAX_ATTEMPT= # 最大繰り返し回数
```

## 注意事項
1文字、2文字、3文字の名前も検索可能ですが、現在のGithub上では4文字以上の名前でなければ設定ができないようになっています。

## ライセンス
このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。