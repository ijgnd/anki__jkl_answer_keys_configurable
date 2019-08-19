# AGPLv3
# Copyright Austin Hasten 2018, ijgnd 2019


from aqt import mw
from anki.hooks import wrap
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
 
