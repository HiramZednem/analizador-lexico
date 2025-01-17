from flask import Flask, request,render_template
import ply.lex as lex

tokens = (
    'IDENTIFICADOR',
    'for',
    'if',
    'do',
    'while',
    'else',
    'ParentesisIzq',
    'ParentesisDer',
)


def t_for(t):
    r'\bfor\b|\bFOR\b'
    t.type = 'for'
    t.description = '<Reservada for>'
    return t

def t_if(t):
    r'\bif\b|\bIF\b'
    t.type = 'if'
    t.description = '<Reservada if>'
    return t

def t_do(t):
    r'\bdo\b|\bDO\b'
    t.type = 'do'
    t.description = '<Reservada do>'
    return t

def t_while(t):
    r'\bwhile\b|\bWHILE\b'
    t.type = 'while'
    t.description = '<Reservada while>'
    return t

def t_else(t):
    r'\belse\b|\bELSE\b'
    t.type = 'else'
    t.description = '<Reservada else>'
    return t


def t_ParentesisIzq(t):
    r'\('
    t.type = 'ParentesisIzq'
    t.description = '<Parentesis de apertura>'
    return t

def t_ParentesisDer(t):
    r'\)'
    t.type = 'ParentesisDer'
    t.description = '<Parentesis de cierre>'
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'IDENTIFICADOR'
    t.description = 'Identificador'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"caracter no permitido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

app = Flask(__name__)

@app.route('/', methods=['GET' , 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.txt'):
                code = file.read().decode('utf-8')
            else:
                return "File type not supported"
        else:
            code = request.form['code']
        lexer.input(code)
        line_counter = 1
        tokens = []
        for token in lexer:
            tokens.append({'type': token.type, 'value': token.value, 'line': line_counter, 'description': token.description})
            if token.value in ['(', ')']:
                line_counter += 1
            else:
                words = token.value.split()
                line_counter += len(words)
        return render_template('index.html', tokens=tokens)

    return render_template('index.html')

if __name__ == '__main__':

    app.run(debug=True)
