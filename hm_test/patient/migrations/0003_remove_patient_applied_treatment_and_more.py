# Generated by Django 4.2.7 on 2024-04-02 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0001_initial'),
        ('patient', '0002_remove_patient_assigned_treatment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='applied_treatment',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='recommended_treatment',
        ),
        migrations.AddField(
            model_name='patient',
            name='applied_treatment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='applied_treatment', to='treatment.treatment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='recommended_treatment',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='recommended_treatment', to='treatment.treatment'),
            preserve_default=False,
        ),
    ]
