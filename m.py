import boto3
import csv
import re
import pandas as pd
from calendar import month_abbr
from datetime import datetime
import os

# Establishing connection with Rekognition API
# Credentials.csv is the file which includes access key and id 
with open('credentials.csv','r') as input:
    next(input)
    reader=csv.reader(input)
    for line in reader:
        access_key_id=line[2]
        secret_access_key=line[3]
client=boto3.client('textract',aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
photo = '/home/sak/DL/material/text_ocr/data-set/ms-9.jpg'
with open(photo,'rb') as source_image:
    source_bytes=source_image.read()
response=client.detect_document_text(Document={'Bytes':source_bytes})
temp=[]
for item in response['Blocks']:
    if item["BlockType"] == "LINE":
        temp.append(item['Text'])
d=['A1','A@','A3','B1','B2','B3','C1','C2','C3','D1']

def get_marks(temp):
    p,c,m=0,0,0
    try:
        for i in range(0,len(temp)):
            if temp[i]=='PHYSICS' or temp[i]=='SCIENCE & TECH.' and temp[i+3]:
                p=temp[i+3]
                if p in d:
                    p=temp[i+2]
                p=list(p)
                for i in range(len(p)):
                    if p[i]=='o':
                        p[i]='0'
                    if p[i]=='B':
                        p[i]='8'
                p=int(''.join(p))
            if temp[i]=='CHEMISTRY' and temp[i+3]:
                c=temp[i+3]
                if c in d:
                    c=temp[i+2]
                c=list(c)
                for i in range(len(c)):
                    if c[i]=='o':
                        c[i]='0'
                    if c[i]=='B':
                        c[i]='8'
                c=int(''.join(c))
            if (temp[i]=='MATHEMATICS' or 'MATH' in temp[i]) and temp[i+3]:

                m=temp[i+3]
                if m in d:
                    m=temp[i+2]
                m=list(m)
                for i in range(len(m)):
                    if m[i]=='o':
                        m[i]='0'
                    if m[i]=='B':
                        m[i]='8'
                m=int(''.join(m))
    except:
        print("Can't predict Some error occured please try uploading again")
    if not p:
        print("Can't predict   Physics marks not found")
        return p,c,m
    if not c:
        print(" cam't predict   Chemistry Marks Not Found")
        return p,c,m
    if not m:
        print(" cam't predict    Mathematics Marks Not Found")
        return p,c,m
    return p,c,m

def college(p,c,m):
    marks=p+c+m
    total=300
    per=(marks/total)*100
    return per
p,c,m=get_marks(temp)
per=college(p,c,m)
if per>=90:
    print("Alpha")
elif per>=80 and per<90:
    print("Beta")
else:
    print("Gamma")