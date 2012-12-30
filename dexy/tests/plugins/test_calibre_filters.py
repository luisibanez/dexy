from dexy.tests.utils import wrap
from dexy.node import DocNode

HTML = """
<h1>Header</h1>
<p>This is some body.</p>
"""

def run_calibre(ext):
    with wrap() as wrapper:
        node = DocNode("book.html|calibre",
                calibre = { 'ext' : ext },
                contents = HTML,
                wrapper=wrapper)
        wrapper.run_docs(node)
        doc = node.children[0]
        assert doc.output().is_cached()

def test_calibre_mobi():
    run_calibre('.mobi')

def test_calibre_epub():
    run_calibre('.epub')

def test_calibre_fb2():
    run_calibre('.fb2')

def test_calibre_htmlz():
    run_calibre('.htmlz')

def test_calibre_lit():
    run_calibre('.lit')

def test_calibre_lrf():
    run_calibre('.lrf')

def test_calibre_pdf():
    run_calibre('.pdf')

def test_calibre_rtf():
    run_calibre('.rtf')

def test_calibre_snb():
    run_calibre('.snb')

def test_calibre_tcr():
    run_calibre('.tcr')

def test_calibre_txt():
    run_calibre('.txt')

def test_calibre_txtz():
    run_calibre('.txtz')
