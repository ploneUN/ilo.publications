from five import grok
from Products.CMFCore.interfaces import IContentish

grok.templatedir('templates')

class Publicationlisting(grok.View):
    grok.context(IContentish)
    grok.name('publicationlisting')
    grok.require('zope2.View')
    grok.template('publicationlisting')
