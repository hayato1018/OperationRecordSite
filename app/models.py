from django.db import models

class MasterData(models.Model):
    project_name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=100)
    phase_number = models.CharField(max_length=100)
    search_text = models.CharField(max_length=100)
    inhouse_work_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project_number} - {self.phase_number} - {self.search_text}"
