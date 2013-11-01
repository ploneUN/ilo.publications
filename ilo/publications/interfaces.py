from five import grok
from plone.directives import dexterity, form
from zope import schema
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.app.dexterity.behaviors.metadata import IBasic
from collective import dexteritytextindexer
from collective.miscbehaviors.behavior.leadimage import ILeadImage
from zope.schema.interfaces import IUnorderedCollection
from zope.interface import directlyProvides

#ILeadImage.get('image').title = u'Lead image'
#ILeadImage.get('imageCaption').title = u'Lead image caption'

class IPublicationSchema(form.Schema, IBasic, IImageScaleTraversable):

    dexteritytextindexer.searchable('subtitle')
    subtitle = schema.TextLine(title=u'Subtitle', required=False)

    description = schema.Text(
        title=u'Short description',
        description=(
            u'A short summary of the content. Please limit your entry to '
            u' less than 300 words.'
        ),
        required=True,
        missing_value=u'',
        max_length=1024
    )

    dexteritytextindexer.searchable('publication_authors')
    publication_authors = schema.List(
        title=u'Authors of the publication',
        description=(
            u'Fill in the names of the authors of this publication, one'
            u' on each line.'
        ),
        required=True,
        value_type=schema.TextLine()
    )

    office = schema.Choice(
        title=u'Publishing office', 
        description=u'If more than one office is involved then the office ' +
        u'taking primary responsibility for the publication process ' +
        u'should be chosen.',
        required=True,
        source='ilo.vocabulary.offices'
    )

    country = schema.Choice(
        title=u'Place of publishing',
        required=True,
        source='ilo.vocabulary.countries'
    )

    publishing_year = schema.Int(
        title=u'Publishing year',
        required=True
    )



    work_areas = schema.List(
        title=u'Areas of work',
        required=True,
        value_type=schema.Choice(
            source='ilo.vocabulary.themes',
        )
    )
    directlyProvides(work_areas, IUnorderedCollection)

    languages = schema.List(
        title=u'Languages',
        description=u'Note: Editions of the same publication in different ' + 
        'languages need  separate RPC applications. For bi and multi-lingual ' + 
        'publications please select all relevant options.',
        required=True,
        value_type=schema.Choice(
            source='ilo.vocabulary.languages'
        )
    )
    directlyProvides(languages, IUnorderedCollection)

#    dexteritytextindexer.searchable('file')
#    file = NamedBlobFile(
#        title=u'File attachment',
#        required=False,
#    )
#



class ICommonChecklistSchema(form.Schema):

    # CIP state

    dexterity.write_permission(submitted_for_cip='ilo.publication.ModifyCIPFields')
    form.widget(submitted_for_cip='z3c.form.browser.radio.RadioFieldWidget')
    submitted_for_cip = schema.Bool(
        title=u'Submitted for Cataloging in Publication (CIP) data', 
        description=u'Have the ISSN, final title and subtitle, author/s, ' +
        'introduction/overview, table of contents and abstract been sent' +
        ' to the librarian of the office that is publishing the item or' +
        ' sent to INFORMCIP@ilo.org to request CIP data?'
    )

    dexterity.write_permission(issued_cip='ilo.publication.ModifyCIPFields')
    form.widget(issued_cip='z3c.form.browser.radio.RadioFieldWidget')
    issued_cip = schema.Bool(
        title=u'Copyright page issued?',
        description=u'Has the copyright page been issued?'
    )



    # Proofreading state

    dexterity.write_permission(proofreading_sent='ilo.publication.ModifyProofreadingFields')
    form.widget(proofreading_sent='z3c.form.browser.radio.RadioFieldWidget')
    proofreading_sent = schema.Bool(
        title=u'Proofread hardcopy sent to RPC?',
        description=u'''
        At this stage the RPC will review your
        publication to ensure it meets the editorial and visual standard
        of the ILO. This will be done by reviewing a sample equivalent to
        approximately 10 per cent of the content. This process will be
        repeated as many times as is necessary to meet the required RPC
        standards. Responsibility for making any required changes will
        remain solely with the author and not the RPC. 
        '''
        )

    dexterity.write_permission(proofreading_done='ilo.publication.ModifyProofreadingFields')
    form.widget(proofreading_done='z3c.form.browser.radio.RadioFieldWidget')
    proofreading_done = schema.Bool(
        title=u'Proofreading done',
        description=(u'Have the proofs (including cover and copyright page) '
        'been corrected and approved ready for printing/online publication?')
    )

      # Printing/Publication state

    dexterity.write_permission(standards_met='ilo.publication.ApprovePrintingPublication')
    form.widget(standards_met='z3c.form.browser.radio.RadioFieldWidget')
    standards_met = schema.Bool(
        title=u'Does the publication meet ILO publication standards?'
    )

    dexterity.write_permission(recommended_formats='ilo.publication.ApprovePrintingPublication')
    recommended_formats = schema.List(
        title=u'The RPC recommends this publication be produced in:',
        value_type=schema.Choice(
            values=[u'Printed format','Electronic/online formats']
        )
    )
    directlyProvides(recommended_formats, IUnorderedCollection)


    dexterity.write_permission(copies_to_print='ilo.publication.ApprovePrintingPublication')
    copies_to_print = schema.Int(
        title=u'Number of copies to be printed.',
        required=True,
    )

    dexterity.write_permission(publication_format='ilo.publication.ApprovePrintingPublication')
    publication_format = schema.List(
        title=u'Format of publication',
        required=True,
        value_type=schema.Choice(source='ilo.vocabulary.publicationformats')
    )
    directlyProvides(publication_format, IUnorderedCollection)

    # Distribution state

    dexterity.write_permission(remote_url='ilo.publication.ModifyDistributionFields')
    remote_url = schema.URI(
        title=u'Link to full text in WCMS',
        required=False
    )

    dexterity.write_permission(distribution_strategy_file='ilo.publication.ModifyDistributionFields')
    distribution_strategy_file = NamedBlobFile(
        title=u'Upload distribution list or strategy document.',
        required=False,
    )

    dexterity.write_permission(qa_done='ilo.publication.ApproveDistribution')
    form.widget(qa_done='z3c.form.browser.radio.RadioFieldWidget')
    qa_done = schema.Bool(
        title=(u'Has the title completed quality control and is ready for '
            'distribution and WCMS uploading?')
    )
#
#    dexterity.write_permission(lowq_pdf='ilo.publication.ModifyDistributionFields')
#    lowq_pdf = NamedBlobFile(
#        title=u'Low resolution PDF',
#        required=False,
#        description=(u'Has a low resolution PDF (max 2,000KB) for WCMS '
#            'uploading  been received from the printer?. If yes, attach it '
#            'here.')
#    )
#
#    dexterity.write_permission(highq_pdf='ilo.publication.ModifyDistributionFields')
#    highq_pdf = NamedBlobFile(
#        title=u'High resolution PDF', 
#        required=False,
#        description=u'Attach high resolution pdf here if available.' 
#    )
#
#    dexterity.write_permission(wcms_uploaded='ilo.publication.ApproveDistribution')
#    form.widget(wcms_uploaded='z3c.form.browser.radio.RadioFieldWidget')
#    wcms_uploaded = schema.Bool(
#        title=u'Has a PDF version been uploaded onto WCMS?'
#    )

class INonOfficialPublicationChecklist(ICommonChecklistSchema):
    
    publication_type = schema.Choice(
        title=u'Type of publication',
        required=True,
        source='ilo.vocabulary.publicationtypes.nonofficialpublication'
    )

  # Layout & Design state

    dexterity.write_permission(layout_done='ilo.publication.ModifyLayoutDesignFields')
    form.widget(layout_done='z3c.form.browser.radio.RadioFieldWidget')
    layout_done = schema.Bool(
        title=u'Layout done',
        description=(u'Has the layout of this non-official publication followed the '
        'standard template set for this type of publication? Has the copyright page, CIP '
        'data, ISBN been inserted?')
        
        
    )

    dexterity.write_permission(design_done='ilo.publication.ModifyLayoutDesignFields')
    form.widget(design_done='z3c.form.browser.radio.RadioFieldWidget')
    design_done = schema.Bool(
        title=u'Design done',
        description=(u'Has the design of this non-official publication followed the '
        'standard template set for this type of publication?')
    )



    #CIP state

    dexteritytextindexer.searchable('isbn')
    dexterity.write_permission(isbn='ilo.publication.ModifyCIPFields')
    isbn = schema.List(
        title=u'ISBN number',
        description=u'Fill in the ISBN number for this non-official publication (one per line).',
        required=False,
        value_type=schema.TextLine()
    )

    # Approval state

    dexterity.write_permission(rpc_approved='ilo.publication.ApproveProposal')
    form.widget(rpc_approved='z3c.form.browser.radio.RadioFieldWidget')
    rpc_approved = schema.Bool(
        title=u'Approved by RPC Focal Point',
        description=(u'Does the proposed publication conform to the '
            'Regional Research Strategy and has it been approved '
            'by RPC focal point?')
    )

    dexterity.write_permission(rpc_submitted='ilo.publication.ApproveProposal')
    form.widget(rpc_submitted='z3c.form.browser.radio.RadioFieldWidget')
    rpc_submitted = schema.Bool(
        title=(u'Has the title been submitted in advanced to the RPC ' 
            'Provisional Publications Programme?')
    )

    # Reviewer

    dexterity.write_permission(ilo_reviewer='ilo.publication.ModifyReviewFields')
    dexteritytextindexer.searchable('ilo_reviewer')
    ilo_reviewer = schema.TextLine(
        title=u'ILO reviewer name and unit',
        required=True,
        description=(u'Has the document been peer reviewed by an ILO '
            'official outside  the authoring unit and written ' 
            'comments submitted? If yes, fill in the reviewer name '
            'and unit here.')
    )


    dexterity.write_permission(external_reviewer='ilo.publication.ModifyReviewFields')
    dexteritytextindexer.searchable('external_reviewer')
    external_reviewer = schema.TextLine(
        title=u'External reviewer / meeting or workshop review',
        required=True,
        description=(u'Has the document been externally peer reviewed, '
            '(i.e. by a reviewer from another organization, or outside the '
            'authoring unit\'s ILO region or examined by a meeting/workshop of '
            'experts. If this was reviewed by an external reviewer '
            'fill in the reviewer name, title, and organization here (External '
            'reviewer must be different than the ILO Reviewer above). '
            'If this was reviewed in a meeting/workshop of experts, fill '
            'in the title, organization and date of the meeting/workshop here.')
    )

    dexterity.write_permission(finalized_draft='ilo.publication.ModifyReviewFields')
    form.widget(finalized_draft='z3c.form.browser.radio.RadioFieldWidget')
    finalized_draft = schema.Bool(
        title=(u'Has the Author revised and finalized the draft in the '
            'light of reviewer comments')
    )

    # Editing state

    dexterity.write_permission(editor_name='ilo.publication.ModifyEditingFields')
    dexteritytextindexer.searchable('editor_name')
    editor_name = schema.TextLine(
        title=u'Name of internal editor',
        description=(u'Has the manuscript been evaluated by the author and '
        'any substantive or copy-editing completed to ILO standards, by the '
        'author/author\'s unit?. If yes, fill in the author/author\'s unit or '
        'editor\'s name if not author.')
    )

    dexterity.write_permission(external_editor_name='ilo.publication.ModifyEditingFields')
    dexteritytextindexer.searchable('external_editor_name')
    external_editor_name = schema.TextLine(
        title=u'Name and position of external editor',
        description=(u'Has a contract (for external editors) been issued and '
            'the editor received the Publications Support Pack?. If yes, fill '
            'in the editor name and position here. (The editor must be from '
            'outside the author\'s unit. Use of a professional editor is '
            'recommended.)')
    )

    dexterity.write_permission(finalized_editing='ilo.publication.ModifyEditingFields')
    form.widget(finalized_editing='z3c.form.browser.radio.RadioFieldWidget')
    finalized_editing = schema.Bool(
        title=(u'Has the editor finalized the manuscript to ILO standards '
        'and submitted it with the Handover Checklist for Editors?')
    )


class IWorkingPaperChecklist(ICommonChecklistSchema):


    publication_type = schema.Choice(
        title=u'Type of publication',
        required=True,
        source='ilo.vocabulary.publicationtypes.workingpaper'
    )

  # Layout & Design state

    dexterity.write_permission(layout_done='ilo.publication.ModifyLayoutDesignFields')
    form.widget(layout_done='z3c.form.browser.radio.RadioFieldWidget')
    layout_done = schema.Bool(
        title=u'Layout done',
        description=(u'Has the layout of this working paper followed the '
        'standard template set for this series? Has the copyright page, CIP '
        'data, ISSN been inserted?')
        
        
    )

    dexterity.write_permission(design_done='ilo.publication.ModifyLayoutDesignFields')
    form.widget(design_done='z3c.form.browser.radio.RadioFieldWidget')
    design_done = schema.Bool(
        title=u'Design done',
        description=(u'Has the design of this working paper followed the '
        'standard template set for this series?')
    )


        #CIP state

    dexteritytextindexer.searchable('isbn')
    dexterity.write_permission(isbn='ilo.publication.ModifyCIPFields')
    isbn = schema.List(
        title=u'ISSN number',
        description=u'Fill in the ISSN number for this Working Paper Series (one per line).',
        required=False,
        value_type=schema.TextLine()
    )


    # Approval state

    dexterity.write_permission(series_title='ilo.publication.ApproveProposal')
    series_title = schema.TextLine(
        title=(u'What is the title of the working paper series (i.e. ILO '
         'Asia-Pacific Working Paper Series)?')
    )

    dexterity.write_permission(rrs_approved='ilo.publication.ApproveProposal')
    form.widget(rrs_approved='z3c.form.browser.radio.RadioFieldWidget')
    rrs_approved = schema.Bool(
        title=(u'Does the proposed publication conform to the Regional '
        'Research Strategy and has it been approved by responsible chief?')
    )

    # Review state

    dexterity.write_permission(ilo_reviewers='ilo.publication.ModifyReviewFields')
    dexteritytextindexer.searchable('ilo_reviewers')
    ilo_reviewers = schema.List(
        title=u'Reviewers',
        description=(u'Has the draft paper been examined by a meeting/workshop or ' 
        'reviewed by two ILO officials, and revised in the light of comments? '
        'If it was reviewed by ILO officials, fill in their name and unit, one '
        'person per line. If it was examined in a meeting/workshop, fill in '
        'the title, organization, and date of the meeting/workshop in a single '
        'line.'),
        value_type=schema.TextLine()
    )

    # Editing state

    dexterity.write_permission(editor_name='ilo.publication.ModifyEditingFields')
    dexteritytextindexer.searchable('editor_name')
    editor_name = schema.List(
        title=u'Editor Name and Title',
        description=(u'The draft has been evaluated for substantive and copy '
            'editing and finalized to the relevant ILO standards: <br/>'
            '<ol><li>The editor has evaluated the draft for substantive or '
            'copy-editing and been issued a contract.</li><li>The editor has '
            'finalized the text to relevant ILO standards.</li></ol>If yes, '
            'fill in the editor\'s name and title here.'),
        value_type=schema.TextLine()
    )


    # Layout & Design state

    dexterity.write_permission(formatting_done='ilo.publication.ModifyLayoutDesignFields')
    form.widget(formatting_done='z3c.form.browser.radio.RadioFieldWidget')
    formatting_done = schema.Bool(
        title=u'Formatting done',
        description=(u'Have the correct formatting style, front/back covers, '
        'font, formatting style, copyright page with CIP data, ISSN, etc. been '
        'followed?')
    )

FIELDS=[
    'submitted_for_cip',
    'issued_cip',
    'isbn',
    'proofreading_done',
    'proofreading_sent',
    'layout_done',
    'design_done',
    'standards_met',
    'recommended_formats',
    'copies_to_print',
    'publication_format',
    'diststrategy_ready',
    'qa_done',
    'lowq_pdf',
    'highq_pdf',
    'wcms_uploaded',
    'rpc_approved',
    'rpc_submitted',
    'ilo_reviewer',
    'external_reviewer',
    'finalized_draft',
    'editor_name',
    'external_editor_name',
    'finalized_editing',
    'series_title',
    'rrs_approved',
    'ilo_reviewers',
    'formatting_done',
    'distribution_strategy_file',
    'remote_url'
    ]

class INonOfficialPublication(IPublicationSchema, INonOfficialPublicationChecklist):
    form.fieldset('stagefields',
        label=u'Add new info',
        fields=FIELDS
    )
    pass

class IWorkingPaper(IPublicationSchema, IWorkingPaperChecklist):
    form.fieldset('stagefields',
        label=u'Add new info',
        fields=FIELDS
    )
    pass
