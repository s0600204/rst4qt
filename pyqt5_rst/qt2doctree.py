
from docutils import (
    frontend,
    nodes,
    utils,
)

from PyQt5.QtGui import QFont

class Qt2Doctree:

    def __init__(self):

        self._section_stack = []
        self._section_level_stack = []

        self._list_stack = []

    def convert(self, qt5_document):
        doctree = utils.new_document("", frontend.get_default_settings())

        self._section_stack = [doctree]
        self._section_level_stack = [0]

        block = qt5_document.firstBlock()
        while block.isValid():
            block_format = block.blockFormat()
            level = block_format.headingLevel()
            if level > 0:
                # This block is a section header
                self.append_header(block)

            else:
                paragraph = nodes.paragraph()
                self.append_text_to_node(paragraph, block)
                self._section_stack[-1].append(paragraph)

            block = block.next()

        return doctree

    def append_header(self, block):

        # Backtrack up the stack if it's a higher-level header
        header_level = block.blockFormat().headingLevel()
        while header_level <= self._section_level_stack[-1]:
            self._section_stack.pop()
            self._section_level_stack.pop()

        # @todo: look up how `ids` and `names` should *actually* be created/formed
        text_lower = block.text().lower()
        new_section = nodes.section(ids=text_lower, names=text_lower)
        self._section_stack[-1].append(new_section)

        self._section_stack.append(new_section)
        self._section_level_stack.append(header_level)

        title = nodes.title()
        self.append_text_to_node(title, block)
        self._section_stack[-1].append(title)

    def append_text_to_node(self, node, block):
        text = block.text()
        for segment in block.textFormats():
            node.append(
                self.format_text_segment(
                    text[segment.start:segment.start + segment.length],
                    segment.format))

    def format_text_segment(self, text_segment, text_format):

        if text_format.fontItalic():
            return nodes.emphasis(text=text_segment)

        if text_format.fontStrikeOut():
            return nodes.inline(text=text_segment, classes=['strike'])

        if text_format.fontUnderline():
            return nodes.inline(text=text_segment, classes=['under'])

        if text_format.fontWeight() == QFont.Bold:
            return nodes.strong(text=text_segment)

        return nodes.Text(text_segment)
