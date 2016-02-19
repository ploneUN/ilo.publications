from setuptools import setup, find_packages
import os

version = '1.5.dev1'

setup(name='ilo.publications',
      version=version,
      description="ILO Publications Process Facility for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Khairul Anwar',
      author_email='anwarbaik88@gmail.com',
      url='https://github.com/ploneUN/ilo.publications',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ilo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity [grok, relations]',
          'plone.namedfile [blobs]',
          'collective.autopermission',
          'collective.wtf',
          'collective.dexteritytextindexer',
          'collective.miscbehaviors',
          'ilo.vocabularies',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      # The next two lines may be deleted after you no longer need
      # addcontent support from paster and before you distribute
      # your package.
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],

      )
