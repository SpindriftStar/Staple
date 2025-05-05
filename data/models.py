from django.db import models

class Host(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    manufacturer = models.CharField(max_length = 100)
    model = models.CharField(max_length = 100)
    series = models.CharField(max_length = 100)
    status = models.BooleanField()
    create_time = models.DateTimeField(auto_now_add = True)
    config = models.CharField(max_length = 100)

    def __str__(self):
        return self.name
    
class Interface(models.Model):
    description = models.CharField(max_length = 100)
    host_id = models.ForeignKey(Host, on_delete = models.CASCADE)
    ip = models.GenericIPAddressField(protocol = 'both')
    port = models.SmallIntegerField()
    status = models.BooleanField()

    def __str__(self):
        return self.description
    
class Auth(models.Model):
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    host_id = models.ForeignKey(Host, on_delete = models.CASCADE)

    def __str__(self):
        return self.username
    
class Template(models.Model):
    description = models.CharField(max_length = 100)
    file = models.CharField(max_length = 100)

    def __str__(self):
        return self.description
    
class Instance(models.Model):
    host_id = models.ForeignKey(Host, on_delete = models.CASCADE)
    template_id = models.ForeignKey(Template, on_delete = models.DO_NOTHING)
    interface_id = models.ForeignKey(Interface, on_delete = models.DO_NOTHING)
    auth_id = models.ForeignKey(Auth, on_delete = models.DO_NOTHING)
    status = models.BooleanField()

    def __str__(self):
        return 'Instance'