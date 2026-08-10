import django.db.models.deletion
from django.db import migrations, models


def criar_organizacao_padrao(apps, schema_editor):
    Organizacao = apps.get_model('empresas', 'Organizacao')
    Empresa = apps.get_model('empresas', 'Empresa')

    organizacao, _ = Organizacao.objects.get_or_create(
        nome='Bay Software',
        defaults={
            'email': '',
            'telefone_whatsapp': '',
            'documento': '',
            'ativa': True,
        },
    )

    Empresa.objects.filter(organizacao__isnull=True).update(organizacao=organizacao)


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0003_empresa_plano_tarefas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organizacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('documento', models.CharField(blank=True, max_length=18)),
                ('email', models.EmailField(blank=True, max_length=150)),
                ('telefone_whatsapp', models.CharField(blank=True, max_length=20)),
                ('ativa', models.BooleanField(default=True)),
                ('observacao', models.TextField(blank=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Organizacao',
                'verbose_name_plural': 'Organizacoes',
                'ordering': ['nome'],
            },
        ),
        migrations.AddField(
            model_name='empresa',
            name='organizacao',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='empresas',
                to='empresas.organizacao',
            ),
        ),
        migrations.RunPython(criar_organizacao_padrao, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='empresa',
            name='organizacao',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='empresas',
                to='empresas.organizacao',
            ),
        ),
    ]
