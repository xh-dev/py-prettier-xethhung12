import json
import sys
import xml.dom.minidom


def format_json(text: str) -> str:
    parsed = json.loads(text)
    return json.dumps(parsed, indent=2, ensure_ascii=False)


def format_xml(text: str) -> str:
    dom = xml.dom.minidom.parseString(text.encode("utf-8"))
    pretty = dom.toprettyxml(indent="  ")
    # Remove the redundant <?xml ...?> declaration line added by toprettyxml
    # if the original input did not have one, keep it clean
    lines = pretty.splitlines()
    if lines and lines[0].startswith("<?xml"):
        lines = lines[1:]
    return "\n".join(line for line in lines if line.strip())


def format_html(text: str) -> str:
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(text, "html.parser")
        return soup.prettify()
    except ImportError:
        print(
            "Warning: 'beautifulsoup4' is not installed. "
            "Falling back to raw output. Install it with: pip install beautifulsoup4",
            file=sys.stderr,
        )
        return text


FORMATTERS = {
    "json": format_json,
    "xml": format_xml,
    "html": format_html,
}


def format_text(text: str, parser: str) -> str:
    parser = parser.lower()
    if parser not in FORMATTERS:
        raise ValueError(f"Unsupported parser '{parser}'. Choose from: {', '.join(FORMATTERS)}")
    return FORMATTERS[parser](text)

