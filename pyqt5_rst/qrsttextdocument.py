
# [Py]Qt5 uses camelCase convention for method and attribute names, so it makes sense to
#   maintain that in a subclass. It would be nice to be able to tell pylint to lint specific
#   files/folders/modules differently, but that is not possible (currently).
# pylint: disable=invalid-name

from docutils.frontend import get_default_settings as docutils_get_default_settings
from docutils.parsers.rst import Parser as RstParser
from docutils.utils import new_document as new_rst_document

from PyQt5.QtGui import QTextDocument

from .doctree2qt import Doctree2Qt


class QRstTextDocument(QTextDocument):

    def setReStructuredText(self, text: str):
        self.clear()
        self.clearUndoRedoStacks()

        doctree = new_rst_document("<string>", docutils_get_default_settings(RstParser))
        RstParser().parse(text, doctree)
        doctree.walkabout(Doctree2Qt(doctree, self))

    def toReStructuredText(self) -> str:
        return ""
