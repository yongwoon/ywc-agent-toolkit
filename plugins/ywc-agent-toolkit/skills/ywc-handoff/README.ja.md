# Handoff

Content write の前に、作成済み handle の identity、regular type、expected owner、mode `0600` を検証します。失敗時は書き込みも chown も行いません。空・未完成ファイルの削除には作成 identity と expected owner の一致を両方確認します。書き込み・close 後の検証も維持します。

Expected owner はファイルを exclusive 作成した、権限のある aggregator プロセスの effective UID/user です。その identity と所有者を比較し、確認不能・不一致なら `NEEDS_CONTEXT` を返します。Chown や所有権が不確実なファイルへの操作は行いません。

現在の会話と明示的に貼り付け・添付された artifact から、一時 Markdown 引き継ぎファイルを作成します。Session log の検索、記載されたパスや URL の読み取り、既存 artifact の複製は行いません。Artifact はパスだけで参照し、credentials、tokens、個人情報、無関係な非公開情報を削除します。

Goal、State、Decisions、Dead ends、Next step、References、Suggested skills の7 section を順に含めます。空欄は理由付きの `N/A — <reason>` とし、状態や決定を創作しません。Read-only agent は inline evidence だけを返し、権限のある aggregator だけが書き込みます。Owner/input/output/status の不一致は `NEEDS_CONTEXT` です。

Canonical `${TMPDIR:-/tmp}` root と検証済みの stable directory handle を使います。名前は `ywc-handoff-`、timestamp、正規化した `[a-z0-9-]` slug、固有 suffix で構成します。両端の hyphen を除き、空なら `session`、正規化後48文字超なら拒否します。外部・逸脱・検証不能なパスを拒否します。Exclusive/no-follow 作成と作成時からの `0600` が必要です。既存ファイルや symlink を上書きしません。名前衝突だけ合計5回まで試行します。権限・書き込み失敗では成功を報告せず、この操作で作成したと証明できるファイルだけを片付けます。

Identity、owner、権限、完成した redacted 内容の検証後にだけ `DONE` とパスを報告します。一時ファイルは自動削除されません。永続保存への移動には保存先への明示的な承認が必要です。

使用: `Use $ywc-handoff to save a concise handoff for this session.`

`allow_implicit_invocation: false` は明示的 invocation の推奨であり、runtime の強制保証ではありません。Eval と source fixture は指示契約のみを検証します。安全な隔離実行がなければ実際の model/tool/filesystem 動作は `UNVERIFIED` です。
