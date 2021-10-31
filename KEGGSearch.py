import Bio
from Bio import KEGG
from Bio.KEGG import REST
from Bio.KEGG import KGML
from Bio.KEGG.KGML import KGML_parser

def getOrgRxnsFromKEGG(org):
	import re
	idList,discList,difList,signalingPathwaysIndex,sigPathID,reactionList=[],[],[],[],[],[]
	pathways=REST.kegg_list("pathway", org).read()
	pathways=pathways.split("\n")
	for path in pathways:
		p1=path.split("\t")
		if len(p1)==2:
			idList=idList+[p1[0].split(":")[1]]
			discList=discList+[p1[1]]
	for disc in discList:
		if re.search('signaling', disc) is not None:
			signalingPathwaysIndex=signalingPathwaysIndex+[discList.index(disc)]
	for index in signalingPathwaysIndex:
		sigPathID=sigPathID+[idList[index]]
	pathIdList=list(set(idList)- set(sigPathID))
	for pathID in pathIdList:
		result = REST.kegg_get(pathID, "kgml").read()
		p1=Bio.KEGG.KGML.KGML_parser.read(result)
		listReacObj = list(p1.reactions)
		if listReacObj:
			for reactionObj in listReacObj:
				reactionList=reactionList+reactionObj.name.split()
	return reactionList

humanRxnList=getOrgRxnsFromKEGG('hsa')#in here, reference organism is homo sapiens
#with open('D:/tezDoctory/tez_new/MyPaper/pythonCodeForModel_iMM1865/humanRxnList.txt','w') as file:
#	file.writelines("% s\t" % rxn for rxn in humanRxnList)
mouseRxnList=getOrgRxnsFromKEGG('mmu')#in here, Target organism is Mus Musculus
#with open('D:/tezDoctory/tez_new/MyPaper/pythonCodeForModel_iMM1865/mouseRxnList.txt','w') as file:
#	file.writelines("% s\t" % rxn for rxn in mouseRxnList)
candidateMouseSpecRxns=list(set(mouseRxnList)-set(humanRxnList))
	