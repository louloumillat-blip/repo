# Minimal renderer: python3 render_example.py [post_id ...]
# pip install playwright && playwright install chromium
import json, sys, pathlib, threading, http.server, functools
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"; OUT.mkdir(exist_ok=True)
only = set(sys.argv[1:])

srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
posts = json.loads((ROOT / "posts.json").read_text())["posts"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1350})
    for post in posts:
        if "slides" not in post or (only and post["id"] not in only):
            continue
        for i in range(len(post["slides"])):
            page.goto(f"http://127.0.0.1:8765/template.html?post={post['id']}&slide={i+1}")
            page.wait_for_function("window.__ready === true")
            page.locator(".slide").screenshot(path=str(OUT / f"{post['id']}_{i+1:02d}.png"))
            print("rendered", post["id"], i + 1)
    browser.close()
srv.shutdown()
# Next: upload OUT/*.png and write manifest.json (see README).
