from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import markdown  # type: ignore


def _find_browser_exe() -> Path | None:
    # Prefer Edge (common on Windows), then Chrome.
    candidates: list[str] = []

    # PATH
    for name in ["msedge", "msedge.exe", "chrome", "chrome.exe"]:
        p = shutil.which(name)
        if p:
            candidates.append(p)

    # Common install locations
    program_files = os.environ.get("ProgramFiles", r"C:\\Program Files")
    program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\\Program Files (x86)")

    candidates += [
        str(Path(program_files) / "Microsoft" / "Edge" / "Application" / "msedge.exe"),
        str(Path(program_files_x86) / "Microsoft" / "Edge" / "Application" / "msedge.exe"),
        str(Path(program_files) / "Google" / "Chrome" / "Application" / "chrome.exe"),
        str(Path(program_files_x86) / "Google" / "Chrome" / "Application" / "chrome.exe"),
    ]

    for c in candidates:
        p = Path(c)
        if p.exists():
            return p

    return None


def _md_to_html(md_text: str, title: str) -> str:
    body = markdown.markdown(
        md_text,
        extensions=[
            "extra",  # tables, fenced code, etc.
            "sane_lists",
        ],
        output_format="html5",
    )

    # Simple, print-friendly styling for A4.
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <style>
    @page {{ size: A4; margin: 14mm; }}
    html, body {{ color: #111; background: #fff; }}
    body {{ font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif; font-size: 12px; line-height: 1.55; }}
    h1 {{ font-size: 20px; margin: 0 0 10px; }}
    h2 {{ font-size: 14px; margin: 14px 0 8px; border-bottom: 1px solid #ddd; padding-bottom: 4px; }}
    h3 {{ font-size: 12.5px; margin: 10px 0 6px; }}
    p {{ margin: 6px 0; }}
    ul {{ margin: 6px 0 6px 18px; padding: 0; }}
    ul ul {{ margin-left: 22px; list-style-type: circle; }}
    ul ul ul {{ margin-left: 22px; list-style-type: square; }}
    li {{ margin: 2px 0; }}
    hr {{ border: 0; border-top: 1px solid #ddd; margin: 12px 0; }}
    a {{ color: #0b57d0; text-decoration: none; }}
    img {{ max-width: 150px; height: auto; border-radius: 12px; float: right; margin: 0 0 8px 12px; }}
    code, pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; }}
    pre {{ white-space: pre-wrap; background: #f6f8fa; padding: 8px; border-radius: 6px; }}
    blockquote {{ margin: 8px 0; padding-left: 10px; border-left: 3px solid #ddd; color: #444; }}
    table {{ border-collapse: collapse; width: 100%; margin: 8px 0; }}
    th, td {{ border: 1px solid #ddd; padding: 6px 8px; vertical-align: top; }}
    th {{ background: #f6f8fa; }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def _export_pdf_with_playwright(html_path: Path, out_pdf: Path) -> bool:
    """Generate PDF without any browser-added header/footer timestamps.

    Requires:
      - pip install playwright
      - python -m playwright install chromium
    """

    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        return False

    file_url = html_path.resolve().as_uri()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(file_url, wait_until="networkidle")
            page.pdf(
                path=str(out_pdf.resolve()),
                format="A4",
                print_background=True,
                display_header_footer=False,
                margin={"top": "14mm", "right": "14mm", "bottom": "14mm", "left": "14mm"},
                prefer_css_page_size=True,
            )
            browser.close()
        return True
    except Exception:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Chinese resume Markdown to PDF via headless Edge/Chrome.")
    parser.add_argument(
        "--input",
        default=str(Path("resume") / "resume.zh-CN.md"),
        help="Input Markdown path. Default: resume/resume.zh-CN.md",
    )
    parser.add_argument(
        "--out-pdf",
        default=str(Path("resume") / "resume.zh-CN.pdf"),
        help="Output PDF path. Default: resume/resume.zh-CN.pdf",
    )
    parser.add_argument(
        "--out-html",
        default=str(Path("resume") / "resume.zh-CN.html"),
        help="Intermediate HTML path. Default: resume/resume.zh-CN.html",
    )
    args = parser.parse_args()

    in_path = Path(args.input)
    out_pdf = Path(args.out_pdf)
    out_html = Path(args.out_html)

    if not in_path.exists():
        print(f"Input not found: {in_path}", file=sys.stderr)
        return 2

    md_text = in_path.read_text(encoding="utf-8")
    html = _md_to_html(md_text, title="刘俊圆 - 中文简历")

    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(html, encoding="utf-8")

    # Prefer Playwright for deterministic PDF output (no header/footer timestamps).
    if _export_pdf_with_playwright(out_html, out_pdf):
        print(f"Wrote PDF: {out_pdf}")
        return 0

    browser = _find_browser_exe()
    if browser is None:
        print("Could not find Edge/Chrome. Please install Microsoft Edge or Google Chrome.", file=sys.stderr)
        print(f"HTML has been generated at: {out_html}", file=sys.stderr)
        print(
            "Tip: to export a clean PDF without header/footer timestamps, install Playwright:\n"
            "  python -m pip install playwright\n"
            "  python -m playwright install chromium",
            file=sys.stderr,
        )
        return 3

    # file:// URL for printing
    file_url = out_html.resolve().as_uri()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--disable-features=PrintCompositorLPAC",
        f"--print-to-pdf={str(out_pdf.resolve())}",
        # Chromium flag to disable header/footer (date/url/page numbers)
        "--print-to-pdf-no-header",
        file_url,
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # Retry with a minimal flag set (compat)
        cmd2 = [
            str(browser),
            "--headless",
            "--disable-gpu",
            f"--print-to-pdf={str(out_pdf.resolve())}",
            "--print-to-pdf-no-header",
            file_url,
        ]
        subprocess.run(cmd2, check=True)

    print(f"Wrote PDF: {out_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
