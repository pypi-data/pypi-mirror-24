def sanitize(time_string):
    if '-' in time_string:
        splitter='-'
    elif ':' in time_string:
        splitter=':'
    else:
        return(time_string)
    (mins,secs)= time_string.split(splitter)
    return(mins+'.'+secs)
'''
def get_coach_data(filename):
    with open(filename) as f:
        data=f.readline().strip().split(',')
        data1={}
        data1['name']=data.pop(0)
        data1['DOB'] =data.pop(0)
        data1['Times']=str(sorted(set([sanitize(t) for t in data]))[0:3])
        return(data1)
sarah = get_coach_data('sarah2.txt')
(sarah_name,sarah_dob) = sarah.pop(0),sarah.pop(0)
print(sarah_name+"'s fastest time are:"+str(sorted(set([sanitize(t) for t in sarah]))[0:3]))


sarah = get_coach_data('sarah2.txt')
print(sarah['name']+"'s fastest time are:"+sarah['Times'])

class Athlete:
    def __init__(self,a_name,a_dob=None,a_times= [ ]): #  __init__这里一定要注意  
        self.name =a_name
        self.dob = a_dob
        self.times=a_times
    def top3(self):
        return(sorted(set([sanitize(t) for t in self.times]))[0:3])
    def add_time(self,time_value):
        self.times.append(time_value)
    def add_times(self,list_of_times):
        self.times.extend(list_of_times)
'''

class Athletelist(list):
    def __init__(self,a_name,a_dob=None,a_times= []):
        list.__init__([])
        self.name =a_name
        self.dob = a_dob
        self.extend(a_times)
    def top3(self):
        return(sorted(set([sanitize(t) for t in self]))[0:3])

        
def get_coach_data(filename):
    with open(filename) as f:
        data = f.readline().strip().split(',')
    return(Athletelist(data.pop(0),data.pop(0),data))
        
#sarah = get_coach_data('sarah2.txt')
#print(sarah.name+"'s fastest time are:"+str(sarah.top3()))

vera= Athletelist('vera vi')
vera.extend(['1.31','1-21','2:22'])

print(vera.top3())
#我就单纯想改一下
