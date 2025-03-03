#simple shot boundary detection

import cv2
import tkinter
import subprocess

from skimage import metrics
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

cutoff_time= 0.25

def main(input_video, output_folder):
    original_video=cv2.VideoCapture(input_video)
    fps=original_video.get(cv2.CAP_PROP_FPS)
    video_length=original_video.get(cv2.CAP_PROP_FRAME_COUNT)/fps

    cur_frame=1
    first_new_frame=[]
    frame2=None

    while(original_video.isOpened()):
        ret1,frame1=original_video.read()
        if ret1 == True:
            #plays the video 
            #cv2.imshow('Frame', frame1)
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
                    #displays frames determined to be cuts for visual debugging
                    #cv2.imshow('FrameBefore', frame2)
                    #cv2.imshow('FrameAfter', frame1)
                    #cv2.waitKey(0)

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
    for time in first_new_frame:
        if time<cutoff_time or(time>(video_length-cutoff_time)):
            first_new_frame.remove(time)
    first_new_frame.append(video_length)
    first_new_frame.insert(0,0)
    cut_and_paste(first_new_frame, output_folder,input_video, 1/fps)

def cut_and_paste(frame_list, output_path, video_path, frame_length):
        print(video_path)
        video_base_name=video_path.rsplit("/",1)[1].split(".")[0]
        print(frame_list)

        video_number=0
        start_time=None
        for cut_time in frame_list:
            end_time=cut_time
            if start_time is not None:
                with VideoFileClip(video_path) as video:
                    new = video.subclipped(start_time, end_time-frame_length)
                    new.write_videofile(f"{output_path}/{video_base_name+str(video_number)}.mp4", audio_codec='aac')
                print(f"Start Time {start_time} End Time {end_time-frame_length} FilePath {output_path}/{video_base_name+str(video_number)}")
                #
                # A faster version using ffmpeg but options will need to be changed to ensure correct encoding, currently not worth using
                #ffmpeg_extract_subclip(video_path, start_time, end_time-frame_length,outputfile=f"{output_path}/{video_base_name+str(video_number)}.mp4")
            
            start_time=end_time
            video_number+=1



if __name__=="__main__":    
    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    original_video = filedialog.askopenfilename()
    output_folder = filedialog.askdirectory()
    if not original_video or not output_folder:
        print("Select video and folder to place clips")
    else:
        main(original_video,output_folder)