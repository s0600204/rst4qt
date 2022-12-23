
from docutils import nodes


class TableBuilder:

    def __init__(self, qt2doctree, qt5_table):
        self._doctree = qt2doctree
        self._current_cell = [-1, -1]
        self._colspecs = []

        table = nodes.table() # <table>
        self.append_node(table)
        self.append_section(table)

        tgroup = nodes.tgroup(cols=qt5_table.columns()) # <tgroup>
        self.append_node(tgroup)
        self.append_section(tgroup)

        for col in range(qt5_table.columns()):
            colspec = nodes.colspec(colwidth=3)
            self.append_node(colspec)
            self._colspecs += [colspec]

        tbody = nodes.tbody() # <tbody>
        self.append_node(tbody)
        self.append_section(tbody)

    def append_node(self, node):
        self._doctree.append_node(node)

    def append_section(self, section):
        self._doctree.append_section(section)

    def finalise(self):
        self.pop_section() # </entry>
        self.pop_section() # </row>
        self.pop_section() # </tbody>
        self.pop_section() # </tgroup>
        self.pop_section() # </table>

    def pop_section(self):
        self._doctree.pop_section()

    def update(self, table, cursor):
        cell = table.cellAt(cursor)
        col = cell.column()
        row = cell.row()

        self._colspecs[col]['colwidth'] = max(
            self._colspecs[col]['colwidth'],
            len(cursor.block().text()) + 2
        )

        if row != self._current_cell[0]:
            if self._current_cell[0] != -1:
                self.pop_section() # </entry>
                self.pop_section() # </row>

            self._current_cell[0] = row
            self._current_cell[1] = -1
            node_row = nodes.row() # <row>
            self.append_node(node_row)
            self.append_section(node_row)

        if col != self._current_cell[1]:
            if self._current_cell[1] != -1:
                self.pop_section() # </entry>

            self._current_cell[1] = col
            node_entry = nodes.entry() # <entry>
            self.append_node(node_entry)
            self.append_section(node_entry)
