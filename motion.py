#importing libraries:
import requests
from gpiozero import MotionSensor
import time
from picamera import PiCamera

camera = PiCamera() #define the PiCamera() to camera variable
camera.resolution = (1920, 1080) #set the resolution to 1920x1080

pir = MotionSensor(4) #setup input for MotionSensor (PIR sensor) at GPIO Pin 4
switch = True #create switch variable for loop sequence, and set to True to begin with

url = 'https://www.dropbox.com/request/obcoRUWqRSSYgWuNVAv1' #url for request pull to upload to dropbox

#defining send_alert function to send alert when motion has been triggered
def send_alert():
    camera.capture('/home/pi/Dropbox-Uploader/capture.jpg') #takes a photo of the motion detected, via the camera module
    files = {'file': open('/home/pi/Dropbox-Uploader/capture.jpg', 'rb')} #makes sure to open the file, in the specified directory, as a 'read-binary' (rb) file
    
    r2 = requests.post(url, files=files) #uses request function to post to url with specified files
    print(r2.status_code)
    #print(r2.text)
    
    r = requests.post("https://maker.ifttt.com/trigger/trigger/with/key/de2f5UHFaIUzOvNTYF1f9k") #uses post request function for IFTTT trigger, with API included
    
    if r.status_code == 200: #if successfull
        print("Alert Sent") #prints and verifies that alert has been sent
        
    else:
        print("Error") #prints and verifies that alert hasn't been sent

#defining loop function that checks whether motion has been detected or not
def loop():
    if pir.motion_detected: #using library to check if PIR sensor has detected any motion
        print("Motion detected!") #prints that motion has been detected
        send_alert() #calls the send_alert function above
        switch = False #switches the switch variable to false, for loop sequence purposes
        
    else:
        print("No motion detected.") #prints that no motion has been detected
        switch = False #switches the switch variable to false, for loop sequence purposes

while switch == True:
    loop() #calls the loop function, in order for it to check it constantly
    time.sleep(15) #delays it though by 15seconds, so it doesn't do it all the time
    switch = True