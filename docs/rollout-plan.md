# 全リポジトリ展開計画（2026-10-29時点、全20リポジトリ）

## ラベル（全リポジトリ共通、16種）
bug / enhancement / documentation / question（多くは既定で存在）、needs-info / security / performance / ci / tests / dependencies / pinned / size/S / size/M / size/L / size/XL
作成方法：専用ツールはないが、Issue へ未存在ラベルを付けると GitHub API が自動作成することを githubbot で実証済み。各リポジトリで「ラベル整備用 Issue」を1件作り、全ラベルを付けてから外し、Issue はクローズする（ラベル自体は残る）。

## 導入セット（リポジトリごとに調整）
- 共通: issue-triage（自動付与オン）、pr-labeler + labeler.yml、stale
- dependabot: pip のみの固定にせず、そのリポジトリに requirements.txt / package.json がある場合だけ該当エコシステムを入れ、github-actions はワークフローがある場合のみ（無いと Dependabot がエラーを出すため）
- ci-summary: CI ワークフロー（名前 CI）が無いリポジトリには入れない
- ci.yml 本体: 他リポジトリの事情（言語・テスト）が違うためコピーしない

## 分類
- A（直接 main へ導入可、16件）: githubbot（導入済み・自動付与オン化中）、wikipediabot、minigame、cocoletter、mywebsite、Arbeit2025、chat_talking_ch、zhtranslate、kakeibomini3、minidiary、plotbox、wikitranslate、volapuktranslate、wikitransgeo、wikisourcesearch、wikiImagesearch
- B（Studylog系、既存ルールで ai/muse ブランチ＋PR 方式、4件）: studylog、studylog-dev-private、Studylog_dev_close、studylogcorporatesite

## 注意点
- stale は 60日無活動＋14日で自動クローズする。古い Issue があるリポジトリでは導入直後から対象になり得るため、B分類と古い Issue のある所は個別確認。
- ワークフローファイルは API から書けない（403）ため、各リポジトリともブラウザ画面からのアップロードになる。16件＋PR4件は複数回に分けて実施する。

## 実施結果（2026-10-29）
- A分類16件（githubbot を含む）への導入が完了。ラベル16種・labeler・dependabot（Actions週次）・ワークフロー3本（issue-triage は自動付与オン、pr-labeler、stale）を全件に導入し、issue-triage.yml の blob（11547b83）が配布版と全リポジトリで一致することを読み戻し確認済み。
- B分類4件（Studylog系）は未実施。ai/muse ブランチ＋PR 方式で別途行う。
- 新規リポジトリの検知は週次チェック（cron: githubbot-weekly-repo-check、毎週月曜）で報告される。自動適用はされない。
