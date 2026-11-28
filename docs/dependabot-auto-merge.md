# Dependabot PR 自動マージ

`templates/dependabot-auto-merge.yml` は、Dependabot が作った PR を自動でマージするための
GitHub Actions ワークフローの雛形。対象リポジトリの `.github/workflows/` に置いて使う。

## 対象

- 作者が `dependabot[bot]` の **非 Draft** PR の **全部**（メジャー更新を含む）。
  朝の未マージPRチェックと同じルール。
- Draft の PR には何もしない（Ready for review になってから対象になる）。
- Dependabot 以外の作者の PR には一切触れない。

## 対象外（絶対に導入しない）

Studylog 系の次のリポジトリには、このワークフローを置かない。

- `studylog`
- `studylog-dev-private`
- `Studylog_dev_close`
- `studylogcorporatesite`
- `studylog_private_app`

## 前提条件

1. 対象リポジトリで Dependabot の更新 PR が作られていること
   （`.github/dependabot.yml` の設定があること）。
2. 対象リポジトリの **Settings > General > Pull Requests** で
   **"Allow auto-merge"** を有効化しておくこと。
   これがオフだと `gh pr merge --auto` が失敗し、ワークフローがエラーになる。
3. ブランチ保護で必須チェックを設定している場合は、そのチェックが通った時点で
   自動マージされる（チェックが終わるまでは待機状態になる）。

## 導入手順

1. 対象リポジトリの **Settings > General > Pull Requests** で
   "Allow auto-merge" を有効化する。
2. `templates/dependabot-auto-merge.yml` の内容を、対象リポジトリの
   `.github/workflows/dependabot-auto-merge.yml` として置く。
   - GitHub App（Muse コネクタ）からは `.github/workflows/` へ書き込めないため、
     配置は **GitHub の Web エディタ経由** で行う。
3. 次に Dependabot の PR が作られたら、ワークフローが auto-merge を有効化し、
   条件がそろい次第マージされることを確認する。

## 動作

- `pull_request` イベント（opened / reopened / synchronize / ready_for_review）で起動。
- ジョブの `if` 条件で、作者が `dependabot[bot]` かつ非 Draft の場合だけ実行する。
- `dependabot/fetch-metadata` で Dependabot の PR であることを確認したうえで、
  `gh pr merge --auto --merge`（`GH_TOKEN` = ワークフローの `GITHUB_TOKEN`）で
  auto-merge を有効化する。実際のマージは GitHub 側が行う。
- **リトライ（2026-11-28 追加）**：auto-merge の有効化は、一時的な API エラー
  （502 Bad Gateway 等）で失敗しても黙って終わらず、30 秒間隔で最大 3 回まで再試行する。
  2026-11-25 に plotbox #5 が 502 の一発失敗で 3 日間滞留した事故を受けた対策。
- **日次スイープ（2026-11-28 追加）**：`schedule`（毎日 04:23 UTC = 13:23 JST）と
  `workflow_dispatch`（手動実行）で起動する `sweep` ジョブが、そのリポジトリの
  オープンな Dependabot PR のうち、非 Draft かつ auto-merge 未設定のものを拾い、
  auto-merge を有効化し直す。PR イベントの発火失敗や、ワークフロー配置前に
  開かれた PR の取りこぼし（2026-11-26 に新規リポ 9 件で発生）を自己修復する。

## 注意

- PR イベントを取りこぼした PR も、日次スイープが最大で約 1 日遅れで拾い直す。
  急ぐ場合は Actions 画面からこのワークフローを手動実行（workflow_dispatch）する。
- 競合している PR は自動マージされず、そのまま残る（手動対応が必要）。
  スイープは auto-merge の有効化までで、競合そのものは解消しない。
- 止めたいときは、対象リポジトリの `.github/workflows/dependabot-auto-merge.yml` を
  削除するか、Actions 画面でワークフローを無効化する。
