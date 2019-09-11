# Generated by Django 2.2.4 on 2019-09-10 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('institutions', '0003_auto_20190821_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutiondetailpage',
            name='translated_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
    ]
