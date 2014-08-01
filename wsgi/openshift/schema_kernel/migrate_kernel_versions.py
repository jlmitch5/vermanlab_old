from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [("migrations", "0001_initial")]

    operations = [
        migrations.AddField("KernelVersion", "pretty_kernel_version_name", models.CharField(max_length=100, default="kernel version")),
    ]