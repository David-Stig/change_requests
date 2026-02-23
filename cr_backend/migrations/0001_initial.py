from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='role', to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('ministry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='systems', to='cr_backend.ministry')),
                ('owners', models.ManyToManyField(blank=True, related_name='owned_systems', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChangeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('change_category', models.CharField(choices=[('bugfix', 'Bugfix'), ('feature', 'Feature'), ('security', 'Security'), ('maintenance', 'Maintenance')], max_length=32)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('implementing', 'Implementing'), ('completed', 'Completed')], default='draft', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='change_requests', to=settings.AUTH_USER_MODEL)),
                ('ministry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='change_requests', to='cr_backend.ministry')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='change_requests', to='cr_backend.system')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeRequestLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('approval', 'Approval'), ('rejection', 'Rejection'), ('implementation', 'Implementation'), ('completion', 'Completion')], max_length=32)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('change_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='cr_backend.changerequest')),
                ('performed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='change_request_actions', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ('-timestamp',)},
        ),
    ]
