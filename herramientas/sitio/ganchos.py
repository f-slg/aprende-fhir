"""Ajustes para que el Markdown escrito para GitHub se vea igual en el sitio."""
import re


def on_page_markdown(markdown, **kwargs):
    # GitHub interpreta Markdown dentro de <details>; MkDocs necesita que se lo pidan.
    markdown = re.sub(r"<details>", '<details markdown="1">', markdown)
    markdown = re.sub(r"<summary>(.*?)</summary>", r"<summary>\1</summary>\n", markdown)
    return markdown
