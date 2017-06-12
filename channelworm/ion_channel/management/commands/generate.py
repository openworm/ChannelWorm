from django.core.management.base import BaseCommand, CommandError
import csv
import sys
from channelworm.ion_channel.models import IonChannel


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        field_names = ['channel_name', 'gene_name',
                       'gene_WB_ID', 'expression_pattern', 'description']
        # field_names = ['channel_name', 'description', 'description_evidences, 'channel_type', 'channel_subtype', 'ion_type',
        #               'ligand_type', 'gene_name', 'gene_WB_ID', 'gene_class', 'proteins', 'expression_pattern', 'expression_evidences', 'last_update']
        with open('IonChannel.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(field_names)
            for obj in IonChannel.objects.all():
                r = []
                for f in field_names:
                    r.append(unicode(getattr(obj, f)).encode('utf-8'))
                writer.writerow(r)
