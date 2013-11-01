from plone.directives import dexterity
from five import grok
from ilo.publications.interfaces import IWorkingPaper

grok.templatedir('templates')

class View(dexterity.DisplayForm):
    grok.template('workingpaper_view')
    grok.context(IWorkingPaper)
    grok.require('zope2.View')
