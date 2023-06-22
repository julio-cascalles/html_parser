import re

class Tag:
    def __init__(self, id: str, **args):
        self.id = id
        self.parent = None
        self.children = []
        attribs = args.get('attribs', {})
        if args.get('simple_txt'):
            self.data = self.id
        else:
            self.data = {self.id: self.children} | attribs

    def add(self, id: str, **args):
        child = Tag(id, **args)
        child.parent = self
        self.children.append(child.data)
        return child


def scan_tags(text: str) -> dict:
    start, end, closing = [False] * 3
    content = ''
    root = Tag('html')
    node = root
    for token in re.split('(<|/|>)', text):
        if not start and token in ['>', '/']:
            content += token
            continue
        match token:
            case '<':
                if content:
                    node.add(content, simple_txt=True)
                    content = ''
                start, end = True, False
            case '>':
                if closing:
                    node = node.parent
                    start, end, closing = [False] * 3
                else:
                    tokens = [t.strip() for t in re.split(' |=|"', content) if t]
                    node = node.add(
                        tokens.pop(0),
                        attribs={k: v for k, v in zip(tokens[::2], tokens[1::2])}
                    )
                    start, end = False, True
                content = ''                    
            case '/':
                closing = True
            case _:
                content += token.strip()
    return root.data
