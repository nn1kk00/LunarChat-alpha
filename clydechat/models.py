from django.db import models

# Create your models here.

class User(models.Model):
    uid = models.IntegerField(help_text="Введите UID юзера", verbose_name="UID юзера", blank=True, null=True)
    name = models.CharField(max_length=18, help_text="Введите логин", verbose_name="Логин юзера", blank=True, null=True)
    role = models.IntegerField(help_text="Введите роль юзера (1-верифицирован, 2-админ)", verbose_name="Роль юзера", blank=True, null=True)
    mute = models.IntegerField(help_text="Введите статус блокировки голоса бзера (0-нет, 1-да)", verbose_name="Блокировка голоса юзера", default=0)
    block = models.IntegerField(help_text="Введите статус блокировки юзера (0-нет, 1-да)", verbose_name="Статус блокировки юзера", default=0)
    last_ip = models.GenericIPAddressField(help_text="Введите последний айпи юзера", verbose_name="IP юзера", blank=True, null=True)
    date_of_create = models.DateField(help_text="Введите дату создания юзера", verbose_name="Дата создания юзера", blank=True, null=True)
    password_hash = models.CharField(max_length=256, blank=True, null=True)
    avatar_status = models.IntegerField(default=0)
    def __str__(self):
        return self.name or ""

class BannedUser(models.Model):
    name = models.ForeignKey("User", on_delete=models.CASCADE, help_text="Имя нарушителя", verbose_name="Имя нарушителя", blank=True, null=True)
    end_date = models.DateField(help_text="Дата окончания блокировки", verbose_name="Дата окончания блокировки юзера", blank=True, null=True)
    def __str__(self):
        return str(self.name)

class BannedIP(models.Model):
    ip = models.ForeignKey("User", on_delete=models.CASCADE, help_text="IP нарушителя", verbose_name="IP нарушителя", blank=True, null=True)
    end_date = models.DateField(help_text="Дата окончания блокировки", verbose_name="Дата окончания блокировки юзера", blank=True, null=True)
    def __str__(self):
        return str(self.ip)

class ActiveSession(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    username = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.ip_address} - {self.username}"

class BannedIPAddress(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    def __str__(self):
        return self.ip_address

class NtIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    def __str__(self):
        return self.ip_address

class GlobalSetting(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.key}: {self.value}"