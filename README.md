# yanxu.io

Yan Xu’s personal website: selected research, visual experiments, and technical writing. Built with Quarto and published to GitHub Pages at <https://yanxu.io>.

## Preview and publish

Install [Quarto](https://quarto.org/docs/get-started/), then run:

```bash
bash scripts/preview.sh
```

Python 3.9+ is required; the profile renderer uses only the standard library. Quarto automatically runs it before building. To build without opening a browser:

```bash
quarto render
```

Pushing to `main` runs `.github/workflows/publish.yml` and deploys `_site/` to GitHub Pages. The custom domain is set in `CNAME`, `_quarto.yml`, and the repository’s Pages settings.

After rendering, `scripts/version_stylesheet.py` adds a content hash to the generated stylesheet filename and updates page links. This keeps cached CSS from a different build from changing the restored layout. Continue editing `styles.css` as usual.

### Private development

During development, keep changes local and open <http://127.0.0.1:4321> after starting the preview above. The helper rebuilds the site and explicitly binds to the loopback address, limiting preview access to this computer. Stop preview with `Ctrl+C`. It uses installed Quarto, with a fallback to the temporary runtime downloaded for this checkout.

The current public version on `yanxu.io` stays online; local edits do not update it. Push to `main` only when ready to publish. This repository is public, so pushing unfinished source to another branch would make that source public even though it does not deploy the site.

GitHub Pages does not offer password protection for personal sites. Private Pages publication is an Enterprise Cloud feature for eligible organization project sites; see [GitHub’s access-control documentation](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site). An online preview restricted to your identity needs authenticated hosting or an access-control service.

## Update personal information

Edit **`profile.json`**, then preview or render. `_includes/home.html`, `blog.html`, `cv.html`, `bio.html`, and `work.html` are generated; do not edit them directly.

- `bio`: an array of paragraphs; plain text, not HTML.
- `bio_links`: optional name-to-URL mapping. Each name is linked only at its first occurrence in the bio; longer names take precedence, so `Gemini Omni` stays a single link.
- `portrait`: an image path in `assets/`, or `null` for the notebook motif.
- `email`, `scholar`, `x`, `linkedin`: add the full profile URL, or just the address for `email`. Empty entries appear as non-clickable icons with a descriptive tooltip. Icons are ordered LinkedIn, Email, Google Scholar, GitHub, X.
- `github`: the profile or repository URL used by the GitHub icon.
- `cv_pdf`: a local PDF path or public URL. When filled, a download link appears on the CV page.
- `career`: timeline entries, latest first. Both the homepage and CV show `years`, organizations, roles or work areas, and work summaries. Use an open end date such as `2025–` for a current role. Write two plain-text sentences: `description` explains the work and methods; `impact` explains the qualitative result on a separate line. Do not publish internal metrics.

Example career entry:

```json
{
  "years": "2022 – present",
  "organization": "Organization name",
  "title": "Your role",
  "description": "What you did and the methods you used.",
  "impact": "The qualitative result of this work.",
  "url": "https://example.com/",
  "logo": "assets/organization.svg"
}
```

Use only dates and roles you have confirmed. `url` and `logo` are optional.

## Add research or multimedia

The homepage’s **Research** lists papers newest first, with a year beside each venue or submission status. Add entries to `work` in that order:

```json
{
  "kind": "Research",
  "year": 2026,
  "venue": "Venue name",
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

For a manuscript under review, use `"venue": "Manuscript under review"` and `"links": []` until public links are available. Add the confirmed author list when ready. `year` and `venue` are optional for other types of work.

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
- `assets/portrait-original.jpg`: the original photo migrated from the supplied [CMU website](https://www.cs.cmu.edu/~yxu2/), preserved unchanged.
- `assets/portrait-headshot.jpg`: a closer head-and-shoulders version used by the site; [editing details](docs/portrait-edit.md).
- `assets/research-*`: paper figures, including the supplied CamRM overview, the official Co-Director pipeline, and figures migrated from the CMU website. [Figure sources](docs/research-assets.md).
- `notebooks/`: experiments; the Day 1 tokenizer notebook is linked from the blog.

The existing experimental work and learning roadmap are retained. Do not publish unsupported closed-model architecture or parameter-count claims; distinguish official facts, estimates, and unknowns.
