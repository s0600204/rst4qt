
# [Py]Qt5 uses camelCase convention for method and attribute names, so it makes sense to
#   maintain that in a subclass. It would be nice to be able to tell pylint to lint specific
#   files/folders/modules differently, but that is not possible (currently).
# pylint: disable=invalid-name

from docutils.frontend import OptionParser as RstOptionParser
from docutils.io import StringOutput as RstStringOutput
from docutils.parsers.rst import Parser as RstParser
from docutils.nodes import document as docutils_doctree
from docutils.utils import new_document as new_docutils_doctree

from rst2rst import Writer as RstWriter

from PyQt5.QtGui import QTextDocument

from .doctree2qt import Doctree2Qt
from .qt2doctree import Qt2Doctree


class QRstTextDocument(QTextDocument):
    """
    QRstTextDocument is functionally identical to QTextDocument, but with the
    added ability to get and set the textual content as reStructuredText.

    See the project's README for the scope of feature compatibility.
    """

    def setReStructuredText(self, text: str):
        """
        Replaces the entire contents of the document with the given
        reStructuredText-formatted text.

        The undo/redo history is reset when this function is called.
        """
        self.clear()
        self.clearUndoRedoStacks()

        settings = RstOptionParser(components=(RstParser, )).get_default_values()
        doctree = new_docutils_doctree("<string>", settings)
        RstParser().parse(text, doctree)
        doctree.walkabout(Doctree2Qt(doctree, self))

    def toDocutilsDoctree(self) -> docutils_doctree:
        """Returns a docutils doctree representation of the document."""
        return Qt2Doctree().convert(self)

    def toReStructuredText(self) -> str:
        """Returns a string containing a reStructuredText representation of the document."""
        # We shouldn't *have* to set the encoding, but we do.
        rst_string = RstStringOutput(encoding='unicode')
        RstWriter().write(self.toDocutilsDoctree(), rst_string)
        return rst_string.destination
