#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector
from Bio import pairwise2

def main():
 print("Content-Type: application/json\n\n")
 form = cgi.FieldStorage()
 term = form.getvalue('search_term')
 term = "Adam12"
 conn = mysql.connector.connect(user='genome', host='genome-mysql.soe.ucsc.edu', database='mm10')
 cursor = conn.cursor()
 query = '''select strand, cdsStart, cdsEnd  from refGene where name2 like %s'''
 cursor.execute(query,(term, ))
 for (gstrd,gsta,ged) in cursor:
  row=(gstrd,gsta,ged)
  gstrand=row[0]
  gstart=row[1]
  gend=row[2]
 file=open("mm10_chr7_repeats.bed","r")
 rplus=[]
 rminus=[]
 for ln in file:
  ln=ln.strip("\n")
  ln=ln.split("\t")
  rcoo=(int(ln[1]),int(ln[2]))
  if ln[5]=="+":
   rplus.append(rcoo)
  if ln[5]=="-":
   rminus.append(rcoo)
 if gstrand=="+":
  com=[]
  for rcoo in rplus:
   if rcoo[0] in range(gstart-5000,gstart+5000):
    dis=gstart-rcoo[0]
    if dis < 0:
     dis=-dis
    com.append((dis,rcoo[0],rcoo[1],"s"))
   if rcoo[1] in range(gend-5000,gend+5000):
    dis=gend-rcoo[1]
    if dis < 0:
     dis=-dis
    com.append((dis,rcoo[0],rcoo[1],"e"))
 def getZ(elem):
  return elem[0]
 com.sort(key=getZ)
 com=com[:5]
 dict={}
 file=open("viral.csv","r")
 vd={}
 for ln in file:
  ln=ln.split(",")
  vd[ln[0]]=ln[1]
 file=open("mm10.fna","r")
 l=file.readline()
 l=l.strip(">")
 for ln in file:
  ln=ln.strip("\n")
  l=l+ln
 sel={}
 for i in com:
  st=i[1]-1
  end=i[2]+1
  se=l[st:end] 
  sel[se]=[i[1],i[2]]
 fd=[]
 for rse in sel:
  for k in vd:
   alignments=pairwise2.align.globalxx(rse,vd[k],one_alignment_only=1, score_only=1)
   if alignments >0:
    fd.append((k,alignments,sel[rse][0],sel[rse][1]))
 def getY(elem):
  return elem[1]
 fd.sort(key=getY,reverse=True)
 results = { 'matches': list() }
 for i in fd:
  rstart=i[2]
  rend=i[3]
  score=i[1]
  a=i[0].split("|")
  acnum=a[0]
  virus=a[1]
  results['matches'].append({'virus': virus, 'acnum': acnum, 'score' : score, 'rstart' : rstart, 'rend' : rend})
 conn.close()
 print(json.dumps(results)) 
 
if __name__ == '__main__':
    main()
