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
	#line.append((line[0]+line[1]+line[2])/3)
	line.append(math.sqrt(line[0]**2+line[1]**2+line[2]**2))
	line.append(line[4]*line[3]/1000)
	data.append(line)
x=1
DATA = data
cleanerData = list()
steps = 0
step_dists = list()
step_times =list()
while len(data)>0:
	curr_dist = 0
	curr_time =0
	y=0
	while curr_dist<3 and len(data):
		line = data.pop(0)
		x=0
	
		y+=1
		curr_time = curr_time+line[3]
		curr_dist = curr_dist+line[5]
	steps+=1
	step_dists.append(curr_dist)
	step_times.append(curr_time)

print steps
print step_dists
print step_times

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
