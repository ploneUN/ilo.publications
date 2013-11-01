from five import grok
from Products.ATContentTypes.interfaces.topic import IATTopic
from Products.ATContentTypes.interfaces.folder import IATFolder

grok.templatedir('templates')

class PublicationSummaryView(grok.View):
    grok.baseclass()
    grok.name('publication_summary_view')
    grok.template('publication_summary_view')

class PublicationSummaryViewFolder(PublicationSummaryView):
    grok.context(IATTopic)


class PublicationSummaryViewFolder(PublicationSummaryView):
    grok.context(IATFolder)
