from collective.dexteritytextindexer.converters import DefaultDexterityTextIndexFieldConverter
from five import grok
from ilo.publications.interfaces import IPublicationSchema
from zope.schema.interfaces import IList
from z3c.form.interfaces import IWidget
from plone.indexer.decorator import indexer

class CustomFieldConverter(DefaultDexterityTextIndexFieldConverter):
    grok.adapts(IPublicationSchema, IList, IWidget)

    def convert(self):
        # implement your custom converter
        # which returns a string at the end
        value = self.field.get(self.context)
        if not value:
            return ''

        try:
            return ' '.join(value)
        except:
            return ''
        



@indexer(IPublicationSchema)
def publicationtype_indexer(obj, **kw):
    if obj.publication_type:
        return (obj.publication_type,)
    return ()

@indexer(IPublicationSchema)
def office_indexer(obj, **kw):
    if obj.office:
        return (obj.office,)
    return ()

@indexer(IPublicationSchema)
def workareas_indexer(obj, **kw):
    return obj.work_areas

@indexer(IPublicationSchema)
def publication_authors_indexer(obj, **kw):
    return ' '.join(getattr(obj, 'publication_authors', []) or [])

@indexer(IPublicationSchema)
def publication_languages_indexer(obj, **kw):
    return getattr(obj, 'languages', ())
