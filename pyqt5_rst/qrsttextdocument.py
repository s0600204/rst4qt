
# [Py]Qt5 uses camelCase convention for method and attribute names, so it makes sense to
#   maintain that in a subclass. It would be nice to be able to tell pylint to lint specific
#   files/folders/modules differently, but that is not possible (currently).
# pylint: disable=invalid-name

from PyQt5.QtGui import QTextDocument


class QRstTextDocument(QTextDocument):

    def setReStructuredText(self, text: str):
        pass

    def toReStructuredText(self) -> str:
        return ""
