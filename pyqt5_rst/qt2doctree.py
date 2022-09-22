
from docutils import (
    frontend,
    nodes,
    utils,
)

class Qt2Doctree:

    BoldWeight = 75
    NormalWeight = 50

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

            elif block.next().blockFormat().indent():
                # This block is the start of a definition list
                block = self.append_definition_list(block)
                continue

            else:
                paragraph = nodes.paragraph()
                self.append_text_to_node(paragraph, block)
                self._section_stack[-1].append(paragraph)

            block = block.next()

        return doctree

    def append_definition_list(self, block):

        def new_definition(definition_list, block):
            item = nodes.definition_list_item()
            term = nodes.term()
            self.append_text_to_node(term, block)
            definition = nodes.definition()

            item.append(term)
            item.append(definition)
            definition_list.append(item)
            return definition

        definition_list = nodes.definition_list()
        self._section_stack[-1].append(definition_list)

        definition = new_definition(definition_list, block)
        self._list_stack.append(['definition', [definition_list, definition]])

        block = block.next()
        while block.isValid():
            list_indent = len(self._list_stack)

            this_block_indent = block.blockFormat().indent()
            next_block_indent = block.next().blockFormat().indent()

            if this_block_indent == list_indent:
                if next_block_indent > this_block_indent:
                    # Nested definition list
                    # @todo
                    pass

                else:
                    # Definition continues
                    paragraph = nodes.paragraph()
                    self.append_text_to_node(paragraph, block)
                    self._list_stack[-1][1][1].append(paragraph)

            elif this_block_indent < list_indent:
                # end of this definition

                if next_block_indent == list_indent:
                    # list continues, new term
                    definition = new_definition(self._list_stack[-1][1][0], block)
                    self._list_stack[-1][1][1] = definition

                else:
                    # list ends
                    self._list_stack.pop()
                    return block

            block = block.next()

        return block

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

        if text_format.fontWeight() == self.BoldWeight:
            return nodes.strong(text=text_segment)

        return nodes.Text(text_segment)
