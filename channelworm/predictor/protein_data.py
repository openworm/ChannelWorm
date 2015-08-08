"""
Script for fetching protein info and storing in db

"""

import os, sys
import time
import django
from Bio import Entrez, SeqIO
Entrez.email = 'vahidghayoomi@gmail.com'
import requests
import operator

sys.path.append("../../channelworm")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web_app.settings"
)
django.setup()

from ion_channel.models import IonChannel, Protein

wb_pro_url = 'https://www.wormbase.org/search/autocomplete/protein?term=' # slo-2

chan_gene = IonChannel.objects.values_list('id','gene_name')
print(chan_gene)
headers = {'content-type': 'application/json'}

prots = {}
for channel,gene in chan_gene:
    print '\n'
    print gene
    prots[gene] = {}
    r = requests.get(wb_pro_url + gene, headers=headers)
    # print(r.json())

    j = r.json()
    for resp in j:
        prot_name = resp['label']
        prot_id = resp['id']

        print prot_id
        print prot_name

        if ('WP:' in prot_id) and (gene.lower() == prot_name.lower() or (gene.lower()+',' in prot_name.lower())):

            prots[gene][prot_id] = prot_name

            print '\n'
            print('channel id:%s'%channel) # channel id
            print('protein:%s'%prot_name) # protein name
            protein_str = '"'+prot_name+'"'
            if Protein.objects.filter(name=prot_name).exists() is False:
                try:
                    handle = Entrez.esearch(db='protein', term=protein_str) # (17554770)
                    records = Entrez.read(handle)
                except:
                    continue
                    # print(records)
                print('count:%i'%int(records["Count"]))

                if len(records["IdList"]) > 0:
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

                    if Protein.objects.filter(name=prot_name).exists() is False:

                        print 'Going to add to database...'
                        prot_model = Protein(name = prot_name,
                                             ion_channel_id = channel,
                                             sequence = record.seq,
                                             fasta = fasta,
                                             gi = records["IdList"][0],
                                             wb_ID=prot_id)
                        prot_model.save()
                        print prot_model

                    else:
                        print 'Already exist'
                        Protein.objects.filter(name=prot_name).update(wb_ID=prot_id)

                else:
                    print('Could not find entry for protein:%s'%prot_name)
                    Protein.objects.filter(name=prot_name).update(wb_ID=prot_id)

                time.sleep(2)

            print('Before sort:')
            print prots[gene]
            prots_s = sorted(prots[gene].items(), key=operator.itemgetter(1))
            prots[gene] = prots_s
            print('After sort:')
            print prots[gene]

            chan_prots = ''
            for key,val in prots[gene]:
                chan_prots += val+'; '
            print chan_prots
            IonChannel.objects.filter(gene_name=gene).update(channel_name=gene.upper(),proteins=chan_prots)
