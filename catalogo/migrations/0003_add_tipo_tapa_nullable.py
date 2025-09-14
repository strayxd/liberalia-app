from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('catalogo', '0002_idioma_moneda_pais_tipotapa_libroficha_alto_cm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='libroficha',
            name='tipo_tapa',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='catalogo.tipotapa',
            ),
        ),
    ]
