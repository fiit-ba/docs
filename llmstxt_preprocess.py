"""Clean notebook HTML before mkdocs-llmstxt turns pages into Markdown."""

NOISE_SELECTORS = [
    ".jp-InputPrompt",         # "In [ ]:"
    ".jp-OutputPrompt",        # "Out[ ]:"
    ".zeroclipboard-container",  # copy button ("Copied!")
    ".clipboard-copy-txt",     # plain-text duplicate of each code cell
    ".md-export",              # our own Markdown buttons
    ".headerlink",             # "¶" anchor next to headings
    ".anchor-link",            # same anchor in notebook pages
]


def preprocess(soup, output):
    for selector in NOISE_SELECTORS:
        for element in soup.select(selector):
            element.decompose()
