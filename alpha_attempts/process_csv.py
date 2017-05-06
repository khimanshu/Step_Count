import re
import math
z=1
fh = open('C:/Users/trose/Documents/default__3.txt','r')
data = list()

for line in fh:
	line = line.strip()
	if re.match('^#.*$', line) or line =='':
		continue	
	line = line.split(' ')
	x =0
	for item in line:
		
		line[x] = float(item)
		x+=1
	line.append(math.sqrt(line[0]**2+line[1]**2+line[2]**2))
	data.append(line)
x=1
#print data
DATA = data
cleanerData = list()
while len(data)>0:
	curr_time = 0
	sec_data = [0.0,0.0,0.0,0.0,0.0]
	y=0
	while sec_data[3] <=1000 and len(data):
		line = data.pop(0)
		x=0
		
		for item in line:
			sec_data[x] = sec_data[x] + item
			x+=1
		y+=1
	x=0
	while x < len(sec_data):
		if x ==3:
			x+=1
			continue
		sec_data[x] = sec_data[x]/y
		x+=1
	cleanerData.append(sec_data)

#print cleanerData
for item in cleanerData:
	print item
print len(cleanerData)

exit()
data_diff = list()
steps =0
while x<len(data):
	movement =0
	diffline = list()
	diffline.append(abs(data[x][0]-data[x-1][0]))
	diffline.append(abs(data[x][1]-data[x-1][1]))
	diffline.append(abs(data[x][2]-data[x-1][2]))
	diffline.append(abs(data[x][4]-data[x-1][4]))
	if diffline[0] >=z:
		movement +=1
	if diffline[1]>=z:
		movement +=1
	if diffline[2]>= z:
		movement +=1
	if diffline[3]>=z or 1:
		
		if movement ==2:
			print str(diffline) + ' ' + str(movement)
			steps+=1
	data_diff.append(diffline)
	x+=1
fh.close()
#print data_diff
print steps
#print data
