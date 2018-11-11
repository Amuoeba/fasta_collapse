import re

def clean_fasta(ele):
    ele = ele.rstrip()
    if ele != "":
        return ele



class FastaSequence:
    id_regex = re.compile("[a-zA-z0-9]*\.[a-zA-z0-9]*",re.IGNORECASE)
    meta_regex = re.compile("(?<=>)(.*?)(?= ) (?<= )(.*?)(?=\[)\[(.*?)(?=\])",re.IGNORECASE)
    id_line_reg = re.compile("^>")

    def __init__(self,id_line):
        self.id_line = id_line
        self.id = None
        self.prot = None
        self.species = None
        self.sequence = []
        self.idList = set()

    def extract_meta(self):
        id_mtch = self.id_regex.findall(self.id_line)
        meta_match = self.meta_regex.findall(self.id_line)
        if id_mtch:
            self.id = id_mtch[0]
            # print("ID: ",id_mtch)
        if meta_match:
            self.prot = meta_match[0][1]
            self.species = meta_match[0][2]
            # print("META",meta_match)

    def concat_seq(self):
        return "".join(self.sequence)

    def fasta_representation(self):
        s = repr(self.idList) +"\n"
        s += self.id_line + "\n"
        for x in self.sequence:
            s += x +"\n"

        return s +"\n"


    def __repr__(self):
        return "Id: {}\nId List: {}\nProt: {}\nSpecies: {}\nSeq: {}\n\n".format(self.id,self.idList,self.prot,self.species,self.concat_seq())

with open("sequence.txt", "r") as f:
    content = f.readlines()
    content = [clean_fasta(x) for x in content]
    content = [x for x in content if x is not None]



fasta_lst = []
for l in content:
    if FastaSequence.id_line_reg.findall(l):
        newFasta = FastaSequence(l)
        newFasta.extract_meta()
        fasta_lst.append(newFasta)
    else:
        fasta_lst[-1].sequence.append(l)


for ind,seq in enumerate(fasta_lst):
    for seqTwo in fasta_lst[ind+1:]:
        if seq.concat_seq() == seqTwo.concat_seq():
            seqTwo.idList.add(seq.id)
            seq.idList.add(seqTwo.id)
            seq.idList.add(seq.id)
            seqTwo.idList.add(seqTwo.id)
        else:
            seq.idList.add(seq.id)
for i in fasta_lst:
    print(i.fasta_representation())

seen_sets = set()
collapsed_fasta = []
for ind,seq in enumerate(fasta_lst):
    for seqTwo in fasta_lst[ind+1:]:
        if seq.idList == seqTwo.idList:
            del fasta_lst[ind]
sum = 0
for seq in fasta_lst:
    sum += len(seq.idList)
    print(seq.fasta_representation())
    with open("collapsed_fasta.txt","a") as f:
        f.write(seq.fasta_representation())

# print(sum)
# print(len(fasta_lst))