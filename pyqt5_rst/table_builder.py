
from docutils import nodes


class TableBuilder:

    def __init__(self, qt2doctree, qt5_table):
        self._doctree = qt2doctree
        self._current_cell = [-1, -1]

        table = nodes.table() # <table>
        self.append_node(table)

        tgroup = nodes.tgroup(cols=qt5_table.columns()) # <tgroup>
        table.append(tgroup)

        for col in range(qt5_table.columns()):
            # No point setting the optional `colwidth` attribute, as that depends
            # on knowing how the text will be represented in reStructuredText.
            tgroup.append(nodes.colspec())

        tbody = nodes.tbody() # <tbody>
        tgroup.append(tbody)
        self.append_section(tbody)

    def append_node(self, node):
        self._doctree.append_node(node)

    def append_section(self, section):
        self._doctree.append_section(section)

    def finalise(self):
        while not isinstance(self.pop_section(), nodes.entry):
            pass           # </entry>
        self.pop_section() # </row>
        self.pop_section() # </tbody></tgroup></table>

    def pop_section(self):
        return self._doctree.pop_section()

    def update(self, table, cursor):
        cell = table.cellAt(cursor)
        col = cell.column()
        row = cell.row()

        if row != self._current_cell[0]:
            if self._current_cell[0] != -1:
                while not isinstance(self.pop_section(), nodes.entry):
                    pass           # </entry>
                self.pop_section() # </row>

            self._current_cell[0] = row
            self._current_cell[1] = -1
            node_row = nodes.row() # <row>
            self.append_node(node_row)
            self.append_section(node_row)

        if col != self._current_cell[1]:
            if self._current_cell[1] != -1:
                while not isinstance(self.pop_section(), nodes.entry):
                    pass           # </entry>

            self._current_cell[1] = col
            node_entry = nodes.entry() # <entry>
            self.append_node(node_entry)
            self.append_section(node_entry)
