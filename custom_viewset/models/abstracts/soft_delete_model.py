"""
Self-managed soft-delete logic, taken directly from the
source code of django-softdelete==0.9.21 package.

Since the related package is already too old,
and upgrading to newest version introduces breaking changes,
we decided to self-manage the soft-delete logic.
"""

from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.query.QuerySet):
    """
    Custom queryset that enables the main soft-delete function. This also enables hard-delete
    """

    def delete(self):
        return self.update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()


class SoftDeleteManager(models.Manager):
    """
    Custom model manager that returns only non-deleted items `(is_deleted=False)`
    """

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, self._db).filter(is_deleted=False)


class DeletedQuerySet(models.query.QuerySet):
    """
    Custom queryset that enables restore function for deleted items
    """

    def restore(self, *args, **kwargs):
        qs = self.filter(*args, **kwargs)
        qs.update(is_deleted=False, deleted_at=None)


class DeletedManager(models.Manager):
    """
    Custom model manager that returns only deleted items `(is_deleted=True)`
    """

    def get_queryset(self):
        return DeletedQuerySet(self.model, self._db).filter(is_deleted=True)


class GlobalManager(models.Manager):
    """
    Alias of django's default model manager, for readability purpose
    """

    pass


class SoftDeleteModel(models.Model):
    """
    Abstract model that wraps soft-delete functionality.

    Note:
    - MUST be used as the FIRST inherritance
    """

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()  # non-deleted objects (`is_deleted=False`)
    deleted_objects = DeletedManager()  # deleted objects (is_deleted=True)
    global_objects = GlobalManager()  # non-deleted and deleted objects

    class Meta:
        abstract = True

    def delete(self, cascade=False, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
        self.after_delete()
        if cascade:
            self.delete_related_objects()

    def restore(self, cascade=False):
        self.is_deleted = False
        self.deleted_at = None
        self.save()
        self.after_restore()
        if cascade:
            self.restore_related_objects()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def get_related_objects(self):
        raise NotImplementedError(
            "Subclasses must implement their own `get_related_objects` if using soft-delete cascade"
        )

    def delete_related_objects(self):
        for obj in self.get_related_objects():
            obj.delete()

    def restore_related_objects(self):
        for obj in self.get_related_objects():
            obj.restore()

    def after_delete(self):
        # subclasses can implement their own after_delete function as needed
        pass

    def after_restore(self):
        # subclasses can implement their own after_restore function as needed
        pass
