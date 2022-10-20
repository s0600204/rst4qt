
from docutils import (
    frontend,
    nodes,
    utils,
)

from PyQt5.QtGui import QFont


class SkipText(Exception):
    """Skip appending a block's text."""

class NextIteration(Exception):
    """Continue with next Iteration."""


class Qt2Doctree:

    def __init__(self):

        self._section_stack = []
        self._section_level_stack = []

        self._list_stack = []

        # In Qt5, it's possible to indent more than once.
        self._indentation_stack = [0]

    @property
    def current_node(self):
        try:
            return self._section_stack[-1][-1]
        except IndexError:
            return None

    @property
    def current_section(self):
        return self._section_stack[-1]

    def append_node(self, node):
        self.current_section.append(node)

    def append_section(self, node):
        self._section_stack.append(node)

    def append_text(self, text, text_format=None):
        if text_format:
            text_node = self.format_text_segment(text, text_format)
        else:
            text_node = nodes.Text(text)

        self.current_node.append(text_node)

    def append_text_from_block(self, block):
        text = block.text()
        for segment in block.textFormats():
            self.append_text(
                text[segment.start:segment.start + segment.length],
                segment.format)

    def build_block_quote(self, block):
        block_indent = block.blockFormat().indent()
        block_quote = nodes.block_quote()

        self.append_node(block_quote)
        self.append_section(block_quote)

        self._indentation_stack.append(block_indent)
        raise NextIteration

    def build_header(self, block):
        # Backtrack up the stack if it's a higher-level header
        header_level = block.blockFormat().headingLevel()
        while header_level <= self._section_level_stack[-1]:
            self._section_stack.pop()
            self._section_level_stack.pop()

        # @todo: look up how `ids` and `names` should *actually* be created/formed
        text_lower = block.text().lower()
        new_section = nodes.section(ids=text_lower, names=text_lower)

        self.append_node(new_section)
        self.append_section(new_section)
        self._section_level_stack.append(header_level)

        self.append_node(nodes.title())

    def build_literal_block(self, block):
        current_node = self.current_node
        if isinstance(current_node, nodes.literal_block):
            # Continuation of a literal block
            block_indent = block.blockFormat().indent()
            indent = '  ' * (block_indent - 1)
            self.append_text('\n%s' % indent)
        else:
            self.append_node(nodes.literal_block())

    def convert(self, qt5_document):
        doctree = utils.new_document("", frontend.get_default_settings())

        self._section_stack = [doctree]
        self._section_level_stack = [0]

        block = qt5_document.firstBlock()
        while block.isValid():
            block_format = block.blockFormat()
            level = block_format.headingLevel()
            block_indent = block.blockFormat().indent()

            try:
                if block_indent > self._indentation_stack[-1]:
                    # This is either a block quote or a literal block
                    format_list = block.textFormats()
                    if len(format_list) == 1 and format_list[0].format.font().family() == 'monospace':
                        self.build_literal_block(block)
                    else:
                        self.build_block_quote(block)

                else:

                    while block_indent < self._indentation_stack[-1]:
                        self._section_stack.pop()
                        self._indentation_stack.pop()

                    if level > 0:
                        # This block is a section header
                        self.build_header(block)

                    else:
                        self.append_node(nodes.paragraph())

                self.append_text_from_block(block)

            except NextIteration:
                continue

            except SkipText:
                pass

            block = block.next()

        return doctree

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
