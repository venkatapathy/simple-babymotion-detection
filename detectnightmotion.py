import cv2
from datetime import datetime
import time
import requests


baseline_image=None
video=cv2.VideoCapture(0)
penalty=0
movement_flag=False
idle_time=0
_penalty_threshold=10
_idle_threshold_time=15
_contour_threshold=500

time.sleep(120)
        
while True:
  # Check if the webcam is opened correctly
    check, frame = video.read()
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)
    baseline_image=gray_frame

    time.sleep(1)

    check, frame = video.read()
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

    delta=cv2.absdiff(baseline_image,gray_frame)
    threshold=cv2.threshold(delta, 10, 255, cv2.THRESH_BINARY)[1]
    (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    penalty_flag=False
    for contour in contours:
        #print(cv2.contourArea(contour))
        #print(threshold)
        if cv2.contourArea(contour) > _contour_threshold:
            penalty+=1
            penalty_flag=True
            idle_time=0
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
        cv2.putText(frame,str(cv2.contourArea(contour)),(x,y),cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255))
    
    if(not penalty_flag):
        idle_time+=1
	
    if idle_time > _idle_threshold_time:
        penalty=0
        movement_flag=False
    
    #print(penalty_flag)

	#if movement detected continnously for 5 units of time update the website
    if penalty>=_penalty_threshold:
        
        #wait for atleast a minute so that the movement is notified
        print("Movement detected at:")
        print(datetime.now())
        #cv2.imwrite('outimg/out'+str(datetime.now())+'.jpg',frame)
        #reset webpage
        '''webchange=open('serverdir/index.html','w')
        webchange.write('<html><head><title>Rishi</title></head><body>No problem</body></html>')
        webchange.close()'''
        try:
            r = requests.get('https://wirepusher.com/send?id=hbBompXx6&title=rishi&message=CheckRishi')
            t = requests.get('https://wirepusher.com/send?id=adBEmpXfw&title=rishi&message=CheckRishiAmma')
            
            #write the video
            # We need to set resolutions. 
            # so, convert them from float to integer. 
            frame_width = int(video.get(3)) 
            frame_height = int(video.get(4)) 
   
            size = (frame_width, frame_height) 
   
            # Below VideoWriter object will create 
            # a frame of above defined The output  
            # is stored in 'filename.avi' file. 
            result = cv2.VideoWriter('outimg/out'+str(datetime.now())+'.avi',cv2.VideoWriter_fourcc(*'MJPG'),10, size) 
            
            for i in range(140):
                ret, frame = video.read() 

                if ret == True:  
                    # Write the frame into the 
                    # file 'filename.avi' 
                    result.write(frame)
            
            result.release()
            
        except:
            print('Movement detected but couldnt publish on internet. Detected at')
                  
        time.sleep(120)
        #reset detection
        penalty=0
        movement_flag=False
        idle_time=0
        

    '''cv2.imshow("gray_frame Frame",gray_frame)
    cv2.imshow("Delta Frame",delta)
    cv2.imshow("Threshold Frame",threshold)
    cv2.imshow("Color Frame",frame)'''
    cv2.waitKey(1)
    #time.sleep(0.25)

    
    
#Clean up, Free memory
video.release()
cv2.destroyAllWindows