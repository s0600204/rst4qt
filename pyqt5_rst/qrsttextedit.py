
# [Py]Qt5 uses camelCase convention for method and attribute names, so it makes sense to
#   maintain that in a subclass. It would be nice to be able to tell pylint to lint specific
#   files/folders/modules differently, but that is not possible (currently).
# pylint: disable=invalid-name

from PyQt5.QtWidgets import QTextEdit

from .qrsttextdocument import QRstTextDocument


class QRstTextEdit(QTextEdit):
    """
    QRstTextEdit is functionally identical to QTextEdit, but with the added ability
    to get and set the textual content as reStructuredText.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDocument(QRstTextDocument())

    @property
    def reStructuredText(self) -> str:
        """This property provides a reStructuredText interface to the text of the text edit."""
        return self.document().toReStructuredText()

    @reStructuredText.setter
    def reStructuredText(self, text: str):
        self.document().setReStructuredText(text)

    def setReStructuredText(self, text: str):
        """
        Changes the text of the text edit.

        Any previous text is removed and the undo/redo history is cleared.

        The input is interpreted as rich text in reStructuredText format.
        """
        self.document().setReStructuredText(text)

    def toReStructuredText(self) -> str:
        """Returns the text of the text edit as reStructuredText."""
        return self.document().toReStructuredText()
