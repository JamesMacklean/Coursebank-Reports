from django.db import models

class CountReport(models.Model):
    """
    Model to store periodic count report data
    """
    created = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=255)
    count_value = models.IntegerField()
    meta = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        display_name = "{}: {}".format(self.key, self.count_value)
        return display_name
