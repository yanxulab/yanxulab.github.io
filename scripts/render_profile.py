"""Render editable profile data into static Quarto includes (standard library only)."""

import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_includes"


def esc(value):
    return html.escape(str(value), quote=True)


def url(value):
    """Accept web/email links and local site paths; emit rendered HTML paths."""
    value = str(value)
    parts = urlsplit(value)
    if parts.scheme:
        if parts.scheme not in {"https", "http", "mailto"}:
            raise ValueError(f"Unsupported link scheme: {parts.scheme}")
        return esc(value)
    if value.startswith("//") or ".." in parts.path.split("/"):
        raise ValueError(f"Use a root-relative site path: {value}")
    if value.startswith("#"):
        return esc(value)
    path = value.removesuffix(".qmd") + (".html" if value.endswith(".qmd") else "")
    return esc("/" + path.lstrip("/"))


def link(label, target, css=""):
    return f'<a class="{css}" href="{url(target)}">{esc(label)}</a>'


# Small inline SVGs keep icons crisp and avoid external fonts or icon requests.
ICONS = {
    "scholar": '<path d="m2 9 10-6 10 6-10 6L2 9Z"/><path d="M6 12v6c3 3 9 3 12 0v-6M22 9v8"/>',
    "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    "github": '<path d="M9 19c-4 1-4-2-6-2m12 4v-3.5c0-1 .1-1.5-.5-2 3-.4 5.5-1.5 5.5-6a4.7 4.7 0 0 0-1.3-3.3 4.3 4.3 0 0 0-.1-3.2s-1-.3-3.4 1.3a11.6 11.6 0 0 0-6.4 0C6.4 2.7 5.4 3 5.4 3a4.3 4.3 0 0 0-.1 3.2A4.7 4.7 0 0 0 4 9.5c0 4.5 2.5 5.6 5.5 6-.6.5-.6 1.3-.5 2V21"/>',
    "x": '<path d="M4 3h4l12 18h-4L4 3ZM20 3 4 21"/>',
    "linkedin": '<path d="M4 9v12M10 21V9m0 5a5 5 0 0 1 10 0v7"/><circle cx="4" cy="4" r="1" fill="currentColor" stroke="none"/>',
}
LABELS = {"linkedin": "LinkedIn", "email": "Email", "scholar": "Google Scholar", "github": "GitHub", "x": "X"}


def socials(profile):
    items = []
    for key, label in LABELS.items():
        icon = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[key]}</svg>'
        target = profile.get(key)
        if target:
            target = "mailto:" + target if key == "email" else target
            items.append(f'<a class="social-icon" href="{url(target)}" aria-label="{label}" title="{label}">{icon}</a>')
        else:
            items.append(f'<span class="social-icon unavailable" role="img" aria-label="{label}: link coming soon" title="{label} · link coming soon">{icon}</span>')
    return '<div class="social-links" aria-label="Find me online">' + "".join(items) + "</div>"


def bio(profile):
    targets = profile.get("bio_links", {})
    # Match complete names, preferring "Gemini Omni" over its "Gemini" prefix.
    names = sorted(targets, key=len, reverse=True)
    pattern = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(name) for name in names) + r")(?!\w)") if names else None
    linked, paragraphs = set(), []
    for paragraph in profile["bio"]:
        parts, start = [], 0
        matches = pattern.finditer(paragraph) if pattern else ()
        for match in matches:
            parts.append(esc(paragraph[start:match.start()]))
            name = match.group()
            parts.append(link(name, targets[name]) if name not in linked else esc(name))
            linked.add(name)
            start = match.end()
        parts.append(esc(paragraph[start:]))
        paragraphs.append('<p>' + "".join(parts) + '</p>')
    return "".join(paragraphs)


def career(profile):
    entries = profile.get("career", [])
    if not entries:
        return '<div class="timeline"><div class="timeline-entry"><div class="timeline-date">Now</div><div class="timeline-detail"><h3>Foundation Models &amp; Post-Training</h3><p>Studying the objectives, implementations, and systems behind language and multimodal models.</p></div></div></div>'
    rows = []
    for entry in entries:
        organization = esc(entry["organization"])
        if entry.get("url"):
            organization = link(entry["organization"], entry["url"])
        logo = f'<img class="career-logo" src="{url(entry["logo"])}" alt="" width="36" height="36" loading="lazy">' if entry.get("logo") else ""
        impact = f'<p class="timeline-impact">{esc(entry["impact"])}</p>' if entry.get("impact") else ""
        rows.append(f'<li class="timeline-entry"><div class="timeline-date">{esc(entry["years"])}</div><div class="timeline-detail">{logo}<h3>{organization}</h3><p class="timeline-role">{esc(entry["title"])}</p><p>{esc(entry.get("description", ""))}</p>{impact}</div></li>')
    return '<ol class="timeline">' + "".join(rows) + "</ol>"


def works(profile, publications=True):
    rows = []
    expand_icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/></svg>'
    for index, item in enumerate(profile["work"]):
        image = f'<img src="{url(item["image"])}" alt="{esc(item["image_alt"])}" loading="lazy" width="800" height="480">' if item.get("image") else ""
        if item.get("video"):
            poster = f' poster="{url(item["image"])}"' if item.get("image") else ""
            media = f'<video controls playsinline preload="none"{poster} aria-label="{esc(item["title"])}"><source src="{url(item["video"])}" type="video/mp4">{image}</video>'
        elif image:
            media = f'<a href="{url(item["image"])}" class="work-image" aria-label="Enlarge: {esc(item["title"])}">{image}<span class="image-expand" aria-hidden="true">{expand_icon}</span></a>'
        else:
            media = ""
        preview = item.get("preview")
        if preview:
            preview_id, method_id = f"work-preview-{index}", f"work-method-{index}"
            video = f'<div class="work-video-shell"><video src="{url(preview["video"])}" poster="{url(preview["poster"])}" controls loop muted playsinline preload="none" data-work-video aria-label="{esc(item["title"])}: generated video excerpt"></video></div>'
            media = f'<div class="media-panel" id="{preview_id}" data-media-panel="preview">{video}</div><div class="media-panel" id="{method_id}" data-media-panel="method">{media}</div><div class="media-toolbar"><div class="media-switch" role="group" aria-label="Choose Project Media" hidden><button type="button" data-media-choice="preview" aria-controls="{preview_id}" aria-pressed="true">Video Preview</button><button type="button" data-media-choice="method" aria-controls="{method_id}" aria-pressed="false">Method</button></div><span class="media-note">12s · Silent Excerpt</span></div>'
        row_class = "work-row" if media else "work-row work-row-text"
        if publications:
            row_class += " publication-row"
        media = f'<div class="work-media"{(" data-work-media" if preview else "")}>{media}</div>' if media else ""
        actions = "".join(link(action["label"] + " ↗", action["url"]) for action in item["links"])
        actions = f'<div class="work-links">{actions}</div>' if actions else ""
        title = item.get("paper_title") or item["title"]
        paper_url = next((action["url"] for action in item["links"] if action["label"].strip().casefold() == "paper"), None)
        heading = link(title, paper_url, "work-title-link") if paper_url else esc(title)
        authors = f'<span class="work-authors">{esc(item["authors"])}</span>' if item.get("authors") else ""
        venue = item.get("venue") or item["kind"].removeprefix("Research · ")
        if item.get("year"):
            venue = f'{venue} {item["year"]}' if publications else f'{item["year"]} · {venue}'
        if item.get("status"):
            venue += f' ({item["status"]})'
        metadata = f'<div class="work-meta">{authors}<span class="work-venue">{esc(venue)}</span></div>'
        summary = f'<p class="work-summary">{esc(item["summary"])}</p>'
        description = actions + summary if publications else summary + actions
        rows.append(f'<article class="{row_class}">{media}<div class="work-copy"><h3>{heading}</h3>{metadata}{description}</div></article>')
    return "".join(rows)


EXPERIMENT = """
<section class="experiment-section" aria-labelledby="experiment-title">
  <div class="experiment-intro">{intro}</div>
  <div class="temperature-demo" data-temperature-demo>
    <div class="demo-heading"><span>Next-Token Probabilities</span><span class="demo-live">Interactive</span></div>
    <div class="probability-bars" role="img" aria-label="Illustrative next-token probabilities at temperature 1.0: the 56.4%, a 25.3%, one 11.4%, this 6.9%.">
      <div class="probability-row"><span class="token-label">the</span><div class="bar-track"><div class="bar-fill" style="width:56.4%"></div></div><span class="probability-value">56.4%</span></div>
      <div class="probability-row"><span class="token-label">a</span><div class="bar-track"><div class="bar-fill" style="width:25.3%"></div></div><span class="probability-value">25.3%</span></div>
      <div class="probability-row"><span class="token-label">one</span><div class="bar-track"><div class="bar-fill" style="width:11.4%"></div></div><span class="probability-value">11.4%</span></div>
      <div class="probability-row"><span class="token-label">this</span><div class="bar-track"><div class="bar-fill" style="width:6.9%"></div></div><span class="probability-value">6.9%</span></div>
    </div>
    <div class="temperature-control"><label for="temperature">Temperature <output for="temperature" id="temperature-value">1.0</output></label><input id="temperature" type="range" min="0.2" max="2" step="0.1" value="1" aria-describedby="temperature-help" disabled><div class="slider-labels"><span>More Focused</span><span>More Varied</span></div></div>
    <p class="demo-note" id="temperature-help">Fixed example logits: [2.0, 1.2, 0.4, −0.1]. Change T to compare the same four candidates.</p>
    <noscript><p class="demo-note">Enable JavaScript to adjust the temperature.</p></noscript>
  </div>
</section>
"""


def experiment(home=False):
    if home:
        intro = '<h3 id="experiment-title">From the Equations<br>to the Code.</h3><p>I learn by building. Small, hands-on experiments in foundation models and post-training.</p><p>Try the temperature slider to see how a model’s next-token probabilities change.</p><div class="experiment-links">' + link('Tokenizer Notebook ↗', 'https://colab.research.google.com/github/yanxulab/yanxulab.github.io/blob/main/notebooks/01_tokenizer_embeddings.ipynb') + '</div>'
    else:
        intro = '<p class="eyebrow">Interactive Explanation</p><h2 id="experiment-title">How Temperature Changes Sampling</h2><p>Adjust the temperature to see how fixed model scores become next-token probabilities.</p><p class="experiment-formula"><code>p = softmax(logits / T)</code></p>'
    return EXPERIMENT.format(intro=intro)


def project_demos(profile):
    entries = []
    for item in profile.get("project_demos", []):
        project_url = next((action["url"] for action in item.get("links", []) if action["label"] == "Project"), None)
        title = link(item["title"], project_url) if project_url else esc(item["title"])
        actions = "".join(link(action["label"] + " ↗", action["url"]) for action in item.get("links", []))
        if item.get("video"):
            poster = f' poster="{url(item["poster"])}"' if item.get("poster") else ""
            media = f'<video class="project-demo-media" src="{url(item["video"])}"{poster} controls loop muted playsinline preload="none" data-work-video aria-label="{esc(item["title"])}: silent project demo"></video>'
        else:
            media = f'<img class="project-demo-media" src="{url(item["image"])}" alt="{esc(item["image_alt"])}" loading="lazy">'
        note = f'<span class="media-note">{esc(item["media_note"])}</span>' if item.get("media_note") else ""
        entries.append(f'<article class="project-demo"{(" data-work-media" if item.get("video") else "")}><div class="project-demo-heading"><h3>{title}</h3><div class="work-links">{actions}</div></div>{media}<div class="project-demo-caption"><p>{esc(item["summary"])}</p>{note}</div></article>')
    if not entries:
        return ""
    return '<section class="project-demos" id="project-demo" aria-labelledby="demo-title"><div class="section-heading"><h2 id="demo-title">Project Demo</h2></div>' + "".join(entries) + '</section>'


def home(profile):
    portrait = f'<img class="portrait" src="{url(profile["portrait"])}" alt="{esc(profile["portrait_alt"])}" width="220" height="220">' if profile.get("portrait") else '<div class="hero-note" aria-hidden="true"><span class="note-index">A working notebook</span><div class="tensor-motif"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><span>Build.<br>Measure.<br>Understand.</span></div>'
    timeline_title = "Experience" if profile.get("career") else "Current Focus"
    scholar_link = f'<span class="section-aside">{link("All Publications ↗", profile["scholar"])}</span>' if profile.get("scholar") else ""
    blog_link = f'<span class="section-aside">{link("Visit the Blog ↗", "essays.qmd")}</span>' if profile.get("blog_published") else ""
    blog_preview = experiment(home=True) if profile.get("blog_published") else '<p class="section-status">Under Development</p>'
    return f"""
<div class="home-shell">
<section class="intro" aria-labelledby="intro-name"><h1 id="intro-name">{esc(profile['name'])}</h1><div class="bio">{bio(profile)}</div><div class="intro-profile">{portrait}{socials(profile)}</div></section>
<section class="career-section" aria-labelledby="career-title"><div class="section-heading"><h2 id="career-title">{timeline_title}</h2><span class="section-aside">{link('CV ↗', 'cv.qmd')}</span></div>{career(profile)}</section>
{project_demos(profile)}
<section class="selected-work" id="selected-work" aria-labelledby="work-title"><div class="section-heading"><h2 id="work-title">Selected Work</h2>{scholar_link}</div>{works(profile)}</section>
<section class="tech-blog-section" id="tech-blog" aria-labelledby="blog-title"><div class="section-heading"><h2 id="blog-title">Tech Blog</h2>{blog_link}</div>{blog_preview}</section>
</div>
"""


def blog(profile):
    if not profile.get("blog_published"):
        return '<div class="reading-shell"><div class="reading-header"><h1 id="blog-page-title">Blog</h1><p class="section-status">Under Development</p></div></div>'
    contents, entries = [], []
    for index, item in enumerate(profile["writing"], 1):
        number = f"{index:02}"
        contents.append(f'<li><a href="#{esc(item["id"])}"><span>{number}</span>{esc(item["title"])}</a></li>')
        title = link(item["title"], item["url"]) if item["published"] else esc(item["title"])
        action = link("Read Essay →", item["url"], "essay-read") if item["published"] else '<p class="preparation-note">This essay is in preparation.</p>'
        topics = "".join(f'<li>{esc(topic)}</li>' for topic in item["topics"])
        entries.append(f'<section class="essay-entry" id="{esc(item["id"])}"><div class="essay-index">{number}</div><div class="essay-copy"><div class="essay-status">{esc(item["status"])}</div><h2>{title}</h2><p class="essay-subtitle">{esc(item["subtitle"])}</p><p>{esc(item["description"])}</p><ul class="essay-topics">{topics}</ul>{action}</div></section>')
    return f"""
<div class="reading-shell"><header class="reading-header"><p class="eyebrow">The Blog</p><h1>Notes on<br>Learning Machines.</h1><p class="reading-deck">Foundation models, post-training, and the systems behind them. From first principles to working code.</p><p class="reading-byline">By {esc(profile['name'])}</p></header>
<nav class="contents-panel" aria-label="Blog contents"><p class="eyebrow">Contents</p><ol>{''.join(contents)}</ol><a class="contents-extra" href="#workbench">From the Workbench ↓</a></nav>
<p class="blog-intro">I’m putting together three connected essays. Each will pair the core ideas with derivations, code, and controlled experiments.</p>
{''.join(entries)}
<section class="workbench" id="workbench"><p class="eyebrow">From the Workbench</p><h2>Start With Something Small.</h2><p>Notebooks and visual explanations, alongside the longer essays.</p>{works({'work': profile.get('experiments', [])}, publications=False)}</section>
{experiment()}
</div>
"""


def cv(profile):
    pdf = f'<p>{link("Download CV (PDF) ↓", profile["cv_pdf"], "text-cta")}</p>' if profile.get("cv_pdf") else '<p class="cv-status">A full CV will be added here.</p>'
    title = "Experience & Education" if profile.get("career") else "Current Focus"
    return f'<div class="reading-shell"><header class="reading-header"><p class="eyebrow">Curriculum Vitae</p><h1>{esc(profile["name"])}</h1>{pdf}</header><section class="cv-summary"><h2>Research Interests</h2>{bio(profile)}{socials(profile)}</section><section class="cv-experience"><h2>{title}</h2>{career(profile)}</section><section class="cv-work"><h2>Selected Work</h2>{works(profile)}</section></div>'


def main():
    profile = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    pages = {"home.html": home(profile), "blog.html": blog(profile), "cv.html": cv(profile), "bio.html": bio(profile), "work.html": works(profile)}
    for filename, content in pages.items():
        (OUT / filename).write_text("```{=html}\n<!-- Generated from profile.json by scripts/render_profile.py. -->\n" + content.strip() + "\n```\n", encoding="utf-8")
    print("Profile rendered: home, blog, CV, bio, selected work.")


if __name__ == "__main__":
    main()
