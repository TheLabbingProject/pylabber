import os

from django.db import models
from smb.smb_structs import OperationFailure
from .smb_directory import SMBDirectory

# from django.urls import reverse


class SMBFileManager(models.Manager):
    def update_smb(self, instance: SMBDirectory):
        files = instance.list_all_files()
        for f in files:
            found = instance.file_set.filter(path=f).first()
            if not found:
                new_file = SMBFile(path=f, source=instance)
                new_file.save()


class SMBFile(models.Model):
    path = models.CharField(max_length=500, blank=False)
    is_archived = models.BooleanField(default=False)
    source = models.ForeignKey(
        SMBDirectory,
        related_name='file_set',
        on_delete=models.PROTECT,
    )

    objects = SMBFileManager()

    class Meta:
        verbose_name_plural = "SMB Files"

    @property
    def dir_name(self):
        return os.path.dirname(self.path)

    @property
    def is_available(self):
        conn = self.source.connect()
        try:
            dir_files = conn.listPath(self.source.share_name, self.dir_name)
        except OperationFailure:
            return False
        file_names = [f.filename for f in dir_files]
        if os.path.basename(self.path) in file_names:
            return True
        return False

    # def get_absolute_url(self):
    #     return reverse('smb_file_detail', args=[str(self.id)])
