"""
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Copyright 2019 ijgnd
#           2018 Austin Hasten
#           2018 Eric Hu


the dictionary "Qt_functions" is taken from the add-on "anki-custom-shortcuts"
which is covered by the following copyright and permission notice,
https://github.com/Liresol/anki-custom-shortcuts/blob/master/LICENSE:

    Copyright 2018 Eric Hu

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""



from anki.hooks import wrap
from aqt import mw
from aqt.qt import *
from aqt.reviewer import Reviewer
from aqt.utils import tooltip


def gc(arg, fail=False):
    return mw.addonManager.getConfig(__name__).get(arg, fail)


def my_answer_hack(self, ease):
    isq = self.state == "question"
    if (isq and not gc("rate_from_question",False)):
        self._getTypedAnswer()
    else:
        if not gc("adjust_the_meaning_of_the_answer_keys_depending_on_number_of_answer_buttons", False):
            self._answerCard(ease)
        else:
            #if mw.col.schedVer() == 1:
            cnt = mw.col.sched.answerButtons(mw.reviewer.card) # Get button count
            if ease == 1:     # 1 is always the leftmost button
                self._answerCard(1)
            elif ease == 4:   # 4 always the rightmost button/highest ease
                self._answerCard(cnt)
            # reviewer:
            # def _defaultEase(self):
            #     if self.mw.col.sched.answerButtons(self.card) == 4:
            #         return 3
            #     else:
            #         return 2
            elif ease == 3:
                self._answerCard(self._defaultEase())
            else:
                if cnt == 4 or cnt == 2:
                    self._answerCard(2)
                # 3 buttons
                elif gc("adjusted_answer_keys__second_key_for_less_than_four_buttons") == "ignore":
                    tooltip('three buttons. Ignoring key ...')
                elif gc("adjusted_answer_keys__second_key_for_less_than_four_buttons") == "defaultease":
                    self._answerCard(2)
                elif gc("adjusted_answer_keys__second_key_for_less_than_four_buttons") == "fail":
                    self._answerCard(1)


Qt_functions = {
                # already used by Anki
                # "Qt.Key_Enter":Qt.Key_Enter, 
                # "Qt.Key_Return":Qt.Key_Return,
                "Qt.Key_Escape": Qt.Key_Escape,
                "Qt.Key_Space": Qt.Key_Space,
                "Qt.Key_Tab": Qt.Key_Tab,
                "Qt.Key_Backspace": Qt.Key_Backspace,
                "Qt.Key_Delete": Qt.Key_Delete,
                "Qt.Key_Left": Qt.Key_Left,
                "Qt.Key_Down": Qt.Key_Down,
                "Qt.Key_Right": Qt.Key_Right,
                "Qt.Key_Up": Qt.Key_Up,
                "Qt.Key_PageUp": Qt.Key_PageUp,
                "Qt.Key_PageDown": Qt.Key_PageDown,
                }


def key_hack(val):
    if val in Qt_functions:
        return Qt_functions[val]
    else:
        return val


def newShortcutKeys(self, _old):
    return _old(self) + [
        (key_hack(gc("reviewer_1", 1)), lambda: my_answer_hack(self, 1)),
        (key_hack(gc("reviewer_2", 2)), lambda: my_answer_hack(self, 2)),
        (key_hack(gc("reviewer_3", 3)), lambda: my_answer_hack(self, 3)),
        (key_hack(gc("reviewer_4", 4)), lambda: my_answer_hack(self, 4)),
    ]

def newAnswerCard(self, ease, _old):
    if gc("rate_from_question", False) and self.state == "question":
        self.state = 'answer'
    _old(self, min(self.mw.col.sched.answerButtons(self.card), ease))


Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, newShortcutKeys, "around")
Reviewer._answerCard = wrap(Reviewer._answerCard, newAnswerCard, "around")

