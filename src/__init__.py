# AGPLv3
# Copyright Austin Hasten 2018, ijgnd 2019

from aqt import mw
from anki.hooks import wrap
from aqt.reviewer import Reviewer


def gc(arg, fail=False):
    return mw.addonManager.getConfig(__name__).get(arg, fail)


def my_answer_hack(self, ease):
    if (self.state == "question" and not gc("rate_from_question",False)):
        self._getTypedAnswer()
    else:
        self._answerCard(ease)


def newShortcutKeys(self, _old):
    return _old(self) + [
        (gc("reviewer_1", 1), lambda: my_answer_hack(self, 1)),
        (gc("reviewer_2", 2), lambda: my_answer_hack(self, 2)),
        (gc("reviewer_3", 3), lambda: my_answer_hack(self, 3)),
        (gc("reviewer_4", 4), lambda: my_answer_hack(self, 4)),
    ]

def newAnswerCard(self, ease, _old):
    if gc("rate_from_question", False) and self.state == "question":
        self.state = 'answer'
    _old(self, min(self.mw.col.sched.answerButtons(self.card), ease))


Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, newShortcutKeys, "around")
Reviewer._answerCard = wrap(Reviewer._answerCard, newAnswerCard, "around")
 
