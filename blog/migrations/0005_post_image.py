# Generated by Django 4.0.4 on 2022-07-29 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/', verbose_name='Post image'),
        ),
    ]
