# 導入手順（対象リポジトリ1件あたり）

1. `templates/workflows/` の YAML を対象リポジトリの `.github/workflows/` へコピー
2. `templates/config/labeler.yml` を `.github/labeler.yml`、`templates/config/dependabot.yml` を `.github/dependabot.yml` へコピー
3. 対象リポジトリにラベルを作成: bug / enhancement / documentation / question / needs-info / ci / tests / dependencies / pinned / security
4. `ci-summary.yml` の `workflows: ['CI']` を対象リポジトリの実際の CI ワークフロー名に合わせる
5. Issue を1件テストで作り、候補コメントが付くことを確認してから `APPLY_LABELS` を 'true' にする
