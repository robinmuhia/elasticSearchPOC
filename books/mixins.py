from django.db import models

class GenericMixin(models.Model):
    """Generic mixin to be inherited by all models."""
    id = models.AutoField(primary_key=True,editable=False,unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-updated_at","-created_at")