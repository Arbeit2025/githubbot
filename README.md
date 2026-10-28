# githubbot👁️👁️🎥

自分の GitHub リポジトリを自動整理する Bot のスターターキット。
常駐サーバーを持たない GitHub Actions 式で、Issue 整理・PR ラベル・CI 連携を行う。

- `bot/label_logic.py` — ラベル判定の純粋ロジック（キーワード／変更ファイル／PRサイズ）。ネットワークなし、単体テスト付き
- `bot/triage.py` — dry-run 専用 CLI。実行してもリポジトリは変更されない
- `templates/workflows/` — 対象リポジトリへコピーするワークフロー雛形（Issue triage、PR labeler、stale、CI失敗通知）
- `templates/config/` — labeler と Dependabot の設定雛形
- `docs/design.md` — 方式比較と安全の既定値 / `docs/install.md` — 導入手順

## ローカル検証
```bash
python -m unittest discover -s tests -v
python -m bot.triage --kind issue --title "ログインでエラー" --body "再現手順: ログインすると500エラー"
python -m bot.triage --kind pr --title "docs update" --files docs/a.md,.github/workflows/ci.yml --lines 120
```

## ステータス
スターターキット作成済み・ローカル検証済み。対象リポジトリへの導入は未実施（導入先1件から試行する）。
