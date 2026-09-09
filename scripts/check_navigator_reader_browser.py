#!/usr/bin/env python3
"""Offline Chromium fixtures for the Navigator reading surface and editor.

Uses the real HTML/CSS/compiled ES modules and exact local repository/public-build
bytes. No HTTP navigation, analytics, canonical write, or repository mutation is
performed. Web Storage, clipboard, and fetch use explicit fixture doubles.
"""
from __future__ import annotations

import argparse
import base64
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
TARGET_ID = "inorganic_alternating_lamp_and_holiday_reading"
META_MARKERS = [
    "Status: Literary essay",
    "Layer: 07_Creative_Offshoots / Literary_Essays",
    "Claim strength: S1-S2/E1/U0/P1/V0",
    "Authority: Creative offshoot; not a concept-definition owner",
    "Public handling:",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", help="Chromium executable; default: system Chromium or Playwright Chromium")
    parser.add_argument("--screenshots", type=Path, help="Optional screenshot directory outside the repository")
    args = parser.parse_args()

    from playwright.sync_api import sync_playwright

    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)

    catalog = json.loads((ROOT / "tools/docs_public_catalog.json").read_text(encoding="utf-8"))
    docs = catalog["documents"]
    source = next((doc for doc in docs if doc.get("id") == TARGET_ID), None)
    if source is None:
        raise SystemExit(f"target fixture document missing: {TARGET_ID}")

    checks = 0
    page_errors: list[str] = []

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(message)

    with sync_playwright() as pw:
        executable = args.browser or shutil.which("chromium") or pw.chromium.executable_path
        browser = pw.chromium.launch(executable_path=executable, headless=True, args=["--no-sandbox"])

        def launch(lang: str, width: int = 1440, developer: bool = False):
            fixture_root = ROOT if developer else ROOT / "_build/pages"
            if not (fixture_root / "navigator/dist/reader-core.js").is_file():
                raise RuntimeError("Build/compile the Navigator and public site before running browser fixtures.")
            shell = fixture_root / "navigator" / ("dev.html" if developer else "index.html")
            html = shell.read_text(encoding="utf-8")
            html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S)
            html = re.sub(r"<link\b[^>]*rel=\"stylesheet\"[^>]*>", "", html)
            css = (fixture_root / "navigator/styles.css").read_text(encoding="utf-8")
            html = html.replace("</head>", f"<style>{css}</style></head>")

            page = browser.new_page(
                viewport={"width": width, "height": 1000 if width > 720 else 844},
                device_scale_factor=1,
            )
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.set_default_timeout(10000)
            page.set_content(html)

            def fetch_bytes(url: str):
                if "api/assessment/runner" in url:
                    data = json.dumps({"repository_assessment_runner": {"available": False, "mode": "export-import"}}).encode()
                    return {"body": base64.b64encode(data).decode("ascii"), "status": 200}
                raw = unquote(urlsplit(url).path)
                rel = posixpath.normpath(posixpath.join("navigator", raw))
                target = (fixture_root / rel).resolve()
                if not target.is_relative_to(fixture_root.resolve()) or not target.is_file():
                    return {"body": "", "status": 404}
                return {"body": base64.b64encode(target.read_bytes()).decode("ascii"), "status": 200}

            page.expose_function("__fixtureFetch", fetch_bytes)
            page.evaluate(
                """({lang}) => {
                    location.hash = new URLSearchParams({lang}).toString();
                    const store = new Map();
                    window.__fixtureStore = store;
                    Object.defineProperty(window, 'localStorage', {configurable:true, value: {
                        getItem(key) { return store.get(key) ?? null; },
                        setItem(key,value) { store.set(key,String(value)); },
                        removeItem(key) { store.delete(key); }
                    }});
                    Object.defineProperty(navigator, 'clipboard', {configurable:true, value: {
                        async writeText(value) { window.__copied = value; }
                    }});
                    window.__requests = [];
                    window.fetch = async (input) => {
                        const url = String(input); window.__requests.push(url);
                        const result = await window.__fixtureFetch(url);
                        const bytes = Uint8Array.from(atob(result.body), ch => ch.charCodeAt(0));
                        return new Response(bytes, {status:result.status, headers:{'Content-Type':'text/plain; charset=utf-8'}});
                    };
                }""",
                {"lang": lang},
            )
            modules = {
                name: (fixture_root / "navigator/dist" / f"{name}.js").read_text(encoding="utf-8")
                for name in ["search-core", "graph-core", "language-core", "reader-core", "app"]
            }
            page.evaluate(
                r"""async (modules) => {
                    const urls = {};
                    for (const [name, source] of Object.entries(modules)) {
                        const code = source.replace(/from\s+["']\.\/([\w-]+)\.js["']/g,
                            (_, dependency) => `from "${urls[dependency]}"`);
                        urls[name] = URL.createObjectURL(new Blob([code], {type:'text/javascript'}));
                    }
                    await import(urls.app);
                }""",
                modules,
            )
            page.wait_for_selector("main.page")
            return page

        def route(page, **values):
            page.evaluate("(values) => { location.hash = new URLSearchParams(values).toString(); }", values)

        def no_overflow(page, label: str):
            width, total = page.evaluate("[innerWidth, document.documentElement.scrollWidth]")
            check(total <= width + 1, f"{label}: horizontal overflow {total}/{width}")

        def shot(page, name: str):
            if args.screenshots:
                page.screenshot(path=str(args.screenshots / f"{name}.png"), full_page=False)

        # Public: no arbitrary recommendation is displayed before an editor selects one.
        for width in [1440, 390, 320]:
            for lang in ["ja", "en"]:
                page = launch(lang, width=width)
                check(page.locator("html").get_attribute("lang") == lang, f"home {lang}: wrong UI language")
                check(page.locator(".reading-channel-card").count() == 0, "unselected reading channel should not fabricate cards")
                check(page.locator(".path").count() == 0, "public home exposes a repository path")
                no_overflow(page, f"home {lang} {width}")
                shot(page, f"home-{lang}-{width}")

                route(page, lang=lang, read=source["path"])
                page.wait_for_selector(".reader-article")
                expected_title = source["title"][lang]
                check(page.locator(".reader-public-title").inner_text() == expected_title, f"reader {lang}: title not localized")
                check(page.locator(".reader-article").get_attribute("lang") == "ja", f"reader {lang}: single-language source mislabeled")
                if lang == "en":
                    check(page.locator(".reader-language-fallback").count() == 1, "English UI did not disclose Japanese-body fallback")
                else:
                    check(page.locator(".reader-language-fallback").count() == 0, "Japanese body incorrectly marked as fallback")

                shell_text = page.locator(".reader-shell").inner_text()
                article_text = page.locator(".reader-article").inner_text()
                for marker in META_MARKERS:
                    check(marker not in shell_text, f"public Reader leaked metadata marker: {marker}")
                    check(marker not in article_text, f"public article leaked metadata marker: {marker}")
                check(source["path"] not in shell_text, "public Reader exposed source path in initial reading surface")
                check(".ja.md" not in page.locator(".reader-header").inner_text(), "public Reader title area exposed filename")
                check(page.locator(".reader-article > h1").count() == 0, "duplicate source H1 was not removed")
                check(page.locator(".reader-toc-links a").count() >= 3, "Reader has no usable contents list")
                no_overflow(page, f"reader {lang} {width}")
                shot(page, f"reader-{lang}-{width}")

                page.locator(".reader-preferences > summary").click()
                page.locator(".reader-size-select").select_option("larger")
                page.locator(".reader-theme-select").select_option("paper")
                check(page.locator(".reader-shell").get_attribute("data-text-size") == "larger", "text size not applied")
                check(page.locator(".reader-shell").get_attribute("data-reading-theme") == "paper", "paper theme not applied")
                check(page.evaluate("window.__fixtureStore.get('scientific-ontology-reader-size:v1')") == "larger", "text size not saved")
                check(page.evaluate("window.__fixtureStore.get('scientific-ontology-reader-theme:v1')") == "paper", "theme not saved")

                # Select a phrase in prose and verify the low-friction Navigator search handoff.
                paragraph = page.locator(".reader-article p").first
                paragraph.wait_for()
                selected = page.evaluate(
                    """(el) => {
                        const node = el.firstChild;
                        const text = (el.textContent || '').trim();
                        if (!node || !text) return '';
                        const length = Math.min(12, text.length);
                        const range = document.createRange();
                        range.setStart(node, 0); range.setEnd(node, length);
                        const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(range);
                        el.dispatchEvent(new MouseEvent('mouseup', {bubbles:true}));
                        return sel.toString().trim();
                    }""",
                    paragraph.element_handle(),
                )
                page.wait_for_timeout(30)
                check(len(selected) >= 2, "fixture could not select Reader prose")
                check(not page.locator(".reader-selection-tools").is_hidden(), "selection reading aid did not appear")
                page.locator(".reader-selection-tools .button.primary").click()
                page.wait_for_selector(".search-page")
                check(selected in page.locator(".search-page .search-input").input_value(), "selected text was not carried into Navigator search")

                no_overflow(page, f"reader/search {lang} {width}")
                shot(page, f"search-from-selection-{lang}-{width}")
                page.close()

        # Developer: every public-catalog document, including README, is selectable.
        dev = launch("ja", developer=True)
        route(dev, lang="ja", view="reading-editor")
        dev.wait_for_selector(".editorial-page")
        options = dev.locator(".editorial-channel-card").first.locator(".editorial-doc-select option")
        check(options.count() == len(docs), f"Developer reading editor does not expose all public docs: {options.count()}/{len(docs)}")
        option_values = options.evaluate_all("els => els.map(el => el.value)")
        check(TARGET_ID in option_values, "07 fixture document not selectable in Developer reading editor")
        readme_ids = {doc["id"] for doc in docs if str(doc.get("path", "")).endswith("README.md")}
        check(readme_ids.issubset(set(option_values)), "README documents are not all selectable in Developer reading editor")

        first_channel = dev.locator(".editorial-channel-card").first
        first_channel.locator(".editorial-doc-select").select_option(TARGET_ID)
        first_channel.locator(".editorial-chooser .button.primary").click()
        check(first_channel.locator(".editorial-selected-row").count() == 1, "Developer editor did not add selected document")
        check("休日の窓辺" in first_channel.locator(".editorial-selected-row").inner_text(), "Developer selected row lost readable title")
        check(dev.locator(".editorial-public-preview .reading-channel-card").count() == 1, "Developer public preview did not reflect the local selection")
        check("休日の窓辺" in dev.locator(".editorial-public-preview .reading-channel-title").inner_text(), "Developer preview lost the public display title")
        check(dev.locator(".path").count() > 0, "Developer editor unexpectedly masks repository paths")
        check(dev.locator("a[href*='view=candidates'], button").count() >= 0, "Developer shell failed after editorial selection")
        no_overflow(dev, "developer editorial")
        shot(dev, "developer-editorial")
        dev.close()

        browser.close()

    if page_errors:
        raise SystemExit("Navigator Reader Browser Check: FAIL\n" + "\n".join(page_errors))
    print(f"Navigator Reader Browser Check: PASS ({checks} checks)")
    print("Boundary note: offline fixture validates DOM/layout/behavior, not HTTP deployment or real browser persistence.")


if __name__ == "__main__":
    main()
