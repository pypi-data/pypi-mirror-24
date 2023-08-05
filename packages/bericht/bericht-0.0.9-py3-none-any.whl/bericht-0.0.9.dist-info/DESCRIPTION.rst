bericht
=======

Improved tabular report generation with ReportLab.

to test things real quick:

.. code-block:: python

    from reportlab.platypus.doctemplate import SimpleDocTemplate
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet

    from bericht.table import TableBuilder, Span

    rlstyle = getSampleStyleSheet()['BodyText']

    builder = TableBuilder(rlstyle)

    builder.row('this is a test1', 'second cell1', 'ending cell1')
    builder.row('this is a test', 'second cell', 'ending cell', 'forth cell')
    builder.row('this is a test', Span.COL, 'forth cell')

    doc = SimpleDocTemplate('test.pdf', pagesize=A4)
    doc.build([builder.table])

you should find a `test.pdf` file in the location where you started python


0.0.9
-----

* Ignore letterhead-page style setting if no letterhead is available.

0.0.8
-----

* CSS supports mm, cm and inch dimensions.

0.0.7
-----

* Proper handling of XObject Resources in letterheads.

0.0.6
-----

* Proper handling of /DescendantFonts when creating letterhead XObject.

0.0.5
-----

* Template bug fix related to compression.

0.0.4
-----

* Added page-break-before CSS property.

0.0.3
-----

* Added missing dependencies.

0.0.2
-----

* Bug fixes and improvements.

0.0.1
-----

* Initial release.


