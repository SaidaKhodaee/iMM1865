>>> from Bio import Entrez
>>> import xmltodict
>>>Entrez.email='s.khodaee@ut.at.ir'
# diffinition of refToTargetGenIdMap function:
# input: Entrez Gene ID of Reference Organism; Name of Target Organism
#Output: List contains Locus Tag,Gene Name and Entrez Gene ID of target organism and Entrez Gene ID of reference organism 
>>> def refToTargetGenIdMap (refGenID,targetOrganism):  
	id=refGenID+"[Gene Id]"
	record=Entrez.esearch(db='homologene',term=id)
	xml=record.read()
	p1=xmltodict.parse(xml)
	if p1['eSearchResult']['IdList'] is None:
		data=['Ref ID is not Valid',refGenID]
	else:
		homoId=p1['eSearchResult']['IdList']['Id']
		record = Entrez.esummary(db="homologene", id=homoId)
		xml=record.read()
		p1 = xmltodict.parse(xml)
		j=0
		for i in p1['eSummaryResult']['DocSum']['Item'][0]['Item']:
			j=j+1
			if i['Item'][0]['#text']==targetOrganism:
				a=i['Item'][2]['#text']
				b=i['Item'][3]['#text']
				c=i['Item'][4]['#text']
				data=[a,b,c,refGenID]
				break
			if j==len(p1['eSummaryResult']['DocSum']['Item'][0]['Item']):
				data=['homologue not found',refGenID]
	return data
>>> import cobra
>>> refmodel=cobra.io.read_sbml_model('D:/tezDoctory/tez_new/NewMouseModel/Models/Recon3D.xml')
>>> refGenes=refmodel.genes
>>> idList=[]
>>> for i in refGenes:
	idList=idList+[i.id[:-4]]       #The substring of IDs from index of 0 to -4 was gotten because gene IDs in Recon3D are followed by '_AT<number>'
>>> def deleteDuplicates(x):
  return list(dict.fromkeys(x))
>>> len(idList)
>>> idList=deleteDuplicates(idList)
>>> idList=idList[1:]                   # In Recon3D, the first gene ID is "", so we ignored idList[0]
>>> dataList=[]
>>>targetOrganism='Mus musculus'

>>> for i in idList:
	data=refToTargetGenIdMap (i,targetOrganism)
	if data is not None:
		dataList=dataList+[data]

