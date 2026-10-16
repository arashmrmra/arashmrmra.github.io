# AI-assisted Persian to English translation

This workflow creates a review-only pull request. It never commits directly to main, merges a PR, or publishes a translation by itself.

## One-time setup

1. In repository Settings, open Secrets and variables → Actions and add repository secret OPENAI_API_KEY.
2. Ensure Actions are enabled and GITHUB_TOKEN can write repository contents and pull requests. The workflow declares only contents: write and pull-requests: write.
3. Keep branch protection/review requirements enabled if available. Never put API keys in source files, issue comments, workflow inputs, or logs.
4. OpenAI API usage is billed separately from a ChatGPT subscription. The selected article text is sent to OpenAI for translation.

## Run

1. Open Actions → Prepare English translation → Run workflow.
2. Select branch main and enter a Persian Markdown post path, e.g. _posts/2026-10-20-my-next-post.md.
3. Inspect the pull request. Check translation quality, technical details, code fences, links, front matter, canonical URL and language alternates.
4. Merge only after human approval. Until then, the draft branch does not affect the live GitHub Pages site.

The source file receives only a translation_url front-matter change, alongside the new English post. Both changes are included in the PR for review.

## Safety and limits

- Manual dispatch only; no run on every push.
- Source path is restricted to Markdown files directly inside _posts; source size is limited to 150 KB.
- Python standard library only; the API key is not printed.
- Fenced and inline code are masked during translation and restored exactly; tests check this behavior.
- Existing translations and permalink collisions are rejected rather than overwritten.
- API output is untrusted and must be reviewed by a human.
- Workflow actions are pinned to full commit SHAs.
- Restrict who may run Actions and protect main; review workflow changes before merging.

## SEO behavior

Each translated post gets a stable /en/posts/<slug>/ permalink, English language metadata, a reciprocal translation_url, and a canonical URL through the existing layout. The sitemap emits reciprocal hreflang links for translated pairs. Existing article text and URLs are otherwise preserved.
