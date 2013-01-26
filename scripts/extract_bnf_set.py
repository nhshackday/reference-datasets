#!/usr/bin/python

import sys
import csv
import json
from pprint import pprint

#
# Usage: extract_bnf_set.py bnf_headings.json T201209CHEM+SUBS.CSV T201209PDPI+BNFT.CSV 
#
#  bnf_headings.json - chapter, section, paragraph, sub paragraph BNF headline structure 
#  T201209CHEM+SUBS.CSV - BNF chemical code to name look up dataset (linked to prescribing data)
#  T201209PDPI+BNFT.CSV - Practice level prescription statistics Source: http://data.gov.uk/dataset/prescribing-by-gp-practice-presentation-level


bnf_file=sys.argv[1]
chem_file=sys.argv[2]
product_file=sys.argv[3]
p_c={}
fullset=[]
bnfdb=[]
with open(bnf_file) as f:
    bnfdb=json.load(f)
chem=[]
with open(chem_file) as f:
	creader=csv.reader(f, delimiter=',', quotechar='"')
	for cd in creader:
		if cd[0]!='CHEM SUB ':
			bnf=cd[0].strip()
			chapter=bnf[0:2]
			section=bnf[2:4]
			paragraph=bnf[4:6]
			sub=bnf[6:7]
			chemical=bnf[7:]
			product_entry={'bnf':bnf,
				'chapter':chapter,
				'section':section,
				'paragraph':paragraph,
				'sub':sub,
				'chemical':chemical,
				'title':cd[1].strip(),
				'level':'chemical'}
			chem.append(product_entry)
			#product_id=prescDB.update({'chemicalcode':bnf,'period':period},product_entry,True,True)
with open(product_file) as f:
	creader=csv.reader(f, delimiter=',', quotechar='"')
	for cd in creader:
		key=cd[3].strip()
		name=cd[4].strip()
		p_c[key]=name
for bnfcode in (sorted(p_c,key=p_c.get)):
    chapter=bnfcode[0:2]
    section=bnfcode[2:4]
    paragraph=bnfcode[4:6]
    sub=bnfcode[6:7]
    chemical=bnfcode[7:9]
    product=bnfcode[9:11]
    formulation=bnfcode[11:13]
    generic=bnfcode[13:15]
    presc_entry={'bnf':bnfcode,
        'chapter':chapter,
        'section':section,
        'paragraph':paragraph,
        'sub':sub,
        'chemical':chemical,
        'title':p_c[bnfcode],
        'product':product,
        'formulation':formulation,
        'generic':generic,
        'level':'prescription'}
    chem.append(presc_entry)
fullset=bnfdb+chem
with open('dump-bnf.json','w') as f:
	json.dump(fullset,f,indent=4)
