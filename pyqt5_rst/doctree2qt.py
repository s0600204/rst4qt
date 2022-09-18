
# @see comment in .pylintrc for reason
# pylint: disable=invalid-name

from docutils.nodes import GenericNodeVisitor

from PyQt5.QtGui import (
    QTextBlockFormat,
    QTextCharFormat,
    QTextCursor,
)

class Doctree2Qt(GenericNodeVisitor):

    BoldWeight = 75
    NormalWeight = 50

    NoOpTags = (
        'definition_list',
        'definition_list_item',
        'document',
    )

    def __init__(self, rst_document, qt5_document):
        super().__init__(rst_document)

        self._qt5_document = qt5_document
        self._cursor = QTextCursor(qt5_document)

        self._flags = {
            'bold': False,
            'definition': False,
            'italic': False,
            'strike': False,
            'underline': False,
        }
        self._section_level = 0

    def default_visit(self, node):
        if node.tagname in self.NoOpTags:
            return
        print(f"Unhandled tag: {node.tagname}")

    def default_departure(self, _):
        pass

    def visit_definition(self, _):
        self._flags['definition'] = True

    def depart_definition(self, _):
        self._flags['definition'] = False

    def depart_document(self, _):
        # Remove empty block at top of created document.
        # (We assume that there's only one doctree per invocation.)
        self._cursor.setPosition(0)
        self._cursor.movePosition(QTextCursor.NextBlock)
        self._cursor.deletePreviousChar()

    def visit_emphasis(self, _):
        self._flags['italic'] = True

    def depart_emphasis(self, _):
        self._flags['italic'] = False

    def visit_inline(self, node):
        classes = node.get('classes', [])
        if 'strike' in classes:
            self._flags['strike'] = True
        if 'underline' in classes:
            self._flags['under'] = True

    def depart_inline(self, node):
        classes = node.get('classes', [])
        if 'strike' in classes:
            self._flags['strike'] = False
        if 'underline' in classes:
            self._flags['under'] = False

    def visit_paragraph(self, _):
        block_format = QTextBlockFormat()
        if self._flags['definition']:
            block_format.setIndent(1)
        self._cursor.insertBlock(block_format)

    def visit_section(self, _):
        self._section_level += 1

    def depart_section(self, _):
        self._section_level -= 1

    def visit_strong(self, _):
        self._flags['bold'] = True

    def depart_strong(self, _):
        self._flags['bold'] = False

    def visit_term(self, _):
        self._cursor.insertBlock()

    def visit_title(self, _):
        block_format = QTextBlockFormat()
        block_format.setHeadingLevel(self._section_level)
        self._cursor.insertBlock(block_format)

    def visit_Text(self, node):
        char_format = QTextCharFormat()
        char_format.setFontItalic(self._flags['italic'])
        char_format.setFontStrikeOut(self._flags['strike'])
        char_format.setFontUnderline(self._flags['underline'])
        char_format.setFontWeight(self.BoldWeight if self._flags['bold'] else self.NormalWeight)
        self._cursor.insertText(node.astext(), char_format)
