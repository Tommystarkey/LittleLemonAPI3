# Generated by Django 4.2.8 on 2023-12-19 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0004_orderitem"),
    ]

    operations = [
        migrations.RenameField(
            model_name="menuitem",
            old_name="fetured",
            new_name="featured",
        ),
    ]
