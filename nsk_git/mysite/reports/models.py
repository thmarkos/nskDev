from django.db import models

class Report(models.Model):
    mh_idr1 = models.IntegerField()
    mh_org = models.CharField(max_length=8)
    do_orgn = models.CharField(max_length=30)
    em_empl = models.IntegerField()
    em_epon = models.CharField(max_length=20)
    em_onoma = models.CharField(max_length=15)
    ProDed = models.CharField(max_length=8)
    eidik_cd = models.IntegerField()
    eidik_nm = models.CharField(max_length=20)
    MH_HMPLHR = models.IntegerField()
    MH_HMASF = models.IntegerField()
    MH_MHNAS_E = models.IntegerField()
    MH_ETOS_E = models.IntegerField()
    MH_MHNAS = models.IntegerField()
    MH_ETOS = models.IntegerField()
    MH_KLIM = models.IntegerField()
    MIS = models.CharField(max_length=2)
    hi_apkra = models.IntegerField()
    apkra_nm = models.CharField(max_length=20)
    poso = models.IntegerField()
    MH_PLHR = models.IntegerField()
    
    def __unicode__(self):
        return u'%s %s' % (self.em_onoma, self.em_epon)