import numpy as np
import matplotlib.pyplot as plt
import math
import scipy

#f = open("data.txt", "r")
f = open("Tire Blowout Research/frontLeft/frontLeft_trial1_6.26_12.51pm", "r")
d=f.read()
y1=[]
y2=[]
y3=[]
y4=[]
y5=[]
y6=[]
arr=[y1,y2,y3,y4,y5,y6,0]
i=0
while d.find("[")>0:
    start=d.find("[")
    end=d.find("]")
    #print(d[start+1:end])
    arr[i]=d[start+1:end].split(",")
    for j in range(len(arr[i])):
        arr[i][j]=float(arr[i][j])
    
        
    d=d[end+1:]
    i+=1

tireFell=float(d[d.find("(")+1:d.find(")")])


start=float(d[d.find("{")+1:d.find("}")])

#tireFell=start
startIndex=arr[6].index(start)
tireFellIndex=arr[6].index(tireFell)
'''
for i in range(len(arr)):
    arr[i] = np.array(arr[i], dtype='float')
    sos = scipy.signal.butter(5, 5, 'lowpass', fs=60, output='sos')
    arr[i] = scipy.signal.sosfiltfilt(sos, arr[i])
    arr[i]=list(arr[i])
'''

from scipy.ndimage import gaussian_filter1d




def guassianBlur(y):
    kernel=[1/4096,12/4096,66/4096,220/4096,495/4096,792/4096,924/4096,792/4096,495/4096,220/4096,66/4096,12/4096,1/4096]
    '''
    for i in range(len(y)-len(kernel)):
        val=0
        sum=0
        for j in range(len(kernel)):
            val+=kernel[j]*y[int(i+j)]
            sum+=kernel[j]
        y[i]=val
        y[i]/=sum
    '''
    
    
    
    
    y=np.convolve(kernel,y,'same')
    return y
    
    
    


#for i in range(6): 
    #arr[i]=guassianBlur(arr[i])

new=[]
new.append(arr[1][0])
for i in range(1,len(arr[1])):
    new.append(arr[1][i]-arr[1][i-1])
arr[1]=new
plt.figure(figsize=(12, 8))  # Adjust the figure size as needed

# Plot 1
plt.subplot(2, 3, 1)  # (rows, columns, panel number)
#print("hi",arr[6].index(start))
plt.plot(arr[6][startIndex:], arr[0][startIndex:])


#plt.scatter(start, arr[0][arr[6].index(start)], color='green', label='Got input here') 
x=[]
y=[]
sdYn=[]
sdYp=[]
sdX=[]
num=1
temp=[]
for i in range(startIndex+30,len(arr[0])):
    sd=np.std(arr[0][startIndex:i])
    mean=np.mean(arr[0][startIndex:i])
    
    if( arr[0][i]>5*(sd)+(mean) or arr[0][i]<-5*(sd)+(mean)):
        x.append(arr[6][i])
        y.append(arr[0][i])
        temp.append(i)
    sdYn.append(num*sd+mean)
  
    sdX.append(arr[6][i])
    sdYp.append(num*-sd+mean)
try:
    print(temp[0],temp[-1])
    print(arr[0][55:75])
    tempX=[arr[6][temp[0]-10],arr[6][temp[-1]+10]]
    tempY=[arr[0][temp[0]-10],arr[0][temp[-1]+10]]

    plt.plot(sdX, sdYn,color="orange")
    plt.plot(sdX, sdYp,color="orange")
    plt.scatter(x, y,color="green")
    print(tireFellIndex)

    plt.scatter(tempX, tempY,color="yellow")
except:
    e=0
print(tireFellIndex)
print(arr[0][tireFellIndex-5:tireFellIndex+15])
plt.scatter(tireFell, arr[0][tireFellIndex], color='red', label='Tire Fell Here') 
plt.title('Time vs. X Angular Velocity')
plt.ylabel('X Angular Velocity (rad/s)') 
plt.xlabel("Time (s)")


# Plot 2
plt.subplot(2, 3, 2)
plt.plot(arr[6][startIndex:], arr[1][startIndex:])


plt.scatter(tireFell, arr[1][tireFellIndex], color='red', label='Tire Fell Here') 
#plt.scatter(start, arr[1][arr[6].index(start)], color='green', label='Got input here') 
plt.title('Time vs. Y Angular Velocity')
plt.ylabel('Y Angular Velocity (rad/s)') 
plt.xlabel("Time (s)")



# Plot 3
plt.subplot(2, 3, 3)
plt.plot(arr[6][startIndex:], arr[2][startIndex:])
plt.scatter(tireFell, arr[2][tireFellIndex], color='red', label='Tire Fell Here') 
#plt.scatter(start, arr[2][arr[6].index(start)], color='green', label='Got input here') 
plt.title('Time vs. Z Angular Velocity')
plt.ylabel('Z Angular Velocity (rad/s)') 
plt.xlabel("Time (s)")



# Plot 4
plt.subplot(2, 3, 4)
plt.plot(arr[6][startIndex:], arr[3][startIndex:])
plt.scatter(tireFell, arr[3][tireFellIndex], color='red', label='Tire Fell Here') 
#plt.scatter(start, arr[3][arr[6].index(start)], color='green', label='Got input here') 


plt.title('Time vs. X Linear Acceleration ')
plt.ylabel('X Linear Acceleration (m/s^2)') 
plt.xlabel("Time (s)")



# Plot 5
plt.subplot(2, 3, 5)
plt.plot(arr[6][startIndex:], arr[4][startIndex:])

plt.scatter(tireFell-0.5, arr[4][tireFellIndex], color='red', label='Tire Fell Here') 
#plt.scatter(start, arr[4][arr[6].index(start)], color='green', label='Got input here') 
plt.title('Time vs. Y Linear Acceleration ')
plt.ylabel('Y Linear Acceleration (m/s^2)') 
plt.xlabel("Time (s)")



# Plot 6
plt.subplot(2, 3, 6)
plt.plot(arr[6][startIndex:], arr[5][startIndex:])
plt.scatter(tireFell-0.5, arr[5][tireFellIndex], color='red', label='Tire Fell Here') 
#plt.scatter(start, arr[5][arr[6].index(start)], color='green', label='Got input here') 
plt.title('Time vs. Z Linear Acceleration ')
plt.ylabel('Z Linear Acceleration (m/s^2)') 
plt.xlabel("Time (s)")



# Adjust layout to prevent overlap of titles and labels
plt.tight_layout()

# Show plot
plt.show()


