from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Genre(MPTTModel):
		name = models.CharField(max_length=50, unique=True)
		parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

		def __unicode__(self):
				return u'%s' % self.name
				
		class MPTTMeta:
				order_insertion_by = ['name']


class Tree(models.Model):
		#user = models.ForeignKey(Employee)
		json_string = models.CharField(max_length = 10000, default = "empty")
		
		#def save(self, *args, **kwargs):
				#self.slug = slugify(self.phone)
				#super(Communication, self).save(*args, **kwargs) # Call the "real" save() method.
				#do_something_else()
						
		def __unicode__(self):
				return self.json_string
				
		#@models.permalink
		#def get_absolute_url(self):
				#return ('show_communication', (), { 'communication_slug': self.slug })
