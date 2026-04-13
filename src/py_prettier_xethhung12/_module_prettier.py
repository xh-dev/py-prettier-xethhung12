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


def xml_to_json(text: str, attr_prefix: str = "@", skip_root: bool = False) -> str:
    import xmltodict
    parsed = xmltodict.parse(text, attr_prefix=attr_prefix)
    if skip_root and isinstance(parsed, dict) and len(parsed) == 1:
        parsed = next(iter(parsed.values()))
    return json.dumps(parsed, indent=2, ensure_ascii=False)


def _auto_mode_transform(obj: object, attr_prefix: str) -> object:
    """Recursively convert a parsed-JSON structure so that primitive values
    become XML attributes (prefixed) and object/array values stay as subnodes."""
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if isinstance(v, (str, int, float, bool)) or v is None:
                result[attr_prefix + k] = v
            else:
                result[k] = _auto_mode_transform(v, attr_prefix)
        return result
    if isinstance(obj, list):
        return [_auto_mode_transform(item, attr_prefix) for item in obj]
    return obj


def json_to_xml(text: str, root: str = "root", attr_prefix: str = "@", mode: str = "default") -> str:
    import xmltodict
    parsed = json.loads(text)
    if mode == "auto":
        parsed = _auto_mode_transform(parsed, attr_prefix)
    # Wrap in root element if the JSON has multiple top-level keys
    if not isinstance(parsed, dict) or len(parsed) != 1:
        parsed = {root: parsed}
    raw = xmltodict.unparse(parsed, attr_prefix=attr_prefix, pretty=False)
    dom = xml.dom.minidom.parseString(raw.encode("utf-8"))
    pretty = dom.toprettyxml(indent="  ")
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

