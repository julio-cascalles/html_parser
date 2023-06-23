import json
from html_parser import scan_tags


print(json.dumps(  # --- Atenção: Rodar usando python 3.10+
    scan_tags('''
        <head>
            <title>Titulo</title>
        </head>
        <body>
            <p>Primeiro paragrafo >>>> </p>
            <div>Uma div qualquer (z = x / y)</div>
            <div id="principal" class="vermelha">
                <div>Uma div dentro da outra...</div>
                ...Texto solto...
                <p>Paragrafo dentro da div</p>
            </div>
            <div>
                --- ultima DIV ---
            </DIV >
            <p>Segundo P</p>
        </body>
        <img src="myalbum/photo20210826.png" />
        <input type="password">Digite a senha</UNKNOW>
    '''),
    indent=4)
)
