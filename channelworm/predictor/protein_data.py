"""
Script for fetching protein info and storing in db

"""

import os, sys
import time
import django
from Bio import Entrez, SeqIO

sys.path.append("../../channelworm")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web_app.settings"
)
django.setup()

from ion_channel.models import IonChannel, Protein

chan_prots = IonChannel.objects.values_list('id','proteins')
print(chan_prots)

for channel,proteins in chan_prots:
    for protein in proteins.split('; '):
        print '\n'
        print('channel id:%s'%channel) # channel id
        print('protein:%s'%protein) # protein name
        protein_str = '"'+protein+'"'
        handle = Entrez.esearch(db='protein', term=protein_str) # (17554770)
        records = Entrez.read(handle)
        # print(records)
        print('count:%i'%int(records["Count"]))
        print('records:%s'%records["IdList"])
        print('first gi:%s'%records["IdList"][0]) # gi

        # for i in range(int(records["Count"])):
        handle = Entrez.efetch(db="protein", id=records["IdList"][0], rettype="fasta")
        handle2= Entrez.efetch(db="protein", id=records["IdList"][0], rettype="fasta")
        # print handle.read()
        rec = list(SeqIO.parse(handle, "fasta"))
        print('rec:\n%s'%rec)
        record = rec[0]
        # for record in SeqIO.parse(handle, "fasta"):
        print('record:%s'%record)
        print('record id:%s'%record.id)
        print('record description:%s'%record.description)
        print('record sequence:%s'%record.seq) # protein sequence

        fasta = str(handle2.read())
        print('fasta:\n%s'%fasta)

        handle.close()
        handle2.close()

        if Protein.objects.filter(name=protein).exists() is False:

            print 'Going to add to database...'
            prot_model = Protein(name = protein,
                                 ion_channel_id = channel,
                                 sequence = record.seq,
                                 fasta = fasta,
                                 gi = records["IdList"][0])
            print prot_model
            prot_model.save()

        else:
            print 'Already exist'

        # print(handle.readline().strip())
        # handle = Entrez.efetch(db="protein", id=records["IdList"][0], rettype="fasta", retmode="xml")
        # record = Entrez.read(handle)
        # print(record)
        # print(record[0]['TSeq_accver'])
        # if record[0]['TSeq_orgname'] == 'Caenorhabditis elegans':
        #     print(record[0]['TSeq_sequence'])

        time.sleep(2)

# 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term="SLO-2, isoform a"&db=protein&tool=biopython&email=vahidghayoomi%40gmail.com'
# 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term=CE23997&db=protein&tool=biopython&email=vahidghayoomi%40gmail.com'
# 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?rettype=fasta&tool=biopython&db=protein&id=17554770&email=vahidghayoomi%40gmail.com'

# >gi|3875659|emb|CAA92115.1| SLO-2, isoform a [Caenorhabditis elegans]
# >gi|71986730|ref|NP_001024527.1| SLO-2, isoform a [Caenorhabditis elegans]

