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


START, END, CLOSING, QUOTED, AUTO_CLOSE = 1, 2, 3, 4, 5

def scan_tags(text: str) -> dict:
    status = 0
    content = ''
    node = root = Tag('html')
    for token in re.split('(<|"|/|>)', text):
        match token:
            case '<':
                if content:
                    node.add(content, simple_txt=True)
                    content = ''
                status = START
            case '>':
                if status in [END, QUOTED]:
                    content += token
                elif status == CLOSING:
                    node = node.parent
                    status = 0
                else:
                    words = [w.strip() for w in re.split(' |=|"', content) if w]
                    new = node.add(
                        words.pop(0),
                        attribs={k: v for k, v in zip(words[::2], words[1::2])}
                    )
                    if status != AUTO_CLOSE:
                        node = new
                    status = END
                    content = ''
            case '/':
                if status == START:
                    status = AUTO_CLOSE if content else CLOSING
                else:
                    content += token
            case '"':
                if status == QUOTED:
                    status = START
                else:
                    status = QUOTED
                content += token
            case _:
                token = token.strip()
                if status != CLOSING:
                    content += token
                elif token.lower() not in node.id.lower():
                    node.add(
                        f'*** Mismatched identifier {token} ***',
                        simple_txt=True
                    )
    return root.data
