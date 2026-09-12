# yanxudev.github.io

Yan Xu's technical blog: foundation models, multimodal generation, post-training, and reinforcement learning.

## One-time setup

1. Sign in to GitHub as `yanxudev`.
2. Create a **public** repository named exactly `yanxudev.github.io` without adding a README or license.
3. From this project directory, run:

   ```bash
   git init
   git add .
   git commit -m "Initialize technical blog"
   git branch -M main
   git remote add origin https://github.com/yanxudev/yanxudev.github.io.git
   git push -u origin main
   ```

4. In the repository, open **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
5. Open the **Actions** tab and wait for “Publish Quarto site” to turn green.
6. Visit <https://yanxudev.github.io>. Initial DNS/TLS propagation can take a few minutes.

## Local preview

Install [Quarto](https://quarto.org/docs/get-started/) once, then run:

```bash
quarto preview
```

The browser will live-reload as you edit `.qmd` files.

## Publishing workflow

1. Write in a post's `index.qmd`.
2. Put experiment notebooks under `notebooks/` and figures beside the post or under `assets/`.
3. Preview locally with `quarto preview`.
4. For a private work-in-progress post, use `draft: true`; set it to `false` when it should appear on the public site.
5. Commit and push. GitHub Actions renders and deploys automatically.

## Editorial rule

Every flagship article should include:

- a historical question and architectural evolution;
- a derivation with dimensions and assumptions;
- a clean, runnable Colab implementation;
- a controlled ablation and labeled visualization;
- failure analysis and interview-grade takeaways;
- links to primary sources and reproducibility details.

Do not publish unsupported layer counts or parameter counts for closed models. Label claims as official, third-party estimate, or unknown.

## Files to personalize before launch

- `about.qmd`: email and professional bio
- `_quarto.yml`: description/footer if desired
- `assets/og-placeholder.svg`: replace with a polished post image later
- Post dates and `draft` flags
