# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

from anki.hooks import wrap
import anki.sync

# markdawn2.py from http://daringfireball.net/projects/markdown/
from markdown2 import Markdown
import re


def markdownconverter(arg = None):

    if arg is None:
        col = mw.col
    else:
        col = arg

    changed = 0
    # Iterate over the cards
    ids = col.findCards("tag:Markdown")
    for id in ids:
        card = col.getCard(id)
        note = card.note()
        for (name, value) in note.items():
            converted = ''
            converted = remade(value)
            #showInfo("%s:\n%s" % (name, converted) )
            note[name] = converted
        note.delTag("Markdown")
        ++changed
        note.flush()
    #   mw.reset()

    if arg is None:
        showInfo("Done: %d db" % changed)

    if changed > 0:
        return changed

# create a new menu item, "test"
action = QAction("Markdown2Html", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), markdownconverter)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


def remade(data):
    md = Markdown()
    html = data
    html = re.sub('<br />','\n', data)
    html = md.convert(html)
    return html

from aqt.sync import SyncManager
#https://groups.google.com/forum/#!topic/anki-addons/qmgXMKG2KRU
#Runs after sync has finished, before collection is reloaded
def mysync(self):

        #reload the colection
        if not self.mw.col:
            self.mw.loadCollection()

        #run my function, 
                #which returns true if something changed.
        if markdownconverter(self.mw.col):
                        #Sometthing changed, so unload and sync again
            self.mw.unloadCollection()
            self._sync()

SyncManager.sync= wrap(SyncManager.sync, mysync)

