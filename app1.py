
from flask import Flask,render_template, request
import boto3
from scipy import misc
import csv
import cv2
import os
d=['A1','A2','A3','B1','B2','B3','C1','C2','C3','D1']

def get_marks(temp,e):
	p,c,m=0,0,0
	try:
		for i in range(0,len(temp)):
			if temp[i]=='PHYSICS' or temp[i]=='SCIENCE & TECH.' and temp[i+3]:
				p=temp[i+3]
				if p in d:
					p=temp[i+2]
				p=list(p)
				print(p)
				for i in range(len(p)):
					if p[i]=='o' or p[i]=='O':
						p[i]='0'
					if p[i]=='B':
						p[i]='8'
				p=int(''.join(p))
				print(p)
			if temp[i]=='CHEMISTRY' and temp[i+3]:
				c=temp[i+3]
				if c in d:
					c=temp[i+2]
				c=list(c)
				print(c)
				for i in range(len(c)):
					if c[i]=='o' or c[i]=='O':
						c[i]='0'
					if c[i]=='B':
						c[i]='8'
				c=int(''.join(c))
				print(c)
			if (temp[i]=='MATHEMATICS' or 'MATH' in temp[i]) and temp[i+3]:
				m=temp[i+3]
				if m in d:
					m=temp[i+2]
				m=list(m)
				print(m)
				for i in range(len(m)):
					if m[i]=='o' or m[i]=='O':
						m[i]='0'
					if m[i]=='B':
						m[i]='8'
				m=int(''.join(m))
				print(m)
	except:
		e=0
		print("Can't predict Some error occured please try uploading again")
	if not p:
		print("Can't predict Physics marks not found")
		return p,c,m
	if not c:
		print(" cam't predict Chemistry Marks Not Found")
		return p,c,m
	if not m:
		print(" cam't predict Mathematics Marks Not Found")
		return p,c,m
	return p,c,m

def college(p,c,m):
	print(p,c,m)
	marks=int(p)+int(c)+int(m)
	total=300
	per=(marks/total)*100
	return per

app=Flask(__name__) 

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def make_prediction():
	if request.method=='POST':
		basepath="/home/sak/"
		# get uploaded image file if it exists
		image_file = request.files['image']
		name=image_file.filename
		if not image_file: return render_template('index.html', label="No file")
		
		# read in file as raw pixels values
		# (ignore extra alpha channel and reshape as its a single image)
		#img = cv2.imread(file)
		file_path = os.path.join(basepath,name)
		image_file.save(file_path)
		with open('credentials.csv','r') as input:
			next(input)
			reader=csv.reader(input)
			for line in reader:
				access_key_id=line[2]
				secret_access_key=line[3]
		client=boto3.client('textract',aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
		with open(file_path,'rb') as source_image:
			source_bytes=source_image.read()
		response=client.detect_document_text(Document={'Bytes':source_bytes})
		temp=[]
		for item in response['Blocks']:
		    if item["BlockType"] == "LINE":
		        temp.append(item['Text'])
		d=['A1','A2','A3','B1','B2','B3','C1','C2','C3','D1']
		e=1
		p,c,m=get_marks(temp,e)
		if p==0:
			return render_template('index.html',label="Physics Marks Not Found")
		if m==0:
			return render_template('index.html',label="Math Marks Not Found")
		if c==0:
			return render_template('index.html',label="Chemistry Marks Not Found")
		if e==0:
			return render_template('index.html',label="Unable to detect marks")


		per=college(p,c,m)
		if per>=90:
		    print("Alpha")
		    s='Alpha'
		    print(s)
		elif per>=80 and per<90:
		    print("Beta")
		    s="Beta"
		    print(s)
		else:
		    print("Gamma")
		    s="Gamma"
		    print(s)
	'''if request.method == 'POST': 
		to_predict_list = request.form.to_dict() 
		news = list(to_predict_list.values()) 
		result = ValuePredictor(news)         
		if result ==0:
			pred='Business'
		if result==1:
			pred='Sport'
		if result==2:
			pred='Technology'''            
	return render_template('index.html', label = 'You can get'+ ' '+s +' '+'college') 

