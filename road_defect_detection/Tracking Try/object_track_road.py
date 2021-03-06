import cv2
import time


def object_tracker(tracker_algo = "MDF", video_path = "road.mp4"):
    if tracker_algo == "boosting":
        tracker = cv2.TrackerBoosting_create()
    if tracker_algo == "CSRT":    
        tracker = cv2.TrackerCSRT_create()
    if tracker_algo == "TLD":    
        tracker = cv2.TrackerTLD_create()
    if tracker_algo == "MIL":    
        tracker = cv2.TrackerMIL_create()
    if tracker_algo == "KCF":      
        tracker = cv2.TrackerKCF_create()
    if tracker_algo == "MDF":    
        tracker = cv2.TrackerMedianFlow_create()
    
    time.sleep(1)
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    width  = cap.get(3) # float
    height = cap.get(4) # float
    bbox = cv2.selectROI("Tracking",frame, False)
    tracker.init(frame, bbox)

    def drawBox(img,bbox):
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(img, (x, y), ((x + w), (y + h)), (0, 255, 0), 3, 3 )
        cv2.line(img, (0,int(height)-5), (int(width),int(height)-5), (255,0,0), 3) 
        print(((x+x+w)/2),((y+y+h)/2))
        cv2.putText(img, "Tracking Started", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    while True:

        timer = cv2.getTickCount()
        success, img = cap.read()
        success, bbox = tracker.update(img)
    
        if success:
            drawBox(img,bbox)
        else:
            cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
        cv2.rectangle(img,(15,15),(200,90),(255,0,255),2)
        cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2);
        cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2);
    
    
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        if fps>60: myColor = (20,230,20)
        elif fps>20: myColor = (230,20,20)
        else: myColor = (20,20,230)
        cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);
    
        cv2.imshow("Tracking", img)
        
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    
         
    cv2.destroyAllWindows()    
    cap.release()


object_tracker()
