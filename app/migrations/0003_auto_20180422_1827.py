# Generated by Django 2.0.4 on 2018-04-22 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180422_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='product_image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('path', models.ImageField(upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='main_picture',
            field=models.ImageField(default='img/logo.png', upload_to=''),
        ),
        migrations.AddField(
            model_name='product_image',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Product'),
        ),
    ]