from django.db import models

class InternalUsers(models.Model):
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=16)
    is_admin = models.BooleanField(default=False)
    
class Project(models.Model):
    name = models.CharField(max_length=80)
    project_description = models.CharField(max_length=80)
    project_manager = models.ForeignKey(InternalUsers, on_delete=models.CASCADE, default=0)
    project_manager_email = models.CharField(max_length=80, default="")

class Cluster(models.Model):
    name = models.CharField(max_length=80)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
    cluster_type = models.CharField(max_length=16, default="")
    cluster_location = models.CharField(max_length=80, default="")

class Contact(models.Model):
    STATUS_PERNIKAHAN = [
        ("sm", "Sudah Menikah"),
        ("bm", "Belum Menikah"),
        ("cn", "Cerai Nikah"),
        ("cm", "Cerai Mati"),
    ]
    name = models.CharField(max_length=80, default="Default Name")
    pendapatan_per_bulan = models.IntegerField()
    pendapatan_lain_lain = models.IntegerField()
    status_pernikahan = models.CharField(max_length=2, choices=STATUS_PERNIKAHAN, default="bm")
    jumlah_anak = models.IntegerField()
    nomor_telepon = models.CharField(max_length=20)
    email = models.CharField(max_length=80)

class Sales(models.Model):
    name = models.CharField(max_length=80)
    projects = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, null=True)
    contacts = models.ForeignKey(Contact, on_delete=models.CASCADE, default=0)
    project_manager = models.ForeignKey(InternalUsers, on_delete=models.CASCADE, default=0)
    project_manager_email = models.CharField(max_length=80, default="")
    lama_cicil = models.IntegerField(default=0)
    down_payment = models.IntegerField(default=0)
    project_type = models.CharField(max_length=16, default="")
    project_location = models.CharField(max_length=80, default="")
    sales_total = models.IntegerField(default=0)

class SalesPaymentDetails(models.Model):
    name = models.CharField(max_length=80)
    sales_ref = models.ForeignKey(Sales, on_delete=models.CASCADE)
    description = models.CharField(max_length=160, default="")
    jumlah_cicil = models.IntegerField(default=0)
    tahun_cicil = models.CharField(max_length=16, default="")
    bulan_cicil = models.CharField(max_length=16, default="")

