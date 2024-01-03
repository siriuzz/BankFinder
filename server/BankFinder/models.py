from django.db import models

class bank(models.Model):
    bank_id=models.AutoField(primary_key=True, unique=True)
    bank_name = models.CharField(max_length=250, null=False, default="-")
    website = models.CharField(max_length=250,null=False, default="N/A")
    contact_number = models.CharField(max_length=15,null=False, default="000-000-0000")
    logo = models.ImageField(upload_to="banks/", default="default/default_bank.png")
    
    def __str__(self):
        return self.bank_name
    pass

class branch(models.Model):
    bank_id=models.ForeignKey(bank, on_delete=models.CASCADE,db_column='bank_id',related_name='branches')
    branch_id = models.AutoField(primary_key=True, unique=True)
    branch_name = models.CharField(max_length=200, null=False)
    location = models.CharField(max_length=200, null=False)
    branch_contact_number = models.CharField(max_length=15, null=False)
    opening_hour = models.TimeField(null=False)
    closing_hour = models.TimeField(null=False)
    
    def __str__(self):
        return str(self.bank_id)+ " " +self.branch_name

class source_currency(models.Model):
    source_currency_id = models.AutoField(primary_key=True,unique=True)
    currency_code = models.CharField(max_length=3,null=False)
    currency_name = models.CharField(max_length=150,null=False)
    pass
    
class target_currency(models.Model):
    target_currency_id = models.AutoField(primary_key=True,unique=True)
    currency_code = models.CharField(max_length=3,null=False)
    currency_name = models.CharField(max_length=150,null=False)
    pass

class exchange_rate(models.Model):
    exchange_rate_id = models.AutoField(primary_key=True, unique=True)
    source_currency_id = models.ForeignKey(source_currency, on_delete=models.CASCADE,null=False, db_column='source_currency_id')
    target_currency_id = models.ForeignKey(target_currency, on_delete=models.CASCADE,null=False, db_column='target_currency_id')
    last_update = models.DateTimeField(null=False)
    def __str__(self):
        return self
    pass

class bank_exchange_rate(models.Model):
    bank_id=models.ForeignKey(bank, on_delete=models.CASCADE, db_column='bank_id')
    exchange_rate_id = models.ForeignKey(exchange_rate,primary_key=True, on_delete=models.CASCADE, db_column='exchange_rate_id')
    rate = models.FloatField(null=False)
    last_update = models.DateTimeField(null=False)