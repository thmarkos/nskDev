# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
#from reportlab.platypus import LongTable, Indenter, Spacer
from reportlab.lib.pagesizes import A4, letter, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


pdfmetrics.registerFont(TTFont('LinLibertine', "LinLibertineTTF/LinLibertine_R.ttf"))
style_sheet = getSampleStyleSheet()
style_sheet.add(ParagraphStyle(name='TestStyle', fontName='LinLibertine', fontSize=10, leading=10))

def my_custom_sql(query, params):
    from django.db import connections, transaction
    cursor = connections['pldb'].cursor()

    """
    # Data modifying operation - commit required
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
    transaction.commit_unless_managed()
    """
    # Data retrieval operation - no commit required
    #cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    cursor.execute(query, params)
    #row = cursor.fetchone()
    rows = cursor.fetchall()
    #rows = dictfetchall(cursor)

    transaction.commit_unless_managed(using='pldb')
    return rows

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def report(request, employee_id=138):
    
    query = """
select lpad(mh_idr1,2,'0') mh_idr1 -- Νοσοκομείο, κεντρο υγείας (Κωδικός)
      ,mh_org       -- Κωδικός στο οργανόγραμμα
      ,do_orgn      -- Τίτλος στο οργανόγραμμα
      ,em_empl      -- Αριθμός μητρώου
      ,em_epon      -- Επώνυμο
      ,em_onoma     -- Όνομα
      ,case when mh_proded = 1 then 'Μόνιμοι' else /* 2 */ 'Εκτακτοι' end ProDed
      ,pe_eidik   eidik_cd   -- ειδικότητα, κωδικός
      ,e.or_onol2 eidik_nm   -- ειδικότητα
      ,MH_HMPLHR     -- Ημέρες πληρωτέες
      ,MH_HMASF     -- Ημέρες ασφάλησης
      ,MH_MHNAS_E   -- Μήνας Εκδ. Μησθοδοσίας
      ,MH_ETOS_E    -- Ετος Εκδ. Μησθοδοσίας
      ,MH_MHNAS     -- Μήνας Μησθοδοσίας
      ,MH_ETOS      -- Ετος Μησθοδοσίας
      ,MH_SYMB      -- Κωδικός Σύμβασης
      ,S.OR_ONOL2 Symb_Nm -- Περιγραφή Σύμβασης
      ,MH_THESH           -- Κωδικός Θέσης
      ,t.OR_ONOL2 thesh_Nm -- Περιγραφή Θέσης
      ,MH_KLIM      -- Κλιμάκειο
      ,case
         when mh_mis = 1 then  'ΜΗ'
         when mh_mis = 2 then  'ΠΑ'
         when mh_mis = 3 then  'ΔΠ'
         when mh_mis = 4 then  'ΔΧ'
         when mh_mis = 5 then  'ΕΑ'
         when mh_mis = 6 then  'Ε1'
         when mh_mis = 7 then  'Ε2'
      end   MIS     -- Είδος μισθοδοσίας
     ,hi_apkra
     ,o.OR_ONOL2 apkra_nm
     ,HI_POSAR  HI_POSAR -- Ποσοστό ή αριθμός
     ,cast(HI_POSO1 / 100 as decimal(8,2)) HI_POSO1 -- Ποσό
     ,case when MH_MIS = 1 and MH_MIS_E = 1
           then cast(MH_PLHR  / 100 / 2 as decimal(8,2))
           else cast(NULL               as decimal(8,2))
      end                                  MH_PLHR15 -- Πληρωταίο (A', B'hmero)
     ,cast(MH_PLHR  / 100 as decimal(8,2)) MH_PLHR -- Πληρωταίο (A', B'hmero)

  from pldb.plmn    -- Μισθοδοσίες - Header record, names are like mh_*
  join pldb.plehist -- Μισθοδοσίες - detail record, names are like hi_*
    on (hi_empl, hi_etos, hi_mhnas, hi_mis)
     = (mh_empl, mh_etos, mh_mhnas, mh_mis)
   and (hi_etos_e, hi_mhnas_e, hi_mis_e)
     = (mh_etos_e, mh_mhnas_e, mh_mis_e)
  join pldb.plempl  -- Εργαζόμενοι, names are like em_*
    on em_empl = mh_empl
  join pldb.plpempl -- Εργαζόμενοι, names are like pe_*
    on pe_empl = em_empl
  join pldb.ploris s  -- Συμβάσεις
    on s.or_grpl = 3 and s.or_codl = MH_SYMB
  join pldb.ploris t  -- Συμβάσεις
    on t.or_grpl = 5 and t.or_codl = MH_THESH
  join pldb.ploris e  -- Ειδικότητες
    on e.or_grpl = 8 and e.or_codl = pe_eidik
  join pldb.ploris o  -- Αποδοχές / Κρατήσεις
    on o.or_grpl = 2 and o.or_codl = hi_apkra
  join pldb.pldomh    -- Οργανόγραμμα, names are like do_*
    on do_idr1 = mh_idr1
   and mh_org  = do_org1 * 1000000 + do_org2 * 10000 + do_org3 * 100 + do_org4

 where mh_empl = %s                      -- Αρ. Μητρώου Εργαζομένου
   and (mh_etos, mh_mhnas, mh_mis )      -- Μισθολογικ΄ή Περίοδος : Ετος μιθοδοσίας, Μήνας μισθοδοσίας, Είδος μισθοδοσίας
     = (%s,       %s,         %s)        -- Είδος μισθοδοσίας 1- Μήνα, 2 Προσθέτων Αμοιβών, 3 Δώρου Πάσχα, 4 Δώρου Χριστουγέννων, 5 Επίδομα Αδείας, 6 Ειδική 1 ,7 Ειδική 2
  and (mh_etos_e, mh_mhnas_e, mh_mis_e ) -- Μισθοδοσία Εκδοσης : Ετος μιθοδοσίας Εκδ, Μήνας Μισθοδοσίας Εκδ, Είδος μισθοδοσίας Εκδ
     = (%s,       %s,         %s)        -- Είδος μισθοδοσίας εκδ.: 1 - Τακτική, 2 - Εκκαθάριση, 3 - Αναδρομική
"""
    
    #employee_id=138
    mh_etos = request.GET.get('year','2012')
    mh_mhnas = request.GET.get('month','1')
    mh_mis = request.GET.get('mis','1')
    mh_etos_e = request.GET.get('year_e','2012')
    mh_mhnas_e = request.GET.get('month_e','1')
    mh_mis_e = request.GET.get('mis_e','1')
    params=[employee_id, mh_etos, mh_mhnas, mh_mis, mh_etos_e, mh_mhnas_e, mh_mis_e]
    rows = my_custom_sql(query, params)    
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ekkatharistiko.pdf'
    
    #pdfmetrics.registerFont(TTFont('LinLibertine', "LinLibertineTTF/LinLibertine_R.ttf"))
    #style_sheet = getSampleStyleSheet()
    #style_sheet.add(ParagraphStyle(name='TestStyle', fontName='LinLibertine', fontSize=14, leading=14))

    doc = SimpleDocTemplate(response, pagesize=A4)
    # container for the 'Flowable' objects
    elements = []
    
    if not rows:
        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)
        p.setFont('LinLibertine', 24)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        msg = 'Ο/Η εργαζόμεν(ος)η με αριθμό μητρώου %s δεν βρέθηκε.' % (employee_id)
        p.drawString(10, 500, msg)

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response

    
    data= [map (unicode, x) for x in list(rows)]
    """
    for data_row in data:
        data_row[22] = Paragraph(data_row[22], style=style_sheet["TestStyle"])
        data_row[24] = Paragraph(data_row[24], style=style_sheet["TestStyle"])
    """
    apodoxes = [ [data[i][22], data[i][24]] for i in range(len(data)) if int(data[i][21])<1000 ] #apodoxes
    krathseis = [ [data[i][22], data[i][24]] for i in range(len(data)) if int(data[i][21])>1000 ] #krathseis
    
    
    report_data = []#[['', '', '', '', '']]
    
    report_data_header = [['ΕΙΔΙΚΩΝ ΠΑΘΗΣΕΩΝ',  data[0][2], 'Σελ 1'],
                          ['Νοσοκομείο', '', 'Μηνός'],
                          ['01 03040100', _P('<u>ΑΝΑΛΥΣΗ ΜΙΣΘΟΔΟΣΙΑΣ</u>'), 'Μήνα']]
    
    report_data_header_table = Table(report_data_header, colWidths=[187, 186, 187], rowHeights=20)
    report_data_header_table.setStyle(TableStyle([('GRID',(0,0),(-1,-1), 0.25, colors.white),
                                                  ('FONT', (0,0),(-1,-1), 'LinLibertine', 10),
                                                  ('LEFTPADDING', (0,0),(2,-1), 0),
                                                  ('ALIGN', (2,0),(2,0), 'RIGHT')]))
    report_data.append([report_data_header_table])
 
    report_data_header = [['Α.Μ.', 'Επώνυμο', 'Όνομα', 'Ειδικότητα', 'Κατηγορία', 'Βαθμ', 'Κλιμ', 'Ημέρες'],
                          [unicode(employee_id), data[0][4], data[0][5], data[0][8], data[0][16], '', data[0][19], data[0][9]]]
    
    report_data_header_table = Table(report_data_header, colWidths=[35, 90, 90, 90, 120, 50, 35, 50], rowHeights=20)
    report_data_header_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1), 0.25, colors.white),
                                                  ('LEFTPADDING', (0,0),(1,-1), 0),
                                                  ('FONT', (0,0),(-1,-1), 'LinLibertine', 10)]))
    report_data.append([report_data_header_table])
    
    #report_data.extend(report_data_header)
    
    report_data_extra = [['ΑΠΟΔΟΧΕΣ', 'ΠΟΣΟ', 'ΚΡΑΤΗΣΕΙΣ', 'ΠΟΣΟ', 'ΗμΑσφ ' + data[0][10]]]
    report_data.extend(report_data_extra)
    
    sum_kr = 0;
    sum_ap = 0;
    
    if len(apodoxes)<len(krathseis):
        cmn = len(apodoxes)
        ovf = 1
    else:
        cmn = len(krathseis)
        ovf = 0

    ap_kr = [[apodoxes[i][0], apodoxes[i][1], krathseis[i][0], krathseis[i][1]] for i in range(cmn)]
    report_data.extend(ap_kr)
    for i in range(cmn):
        sum_ap += float(apodoxes[i][1]);
        sum_kr += float(krathseis[i][1]);        
    
    if ovf == 1:
        ap_kr_ovf = [['', '', krathseis[i][0], krathseis[i][1]] for i in range(len(apodoxes), len(krathseis))]
        for i in range(len(apodoxes), len(krathseis)):
            sum_kr += float(krathseis[i][1]);        
    if ovf == 0:
        ap_kr_ovf = [[apodoxes[i][0], apodoxes[i][1], '', ''] for i in range(len(krathseis), len(apodoxes))]
        for i in range(len(krathseis), len(apodoxes)):
            sum_ap += float(apodoxes[i][1]);
    report_data.extend(ap_kr_ovf)
    
    report_data_extra = [['', '', '', ''],
                         ['ΣΥΝΟΛΟ', unicode(sum_ap), 'ΣΥΝΟΛΟ', unicode(sum_kr)]]
    report_data.extend(report_data_extra)
    
    report_data_bottom = [['Καθ.Πληρωτ.Μηνός', "Α' 15ΗΜΕΡΟ", "Β' 15ΗΜΕΡΟ"],
                         [data[0][25], data[0][26], data[0][26], data[0][26], 'Λογ/σμός 014'],
                         ['Ένταλμα :', 'Ιατροί ΕΣΥ Μόνιμοι', '(0110)', '(Μόνιμοι)', 'Α/Α: 1']]
    report_data_bottom_table = Table(report_data_bottom, colWidths=[112,112,112,112,112], rowHeights=20)
    report_data_bottom_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1), 0.25, colors.white),
                                                  ('FONT', (0,0),(-1,-1), 'LinLibertine', 10),
                                                  ('LEFTPADDING', (-6,0),(-1,-1), 0)]))
    report_data.append([report_data_bottom_table])
    
    report_data_table = Table(report_data, colWidths=[164,60,164,60,112], rowHeights=20)
    report_data_table._argH[-1]=80
    report_data_table._argH[0]=63 # 60 + 3 toppadding
    report_data_table._argH[1]=40
    report_data_table.setStyle(TableStyle([('BOX',(0,0),(-1,-1), 0.25, colors.white),
                                           ('FONT', (0,0),(-1,-1), 'LinLibertine', 10),
                                           ('LEFTPADDING', (0, 0),(-1,-1), 0),
                                           ('RIGHTPADDING', (1,0),(2,-1), 0)]))
    """
    data= [['00', '01', '02', '03', '04'],
    ['10', '11', '12', '13', '14'],
    ['20', '21', '22', '23', '24'],
    ['30', '31', '32', '33', '34']]
    """
    """    
    elements.append(Spacer(0*inch, 1.8*inch))
    elements.append(Indenter(left= 3.4*inch))
    elements.append(s)
    """
    # write the document to disk
    elements.append(report_data_table)
    doc.build(elements)
    
    #canvas = doc.canv
    #canvas.setFont('LinLibertine', 32)

    return response

def _P(data):
    return Paragraph(data, style=style_sheet["TestStyle"])

def report2(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

import csv

def some_view(request, employee_id=138):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=somefilename.csv'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response

def report3(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    doc = SimpleDocTemplate(response, pagesize=letter)
    # container for the 'Flowable' objects
    elements = []
 
    data= [['00', '01', '02', '03', '04'],
    ['10', '11', '12', '13', '14'],
    ['20', '21', '22', '23', '24'],
    ['30', '31', '32', '33', '34']]
    t=Table(data)
    t.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.green), ('TEXTCOLOR',(0,0),(1,-1),colors.red)]))
    elements.append(t)
    # write the document to disk
    doc.build(elements)

    return response

def report4(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
 
    doc = SimpleDocTemplate(response, pagesize=letter)
    # container for the 'Flowable' objects
    elements = []
 
    styleSheet = getSampleStyleSheet()
 
    I = Image('replogo.jpeg')
    I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
    I.drawWidth = 1.25*inch
    P0 = Paragraph('''
                   <b>A pa<font color=red>r</font>a<i>graph</i></b>
                   <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
        <para align=center spaceb=3>The <b>ReportLab Left
        <font color=red>Logo</font></b>
        Image</para>''',
        styleSheet["BodyText"])
    data= [['A', 'B', 'C', P0, 'D'],
           ['00', '01', '02', [I,P], '04'],
           ['10', '11', '12', [P,I], '14'],
           ['20', '21', '22', '23', '24'],
           ['30', '31', '32', '33', '34']]
 
    t=Table(data,style=[('GRID',(1,1),(-2,-2),1,colors.green),
                        ('BOX',(0,0),(1,-1),2,colors.red),
                        ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                        ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                        ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                        ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                        ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                        ('BOX',(0,0),(-1,-1),2,colors.black),
                        ('GRID',(0,0),(-1,-1),0.5,colors.black),
                        ('VALIGN',(3,0),(3,0),'BOTTOM'),
                        ('BACKGROUND',(3,0),(3,0),colors.limegreen),
                        ('BACKGROUND',(3,1),(3,1),colors.khaki),
                        ('ALIGN',(3,1),(3,1),'CENTER'),
                        ('BACKGROUND',(3,2),(3,2),colors.beige),
                        ('ALIGN',(3,2),(3,2),'LEFT'),
    ])
    t._argW[3]=1.5*inch
 
    elements.append(t)
    # write the document to disk
    doc.build(elements)
    
    return response

#Example code using the cStringIO library as a temporary holding place for your PDF file. 
#This library provides a file-like object interface that is particularly efficient.
"""
# Fall back to StringIO in environments where cStringIO is not available
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    buffer = StringIO()

    # Create the PDF object, using the StringIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the StringIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
"""