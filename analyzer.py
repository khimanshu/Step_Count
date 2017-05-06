import ConfigParser
import argparse
import re
import math

def conv_line_to_float(line,conv):
    line = line.split()
    x= 0
    for item in line:
        if x<3:
            if conv==1:
                # convert meters to ft
                line[x] = float(item)*3.28084
            elif conv==2:
                # convert ft to meters
                line[x] = float(item)*0.3048
            else:
                line[x] = float(item)
        else:
            line[x] = float(item)

        x+=1
    return line

def cal_dist(line, vline,sline):
    # attemps to us acceleration to calculate the distance traveled, 
    # Sources
    # http://www.engineeringtoolbox.com/acceleration-velocity-d_1769.html
    # https://github.com/bagilevi/android-pedometer/blob/master/src/name/bagi/levente/pedometer/StepDetector.java

    dline = list()
    t = line[3]*.001
    x=0
    y=1
    while x < 3:
        # averaging the acceleration across two polling to, doesn't seem to 
        # have an affect when using ABS
        #sline[x] += ((abs(vline[x])+abs(line[x]))*t)/2
        sline[x] += (abs(line[x])*t)
        sline[y] +=sline[x]*t 
        x+=1
        y+=2
    return math.sqrt(sline[0]**2+sline[1]**2+sline[2]**2),sline

def cal_step(line,pline):
    # Source
    # https://www.firstlinesoftware.com/outsourcery/16-counting-steps
    # Uses the angle magnitude to guess if a step has taken place
    m =math.sqrt(line[0]**2+line[1]**2+line[2]**2)
    m2 = math.sqrt(pline[0]**2+pline[1]**2+pline[2]**2)
    t = line[0]*pline[0]+line[1]*pline[1]+line[2]*pline[2]
    if m2==0 or m==0:
        return 0
    a = t/(m*m2)
    if a < 0:
        return 1 
    else:
        return 0


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Accelerometer Analyzer')
    parser.add_argument('-f','--file',default='', help='Data File')
    parser.add_argument('-i','--ini',default='./analyzer.ini',help='ini File')

    args = parser.parse_args()
    if args.file=='':
        raise ValueError('Data File Can not be blank')
    config = ConfigParser.ConfigParser()
    config.read(args.ini)
    units = config.get('Analyzer','units','ft')
    file_units=units
    stride = float(config.get('Analyzer', 'stride', '2.6'))
    log_dir = config.get('Analyzer', 'log_dir', './log')    
    fileh = open(args.file,'r')
    total_dist = 0
    total_time = 0
    dsteps = 0
    asteps = 0
    curr_dist = 0
    conv = 0
    prev_vel = [0,0,0,0]
    prev_line = [0,0,0,0]
    sline = [0,0,0,0,0,0]
    for line in fileh:
        # clean up and skip blank lines
        line = line.strip()
        if line =='':
            continue
        # grab file units to match against ini preference
        reunit = re.search('# units set to: (\w+)/sec',line)
        if reunit:
            file_units = reunit.group(1)
            if file_units!=units:
                if units =='ft':
                    conv = 1
                elif units =='m':
                    conv = 2
        # skip all comment lines
        if re.match('^#.*$',line):
            continue
        line = conv_line_to_float(line,conv)
        total_time+=line[3]/1000
        curr_dist, sline = cal_dist(line,prev_line,sline)
        asteps+=cal_step(line,prev_line)
        prev_line = line
        # let curr_dist accumulate until >= user defined stride
        # then add to total_dist increment dsteps and rest
        if curr_dist >= stride:
            dsteps +=1
            total_dist+=curr_dist
            curr_dist=0
            sline = [0,0,0,0,0,0]
    fileh.close()
    total_dist+=curr_dist
    if curr_dist!=0:
        dsteps+=1
    print 'Total Distance Traveled: '+str(total_dist)+ ' '+ units
    print 'Total Time: '+ str(total_time) + ' sec'
    print 'Stride Length: '+str(stride) + ' '+ units
    print 'Steps by stride length: ' + str(dsteps)
    print 'Steps by accleration angle difference: '+ str(asteps)
    print 'Best guess steps: '+ str((dsteps+asteps)/2) 
    if units =='ft':
        print 'Average speed: ' + str(total_dist*0.681818/total_time)+ ' mph *assumes continuous movement'
    elif units =='m':
        print 'Average speed: ' + str(total_dist*3.6/total_time)+ ' kph *assumes continuous movement'


