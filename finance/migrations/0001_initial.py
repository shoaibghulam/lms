# Generated by Django 3.0.4 on 2021-01-09 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('faculty', '0002_auto_20210109_1835'),
        ('UniversityApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherSalary',
            fields=[
                ('SalaryId', models.AutoField(primary_key=True, serialize=False)),
                ('IssueDate', models.DateTimeField(auto_now_add=True)),
                ('Salaryamount', models.IntegerField(default=0)),
                ('Salaryteacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Instructor')),
                ('branchId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityBranch')),
                ('uniId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityAccount')),
            ],
        ),
        migrations.CreateModel(
            name='StudetFee',
            fields=[
                ('FeeId', models.AutoField(primary_key=True, serialize=False)),
                ('IssueDate', models.DateTimeField(auto_now_add=True)),
                ('FeeAmount', models.IntegerField(default=0)),
                ('StudentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student_Profile')),
                ('branchId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityBranch')),
                ('uniId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityAccount')),
            ],
        ),
        migrations.CreateModel(
            name='FianceUser',
            fields=[
                ('Fid', models.AutoField(primary_key=True, serialize=False)),
                ('FirstName', models.CharField(default='First Name', max_length=60)),
                ('LastName', models.CharField(default='Last Name', max_length=60)),
                ('Email', models.CharField(default='youremail@gmail.com', max_length=100)),
                ('Password', models.TextField(max_length=1300)),
                ('branchId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityBranch')),
                ('uniId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityAccount')),
            ],
        ),
    ]
