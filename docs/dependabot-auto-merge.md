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

## 注意

- 既にオープンしている PR には遡って効かない。対象にしたい場合は PR を
  一度 close して reopen するか、次の Dependabot PR から適用されるのを待つ。
- 競合している PR は自動マージされず、そのまま残る（手動対応が必要）。
- 止めたいときは、対象リポジトリの `.github/workflows/dependabot-auto-merge.yml` を
  削除するか、Actions 画面でワークフローを無効化する。
