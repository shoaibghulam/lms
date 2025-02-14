# Generated by Django 3.0.4 on 2021-01-09 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('faculty', '0001_initial'),
        ('UniversityApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam_result',
            name='Batch_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.Batch'),
        ),
        migrations.AddField(
            model_name='exam_result',
            name='Course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Course'),
        ),
        migrations.AddField(
            model_name='exam_result',
            name='Department_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Department'),
        ),
        migrations.AddField(
            model_name='exam_result',
            name='InstructerId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Instructor'),
        ),
        migrations.AddField(
            model_name='exam_result',
            name='Semester_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty.Semester'),
        ),
        migrations.AddField(
            model_name='exam_result',
            name='Student_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student_Profile'),
        ),
        migrations.AddField(
            model_name='exam_result',
            name='branchId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityBranch'),
        ),
        migrations.AddField(
            model_name='exam_result',
            name='uniId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityAccount'),
        ),
        migrations.AddField(
            model_name='department',
            name='Instructor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Instructor'),
        ),
        migrations.AddField(
            model_name='department',
            name='branchId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityBranch'),
        ),
        migrations.AddField(
            model_name='department',
            name='uniId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityAccount'),
        ),
        migrations.AddField(
            model_name='coursevideos',
            name='CourseId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Course'),
        ),
        migrations.AddField(
            model_name='coursevideos',
            name='InstructerId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Instructor'),
        ),
        migrations.AddField(
            model_name='coursevideos',
            name='branchId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityBranch'),
        ),
        migrations.AddField(
            model_name='coursevideos',
            name='uniId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityAccount'),
        ),
        migrations.AddField(
            model_name='course',
            name='Department_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Department'),
        ),
        migrations.AddField(
            model_name='course',
            name='Instructor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='Semester_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Semester'),
        ),
        migrations.AddField(
            model_name='course',
            name='branchId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityBranch'),
        ),
        migrations.AddField(
            model_name='course',
            name='uniId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityAccount'),
        ),
        migrations.AddField(
            model_name='assigmentmodel',
            name='Course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Course'),
        ),
        migrations.AddField(
            model_name='assigmentmodel',
            name='Instructor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.Instructor'),
        ),
        migrations.AddField(
            model_name='assigmentmodel',
            name='branchId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityBranch'),
        ),
        migrations.AddField(
            model_name='assigmentmodel',
            name='uniId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniversityApp.UniversityAccount'),
        ),
    ]
