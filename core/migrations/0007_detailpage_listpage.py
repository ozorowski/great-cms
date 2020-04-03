# Generated by Django 2.2.10 on 2020-04-03 14:03

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail_personalisation.blocks
import wagtail_personalisation.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('core', '0006_auto_20200323_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_personalisation.models.PersonalisablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='ListPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([('body', wagtail.core.blocks.StructBlock([('segment', wagtail.core.blocks.ChoiceBlock(choices=wagtail_personalisation.blocks.list_segment_choices, help_text='Only show this content block for users in this segment', label='Personalisation segment', required=False)), ('paragraph', wagtail.core.blocks.RichTextBlock())], icon='pilcrow', template='core/personalised_page_struct_block.html'))])),
                ('custom_template', models.CharField(blank=True, max_length=255, verbose_name='Template')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail_personalisation.models.PersonalisablePageMixin, 'wagtailcore.page'),
        ),
    ]
