
# @see comment in .pylintrc for reason
# pylint: disable=invalid-name

from docutils.nodes import (
    GenericNodeVisitor,
    SkipNode,
)

from PyQt5.QtGui import (
    QFont,
    QFontDatabase,
    QTextBlockFormat,
    QTextCharFormat,
    QTextCursor,
)

class Doctree2Qt(GenericNodeVisitor):

    HeadingSizeMagic = 4

    NoOpTags = (
        'colspec',
        'document',
        'table',
        'tbody',
    )

    def __init__(self, rst_document, qt5_document):
        super().__init__(rst_document)

        self._qt5_document = qt5_document
        self._cursor = QTextCursor(qt5_document)
        self._char_format = QTextCharFormat()
        self._char_format_mono = QTextCharFormat()

        self._mono_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self._mono_font.setStyleHint(QFont.Monospace)
        self._char_format_mono.setFont(self._mono_font)

        self._flags = {
        }
        self._section_level = 0
        self._indentation_level = 0

        self._table_coords = {}

    def default_visit(self, node):
        if node.tagname in self.NoOpTags:
            return
        print(f"Unhandled tag: {node.tagname}")

    def default_departure(self, _):
        pass

    def visit_block_quote(self, _):
        self._indentation_level += 1

    def depart_block_quote(self, _):
        self._indentation_level -= 1

    def depart_document(self, _):
        # Remove empty block at top of created document.
        # (We assume that there's only one doctree per invocation.)
        self._cursor.setPosition(0)
        self._cursor.movePosition(QTextCursor.NextBlock)
        self._cursor.deletePreviousChar()

    def visit_emphasis(self, _):
        self._char_format.setFontItalic(True)

    def depart_emphasis(self, _):
        self._char_format.setFontItalic(False)

    def visit_entry(self, node):
        self._table_coords['col'] += 1
        self._cursor = self._cursor.currentTable().cellAt(
            self._table_coords['row'],
            self._table_coords['col']
        ).firstCursorPosition()

    def visit_inline(self, node):
        classes = node.get('classes', [])
        if 'strike' in classes:
            self._char_format.setFontStrikeOut(True)
        if 'underline' in classes:
            self._char_format.setFontUnderline(True)

    def depart_inline(self, node):
        classes = node.get('classes', [])
        if 'strike' in classes:
            self._char_format.setFontStrikeOut(False)
        if 'underline' in classes:
            self._char_format.setFontUnderline(False)

    def visit_literal(self, node):
        self._cursor.insertText(node.astext(), self._char_format_mono)
        raise SkipNode

    def visit_literal_block(self, node):
        self._indentation_level += 1
        # Create an indented block
        self.visit_paragraph(node)

        self._cursor.insertText(node.astext(), self._char_format_mono)
        self._indentation_level -= 1
        raise SkipNode

    def visit_paragraph(self, _):
        block_format = QTextBlockFormat()
        block_format.setIndent(self._indentation_level)
        self._cursor.insertBlock(block_format)

    def visit_row(self, node):
        self._table_coords['row'] += 1
        self._table_coords['col'] = -1

        table = self._cursor.currentTable()
        if self._table_coords['row'] + 1 > table.rows():
            table.appendRows(1)

    def visit_section(self, _):
        self._section_level += 1

    def depart_section(self, _):
        self._section_level -= 1

    def visit_strong(self, _):
        self._char_format.setFontWeight(QFont.Bold)

    def depart_strong(self, _):
        self._char_format.setFontWeight(QFont.Normal)

    def depart_table(self, _):
        self._cursor.movePosition(QTextCursor.End)

    def visit_term(self, _):
        self._cursor.insertBlock()

    def visit_tgroup(self, node):
        column_count = node['cols']
        self._cursor.insertTable(1, column_count)
        self._table_coords = {
            'row': -1,
            'col': -1,
        }

    def visit_title(self, _):
        block_format = QTextBlockFormat()
        block_format.setHeadingLevel(self._section_level)

        self._char_format.setProperty(
            QTextCharFormat.FontSizeAdjustment,
            self.HeadingSizeMagic - self._section_level)

        self._cursor.insertBlock(block_format)

    def depart_title(self, _):
        self._char_format = QTextCharFormat()

    def visit_Text(self, node):
        self._cursor.insertText(node.astext().replace('\n', ' '), self._char_format)
