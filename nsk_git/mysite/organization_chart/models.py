from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Chart(MPTTModel):
        title = models.CharField(max_length=30)
        description = models.CharField(max_length=60, blank=True)
        code = models.BigIntegerField(unique=True)
        parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

        def __unicode__(self):
                return u'%s - %s' % (self.title, self.code)
            
        def get_code_list(self):
            leaves = self.get_leafnodes(include_self=True)
            leaf_codes = [leaf.code for leaf in leaves]
            return leaf_codes
                            
        class MPTTMeta:
                order_insertion_by = ['code']