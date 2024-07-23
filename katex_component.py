import mesop.labs as mel

@mel.web_component(path="./katex_component.js")
def katex_component(content: str):
    return mel.insert_web_component(
        name="katex-element",
        properties={"content": content}
    )