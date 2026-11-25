# Instagram pipeline: content → images → Metricool

```
posts.json ──► template.html ──► your script (render + upload) ──► manifest.json ──► Claude schedules in Metricool
(Claude writes)   (brand template)                                  (public image URLs)     (you approve)
```

## Files
- **posts.json**: the 14-day plan. Each post has `id`, `date`, `time`, `timezone`, `format` (`carousel` · `single` · `reel`), `caption`, and `slides` (or `reel` = a filming script). Posts with `manual` need something from you (filming, screenshots).
- **template.html**: renders any slide in the brand (teal + saffron, Bricolage / Inter / Tajawal). Slide types: `cover · phrase · mistake · list · steps · rule · compare · quiz · answers · cta · screenshot`.
- **render_example.py**: a minimal Playwright renderer to start from.

## Preview
```bash
python3 -m http.server 8000      # in this folder
# open http://localhost:8000/template.html?post=2026-11-26-mistakes
```

## What your script should do
1. **Serve** this folder over http (fonts and `fetch('posts.json')` need http, not file://).
2. **Render** each slide: open `template.html?post=<id>&slide=<n>` (1-based), wait for `window.__ready === true`, screenshot the `.slide` element at **1080×1350** → `<id>_<nn>.png`. Skip `format: "reel"`.
3. **Upload** the PNGs to public storage that serves direct image URLs (Cloudinary, Supabase Storage, S3, or Google Drive linked in Metricool).
4. **Write manifest.json**:
```json
[
  { "id": "2026-11-26-mistakes", "slides": ["https://…/2026-11-26-mistakes_01.png", "…_02.png"] }
]
```
5. Give Claude the manifest (paste it or a public link). Claude creates each post in Metricool with the images in order, the caption from posts.json, the date and time, as a **draft** for you to approve, unless you say "auto-publish".

## Tips
- Re-render only changed posts: pass post ids as arguments.
- Keep file names stable (`<id>_<nn>.png`) so re-uploads overwrite cleanly.
- New content = Claude adds entries to posts.json; your script stays the same.
- Reels: film from the `reel.shots` script, then upload the video; Claude schedules it the same way (`format: reel`).
