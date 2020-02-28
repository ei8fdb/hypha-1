# Generated by Django 2.0.13 on 2019-05-21 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_metacategory'),
        ('funds', '0064_group_toggle_end_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationsubmission',
            name='meta_categories',
            field=models.ManyToManyField(blank=True, related_name='submissions', to='categories.MetaCategory'),
        ),
    ]