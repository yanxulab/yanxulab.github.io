# yanxu.io

Yan Xu’s personal website: selected research, visual experiments, and technical writing. Built with Quarto and published to GitHub Pages at <https://yanxu.io>.

## Preview and publish

Install [Quarto](https://quarto.org/docs/get-started/), then run:

```bash
quarto preview
```

Python 3.9+ is required; the profile renderer uses only the standard library. Quarto automatically runs it before building. To build without opening a browser:

```bash
quarto render
```

Pushing to `main` runs `.github/workflows/publish.yml` and deploys `_site/` to GitHub Pages. The custom domain is set in `CNAME`, `_quarto.yml`, and the repository’s Pages settings.

## Update personal information

Edit **`profile.json`**, then preview or render. `_includes/home.html`, `blog.html`, `cv.html`, `bio.html`, and `work.html` are generated; do not edit them directly.

- `bio`: an array of paragraphs; plain text, not HTML.
- `focus`: the short line above your name.
- `portrait`: an image path in `assets/`, or `null` for the notebook motif.
- `email`, `scholar`, `x`, `linkedin`: currently `null` as requested. Add the full profile URL, or just the address for `email`. Empty entries appear as non-clickable icons with a descriptive tooltip.
- `github`: the existing lab GitHub link.
- `cv_pdf`: a local PDF path or public URL. When filled, a download link appears on the CV page.
- `career`: timeline entries, latest first. Dates and roles currently reflect the supplied CMU site; update them as needed.

Example career entry:

```json
{
  "years": "2022 – present",
  "organization": "Organization name",
  "title": "Your role",
  "description": "One sentence about the work.",
  "url": "https://example.com/",
  "logo": "assets/organization.svg"
}
```

Use only dates and roles you have confirmed. `url` and `logo` are optional.

## Add research or multimedia

The homepage’s **Selected work** is curated rather than exhaustive. Add entries to `work`:

```json
{
  "kind": "Research · Venue Year",
  "title": "A short, readable headline",
  "paper_title": "The full paper title",
  "authors": "Author list",
  "summary": "What problem does this solve, and why should someone care?",
  "image": "assets/project-figure.png",
  "image_alt": "Describe what this figure shows.",
  "links": [
    {"label": "Paper", "url": "https://example.com/paper"},
    {"label": "Demo", "url": "https://example.com/demo"}
  ]
}
```

For a playable video, add `"video": "assets/demo.mp4"`; `image` becomes its poster. Videos use controls and do not autoplay. For YouTube or Drive videos, add a `Video` link instead. Images enlarge when clicked. `paper_title` and `authors` are optional, so the same layout works for demos, talks, and visual projects.

Put smaller notebooks and figures in `experiments`; they appear under **From the workbench** on the blog page. Keep the homepage to a few strong examples.

## Write a blog post

The blog index is `essays.qmd`. It follows a reading-first layout: title, contents navigation, then the essays. The three existing outlines are labeled **In preparation** and have no read link in the index.

1. Write the article in `posts/<slug>/index.qmd`:

   ```yaml
   ---
   title: "Article title"
   description: "A short introduction."
   author: "Yan Xu"
   date: 2026-10-16
   draft: true
   toc: true
   ---
   ```

2. Add Markdown headings, equations, code, figures, and notebook links. `posts/_metadata.yml` supplies the article style and an above-body table of contents.
3. Add or update its entry in `profile.json` → `writing`. Use a unique `id` with lowercase letters and hyphens, a title, subtitle, description, topics, status, published flag, and local `url` ending in `.qmd`.
4. When ready, set the article’s `draft: false`, the entry’s `published: true`, and its `status` to a useful label such as `Essay · 2026`. The blog title and read link then point to the article.
5. Preview, commit, and push.

Existing article URLs are preserved. Their source outlines remain directly accessible and clearly marked as works in progress. Changing `published` controls index links; it is not access control.

## Files

- `styles.css`: shared design, responsive layouts, and article typography.
- `assets/site.js`: the interactive temperature demonstration.
- `scripts/render_profile.py`: generates static HTML from the profile data.
- `assets/portrait.jpg`, `assets/research-*.png`: migrated from the supplied [CMU website](https://www.cs.cmu.edu/~yxu2/).
- `notebooks/`: experiments; the Day 1 tokenizer notebook is linked from the blog.

The existing experimental work and learning roadmap are retained. Do not publish unsupported closed-model architecture or parameter-count claims; distinguish official facts, estimates, and unknowns.
