# Generated by Django 2.2.7 on 2020-10-10 17:54

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal_title', models.CharField(max_length=60)),
                ('journal_details', ckeditor.fields.RichTextField(default='enter something for details')),
                ('jornal_author', models.CharField(max_length=30)),
                ('publication_year', models.DateField()),
                ('journal_category', models.CharField(choices=[('Data mining', 'Data mining'), ('Science', 'Science'), ('Technology', 'Technology'), ('Artificial Intelligence', 'Artificial Intelligence'), ('Machine Learning', 'Machine Learning')], max_length=40)),
                ('document_type', models.CharField(choices=[('Pdf', 'Pdf'), ('Doc', 'Doc')], max_length=10)),
                ('jornal_cover', models.ImageField(upload_to='journal/')),
                ('journal_type', models.CharField(choices=[('Free', 'Free'), ('Paid', 'Paid')], max_length=10)),
                ('price', models.PositiveIntegerField(blank=True, default=0.0)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('journal_file', models.FileField(upload_to='journal_file/')),
                ('download_count', models.IntegerField(blank=True, default=0)),
                ('access', models.ManyToManyField(blank=True, related_name='journal_access', to=settings.AUTH_USER_MODEL)),
                ('journal_view', models.ManyToManyField(blank=True, related_name='journal_view', to=settings.AUTH_USER_MODEL)),
                ('post_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequestWithdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paypal', models.EmailField(max_length=20, null=True)),
                ('payment', models.FloatField(default=0)),
                ('request_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JournalPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.FloatField(default=0.0)),
                ('jouenal_owner', models.ForeignKey(on_delete=django.db.models.expressions.Case, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JournalOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('journal', models.ForeignKey(blank=True, max_length=100, null=True, on_delete=False, to='journal.Journal')),
            ],
        ),
        migrations.CreateModel(
            name='JournalComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=160)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.Journal')),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='journal.JournalComment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RatedJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratting_r', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('journal_r', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.Journal')),
                ('user_r', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_r', 'journal_r')},
                'index_together': {('user_r', 'journal_r')},
            },
        ),
    ]
