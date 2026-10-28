# 設計

## 方式の選択（サーバーを持たない GitHub Actions 式を第一候補とする）
- A. GitHub Actions 式（採用候補）: 各リポジトリに小さなワークフローを置く。常駐サーバー不要、権限は標準の GITHUB_TOKEN のみ、無料枠で十分。Issue整理・PRラベル・stale・CI失敗通知・Dependabot は全てこの方式で実現できる。
- B. Probot（Node.js）式 GitHub App: イベント反応が最も柔軟だが、App登録・秘密鍵管理・ホスティング（Render等）が要る。Aで不足が出たら移行。
- C. Python Webhook 式: Flask + Render（minigame と同じ構成）に Webhook を受ける。既存スタックと一致するが、署名検証と常駐管理が増える。

## 安全の既定値
- ラベル自動付与は最初 `APPLY_LABELS: 'false'`（候補をコメントで提示するだけ）。試行期間後にオン。
- ワークフローの permissions は必要最小限（issues/pull-requests の write のみ、contents は read）。
- stale のクローズは 60日+14日、pinned/security ラベルは免除。
- 対象リポジトリへは1件ずつ導入し、挙動を見てから広げる（最初は新規 or 小さいリポジトリ推奨）。

## 機能一覧
1. Issue整理: キーワード→ラベル候補、本文が短い Issue へ needs-info、stale 管理、Dependabot
2. PR整理: 変更ファイル→ラベル（actions/labeler）、サイズ目安は bot/label_logic.py
3. CI連携: CI失敗時に PR へ要約コメント、Actions 自体の更新も Dependabot で追従
