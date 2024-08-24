from django.db import models


class BaseTimeStampSoftDeleteModel(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        
    def delete(self):
        self.is_deleted = True
        self.save()
