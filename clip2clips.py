#simple shot boundary detection

import sys
import cv2

from skimage import metrics
#Van Anderson python video to clips maker
#def main(video, outputFolder):
#    pass



#if __name__=="__main__":
#    if len(sys.argv)>2:
#        print("too many arguments, choose input video and output folder name")
#    else:
#        main(sys.argv[0],sys.argv[1])
#


#count frame numbers, add them to a list
#get total video frames and fps
#divide CutFrame/fps to get seconds
#use seconds to cut video

original_video=cv2.VideoCapture("./30SecTest.mp4")
fps=original_video.get(cv2.CAP_PROP_FPS)
cur_frame=1
first_new_frame=[]

frame2=None

while(original_video.isOpened()):
    ret1,frame1=original_video.read()
    if ret1 == True:
        cv2.imshow('Frame', frame1)
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame1_HSV=cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)
        hist_h1 = cv2.calcHist([frame1_HSV], [0], None, [256], [0, 256])
        hist_s1 = cv2.calcHist([frame1_HSV], [1], None, [256], [0, 256])
        hist_v1 = cv2.calcHist([frame1_HSV], [2], None, [256], [0, 256])
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        if frame2 is not None:
            hist_sim_h = cv2.compareHist(hist_h1, hist_h2, cv2.HISTCMP_CORREL)
            hist_sim_s = cv2.compareHist(hist_s1, hist_s2, cv2.HISTCMP_CORREL)
            hist_sim_v = cv2.compareHist(hist_v1, hist_v2, cv2.HISTCMP_CORREL)
            avg_hist_diff=(hist_sim_h+hist_sim_s+hist_sim_v)/3.0
            ssim_score = metrics.structural_similarity(frame1_gray, frame2_gray, full=False, channel_axis=None)
    
            if (ssim_score<.7 and avg_hist_diff<0.80) or avg_hist_diff<0.50 or ssim_score<.5:
                print(f"SSIM Score: ", ssim_score,"  hist_diff:",avg_hist_diff,"  Cut time:",cur_frame/fps, "Frame:", cur_frame)
                first_new_frame.append(cur_frame/fps)
                cv2.imshow('FrameBefore', frame2)
                cv2.imshow('FrameAfter', frame1)
                cv2.waitKey(0)

        cur_frame+=1
        frame2 = frame1
        hist_h2=hist_h1
        hist_s2=hist_s1
        hist_v2=hist_v1
        frame2_gray=frame1_gray

        if cv2.waitKey(1) == ord('q'):
            break
    else:
        break

print(first_new_frame)
original_video.release()
cv2.destroyAllWindows()