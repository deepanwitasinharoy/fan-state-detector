import cv2
import numpy as np
vid= cv2.VideoCapture("videos/fan.mp4")
#SET UP #

thresh = 2.5 
running_count=0
stopped_count= 0
status= "STOPPED"

#VIDEO PROPERTIES

width= int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps= vid.get(cv2.CAP_PROP_FPS)

#OUTPUT VIDEO
fourcc= cv2.VideoWriter_fourcc(*"mp4v")
output= cv2.VideoWriter("output/fan_detection.mp4",fourcc,fps,(width,height))

#READING INITIAL FRAME
ret, frame= vid.read()
if not ret:
    print("Video cannot be opened")
    vid.release()
    exit()

#PUTTING MANUAL ROI

roi = frame[70:590, 40:450] # manual region of interest
prev_gray= cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

#GOING TO COMPARE EVERY 10TH FRAME (FOR EASE)

frame_skip = 10
count = 0

#IMPORTANT REGIONS OF THE FAN
center= (205,260)
out_radius= 190
inn_radius= 55

#CIRCULAR MASK

mask = np.zeros (prev_gray.shape, dtype= np.uint8)
cv2.circle(mask,center,out_radius,255, -1)
cv2.circle(mask,center, inn_radius,0 , -1)

#MAIN CODE#

while True:
    ret,frame= vid.read()
    if not ret:
        break
    count+=1
    if count % frame_skip !=0 :
        continue
    roi= frame[70:590, 40:450] #extracting current roi
    current_gray= cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    difference = cv2.absdiff(prev_gray, current_gray)

    #CONSIDERING PIXELS INSIDE THE FAN REGION
    fan_difference= difference[mask == 255] #only consider the fan blade region
    changed_pixels= np.sum(fan_difference>10) #ignore tiny changes
    total_pixels= len(fan_difference)

    #CALCULATING MOTION

    motion_percentage=(changed_pixels/total_pixels)*100

    #DETECTION OF STATUS

    if motion_percentage > thresh :
        running_count+= 1
        stopped_count=0
    else:
        stopped_count+=1
        running_count= 0
    if running_count>=3:
        status= "RUNNING"
    elif stopped_count>=3:
        status= "STOPPED"

        
    print(f"Motion: {motion_percentage:.2f}% | Status: {status}")

    
    prev_gray= current_gray

    #DISPLAY OF STATUS
    cv2.putText(frame,"FAN "+ status,(20,50),cv2.FONT_HERSHEY_DUPLEX,1.2,(0,255,0),3)

    #ROI rectangle
    cv2.rectangle(frame,(40,70),(450,590),(255,0,0),2)

    #DISPLAY VIDEO
    cv2.imshow("FAN DETECTOR", frame)
    output.write(frame)

    if cv2.waitKey(30) & 0xFF == ord('e'): #press e to end the video
        break
vid.release()
output.release()
cv2.destroyAllWindows()

print("DETECTION COMPLETE")
print("OUTPUT SAVED")

