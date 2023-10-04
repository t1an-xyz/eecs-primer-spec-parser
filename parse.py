import requests
import os
from bs4 import BeautifulSoup
import urllib

URL = "https://eecs280staff.github.io/tutorials/setup_vscode_macos.html"
o = urllib.parse.urlparse(URL)
base_url = o.scheme + "://" + o.netloc + "/" + "".join(o.path.split("/")[:-1]) + "/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
# print(soup)
main_content = soup.find(id="primer-spec-preact-main-content")


def recursiveSearch(element):
    if not element or element == "\n":
        return ""
    if str(type(element)) != "<class 'bs4.element.Tag'>" or not element.children:
        return element.get_text()
    headingsDict = {
        "h1": "# ",
        "h2": "## ",
        "h3": "### ",
        "h4": "#### ",
        "h5": "##### ",
        "h6": "###### ",
    }
    if element.name == "p":
        return "".join(recursiveSearch(child) for child in element.children) + "\n\n"
    elif element.name in headingsDict:
        out = (
            headingsDict[element.name]
            + "".join(recursiveSearch(child) for child in element.children)
            + "\n"
        )
        if element.name == "h1":
            out += "====================\n"
        elif element.name == "h2":
            out += "--------------------\n"
        return out
    elif element.name == "a":
        return "[" + element.get_text() + "](" + element["href"] + ")"
    elif element.name == "img":
        start_path = os.path.join(os.getcwd(), "docs")
        final_path = os.path.join(start_path, element["src"])
        if not os.path.exists(os.path.dirname(final_path)):
            os.makedirs(os.path.dirname(final_path))
        r = requests.get(base_url + element["src"], allow_redirects=True)
        open(final_path, "wb").write(r.content)
        if "alt" in element.attrs:
            return "![" + element["alt"] + "](" + element["src"] + ")"
        return "![](" + element["src"] + ")"
    elif element.name == "code":
        return "`" + element.get_text() + "`"
    elif element.name == "pre":
        return "\n```\n" + element.get_text() + "```\n"
    elif element.name == "div":
        if "class" not in element.attrs:
            return "".join(recursiveSearch(child) for child in element.children)
        if "primer-spec-code-block" in element["class"]:
            out = "\n```c++\n"
            table = out.find("table")
            for row in table.findAll("tr"):
                out += list(row.children)[1].get_text() + "\n"
            out += "```\n"
            return out
        elif "primer-spec-callout" in element["class"]:
            return (
                "> "
                + "".join(recursiveSearch(child) for child in element.children)
                + "\n"
            )
        else:
            return "".join(recursiveSearch(child) for child in element.children)
    elif element.name == "strong":
        return (
            "**" + "".join(recursiveSearch(child) for child in element.children) + "**"
        )
    elif element.name == "em":
        return "*" + "".join(recursiveSearch(child) for child in element.children) + "*"
    elif element.name == "table":
        for row in element.findAll("tr"):
            for cell in row.findAll("td"):
                for img in cell.findAll("img"):
                    img = recursiveSearch(img)
        return str(element)
    elif element.name == "body":
        return "".join(recursiveSearch(child) for child in element.children)
    else:
        return "".join(recursiveSearch(child) for child in element.children)


if not os.path.exists(os.path.join(os.getcwd(), "docs")):
    os.makedirs(os.path.join(os.getcwd(), "docs"))

with open("docs/README.md", "w") as f:
    f.write(recursiveSearch(soup.body))

# with open("docs/output.html", "w") as f:
#    f.write(str(soup.body))
