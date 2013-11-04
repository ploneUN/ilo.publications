from plone.directives import dexterity
from five import grok
from ilo.publications.interfaces import INonOfficialPublication

grok.templatedir('templates')

class View(dexterity.DisplayForm):
    grok.template('nonofficialpublication_view')
    grok.context(INonOfficialPublication)
    grok.require('zope2.View')

    def newline_to_comma(self, value):
        return value.replace('\r', ';')

