# Portrait versions

- Original: `assets/portrait-original.jpg`, renamed from `assets/portrait.jpg` without modifying its bytes.
- Original SHA-256: `8078eb1933f954d9100325f24e7ab75517180c01bdb2716b5dd6b610129f3b17`.
- Website version: `assets/portrait-headshot.jpg`.
- Method: built-in imagegen editing, then JPEG encoding at quality 85 for the website. The edited version is separate from the source photograph.
- Homepage framing: `styles.css` crops the website version more tightly inside `.portrait-frame`, reducing visible shoulders. This display adjustment does not alter either image file.

## Imagegen prompt

Use case: identity-preserve. Edit target: the provided original outdoor portrait of Yan Xu. Asset type: a personal research website avatar. Primary request: ONLY zoom in and crop the existing photograph into a square head-and-shoulders portrait. Use the exact existing person and image content. Preserve his exact facial features, glasses, hair, smile, skin texture, clothing, pose, sunlight, and background. Do not beautify, retouch, relight, invent details, change expression, replace clothing, or replace background. Composition: center on his head and shoulders with modest headroom, top of the hair fully visible, crop around the upper chest. The face should be substantially larger than in the original. Keep enough room at the sides so a circular website mask will include the entire head and shoulders. Output a normal opaque square photograph, no circular frame, no borders, no text. This is a faithful reframing of the existing photograph, not a newly imagined headshot.
