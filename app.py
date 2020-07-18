while True:

    import imutils
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output, State
    import dash_bootstrap_components as dbc
    import flask
    from flask import Flask, Response
    import threading
    import cv2
    import time
    import os
    import matplotlib.pyplot as plt
    import base64
    import dash_daq as daq
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
    import youtube_dl
    from shutil import copyfile
    import shutil
    import glob
    from mhyt import yt_download
    from moviepy.editor import VideoFileClip, concatenate_videoclips
    import sys
    import queue
    from subprocess import getoutput
    from IPython.display import HTML
    from google.colab import drive
    import random
    import string
    from multiprocessing import Process, Queue
    global thread_list
    import subprocess
    global subprocess_list
    subprocess_list = []
    from subprocess import Popen
    import pickle
    import signal
    import dash_editor_components
    from flask import request
    import sys
    sys.path.append('/content/FaceClust')
    import FaceClust.face_clustering as ffc
    global cvt_id
    cvt_id = None
    global open_choose_box
    open_choose_box = False
    global npy_files
    npy_files = [i for i in os.listdir('/tmp') if i.endswith('.npy')]
    from multiprocessing import Process, Value,Manager
    global src_child
    global dst_child
    src_child = ''
    dst_child = ''
    import sys  
    sys.path.append('/content/DeepFaceLab')
    from merger import Merger_tune
    import matplotlib.pyplot as plt
    import numpy as np
    from facelib import FaceType
    global labelsdict
    manager = Manager()
    labelsdict = manager.dict()
    labelsdict['src_face_labels'] = {}
    labelsdict['dst_face_labels'] = {}
    
    class merging_vars:

      def __init__(self, 
                    face_type = None,
                   output_face_scale = 0,
                   super_resolution_power = 0,
                   mask_mode = 3,
                   mode = 'overlay',
                   erode_mask_modifier = 0,
                   blur_mask_modifier = 0,
                   color_transfer_mode = 0,
                   masked_hist_match = True,
                   hist_match_threshold = 255,
                   motion_blur_power = 0,
                   blursharpen_amount = 0,
                   image_denoise_power = 0,
                   bicubic_degrade_power = 0,
                   sharpen_mode = 1,
                   color_degrade_power = 0,
                   horizontal_shear = 0,
                   vertical_shear = 0,
                   horizontal_shift = 0,
                   vertical_shift = 0
                   ):

        self.face_type = face_type
        self.output_face_scale = output_face_scale
        self.super_resolution_power = super_resolution_power
        self.mask_mode = mask_mode
        self.mode = mode
        self.erode_mask_modifier = erode_mask_modifier
        self.blur_mask_modifier = blur_mask_modifier
        self.color_transfer_mode = color_transfer_mode
        self.masked_hist_match = masked_hist_match
        self.hist_match_threshold = hist_match_threshold
        self.motion_blur_power = motion_blur_power
        self.blursharpen_amount = blursharpen_amount
        self.image_denoise_power = image_denoise_power
        self.bicubic_degrade_power = bicubic_degrade_power
        self.sharpen_mode = sharpen_mode
        self.color_degrade_power = color_degrade_power
        self.horizontal_shear = horizontal_shear
        self.vertical_shear = vertical_shear
        self.horizontal_shift = horizontal_shift
        self.vertical_shift = vertical_shift

        
    
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    if os.path.isfile('/content/DeepFaceLab/settings.py'):

        with open('/content/DeepFaceLab/settings.py', 'r') as f:
            
            settings_text = f.read()
                
                
            f.close()
    else:

        settings_text = 'No Settings File Found'

    with open('/tmp/log.txt', 'w') as f:
            f.close()
            
            
    def run_cmd(cmd):
        p = subprocess.Popen("exec " + cmd, shell=True)
        
        
        with open('/tmp/log.txt', 'a') as f:
            f.write(str(p.pid)+ '\n')
            f.close()
            
        p.wait()

    thread_list = []

    if not os.path.isdir('/content/workspace'): os.mkdir('/content/workspace')
    if not os.path.isdir('/content/workspace/data_dst'): os.mkdir('/content/workspace/data_dst')
    if not os.path.isdir('/content/workspace/data_src'): os.mkdir('/content/workspace/data_src')
    if not os.path.isdir('/content/workspace/model'): os.mkdir('/content/workspace/model')
    from inspect import currentframe, getframeinfo

    global convert_id
    convert_id = ''

    class VideoCamera(object):
        def __init__(self):
            self.open = True
            self.fourcc = "VID"
            self.video = cv2.VideoCapture(0)
           # self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
            self.video_out = cv2.VideoWriter('videos/Record/temp.mp4', -1, 20.0, (640,480))
            self.frame_counts = 1

        def __del__(self):
            self.video.release()

        def get_frame(self):
            
            try:
                self.success, self.image = self.video.read()
                ret, jpeg = cv2.imencode('.jpg', self.image)
                return jpeg.tobytes()
            except:
                pass
        
        def record(self):

            timer_start = time.time()
            timer_current = 0

            while(self.open==True):
                try:
                    ret, video_frame = self.success, self.image
                  
                except:
                    break
                if (ret==True):

                        self.video_out.write(video_frame)
                        self.frame_counts += 1
                        time.sleep(1/10)
                else:
                    break

        def stop(self):

            if self.open==True:

                self.open=False
                self.video_out.release()
                self.video.release()
                cv2.destroyAllWindows()

            else: 
                pass


        def start(self):
            video_thread = threading.Thread(target=self.record)
            video_thread.start()


    def gen(camera):
        while camera.open:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def get_sec2time(s):


        hours, rem = divmod(s, 3600)
        minutes, seconds = divmod(rem, 60)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)

        if hours == 0:
          if  minutes <10:
            if seconds <10:
              return '0'+str(minutes)+':0'+str(seconds)
            else:
              return '0'+str(minutes)+':'+str(seconds)
          else:
            return str(minutes)+':'+str(seconds)
        else:
          return str(hours)+':'+str(minutes)+':'+str(seconds)


    def get_interval_func(start_time):

        hours, rem = divmod(time.time()-start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)


        def sec(s):
          if s == 0:
            return ''
          elif s == 1:
            return str(1) + ' second '
          else:
            return str(s) + ' seconds'

        def min(s):
          if s == 0:
            return ''
          elif s == 1:
            return str(1) + ' minute '
          else:
            return str(s) + ' minutes '

        def hour(s):
          if s == 0:
            return ''
          elif s == 1:
            return str(1) + ' hour '
          else:
            return str(s) + ' hours '


        return str(hours)+':'+str(minutes)+':'+str(seconds)#hour(hours) + min(minutes) + sec(seconds)

    class stopWatch:

      def __init__(self):
        pass
      def start(self):
        self.start_time = time.time() 
      def end(self):
        self.end_time = time.time()

      def get_interval(self):
        return get_sec2time(time.time()-self.start_time)

    def Convert():
            
            
          
        output_name = 'result' + '_' + convert_id + '.mp4'

        #print ('###############################' + output_name)

        os.system('echo | python DeepFaceLab/main.py merge --input-dir workspace/data_dst --output-dir workspace/data_dst/merged --output-mask-dir workspace/data_dst/merged_mask --aligned-dir workspace/data_dst/aligned --model-dir workspace/model --model SAEHD')
        os.system('echo | python DeepFaceLab/main.py videoed video-from-sequence --input-dir workspace/data_dst/merged --output-file workspace/'+output_name+' --reference-file workspace/data_dst.mp4 --include-audio')
        os.system('cp /content/workspace/'+output_name+' /content/drive/My\ Drive/')
        # need to install xattr
        
        #print ('###############################' + 'convertion done')
        
       
    

    def save_workspace_data():

      os.system('zip -r -q workspace_'+convert_id+'.zip workspace'); 
      os.system('cp /content/workspace_'+convert_id+'.zip /content/drive/My\ Drive/')
      #print ('###############################' + 'save_workspace_data')

    def save_workspace_model():

      while 1:

        time.sleep(3600*2)

        os.system('zip -ur workspace_'+convert_id+'.zip workspace/model'); os.system('cp /content/workspace_'+convert_id+'.zip /content/drive/My\ Drive/')
        #print ('###############################' + 'save_workspace_model')


    from random import *

    def Main(q, labelsdict, run, option_id):
        
        #print ('############')
        #print (mode)
         
        global option_
        global thread_list
        import os
        global convert_id
        import time
        #print (option_)

        model = [i['label'] for i in option_ if i['value'] == int(option_id)][0]
        

        
        if model == '(1) New Workspace':

            if convert_id == '':
        
                convert_id = (''.join(map(choice,["bcdfghjklmnpqrstvwxz","aeiouy"]*3)))
                
            if len(src_vids_clip)>0 and len(tar_vids_clip)>0:    
                    
                if os.path.isdir('/content/workspace/'):
                    shutil.rmtree('/content/workspace/')

                if not os.path.isdir('/content/workspace'): os.mkdir('/content/workspace')
                if not os.path.isdir('/content/workspace/data_dst'): os.mkdir('/content/workspace/data_dst')
                if not os.path.isdir('/content/workspace/data_src'): os.mkdir('/content/workspace/data_src')
                if not os.path.isdir('/content/workspace/model'): os.mkdir('/content/workspace/model')
                    
                
                q.put('#ID-' + convert_id)
                
                model_name = 'workspace_'+convert_id + '.zip'
                
                q.put('Loading Workspace')
                
                time.sleep(3)
         
                q.put  ('Merging Source Videos')
            
                try:
                
                    source_files_merge = concatenate_videoclips(src_vids_clip)

                    source_files_merge.write_videofile('/content/workspace/data_src.mp4') 
                    
                except:
                
                    q.put('Error during merging source videos! ')
                    
                    return False
                    

                q.put  ('Merging Target Videos')
                
                try:

                    target_files_merge = concatenate_videoclips(tar_vids_clip)

                    target_files_merge.write_videofile('/content/workspace/data_dst.mp4') 
                    
                except:
                
                    q.put('Error during merging target videos! ')
                    
                    return False
                    
                
                q.put  ('Extracting Source frames ')
                p = os.system("echo | python /content/DeepFaceLab/main.py videoed extract-video --input-file /content/workspace/data_src.* --output-dir /content/workspace/data_src/")
                if p != 0: 
                    q.put('Error while extracting source frames! ')
                    return False
                
                q.put  ('Denoising Source frames ')
                p = os.system("echo | python /content/DeepFaceLab/main.py videoed denoise-image-sequence --input-dir /content/workspace/data_src --factor 1")
                if p != 0: 
                    q.put('Error while denoising source frames! ')
                    return False
                
                q.put  ('Extracting Source faces ')
                p = os.system("echo | python /content/DeepFaceLab/main.py extract --input-dir /content/workspace/data_src --output-dir /content/workspace/data_src/aligned --detector s3fd")
                if p != 0: 
                    q.put('Error during extracting source faces! ')
                    return False
                
                #q.put  ('Source frame Sorting ')
                #p = os.system("echo | python /content/DeepFaceLab/main.py sort --input-dir /content/workspace/data_src/aligned --by hist")
                #if p != 0: 
                #    q.put('Error during sorting source faces! ')
                #    return False
                
                
                #q.put  (' Enhancing Source Faces ')
                #p = os.system("echo | python /content/DeepFaceLab/main.py facesettool enhance --input-dir /content/workspace/data_src/aligned")
                #if p != 0: 
                #    q.put('Error during source face enhancement process! ')
                #    return False

                q.put  ('Extracting Target frames ')
                p = os.system("echo | python /content/DeepFaceLab/main.py videoed extract-video --input-file /content/workspace/data_dst.* --output-dir /content/workspace/data_dst/")
                if p != 0: 
                    q.put('Error while extracting target frames! ')
                    return False
                
                q.put  ('Denoising Target frames ')
                p = os.system("echo | python /content/DeepFaceLab/main.py videoed denoise-image-sequence --input-dir /content/workspace/data_dst --factor 1")
                if p != 0: 
                    q.put('Error while denoising target frames! ')
                    return False
                
                q.put  ('Extracting Target faces ')
                p = os.system("echo | python /content/DeepFaceLab/main.py extract --input-dir /content/workspace/data_dst --output-dir /content/workspace/data_dst/aligned --detector s3fd")
                if p != 0: 
                    q.put('Error during extracting target faces! ')
                    return False
                
                
                #q.put  ('Target frame Sorting ')
                #p = os.system("echo | python /content/DeepFaceLab/main.py sort --input-dir /content/workspace/data_dst/aligned --by hist")
                #if p != 0: 
                #    q.put('Error during sorting target faces! ')
                #    return False
                
                #q.put  ('Enhancing Target Faces ')
                #p = os.system("echo | python /content/DeepFaceLab/main.py facesettool enhance --input-dir /content/workspace/data_dst/aligned")
                #if p != 0: 
                #    q.put('Error during target face enhancement process! ')
                #    return False
                
                
                
                labelsdict['src_face_labels'] = ffc.Get_face_clustered_labels('workspace/data_src/aligned')
                labelsdict['dst_face_labels'] = ffc.Get_face_clustered_labels('workspace/data_dst/aligned')
                
                
                run.value = 1
                
                
                while True:
                
                    if run.value:
                    
                        time.sleep(4)
                        
                    else:
                    
                        break
                
                
                q.put  ('Extracting face masks ')
                p = os.system('python face_seg.py')
                if p != 0: 
                    q.put('Error while extracting face masks! ')
                    return False

                q.put  ('Processsing Done')
                thr1 = Process(target = save_workspace_data, args=())
                thr1.daemon=True   
                thr1.start()
                thread_list.append(thr1)


                import os
                os.chdir("/content")


                import psutil, os, time

                thr2 = Process(target = save_workspace_model, args=())
                thr2.daemon=True   
                thr2.start()
                thread_list.append(thr2)

                q.put('Training started')


                p = os.system('echo | python DeepFaceLab/main.py train --training-data-src-dir workspace/data_src/aligned --training-data-dst-dir workspace/data_dst/aligned --pretraining-data-dir pretrain --model-dir workspace/model --model SAEHD')

                if p != 0: 
                    q.put('Error during training process! ')
                    return False
                    
                return True
            else:
            
                q.put('Error! No training data.')
                return False
            
            
        elif model == '(2) Resume Workspace':
        
            
        
            if convert_id == '':
        
                convert_id = (''.join(map(choice,["bcdfghjklmnpqrstvwxz","aeiouy"]*3)))
        
            
            q.put('#ID-' + convert_id)
                
                
            if len(os.listdir('/content/workspace/model/'))>1:
                                
                #q.put('Removing any saved models')
            
                #if os.path.isdir('/content/workspace/model'): shutil.rmtree('/content/workspace/model') 
               
                
                
                thr1 = Process(target = save_workspace_data, args=())
                thr1.daemon=True   
                thr1.start()
                thread_list.append(thr1)


                import os
                os.chdir("/content")


                import psutil, os, time

                thr2 = Process(target = save_workspace_model, args=())
                thr2.daemon=True   
                thr2.start()
                thread_list.append(thr2)

                q.put('Training started')


                p = os.system('echo | python DeepFaceLab/main.py train --training-data-src-dir workspace/data_src/aligned --training-data-dst-dir workspace/data_dst/aligned --pretraining-data-dir pretrain --model-dir workspace/model --model SAEHD')

                if p != 0: 
                    q.put('Error during training process! ')
                    return False
                    
                return True
                
                
                
            else:
            
                if os.path.isfile('/content/workspace/data_dst.mp4') and os.path.isfile('/content/workspace/data_src.mp4'):
                
                    q.put('Loading Workspace')
                    
                    time.sleep(3)


                    q.put  ('Extracting Source frames ')
                    p = os.system("echo | python /content/DeepFaceLab/main.py videoed extract-video --input-file /content/workspace/data_src.* --output-dir /content/workspace/data_src/")
                    if p != 0: 
                        q.put('Error while extracting source frames! ')
                        return False
                    
                    q.put  ('Denoising Source frames ')
                    p = os.system("echo | python /content/DeepFaceLab/main.py videoed denoise-image-sequence --input-dir /content/workspace/data_src --factor 1")
                    if p != 0: 
                        q.put('Error while denoising source frames! ')
                        return False
                    
                    q.put  ('Extracting Source faces ')
                    p = os.system("echo | python /content/DeepFaceLab/main.py extract --input-dir /content/workspace/data_src --output-dir /content/workspace/data_src/aligned --detector s3fd")
                    if p != 0: 
                        q.put('Error during extracting source faces! ')
                        return False
                    
                    q.put  ('Source frame Sorting ')
                    p = os.system("echo | python /content/DeepFaceLab/main.py sort --input-dir /content/workspace/data_src/aligned --by hist")
                    if p != 0: 
                        q.put('Error during sorting source faces! ')
                        return False
                    
                    
                    q.put  (' Enhancing Source Faces ')
                    p = os.system("echo | python /content/DeepFaceLab/main.py facesettool enhance --input-dir /content/workspace/data_src/aligned")
                    if p != 0: 
                        q.put('Error during source face enhancement process! ')
                        return False

                    q.put  ('Extracting Target frames ')
                    p = os.system("echo | python /content/DeepFaceLab/main.py videoed extract-video --input-file /content/workspace/data_dst.* --output-dir /content/workspace/data_dst/")
                    if p != 0: 
                        q.put('Error while extracting target frames! ')
                        return False
                    
                    q.put  ('Denoising Target frames ')
                    p = os.system("echo | python /content/DeepFaceLab/main.py videoed denoise-image-sequence --input-dir /content/workspace/data_dst --factor 1")
                    if p != 0: 
                        q.put('Error while denoising target frames! ')
                        return False
                    
                    q.put  ('Extracting Target faces ')
                    p = os.system("echo | python /content/DeepFaceLab/main.py extract --input-dir /content/workspace/data_dst --output-dir /content/workspace/data_dst/aligned --detector s3fd")
                    if p != 0: 
                        q.put('Error during extracting target faces! ')
                        return False
                    
                    
                    q.put  ('Target frame Sorting ')
                    p = os.system("echo | python /content/DeepFaceLab/main.py sort --input-dir /content/workspace/data_dst/aligned --by hist")
                    if p != 0: 
                        q.put('Error during sorting target faces! ')
                        return False
                    
                    q.put  ('Enhancing Target Faces ')
                    p = os.system("echo | python /content/DeepFaceLab/main.py facesettool enhance --input-dir /content/workspace/data_dst/aligned")
                    if p != 0: 
                        q.put('Error during target face enhancement process! ')
                        return False
                    
                    
                    q.put  ('Extracting face masks ')
                    p = os.system('python face_seg.py')
                    if p != 0: 
                        q.put('Error while extracting face masks! ')
                        return False

                    q.put  ('Processsing Done')
                    thr1 = Process(target = save_workspace_data, args=())
                    thr1.daemon=True   
                    thr1.start()
                    thread_list.append(thr1)


                    import os
                    os.chdir("/content")


                    import psutil, os, time

                    thr2 = Process(target = save_workspace_model, args=())
                    thr2.daemon=True   
                    thr2.start()
                    thread_list.append(thr2)

                    q.put('Training started')


                    p = os.system('echo | python DeepFaceLab/main.py train --training-data-src-dir workspace/data_src/aligned --training-data-dst-dir workspace/data_dst/aligned --pretraining-data-dir pretrain --model-dir workspace/model --model SAEHD')

                    if p != 0: 
                        q.put('Error during training process! ')
                        return False
                        
                    return True
                    
                else:


                    if len(src_vids_clip)>0 and len(tar_vids_clip)>0:
                    
                    
                    
                    
                        if os.path.isdir('/content/workspace/'):
                        
                            shutil.rmtree('/content/workspace/')

                        if not os.path.isdir('/content/workspace'): os.mkdir('/content/workspace')
                        if not os.path.isdir('/content/workspace/data_dst'): os.mkdir('/content/workspace/data_dst')
                        if not os.path.isdir('/content/workspace/data_src'): os.mkdir('/content/workspace/data_src')
                        if not os.path.isdir('/content/workspace/model'): os.mkdir('/content/workspace/model')
                    
                        model_name = 'workspace_'+convert_id + '.zip'
            
                        q.put('Loading Workspace')
                        
                        time.sleep(3)
                 

                        q.put  ('Merging Source Videos')
        
                        try:
                        
                            source_files_merge = concatenate_videoclips(src_vids_clip)

                            source_files_merge.write_videofile('/content/workspace/data_src.mp4') 
                            
                        except:
                        
                            q.put('Error during merging source videos! ')
                            
                            return False
                            

                        q.put  ('Merging Target Videos')
                        
                        try:

                            target_files_merge = concatenate_videoclips(tar_vids_clip)

                            target_files_merge.write_videofile('/content/workspace/data_dst.mp4') 
                            
                        except:
                        
                            q.put('Error during merging target videos! ')
                            
                            return False
                            
                        
                        q.put  ('Extracting Source frames ')
                        p = os.system("echo | python /content/DeepFaceLab/main.py videoed extract-video --input-file /content/workspace/data_src.* --output-dir /content/workspace/data_src/")
                        if p != 0: 
                            q.put('Error while extracting source frames! ')
                            return False
                        
                        q.put  ('Denoising Source frames ')
                        p = os.system("echo | python /content/DeepFaceLab/main.py videoed denoise-image-sequence --input-dir /content/workspace/data_src --factor 1")
                        if p != 0: 
                            q.put('Error while denoising source frames! ')
                            return False
                        
                        q.put  ('Extracting Source faces ')
                        p = os.system("echo | python /content/DeepFaceLab/main.py extract --input-dir /content/workspace/data_src --output-dir /content/workspace/data_src/aligned --detector s3fd")
                        if p != 0: 
                            q.put('Error during extracting source faces! ')
                            return False
                        
                        q.put  ('Source frame Sorting ')
                        p = os.system("echo | python /content/DeepFaceLab/main.py sort --input-dir /content/workspace/data_src/aligned --by hist")
                        if p != 0: 
                            q.put('Error during sorting source faces! ')
                            return False
                        
                        
                        q.put  (' Enhancing Source Faces ')
                        p = os.system("echo | python /content/DeepFaceLab/main.py facesettool enhance --input-dir /content/workspace/data_src/aligned")
                        if p != 0: 
                            q.put('Error during source face enhancement process! ')
                            return False

                        q.put  ('Extracting Target frames ')
                        p = os.system("echo | python /content/DeepFaceLab/main.py videoed extract-video --input-file /content/workspace/data_dst.* --output-dir /content/workspace/data_dst/")
                        if p != 0: 
                            q.put('Error while extracting target frames! ')
                            return False
                        
                        q.put  ('Denoising Target frames ')
                        p = os.system("echo | python /content/DeepFaceLab/main.py videoed denoise-image-sequence --input-dir /content/workspace/data_dst --factor 1")
                        if p != 0: 
                            q.put('Error while denoising target frames! ')
                            return False
                        
                        q.put  ('Extracting Target faces ')
                        p = os.system("echo | python /content/DeepFaceLab/main.py extract --input-dir /content/workspace/data_dst --output-dir /content/workspace/data_dst/aligned --detector s3fd")
                        if p != 0: 
                            q.put('Error during extracting target faces! ')
                            return False
                        
                        
                        q.put  ('Target frame Sorting ')
                        p = os.system("echo | python /content/DeepFaceLab/main.py sort --input-dir /content/workspace/data_dst/aligned --by hist")
                        if p != 0: 
                            q.put('Error during sorting target faces! ')
                            return False
                        
                        q.put  ('Enhancing Target Faces ')
                        p = os.system("echo | python /content/DeepFaceLab/main.py facesettool enhance --input-dir /content/workspace/data_dst/aligned")
                        if p != 0: 
                            q.put('Error during target face enhancement process! ')
                            return False
                        
                        
                        q.put  ('Extracting face masks ')
                        p = os.system('python face_seg.py')
                        if p != 0: 
                            q.put('Error while extracting face masks! ')
                            return False

                        q.put  ('Processsing Done')
                        thr1 = Process(target = save_workspace_data, args=())
                        thr1.daemon=True   
                        thr1.start()
                        thread_list.append(thr1)


                        import os
                        os.chdir("/content")


                        import psutil, os, time

                        thr2 = Process(target = save_workspace_model, args=())
                        thr2.daemon=True   
                        thr2.start()
                        thread_list.append(thr2)

                        q.put('Training started')


                        p = os.system('echo | python DeepFaceLab/main.py train --training-data-src-dir workspace/data_src/aligned --training-data-dst-dir workspace/data_dst/aligned --pretraining-data-dir pretrain --model-dir workspace/model --model SAEHD')

                        if p != 0: 
                            q.put('Error during training process! ')
                            return False
                            
                        return True
                        
                    else:

                        q.put('Error! No training data! ')
                        
                        return False
                        
                    
        elif  int(option_id)>2:
        
        
        
            convert_id = model.split('_')[-1].split('.')[0]
            #print (convert_id)
            
            q.put('#ID-' + convert_id)
            
            model_name = 'workspace_'+convert_id + '.zip'

            if os.path.isfile('/content/workspace/data_dst.mp4') and os.path.isfile('/content/workspace/data_src.mp4'):
            
                q.put('Downlaoding Model' )
        
                import zipfile

                archive = zipfile.ZipFile('/content/drive/My Drive/'+model_name)

                for file in archive.namelist():
                    if file.startswith('workspace/model/'):
                        archive.extract(file, '/content/')
                        
                
                q.put('Loading Workspace')
                
                
                thr1 = Process(target = save_workspace_data, args=())
                thr1.daemon=True   
                thr1.start()
                thread_list.append(thr1)


                import os
                os.chdir("/content")


                import psutil, os, time

                thr2 = Process(target = save_workspace_model, args=())
                thr2.daemon=True   
                thr2.start()
                thread_list.append(thr2)

                q.put('Training started')


                p = os.system('echo | python DeepFaceLab/main.py train --training-data-src-dir workspace/data_src/aligned --training-data-dst-dir workspace/data_dst/aligned --pretraining-data-dir pretrain --model-dir workspace/model --model SAEHD')

                if p != 0: 
                    q.put('Error during training process! ')
                    return False
                    
                return True
                
                
            else:
            
            
                if os.path.isdir('/content/workspace/'):
                    shutil.rmtree('/content/workspace/')

                if not os.path.isdir('/content/workspace'): os.mkdir('/content/workspace')
                if not os.path.isdir('/content/workspace/data_dst'): os.mkdir('/content/workspace/data_dst')
                if not os.path.isdir('/content/workspace/data_src'): os.mkdir('/content/workspace/data_src')
                if not os.path.isdir('/content/workspace/model'): os.mkdir('/content/workspace/model')
                
                q.put('Downlaoding Workspace')
                
                os.system('echo A | unzip /content/drive/My\ Drive/'+model_name)
                
                
                
                q.put('Loading Workspace')
                
                thr1 = Process(target = save_workspace_data, args=())
                thr1.daemon=True   
                thr1.start()
                thread_list.append(thr1)


                import os
                os.chdir("/content")


                import psutil, os, time

                thr2 = Process(target = save_workspace_model, args=())
                thr2.daemon=True   
                thr2.start()
                thread_list.append(thr2)

                q.put('Training started')


                p = os.system('echo | python DeepFaceLab/main.py train --training-data-src-dir workspace/data_src/aligned --training-data-dst-dir workspace/data_dst/aligned --pretraining-data-dir pretrain --model-dir workspace/model --model SAEHD')

                if p != 0: 
                    q.put('Error during training process! ')
                    return False
                    
                return True


    import os

    import logging

    server = Flask(__name__)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://use.fontawesome.com/releases/v5.7.2/css/all.css"])

    global slider_prev_instance 
    slider_prev_instance = [0,1000]


    global threadon 

    threadon = True
    global threadon_ 

    threadon_ = True
    global gui_queue
    gui_queue = Queue() 
    global slider_prev_instance2 
    slider_prev_instance2 = [0,1000]
    global storemsg
    storemsg= ''

    global start
    start = ''
    global tt
    tt = False
    global watch
    watch = stopWatch()

    global tt1
    tt1 = False
    

    global tt2
    tt2 = False
    global msglist 

    global HEIGHT
    HEIGHT = 256

    global src_vids
    src_vids = []
    global tar_vids
    tar_vids = []
    msglist = 'Starting ... '


    global src_vids_clip
    src_vids_clip = []

    global tar_vids_clip
    tar_vids_clip = []
    
    
    global horizontal_shear
    global vertical_shear
    global horizontal_shift
    global vertical_shift
    global ind_preview
    
    horizontal_shear = 0
    vertical_shear = 0
    horizontal_shift = 0
    vertical_shift = 0
    ind_preview = 0

    if not os.path.isdir('videos'): os.mkdir('videos')

    if not os.path.isdir('videos/Source'): os.mkdir('videos/Source')
    if not os.path.isdir('videos/Source/Youtube'): os.mkdir('videos/Source/Youtube')
    if not os.path.isdir('videos/Source/Upload'): os.mkdir('videos/Source/Upload')
    if not os.path.isdir('videos/Source/Record'): os.mkdir('videos/Source/Record')
    if not os.path.isdir('videos/Source/Final'): os.mkdir('videos/Source/Final')

    if not os.path.isdir('videos/Target'): os.mkdir('videos/Target')
    if not os.path.isdir('videos/Target/Youtube'): os.mkdir('videos/Target/Youtube')
    if not os.path.isdir('videos/Target/Upload'): os.mkdir('videos/Target/Upload')
    if not os.path.isdir('videos/Target/Record'): os.mkdir('videos/Target/Record')
    if not os.path.isdir('videos/Target/Final'): os.mkdir('videos/Target/Final')
      

    record = [html.Div(children = [html.Img(src="/video_feed", style={
                'width': '266px',
                'height': '200px'
                }), html.Hr(), dbc.Button("Start", outline=True, color="primary", className="mr-1", id='rec_button')])]
            
    def loading(children):
      return dcc.Loading(children, type='dot', fullscreen=False, style={'opacity': 0.2})	




    def video_index():
      global src_vids_clip
      
      return len(src_vids_clip)

    def video_index2():
      global tar_vids_clip
      return len(tar_vids_clip)

    def duration():
      global src_vids_clip
      return int(sum([i.duration for i in src_vids_clip]))
    def duration2():
      global tar_vids_clip
      return int(sum([i.duration for i in tar_vids_clip]))
      
      
    image_filename = 'images/img1.jpg' # replace with your own image
    img1 = base64.b64encode(open(image_filename, 'rb').read())

    image_filename = 'images/img2.jpg' # replace with your own image
    img2 = base64.b64encode(open(image_filename, 'rb').read())

    image_filename = 'images/img3.jpg' # replace with your own image
    img3 = base64.b64encode(open(image_filename, 'rb').read())


    col1  = dbc.Card(
        [
            dbc.CardBody( html.Div(dbc.Checkbox( id = 'full_face'
                    )), style = {'margin':'auto'}),
            dbc.CardImg(style = {'width' : '80px', 'height' : '80px', 'margin':'auto'}, src='data:image/png;base64,{}'.format(img1.decode()), bottom=True),
        ],
        style={"width": "6rem","height": "8rem"}
    )


    col2  = dbc.Card(
        [
            dbc.CardBody( html.Div(dbc.Checkbox( id = 'head'
                    )), style = {'margin':'auto'}),
            dbc.CardImg(style = {'width' : '80px', 'height' : '80px', 'margin':'auto'}, src='data:image/png;base64,{}'.format(img2.decode()), bottom=True),
        ],
        style={"width": "6rem","height": "8rem"}
    )

    col3  = dbc.Card(
        [
            dbc.CardBody( html.Div(dbc.Checkbox( id = 'half_face'
                    )), style = {'margin':'auto'}),
            dbc.CardImg(style = {'width' : '80px', 'height' : '80px', 'margin':'auto'}, src='data:image/png;base64,{}'.format(img3.decode()), bottom=True),
        ],
        style={"width": "6rem","height": "8rem"})

      
      
      

    global option_  
    option_ = [{"label": '(1) New Workspace', "value" : 0}, {"label": '(2) Resume Workspace', "value" : 1}, {"label": '(3) Load Workspace', "value" : 2, 'disabled': True}]

    for j,idx in enumerate([i for i in os.listdir('/content/drive/My Drive') if i.startswith('workspace')]):

        option_.append({"label": ' ' + idx + ' [' + str(os.path.getsize('/content/drive/My Drive/'+idx) >> 20) +' MB]', "value" : j+3} )


    Progress =  html.Div([dbc.InputGroup(
                [dbc.InputGroupAddon("Model", addon_type="prepend"), dbc.Select(id = 'start_text_input', options = option_, value = '0'), 
                dbc.Button(outline=True, id = 'start_text_continue', active=False, disabled = False, color="success", className="fas fa-check-circle")
        ], 
                size="sm",
            ), dbc.CardDeck([col2, col1, col3])]), #dcc.RadioItems(id = 'Progress_select', value = ''), html.Hr(id = 'hr2'), 
    #dbc.Button('Continue', size="sm", id = 'start_text_continue'), 
    #html.Hr(id = 'hr3'), html.Div(id = 'progress_field')]


    Images = loading([
    dbc.Tabs(
        [
            dbc.Tab(html.Img(id = 'Face', style = {'width' : '100%', 'height' : '100%'}), label="Images-1"),
            dbc.Tab(html.Img(id = 'Mask', style = {'width' : '100%', 'height' : '100%'}), label="Images-2"),
            
        ]), dbc.Button(outline=True, id = 'Images-refresh', active=False, disabled = False, color="success", className="fas fa-redo-alt")]
    )#[(html.Div(id = 'ImagesG'))]
    #Result = [(html.Div(id = 'Result_out'))]

    Settings = loading(html.Div([ dbc.Button(outline=True, id = 'save_settings_file', active=False, disabled = False, color="success", className="fas fa-check-circle"),
        dash_editor_components.PythonEditor(
            id='settings_file', value = settings_text, style = {"overflow": "auto"}
        ),dbc.Tooltip('Save', target="save_settings_file"),
    ]))

    
    choose_face = html.Div([html.Div(id = 'source_imgs_faces'),
    html.Div(id = 'target_imgs_faces'),
    dbc.Button(outline=True, id = 'okay_face_select', active=False, color="success", className="fas fa-check-circle")])
    
    controls_start = dbc.Jumbotron(
        [
            html.H1("Start the Process", id  = 'status'),
            html.P(
                "Generate faceswaped output",
                
                className="lead",
            ),

            dbc.ButtonGroup(
                [dbc.Button(outline=True, id = 'Start-click', active=False, disabled = False, color="success", className="fas fa-hourglass-start"),
    dbc.Button(outline=True, id = 'Images-addclick', active=False,disabled = True, color="primary", className="fas fa-image"),
    dbc.Button(outline=True, id = 'Settings-addclick', active=False,disabled = False, color="primary", className="fas fa-users-cog"),
    dbc.Button(outline=True, id = 'Resetal-addclick', active=False, disabled = False, color="danger", className="fas fa-power-off"),
    dbc.Button(outline=True, id = 'delete-addclick', active=False, disabled = False, color="danger", className="fas fa-trash-alt")],
               
                className="mr-1"),
                
            html.Hr(className="my-2"),
            dbc.Toast(Progress, id="toggle-add-Progress",header="Getting Started",is_open=False,icon="primary",dismissable=True,  style={"maxWidth": "400px"}),
            dbc.Toast(Images, id="toggle-add-Images",header="Generated Images",is_open=False,icon="primary",dismissable=True,  style={"maxWidth": "800px"}),
            dbc.Toast(Settings, id="toggle-add-Settings",header="Edit configuration file",is_open=False,icon="primary",dismissable=True,  style={"maxWidth": "800px"}),
            #dbc.Toast(Result, id="toggle-add-Result",header="Output",is_open=False,icon="primary",dismissable=True),
            dbc.Toast(choose_face, id="toggle-add-face",header="Choose face profile",is_open=False,icon="primary",dismissable=True,  style={"maxWidth": "800px"}),
            html.Hr(className="my-2"),
            #html.P("Don't close this window during the process. You can Play or Download the Generated video anytime by clicking on the Result Tab ", id = 'output_text_3'),
         dcc.Interval(
                id='interval-1',
                interval=5000, # in milliseconds
                n_intervals=0
            )
        ,
            
            
        dbc.Tooltip('Start the process', target="Start-click"),
        dbc.Tooltip('Show generated results', target="Images-addclick"),
        dbc.Tooltip('Stop training', target="Resetal-addclick"),
        dbc.Tooltip('Delete workspace and model', target="delete-addclick"),
        dbc.Tooltip('Edit Configuration file', target="Settings-addclick"),
        
        ]
    )


    upload= loading([(dcc.Upload([
            'Drag and Drop or ',
            html.A('Select a File')
            ], style={
            'width': '100%',
            'height': '100%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
            
            }, id = 'upload-file')),
            (html.Div(id = 'uploading'))])
            
            
    Youtube = loading([dbc.InputGroup(
                [dbc.Input(bs_size="sm", id = 'utube-url'), dbc.Button("Submit", color="primary", id = 'utube-button', size="sm")],
                size="sm",
            ),

        
        (html.Div(id = 'youtube-display'))

    ])	

    #<i class="fab fa-youtube"></i>

    #<i class="fas fa-cloud-upload-alt"></i>

    #<i class="fas fa-trash-restore"></i>



    
    controls = dbc.Jumbotron(
        [
            html.H1(["Source Video" ]),
            html.Hr(),
            html.P(['Total ',dbc.Badge(video_index(), id = 'n_video', color="light", className="ml-1"), 
            ' videos added of', dbc.Badge(str(duration())+'s', id = 'n_sec_video', color="light",
            className="ml-1"), ' duration'], className="lead",
            ),
            
            dbc.ButtonGroup(
                [dbc.Button(outline=True, id = 'Youtube-addclick',active=False, color="primary", className="fab fa-youtube"),
                dbc.Button(outline=True, id = 'Upload-addclick',active=False, color="primary", className="fas fa-cloud-upload-alt"),
                dbc.Button(
                   outline=True, color="danger", disabled = True, active=False,className="fas fa-trash-restore", id = 'Reset-addclick'),
                  ],
          
                className="mr-1"),
        
            html.Hr(className="my-2"),
            dbc.Toast(upload, id="toggle-add-upload",header="Upload your Video",is_open=False,icon="primary",dismissable=True, style={"maxWidth": "500px"}),
            dbc.Toast(Youtube, id="toggle-add-utube",header="Download Video from Youtube",is_open=False,icon="primary",dismissable=True,  style={"maxWidth": "500px"}),
            dbc.Toast(record, id="toggle-add-record",header="Record your own Video",is_open=False,icon="primary",dismissable=True,  style={"maxWidth": "500px"}),
            #html.Hr(className="my-2"),
            #html.P("You haven\'t added any videos. Let\'s add one. You have the option to add video by Upload, Youtube or Webcam", id = 'output_text')
            
            dbc.Tooltip('Add videos from Youtube', target="Youtube-addclick"),
            dbc.Tooltip('Upload from your machine', target="Upload-addclick"),
            dbc.Tooltip('Reset', target="Reset-addclick"),
         
        ]
    )



    upload_= loading([(dcc.Upload([
            'Drag and Drop or ',
            html.A('Select a File')
            ], style={
            'width': '100%',
            'height': '100%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
            
            }, id = 'upload-file_2')),
            (html.Div(id = 'uploading_2'))])
            

            
            
    Youtube_ = loading([dbc.InputGroup(
                [dbc.Input(bs_size="sm", id = 'utube-url_2'), dbc.Button("Submit", color="primary", id = 'utube-button_2', size="sm" )],
                size="sm",
            ),

        
        (html.Div(id = 'youtube-display_2'))

    ])	


    
    controls_ = dbc.Jumbotron(
        [
            html.H1("Target Video"),
            html.Hr(),
            html.P(['Total ',dbc.Badge(video_index(), id = 'n_video_2', color="light", className="ml-1"), 
            ' videos added of', dbc.Badge(str(duration())+'s', id = 'n_sec_video_2', color="light",
            className="ml-1"), ' duration'], className="lead",
            ),
            
            dbc.ButtonGroup(
                [dbc.Button(outline=True, id = 'Youtube-addclick_2',active=False, color="primary", className="fab fa-youtube"),
                dbc.Button(outline=True, id = 'Upload-addclick_2',active=False, color="primary", className="fas fa-cloud-upload-alt"),
                dbc.Button(
                   outline=True, color="danger", disabled = True, active=False,className="fas fa-trash-restore", id = 'Reset-addclick_2'),
                   ],
          
                className="mr-1"),
                
            html.Hr(className="my-2"),
            dbc.Toast(upload_, id="toggle-add-upload_2",header="Upload your Video",is_open=False,icon="primary",dismissable=False,  style={"maxWidth": "500px"}),
            dbc.Toast(Youtube_, id="toggle-add-utube_2",header="Download Video from Youtube",is_open=False,icon="primary",dismissable=False,  style={"maxWidth": "500px"}),
            #dbc.Toast(record, id="toggle-add-record_2",header="Record your own Video",is_open=False,icon="primary",dismissable=False),
            #html.Hr(className="my-2"),
            #html.P("You haven\'t added any videos here. Let\'s add one. You have the option to add video by Upload, Youtube or Webcam", id = 'output_text_2')
            dbc.Tooltip('Add videos from Youtube', target="Youtube-addclick_2"),
            dbc.Tooltip('Upload from your machine', target="Upload-addclick_2"),
            dbc.Tooltip('Reset', target="Reset-addclick_2"),
         
        ]
    )
    #cc =  dbc.Container([dbc.Row([dbc.Col(controls), dbc.Col(controls)])])


    Upload_Tab = dbc.Row(
                [
                    dbc.Col(controls),#width={"size": 6, "offset": 3}
                    dbc.Col(controls_),               
               ],
                align="center",       
                
            )
            
            
    Training_Tab =  dbc.Row(
                [
                
                 dbc.Col(controls_start),
                       
                    
                ],
                align="center",
                  
            )
    print (len(npy_files))
    if len(npy_files)>0:
        convert_disabled = False
        
    else:
        convert_disabled = True
        
    
    size_layout  = dbc.Card(
        dbc.CardBody(
        
        
            [   dbc.Row(daq.Slider(min=0,max=50,value=10,step=1, id = "size_step", size = 150)),
            
                html.Hr(),
             
                dbc.Row(dbc.Button(outline=True, id = 'v_plus_size', active=False, disabled = convert_disabled, color="success", className="fas fa-plus-circle"),justify="center",),
             
                dbc.Row([dbc.Col(dbc.Button(outline=True, id = 'h_minus_size', active=False, disabled = convert_disabled, color="success", className="fas fa-minus-circle")),  dbc.Col(dbc.Button(outline=True, id = 'h_plus_size', active=False, disabled = convert_disabled, color="success", className="fas fa-plus-circle"))]),
          
                dbc.Row(dbc.Button(outline=True, id = 'v_minus_size', active=False, disabled = convert_disabled, color="success", className="fas fa-minus-circle"), justify="center"),
            ]
        ),
        style={"width": "10rem"},
    )



    shift_layout = dbc.Card(
        dbc.CardBody(
            [   dbc.Row(daq.Slider(min=0,max=50,value=10,step=1, id = "shift_step", size = 150)),
                
                html.Hr(),
                
                dbc.Row(dbc.Button(outline=True, id = 'v_plus_shift', active=False, disabled = convert_disabled, color="success", className="fas fa-chevron-circle-up"),justify="center",),
             
                dbc.Row([dbc.Col(dbc.Button(outline=True, id = 'h_minus_shift', active=False, disabled = convert_disabled, color="success", className="fas fa-chevron-circle-left")),  dbc.Col(dbc.Button(outline=True, id = 'h_plus_shift', active=False, disabled = convert_disabled, color="success", className="fas fa-chevron-circle-right"))]),
          
                dbc.Row(dbc.Button(outline=True, id = 'v_minus_shift', active=False, disabled = convert_disabled, color="success", className="fas fa-chevron-circle-down"), justify="center"),
            ]
        ),
        style={"width": "10rem"},
    )
    
    global option_convert  
    option_convert = [{"label": '(1) Current Workspace', "value" : 0}, {"label": '(2) Load Workspace', "value" : 1, 'disabled': True}]

    for j,idx in enumerate([i for i in os.listdir('/content/drive/My Drive') if i.startswith('workspace')]):

        option_convert.append({"label": ' ' + idx + ' [' + str(os.path.getsize('/content/drive/My Drive/'+idx) >> 20) +' MB]', "value" : j+2} )



    Convert_Tab =  dbc.Row([dbc.Card(
        [   
           
            dbc.CardHeader(dbc.InputGroup(
                    [dbc.InputGroupAddon("Model", addon_type="prepend"), dbc.Select(id = 'convert_model_id', options = option_convert, value = '0'), 
                    dbc.Button(outline=True, id = 'convert_model_continue', active=False, disabled = False, color="success", className="fas fa-check-circle")
            , dbc.Button(outline=True, id = 'refresh_img', active=False, disabled = convert_disabled, color="primary", className="fas fa-redo"), 
            dbc.Button(outline=True, id = 'okay_merge', active=False, disabled = convert_disabled, color="danger", className="fas fa-sign-in-alt")], 
                    size="sm",
                )),
         
            html.Div(id = 'convert_result', style = {'text-align' : 'center'}),
            html.Div(id = 'convert_load', style = {'text-align' : 'center'}),
            html.Hr(),
            
            dbc.CardImg(top=True, id = 'Convert_Image'),
            
            dbc.Progress(id = 'merge_progress'),
            
            dcc.Loading(html.Div(id = 'test_div'), type = 'dot'),
            
            #dcc.Loading(html.Div('  ', id = 'test_div'), type = 'circle'),
            dbc.CardBody( 
                
                dbc.InputGroup(
                    [
                    
                    #dbc.Button(outline=True, id = 'mask_mode', active=False, disabled = convert_disabled, color="primary", className="fas fa-theater-masks"),
                    #dbc.Button(outline=True, id = 'mode', active=False, disabled = convert_disabled, color="primary", className="fas fa-cogs"),
                    #dbc.Button(outline=True, id = 'scale_face', active=False, disabled = convert_disabled, color="primary", className="fas fa-arrows-alt"),

                    #dbc.Button(outline=True, id = 'erode_mask_modifier', active=False, disabled = convert_disabled, color="primary", className="fas fa-crop-alt"),
                    #dbc.Button(outline=True, id = 'color_mode', active=False, disabled = convert_disabled, color="primary", className="fas fa-palette"),
                    #dbc.Button(outline=True, id = 'adv_settings', active=False, disabled = convert_disabled, color="primary", className="fas fa-sliders-h"),
                  
                    dbc.Row([dbc.Col(size_layout), dbc.Col(shift_layout)]),
                    
                    ], 
                  
                ),
              
                

            
            ),
        ],
        style={"width": "25rem"}, 
    ),












    dbc.Toast([
    
    dbc.InputGroup([dbc.InputGroupAddon("Face type", addon_type="prepend"),dbc.Select(id = 'face_type_', options = [{'label':'Head', "value" :0},
    {'label':'Face', "value" :1}, 
    {'label':'Full Face', "value" :2}, 
    ], value = '0')], size="sm"),
    
    dbc.InputGroup([dbc.InputGroupAddon("Mask type", addon_type="prepend"),dbc.Select(id = 'mask_mode_', options = [{'label':'dst', "value" :1},
    {'label':'learned-prd', "value" :2}, 
    {'label':'learned-dst', "value" :3}, 
    {'label':'learned-prd*learned-dst', "value" :4}, 
    {'label':'learned-prd+learned-dst', "value" :5},  
    {'label':'XSeg-prd', "value" :6}, 
    {'label':'XSeg-dst', "value" :7},  
    {'label':'XSeg-prd*XSeg-dst', "value" :8}, 
    {'label':'learned-prd*learned-dst*XSeg-prd*XSeg-dst', "value" :9}], value = 3),], size="sm",),
    
    dbc.InputGroup([dbc.InputGroupAddon("Mode", addon_type="prepend"),dbc.Select(id = 'mode_', options = [{'label':'original', "value" :'original'},
    {'label':'overlay', "value" :'overlay'}, 
    {'label':'hist-match', "value" :'hist-match'}, 
    {'label':'seamless', "value" :'seamless'}, 
    {'label':'seamless-hist-match', "value" :'seamless-hist-match'},  
    {'label':'raw-rgb', "value" :'raw-rgb'}, 
    {'label':'raw-predict', "value" :'raw-predict'}], value = 'overlay') ], size="sm",)
    
    ,dbc.InputGroup([dbc.InputGroupAddon("Color mode", addon_type="prepend"),dbc.Select(id = 'color_mode_', options = [{'label':'None', "value" :0},
    {'label':'rct', "value" :1}, 
    {'label':'lct', "value" :2}, 
    {'label':'mkl', "value" :3}, 
    {'label':'mkl-m', "value" :4},  
    {'label':'idt', "value" :5}, 
    {'label':'idt-m', "value" :6},  
    {'label':'sot-m', "value" :7}, 
    {'label':'mix-m', "value" :8}], value = '0')], size="sm"),
    
    
    dbc.Card(
        dbc.CardBody([dcc.Slider(
      min=0,
      max=100,
      value=0,
      step=1,
      id = "motion_blur_power_", marks = {0: '0', 100:'100', 50: 'Motion Blur Power'}
    ),
    
    html.Br(),
    dcc.Slider(
      min=-400,
      max=400,
      value=0,
      step=1,
      id = "Erode_" , marks = {-400: '-400', 0:'Erode', 400:'+400'}
    )
    ,
    html.Br(),
      dcc.Slider(
      min=0,
      max=400,
      value=0,
      step=1,
      id = "Blur_", marks = {0: '0', 200:'Blur', 400:'+400'}
    )
    ,
    html.Br(),
      dcc.Slider(
      min=-100,
      max=100,
      value=0,
      step=1,
      id = "blursharpen_amount_",  marks = {-100: '-100', 100:'100', 0: 'Blur-sharpen Amount'}
    )
    ,
    html.Br(),
      dcc.Slider(
      min=0,
      max=500,
      value=0,
      step=1,
      id = "image_denoise_power_",  marks = {0: '0', 500:'500', 250: 'Image Denoise Power'}
    )
    ,   
    html.Br(),
      dcc.Slider(
      min=0,
      max=100,
      value=0,
      step=1,
      id = "color_degrade_power_",  marks = {0: '0', 100:'100', 50: 'Color Degrade Power'}
    )])),
    
], id="Settings_toggle_",header="Advanced Settings",is_open=True,icon="primary",dismissable=False, style={"maxWidth": "400px"})]),
    
   




    
    
    
    
    
    
    
    
    
    tabs = html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(Upload_Tab, label="Upload", tab_id="tab-1"),
                    dbc.Tab(Training_Tab, label="Train/Resume", tab_id="tab-2"),
                    dbc.Tab(Convert_Tab, label="Convert", tab_id="tab-3"),
                ],
                id="tabs",
                active_tab="tab-1",
            ),
            html.Div(id="content"),
        ]
    )


    modal_error = dbc.Modal(
                [
                    dbc.ModalHeader("Unexpected Error!"),
                    dbc.ModalBody(id = 'modal_error_details'),
                    dbc.ModalFooter(
                        html.A(dbc.Button("Refresh", id="Refresh_error"), href='/')
                    ),
                ],
                id="modal_error",
            )
    



    


    app.layout = dbc.Container(
        [
            html.H1(["Deep", dbc.Badge("Fakes", className="ml-1")],  style={"text-align":"center"}),
            
            tabs,
            
            modal_error,
            
            html.Div(id = 'temp1', style = {'display': 'none'})    ,
            html.Div(id = 'temp2', style = {'display': 'none'}),
            html.Div(id = 'temp1_2', style = {'display': 'none'})    ,
            html.Div(id = 'temp2_2', style = {'display': 'none'}),
            html.Div(id = 'tempvar', style = {'display': 'none'}), 
            html.Div(id = 'refresh__', style = {'display': 'none'})   ,
            html.Div(id = 'confirm_delete', style = {'display': 'none'})                    
    ],fluid=True, style = {'width':'60%'}
    )




    @app.callback(
        Output("toggle-add-upload", "is_open"),
        [Input("Upload-addclick", "n_clicks")], [State("toggle-add-upload", "is_open")]
    )
    def open_toast2(n, is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        if n:
            return not is_open
        else:
            return  is_open



    @app.callback(
        Output("Upload-addclick", "active"),
        [Input("toggle-add-upload", "is_open")]
    )
    def open_toast2(is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        return is_open


    @app.callback(
        Output("toggle-add-utube", "is_open"),
        [Input("Youtube-addclick", "n_clicks")], [State("toggle-add-utube", "is_open")]
    )
    def open_toast2(n, is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        if n:
            return not is_open
        else:
            return  is_open



    @app.callback(
        Output("Youtube-addclick", "active"),
        [Input("toggle-add-utube", "is_open")]
    )
    def open_toast2(is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        return is_open
        
        
    @app.callback(
        [Output("toggle-add-record", "is_open"), Output("Record-addclick", "active")],
        [Input("Record-addclick", "n_clicks")],[State("toggle-add-record", "is_open"), State("Record-addclick", "active")]
    )
    def open_toast3(n, is_open, is_active):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        if n:
            return not is_open, not is_active
        else:
            return  is_open,  is_active
            
            
            
  
   
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

    @server.route('/video_feed')
    def video_feed():
        global camera 
        camera = VideoCamera()
        if camera.open:
            return Response(gen(camera),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.callback(
        [Output('rec_button', 'children'),Output("Record-addclick", "n_clicks")],
        [Input('rec_button', 'n_clicks')],
        [State('rec_button', 'children')])

    def update_button(n_clicks, butt):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        
        global camera
        
        if n_clicks is not None:
            
            if n_clicks%3==1:
                camera.start()

                return 'Stop', 1

            elif n_clicks%3==2:

                camera.stop()
                return 'Add', 1

            elif n_clicks%3==0:
              
           
                copyfile('videos/Source/Record/temp.mp4', 'videos/Source/final/temp'+str(video_index())+'.mp4')
                return 'Added Successfully', 2



            
        else:
            return butt, 0
        

        
    @app.callback(
        Output('uploading', 'children'),
        [Input('upload-file', 'contents')])


    def update_upload(data):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        
        if data is not None:
            content_type, content_string = data.split(',')

            decoded = base64.b64decode(content_string)
            ##print (decoded)
            with open('videos/Source/Upload/temp.mp4', "wb") as fp:
                fp.write(decoded)
            global src_vids
            global HEIGHT

            VID = VideoFileClip('videos/Source/Upload/temp.mp4')
            #VID = VID.resize((int((VID.aspect_ratio*HEIGHT)//2)*2, HEIGHT))
            src_vids.append(VID)

            frame = VID.get_frame(0)

            frame = imutils.resize(frame, height=64)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ret, frame = cv2.imencode('.png', frame)

            frame = base64.b64encode(frame)

            return html.Div( 
                [html.Hr(), html.Img(id = 'playback', style={
                'width': '100%',
                'height': '100%', 'padding-left':'8.5%', 'padding-right':'8.5%'
                }, src = 'data:image/png;base64,{}'.format(frame.decode())), dcc.RangeSlider(
                    id='my-range-slider',
                    min=0,
                    max=1000,
                    step=1,
                    value=[1, 999], marks = {0: '0:00', 1000: get_sec2time(VID.duration)}),
                     dbc.Button(["+",  dbc.Badge(str(int(VID.duration)), id = 'n_upload', color="primary", className="ml-1")], id='crop_button', color="light", size="sm",  style = {'margin-top': '-20px', 'margin-left': '39%', 'font-weight': 'bold'})])

      

        
    @app.callback(
        Output('youtube-display', 'children'),
        [Input('utube-button', 'n_clicks')],[State('utube-url', 'value')])


    def update_youtube(n, url):
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        
        
        if n is not None:
            ytdl_format_options = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'videos/Source/Youtube/temp'
               
            }
            
            files = glob.glob('videos/Source/Youtube/temp*')
            if len(files)>0:
                for i in files:
                    os.remove(i)
            
            
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                 ydl.download([url])

            global src_vids
            global HEIGHT

            VID = VideoFileClip('videos/Source/Youtube/temp.mp4')
            #VID = VID.resize((int((VID.aspect_ratio*HEIGHT)//2)*2, HEIGHT))
            src_vids.append(VID)
            frame = VID.get_frame(0)

            frame = imutils.resize(frame, height=64)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ret, frame = cv2.imencode('.png', frame)

            frame = base64.b64encode(frame)
            
     
            
            return html.Div( 
                [html.Hr(), html.Img(id = 'playback_utube', style={
                'width': '100%',
                'height': '100%','padding-left':'8.5%', 'padding-right':'8.5%'
                }, src = 'data:image/png;base64,{}'.format(frame.decode())), dcc.RangeSlider(
                    id='my-range-slider_utube',
                    min=0,
                    max=1000,
                    step=1,
                    value=[1, 999], marks = {0: '0:00', 1000: get_sec2time(VID.duration)}), 
                    dbc.Button(['+', dbc.Badge(str(int((VID.duration))), id = 'n_utube', color="primary", className="ml-1")],id='crop_button_utube', 
    color="light", size="sm",  style = {'margin-top': '-20px', 'margin-left': '39%', 'font-weight': 'bold'})])




    @app.callback(
        [
         
         Output("Reset-addclick", "disabled"),
         Output("n_video", "children"),
         Output("n_sec_video", "children")],
        [Input('temp1', 'children'), 
         Input('temp2', 'children'),
         Input('Reset-addclick', 'n_clicks'),
         Input('Resetal-addclick', 'n_clicks'),
         Input('delete-addclick', 'n_clicks')],

         [
         State("Reset-addclick", "disabled"),
         State("n_video", "children"),
         State("n_sec_video", "children")]
         )

    def update_details(t1, t2, n, n1, n2, s2, s3, s4):

      print('######################################################')
      print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
      print('######################################################')


      trigger_id = dash.callback_context.triggered[0]['prop_id']
      trgger_value = dash.callback_context.triggered[0]['value']
      global src_vids_clip
       
      global src_vids
        
      global tar_vids_clip
        
      global tar_vids
      
      
      if trigger_id == 'Resetal-addclick.n_clicks':
        
       
        src_vids_clip = []
       
        #src_vids = []
        
        tar_vids_clip = []
        
        #tar_vids = []
        
        #shutil.rmtree('videos/Source/Final'); os.mkdir('videos/Source/Final')

        
        
        global thread_list
        
        
        print (subprocess_list)
        print (thread_list)
        
        for i in thread_list:

            i.terminate() 
                
            #if os.path.isdir('/content/workspace/'):
            #    shutil.rmtree('/content/workspace/')

            #if not os.path.isdir('/content/workspace'): os.mkdir('/content/workspace')
            #if not os.path.isdir('/content/workspace/data_dst'): os.mkdir('/content/workspace/data_dst')
            #if not os.path.isdir('/content/workspace/data_src'): os.mkdir('/content/workspace/data_src')
            #if not os.path.isdir('/content/workspace/model'): os.mkdir('/content/workspace/model')
                
        #threading.Thread(target=resetall, args=(), daemon=True).start()
        
       
        
        
        with open('/tmp/log.txt', 'r') as f:
            pids = [i[:-1] for i in f.readlines()] 
            f.close()
        
        print (pids)
        
        for pid_ in pids:
        
            try:
                os.kill(int(pid_), signal.SIGTERM)
                
                print ('Ended')
                
            except:
                pass
            
        return  [ True, str(video_index()), str(duration()) + 's']
      
      
      if trigger_id == 'delete-addclick.n_clicks':
        
       
        
        
        #tar_vids = []
        
        #shutil.rmtree('videos/Source/Final'); os.mkdir('videos/Source/Final')

     

                
        if os.path.isdir('/content/workspace/'):
            shutil.rmtree('/content/workspace/')

        if not os.path.isdir('/content/workspace'): os.mkdir('/content/workspace')
        if not os.path.isdir('/content/workspace/data_dst'): os.mkdir('/content/workspace/data_dst')
        if not os.path.isdir('/content/workspace/data_src'): os.mkdir('/content/workspace/data_src')
        if not os.path.isdir('/content/workspace/model'): os.mkdir('/content/workspace/model')
                

        

        
        return  [ True, str(video_index()), str(duration()) + 's']

      elif trigger_id == 'Reset-addclick.n_clicks':
      
        src_vids_clip = []
        #src_vids = []
        
        #shutil.rmtree('videos/Source/Final'); os.mkdir('videos/Source/Final')

        output = 'You have added total ' + str(video_index()) + ' video(s). You can add more videos' 

        return  [True, str(video_index()), str(duration()) + 's']

      elif t1 == 'True' or t2 == 'True':

        output = 'You have added total ' + str(video_index()) + ' video(s). You can add more videos' 
        #print ('ffff')

        return [ False, str(video_index()), str(duration()) + 's']

      else:
        return [s2, s3, s4]








    @app.callback(
        [Output('playback_utube', 'src'),
         #Output("Youtube-addclick", "n_clicks"), 
         Output("temp1", "children"),
         Output("n_utube", "children"),
         Output("my-range-slider_utube", "marks")],
        [Input('my-range-slider_utube', 'value'), 
         Input('crop_button_utube', 'n_clicks') 
         ],[State('playback_utube', 'src')])

    def upload_playback_utube(rang, n_clicks, s):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        global src_vids
        global src_vids_clip
        
        
     
        VID = src_vids[-1]
        


        #cap = cv2.VideoCapture(file)

        fps = VID.fps 

        T = VID.duration
        #fps = cap.get(cv2.CAP_PROP_FPS)

        totalNoFrames = T*fps

        trigger_id = dash.callback_context.triggered[0]['prop_id']
        trgger_value = dash.callback_context.triggered[0]['value']

     
        if trigger_id == 'crop_button_utube.n_clicks':
            
           
       
            #print (n_clicks)
            
            #res, frame = cap.read()
            #frame = cv2.resize(frame, (100, 70),interpolation=cv2.INTER_CUBIC)
            #ret, frame = cv2.imencode('.png', frame)
            #frame = base64.b64encode(frame)
            ##print (rang)
            str_time = T*rang[0]/1000
            end_time = T*rang[1]/1000
            VID = VID.subclip(str_time, end_time)


            #del src_vids[-1]

            src_vids_clip.append(VID)

         
            
            #cap.release()
            output = 'You have added total ' + str(video_index()) + ' video(s). You can add more videos.' 

            length = VID.duration
            #print ('jkbdasflsfkafbkasbkfasaskasksbkabkaj' )
            #print (length)

            return [s, 'True', str(int((length))) + 's', {0: get_sec2time(str_time), 1000: get_sec2time(end_time)}]


            
        else:
            
            global slider_prev_instance 
        
      
            #print (totalNoFrames)
            if slider_prev_instance[0] == rang[0]:
                time_n = int(T*rang[1]/1000)
            elif slider_prev_instance[1] == rang[1]:
                time_n = int(T*rang[0]/1000)
            else:
                time_n = int(T*rang[0]/1000)

            slider_prev_instance = rang


            #cap.set(1, frame_number)

            #res, frame = cap.read()

            frame = VID.get_frame(time_n)

            frame = imutils.resize(frame, height=64)

            str_time = T*rang[0]/1000
            end_time = T*rang[1]/1000


            #frame = cv2.resize(frame, (100, 70),interpolation=cv2.INTER_CUBIC)

            ##print (res)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ret, frame = cv2.imencode('.png', frame)
            #frame = cv2.resize(frame, (128,128))
            length = end_time - str_time
            frame = base64.b64encode(frame)
            
            return ['data:image/png;base64,{}'.format(frame.decode()),'False', str(int((length))) + 's', {0: get_sec2time(str_time), 1000: get_sec2time(end_time)}]



    @app.callback(
        [Output('playback', 'src'), 
         #Output("Upload-addclick", "n_clicks"), 
         Output("temp2", "children"),
         Output("n_upload", "children"),
         Output("my-range-slider", "marks")],
        [Input('my-range-slider', 'value'), Input('crop_button', 'n_clicks')],[State('playback', 'src')])

    def upload_playback(rang,n_clicks,s):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        
        global src_vids
        global src_vids_clip
        
        
     
        VID = src_vids[-1]
        


        #cap = cv2.VideoCapture(file)

        fps = VID.fps 

        T = VID.duration
        #fps = cap.get(cv2.CAP_PROP_FPS)

        totalNoFrames = T*fps
        
        trigger_id = dash.callback_context.triggered[0]['prop_id']
        trgger_value = dash.callback_context.triggered[0]['value']

     
        if trigger_id == 'crop_button.n_clicks':


            str_time = T*rang[0]/1000
            end_time = T*rang[1]/1000
            VID = VID.subclip(str_time, end_time)
            src_vids_clip.append(VID)
            length = VID.duration
            output = 'You have added total ' + str(video_index()) + ' video(s). You can add more videos' 
        
            return [s, 'True',str(int((length))) + 's', {0: get_sec2time(str_time), 1000: get_sec2time(end_time)}]
            
        else:
            
            global slider_prev_instance 
        
      
            #print (totalNoFrames)
            if slider_prev_instance[0] == rang[0]:
                time_n = int(T*rang[1]/1000)
            elif slider_prev_instance[1] == rang[1]:
                time_n = int(T*rang[0]/1000)
            else:
                time_n = int(T*rang[0]/1000)

            slider_prev_instance = rang
            frame = VID.get_frame(time_n)

            frame = imutils.resize(frame, height=64)

            str_time = T*rang[0]/1000
            end_time = T*rang[1]/1000


            #frame = cv2.resize(frame, (100, 70),interpolation=cv2.INTER_CUBIC)

            ##print (res)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ret, frame = cv2.imencode('.png', frame)

            frame = base64.b64encode(frame)
            length = end_time - str_time

            return ['data:image/png;base64,{}'.format(frame.decode()), 'False', str(int((length))) + 's', {0: get_sec2time(str_time), 1000: get_sec2time(end_time)}]










    @app.callback(
        Output("toggle-add-upload_2", "is_open"),
        [Input("Upload-addclick_2", "n_clicks")], [State("toggle-add-upload_2", "is_open")]
    )
    def open_toast2(n, is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        if n:
            return not is_open
        else:
            return  is_open



    @app.callback(
        Output("Upload-addclick_2", "active"),
        [Input("toggle-add-upload_2", "is_open")]
    )
    def open_toast2(is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        return is_open

    @app.callback(
        Output("toggle-add-utube_2", "is_open"),
        [Input("Youtube-addclick_2", "n_clicks")], [State("toggle-add-utube_2", "is_open")]
    )
    def open_toast2(n, is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        if n:
            return not is_open
        else:
            return  is_open



    @app.callback(
        Output("Youtube-addclick_2", "active"),
        [Input("toggle-add-utube_2", "is_open")]
    )
    def open_toast2(is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        return is_open

        
    @app.callback(
        [Output("toggle-add-record_2", "is_open"), Output("Record-addclick_2", "active")],
        [Input("Record-addclick_2", "n_clicks")],[State("toggle-add-record_2", "is_open"), State("Record-addclick_2", "active")]
    )
    def open_toast3(n, is_open, is_active):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        if n:
            return not is_open, not is_active
        else:
            return  is_open,  is_active

    @server.route('/video_feed_')
    def video_feed_():
        global camera 
        camera = VideoCamera()
        if camera.open:
            return Response(gen(camera),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.callback(
        [Output('rec_button_2', 'children'),Output("Record-addclick_2", "n_clicks")],
        [Input('rec_button_2', 'n_clicks')],
        [State('rec_button_2', 'children')])

    def update_button(n_clicks, butt):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        
        global camera
        
        if n_clicks is not None:
            
            if n_clicks%3==1:
                camera.start()

                return 'Stop', 1

            elif n_clicks%3==2:

                camera.stop()
                return 'Add', 1

            elif n_clicks%3==0:
          
                copyfile('videos/Target/Record/temp.mp4', 'videos/Target/final/temp'+str(video_index2())+'.mp4')
                return 'Added Successfully', 2



            
        else:
            return butt, 0
        
    @app.callback(
        [
         
         Output("Reset-addclick_2", "disabled"),
         Output("n_video_2", "children"),
         Output("n_sec_video_2", "children")],
        [Input('temp1_2', 'children'), 
         Input('temp2_2', 'children'),
         Input('Reset-addclick_2', 'n_clicks')],

         [
         State("Reset-addclick_2", "disabled"),
         State("n_video_2", "children"),
         State("n_sec_video_2", "children")]
         )
    def update_details(t1, t2, n, s2, s3, s4):

      print('######################################################')
      print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
      print('######################################################')

      trigger_id = dash.callback_context.triggered[0]['prop_id']
      trgger_value = dash.callback_context.triggered[0]['value']

      if trigger_id == 'Reset-addclick_2.n_clicks':

        
        #global tar_vids
        #tar_vids = []
        global tar_vids_clip
        tar_vids_clip = []
        #output = 'You have added total ' + str(video_index2()) + ' video(s). You can add more videos' 

        return  [True, str(video_index2()), str(duration2()) + 's']

      elif t1 == 'True' or t2 == 'True':

        #output = 'You have added total ' + str(video_index2()) + ' video(s). You can add more videos' 
        #print ('ffff')

        return [ False, str(video_index2()), str(duration2()) + 's']

      else:
        return [s2, s3, s4]

        
    @app.callback(
        Output('uploading_2', 'children'),
        [Input('upload-file_2', 'contents')])


    def update_upload(data):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        
        if data is not None:
            content_type, content_string = data.split(',')

            decoded = base64.b64decode(content_string)
            ##print (decoded)
            with open('videos/Target/Upload/temp.mp4', "wb") as fp:
                fp.write(decoded)
                
            global tar_vids
            global HEIGHT

            VID = VideoFileClip('videos/Target/Upload/temp.mp4')
            #VID = VID.resize((int((VID.aspect_ratio*HEIGHT)//2)*2, HEIGHT))
            tar_vids.append(VID)
            frame = VID.get_frame(0)

            frame = imutils.resize(frame, height=64)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ret, frame = cv2.imencode('.png', frame)

            frame = base64.b64encode(frame)
            
            return html.Div( 
                [html.Hr(), html.Img(id = 'playback_2', style={
                'width': '100%',
                'height': '100%', 'padding-left':'8.5%', 'padding-right':'8.5%'
                }, src = 'data:image/png;base64,{}'.format(frame.decode())), dcc.RangeSlider(
                    id='my-range-slider_2',
                    min=0,
                    max=1000,
                    step=1,
                    value=[1, 999],marks = {0: '0:00', 1000: get_sec2time(VID.duration)}),  dbc.Button(['+', dbc.Badge(str(int((VID.duration))), id = 'n_upload_2', color="primary", className="ml-1")], id ='crop_button_2',
                                                                                              color="light", size="sm",  style = {'margin-top': '-20px', 'margin-left': '39%', 'font-weight': 'bold'})])
      

        
    @app.callback(
        Output('youtube-display_2', 'children'),
        [Input('utube-button_2', 'n_clicks')],[State('utube-url_2', 'value')])


    def update_youtube(n, url):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        
        
        if n is not None:
            ytdl_format_options = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'videos/Target/Youtube/temp'
               
            }
            
            files = glob.glob('videos/Target/Youtube/temp*')
            if len(files)>0:
                for i in files:
                    os.remove(i)
            
            
            with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                 ydl.download([url])
                 
            global tar_vids
            global HEIGHT

            VID = VideoFileClip('videos/Target/Youtube/temp.mp4')
            #VID = VID.resize((int((VID.aspect_ratio*HEIGHT)//2)*2, HEIGHT))
            tar_vids.append(VID)
            
            frame = VID.get_frame(0)

            frame = imutils.resize(frame, height=64)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ret, frame = cv2.imencode('.png', frame)

            frame = base64.b64encode(frame)
            
            return html.Div( 
                [html.Hr(), html.Img(id = 'playback_utube_2', style={
                'width': '100%',
                'height': '100%','padding-left':'8.5%', 'padding-right':'8.5%'
                }, src = 'data:image/png;base64,{}'.format(frame.decode())), dcc.RangeSlider(
                    id='my-range-slider_utube_2',
                    min=0,
                    max=1000,
                    step=1,
                    value=[1, 999], marks = {0: '0:00', 1000: get_sec2time(VID.duration)}), dbc.Button(["+", dbc.Badge(str(int((VID.duration))), id = 'n_utube_2', color="primary", className="ml-1")], id = 'crop_button_utube_2',
                                                                                              color="light", size="sm",  style = {'margin-top': '-20px', 'margin-left': '39%', 'font-weight': 'bold'})])


        



    @app.callback(
        [Output('playback_utube_2', 'src'),
         #Output("Youtube-addclick_2", "n_clicks"), 
         Output("temp1_2", "children"),
         Output("n_utube_2", "children"),
         Output("my-range-slider_utube_2", "marks")],
        [Input('my-range-slider_utube_2', 'value'), 
         Input('crop_button_utube_2', 'n_clicks')]
         ,[State('playback_utube_2', 'src')])

    def upload_playback_utube(rang, n_clicks, s):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        
        global tar_vids
        global tar_vids_clip
        
        
     
        VID = tar_vids[-1]

        trigger_id = dash.callback_context.triggered[0]['prop_id']
        
        #print ('#############################################################################################3')
        #print (trigger_id)
        trgger_value = dash.callback_context.triggered[0]['value']
        fps = VID.fps 

        T = VID.duration
        totalNoFrames = T*fps
     
        if trigger_id == 'crop_button_utube_2.n_clicks':
        
            str_time = T*rang[0]/1000
            end_time = T*rang[1]/1000
            VID = VID.subclip(str_time, end_time)
            tar_vids_clip.append(VID)
         
        
            output = 'You have added total ' + str(video_index2()) + ' video(s). You can add more videos' 
            length = VID.duration

            

            return [s, 'True', str(int((length))) + 's', {0: get_sec2time(str_time), 1000: get_sec2time(end_time)}]


            
        else:
            
            global slider_prev_instance2 
        
      
            #print (totalNoFrames)
            if slider_prev_instance2[0] == rang[0]:
                time_n = int(T*rang[1]/1000)
            elif slider_prev_instance2[1] == rang[1]:
                time_n = int(T*rang[0]/1000)
            else:
                time_n = int(T*rang[0]/1000)

            slider_prev_instance2 = rang
            
            frame = VID.get_frame(time_n)

            frame = imutils.resize(frame, height=64)

            str_time = T*rang[0]/1000
            end_time = T*rang[1]/1000

            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ret, frame = cv2.imencode('.png', frame)
            #frame = cv2.resize(frame, (128,128))
            length = end_time - str_time
            frame = base64.b64encode(frame)
            
            return ['data:image/png;base64,{}'.format(frame.decode()), 'False', str(int((length))) + 's', {0: get_sec2time(str_time), 1000: get_sec2time(end_time)}]



    @app.callback(
        [Output('playback_2', 'src'), 
         #Output("Upload-addclick_2", "n_clicks"), 
         Output("temp2_2", "children"),
         Output("n_upload_2", "children"),
         Output("my-range-slider_2", "marks")],
        [Input('my-range-slider_2', 'value'), Input('crop_button_2', 'n_clicks')],[State('playback_2', 'src')])

    def upload_playback(rang,n_clicks,s):

        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        
        global tar_vids
        global tar_vids_clip
        
        
     
        VID = tar_vids[-1]
        fps = VID.fps 

        T = VID.duration
        #fps = cap.get(cv2.CAP_PROP_FPS)

        totalNoFrames = T*fps
        
        trigger_id = dash.callback_context.triggered[0]['prop_id']
        trgger_value = dash.callback_context.triggered[0]['value']

     
        if trigger_id == 'crop_button_2.n_clicks':

        
            str_time = T*rang[0]/1000
            end_time = T*rang[1]/1000
            VID = VID.subclip(str_time, end_time)


            #del src_vids[-1]

            tar_vids_clip.append(VID)
            
            length = VID.duration
            output = 'You have added total ' + str(video_index2()) + ' video(s). You can add more videos' 
        
            return [s,  'True',str(int((length))) + 's', {0: get_sec2time(str_time), 1000: get_sec2time(end_time)}]
            
        else:
            
            global slider_prev_instance 
        
      
            #print (totalNoFrames)
            if slider_prev_instance[0] == rang[0]:
                time_n = int(T*rang[1]/1000)
            elif slider_prev_instance[1] == rang[1]:
                time_n = int(T*rang[0]/1000)
            else:
                time_n = int(T*rang[0]/1000)

            slider_prev_instance = rang
            frame = VID.get_frame(time_n)

            frame = imutils.resize(frame, height=64)

            str_time = T*rang[0]/1000
            end_time = T*rang[1]/1000


            #frame = cv2.resize(frame, (100, 70),interpolation=cv2.INTER_CUBIC)

            ##print (res)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           
            ret, frame = cv2.imencode('.png', frame)

            frame = base64.b64encode(frame)
            length = end_time - str_time

            return ['data:image/png;base64,{}'.format(frame.decode()),  'False', str(int((length))) + 's', {0: get_sec2time(str_time), 1000: get_sec2time(end_time)}]




    @app.callback(
        Output("toggle-add-Images", "is_open"),
        [Input("Images-addclick", "n_clicks")],[State("toggle-add-Images", "is_open")]
    )
    def open_toast1(n, is_open):
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        try:
            if n>0:
                return not is_open
            else:
                return is_open
        except:
            return is_open



    @app.callback(
        Output("Images-addclick", "active"),
        [Input("toggle-add-Images", "is_open")]
    )
    def open_toast2(is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        return is_open
        



    @app.callback(
        Output("toggle-add-Settings", "is_open"),
        [Input("Settings-addclick", "n_clicks")], [State("toggle-add-Settings", "is_open")]
    )
    def open_toast2(n, is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        if n:
            return not is_open
        else:
            return  is_open



    @app.callback(
        Output("Settings-addclick", "active"),
        [Input("toggle-add-Settings", "is_open")]
    )


    def open_toast2(is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        return is_open


    @app.callback(
        Output("settings_file", "value"),
        [Input("save_settings_file", "n_clicks")], [State("settings_file", "value")]
    )

    def update_settings(n, text):

        with open('/content/DeepFaceLab/settings.py', 'w') as f:
        
            f.write(text)
            
            
            f.close()

        
        return text
        


    @app.callback([Output("Face", "src"),Output("Mask", "src")],
                  
        [Input('Images-addclick', 'n_clicks'), Input('Images-refresh', 'n_clicks')])

    def update_images(n, n2):
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')


        jpgs = glob.glob('workspace/model/*.jpg')
        
        #print (jpgs)
        
        if len(jpgs)>1:
            
            img1 = cv2.imread(jpgs[0])
            #img1 = imutils.resize(img1, height = 256)
            ret, img1 = cv2.imencode('.jpg', img1)
            
            img1 = base64.b64encode(img1)
            src1 = 'data:image/jpg;base64,{}'.format(img1.decode())
            
        

            img2 = cv2.imread(jpgs[1])
            #img2 = imutils.resize(img2, height = 256)
            ret, img2 = cv2.imencode('.jpg', img2)
            img2 = base64.b64encode(img2)
            src2 = 'data:image/jpg;base64,{}'.format(img2.decode())
            return [src2, src1]
        
        else:
        
            return ['','']

        

        
        
    @app.callback(
        Output("toggle-add-Progress", "is_open"),
        [Input("Start-click", "n_clicks")],[State("toggle-add-Progress", "is_open")]
    )
    def open_toast1(n, is_open):
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')
        try:
            if n>0:
                return not is_open
            else:
                return is_open
        except:
            return is_open



    @app.callback(
        Output("Start-click", "active"),
        [Input("toggle-add-Progress", "is_open")]
    )
    def open_toast2(is_open):
        #print ('utubessssff')
        
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        return is_open
        

            
    @app.callback(Output("tempvar", "value"), [Input('Start-click', 'n_clicks')])

    def update_var(inf):
        print('######################################################')
        print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
        print('######################################################')

        return ''

            
    @app.callback(Output('refresh__', 'children'),
                  [Input('Refresh_error', 'n_clicks')])
    def display_page(n):
        if n:
            shutdown()
        
        



      
    @app.callback( [
                    Output('Images-addclick', 'disabled'), 
                    Output('status', 'children'), 
                    #Output("progress_field", "children"),
                    Output("toggle-add-Progress", "header"),
                   # Output("Progress_select", "style"),
                    Output("start_text_continue", "disabled"),
                    Output("start_text_input", "disabled"),
                    Output("full_face", "disabled"),
                    Output("head", "disabled"),
                    Output("half_face", "disabled"),
                    Output("modal_error_details", "children"),
                    Output("modal_error", "is_open"),
                    Output("interval-1", "interval"),
                    Output("toggle-add-face", "is_open"),
                    Output("source_imgs_faces", "children"),
                    Output("target_imgs_faces", "children"),
                    ],
                  
        [Input('start_text_continue', 'n_clicks'),Input('interval-1', 'n_intervals'), Input('confirm_delete', 'children')],
        [State("toggle-add-face", "is_open"),State("Images-addclick", "disabled"), State('start_text_input', 'value'), State("start_text_input", "disabled"), State("full_face", "checked"),State("head", "checked"), State("half_face", "checked"), State("interval-1", "interval")])

    def update_start(n, intval,confirm_delete, t1, d1, model_name, d3, s1, s2, s3, s4):

      if dash.callback_context.triggered[0]['prop_id'] != 'interval-1.n_intervals':
          print('######################################################')
          print (dash.callback_context.triggered[0]['prop_id'], currentframe().f_lineno)
          print('######################################################')

      global threadon 
      global msglist
      global storemsg
      global src_vids_clip
      global tar_vids_clip
      global gui_queue
      global cvt_id
      global thread_list
      global threadon_
      global src_child 
      global dst_child
      global open_choose_box
      
      trigger_id = dash.callback_context.triggered[0]['prop_id']
      
      if n is not None and trigger_id == 'start_text_continue.n_clicks':
      
          if s1 == True:
          
            with open('/content/DeepFaceLab/settings.py', 'a') as f:

                f.write("\nFace_Type = 'wf'" + "\n")
                f.close()
                
          elif s2 == True:
          
            with open('/content/DeepFaceLab/settings.py', 'a') as f:

                f.write("\nFace_Type = 'head'" + "\n")
                f.close()
                
          elif  s3 == True:
          
            with open('/content/DeepFaceLab/settings.py', 'a') as f:

                f.write("\nFace_Type = 'f'" + "\n")
                f.close()    
          
          else:
            
            with open('/content/DeepFaceLab/settings.py', 'a') as f:

                f.write("\nFace_Type = 'f'" + "\n")
                f.close()
      
      
      if n is not None:
      
          global watch
        
          global labelsdict
          global run

          if threadon and trigger_id == 'start_text_continue.n_clicks':
            
            
            run = Value("i", 0)
            
          
            thr = Process(target = Main, args=(gui_queue, labelsdict, run, model_name,))
            
            thr.start()
            thread_list.append(thr)
            

            #threading.Thread(target=Main, args=(gui_queue,), daemon=True).start()
            
                    
            watch.start()
            #print ( 'ddabjhjkasfawbwfbjbkwfbkfabkfbkfafbkkbaf')

            threadon = False

          if not threadon_:
          
            src_child = dash.no_update
            dst_child = dash.no_update
            
          if run.value and threadon_:
             
            if len(labelsdict['src_face_labels']) <=1 and len(labelsdict['dst_face_labels']) <=1:
            
                run.value = 0
                
            else:
            
                src_imgs = []
                
                print (labelsdict['src_face_labels'])
                
                
                for cli in labelsdict['src_face_labels']:
                    
                    img = cv2.imread(labelsdict['src_face_labels'][cli][0])
                    
                    ret, frame = cv2.imencode('.png', img)

                    frame = base64.b64encode(frame)

                    src_imgs.append('data:image/png;base64,{}'.format(frame.decode()))
                    
                dst_imgs = []
            
                for cli in labelsdict['dst_face_labels']:
                    
                    img = cv2.imread(labelsdict['dst_face_labels'][cli][0])
                    
                    ret, frame = cv2.imencode('.png', img)

                    frame = base64.b64encode(frame)

                    dst_imgs.append('data:image/png;base64,{}'.format(frame.decode()))    
                    
                print ('#######################################################')
                print (len(src_imgs))
                print (len(dst_imgs))
                src_child  = dbc.CardGroup([dbc.Card([dbc.CardBody( html.Div(dbc.Checkbox(id = 'src_img_'+ str(idx) )), style = {'margin':'auto'}),
                        dbc.CardImg(style = {'width' : '80px', 'height' : '80px', 'margin':'auto'}, 
                        src=src_img, bottom=True), html.Br()],style={"width": "6rem","height": "8rem"}) for idx, src_img in enumerate(src_imgs)  ])
                
                dst_child  = dbc.CardGroup([dbc.Card([dbc.CardBody( html.Div(dbc.Checkbox(id = 'dst_img_'+ str(idx) )), style = {'margin':'auto'}),
                        dbc.CardImg(style = {'width' : '80px', 'height' : '80px', 'margin':'auto'}, 
                        src=dst_img, bottom=True), html.Br()],style={"width": "6rem","height": "8rem"}) for idx, dst_img in enumerate(dst_imgs)  ])
                
                
                
                open_choose_box = True
                threadon_ = False

          
          
          if trigger_id == 'confirm_delete.children':
          
            open_choose_box = False
            
            run.value = 0
            
            
          
          try:
              message = gui_queue.get_nowait()
          except:            
              message = None 


          if message:
            

            #print('fafas')
            
            
            
            
            
            if message.startswith('#ID-'):
            
                cvt_id = message
            else:
                
                msglist = message
                
                
            if message.startswith('Error'):
            
                error = message
                
                heading_update = 'Error! Refresh Page'
                
                time.sleep(2)
                
               
                
                return [d1, heading_update, 'Training stopped', True, True, True, True, True, error, True, 1000000, open_choose_box, src_child, dst_child]
                
                
                
            
          try:
          
            heading_update = ['Training ' , dbc.Badge(cvt_id, color="light", className="ml-1")]
            
          except:
            
            heading_update =  ['Training ...']
            
            
          jpgs = len(glob.glob('workspace/model/*.jpg'))
          mp4s = len(glob.glob('workspace/result*.mp4'))
          
          
          if jpgs>0:
            
            img_disabled = False
            
          else:
            
            img_disabled = True
            
          if mp4s>0:
            
            res_disabled = False
            
          else:
            
            res_disabled = True 
            
            
          try:
            
            header = watch.get_interval()
             
          except:
          
          
            header = ''
          
          
          return [ img_disabled, heading_update,'['+header+'] '+msglist, True, True, True, True, True, '', False, s4, open_choose_box, src_child, dst_child]
          
      else:
      
          return [ d1, 'Start the Process', 'Choose an option', False, d3, False, False, False, '', False, s4, open_choose_box, src_child, dst_child]
    

    @app.callback(Output('confirm_delete', 'children'),
                   [Input('okay_face_select', 'n_clicks')],
                   [State('src_img_'+ str(idx), 'checked') for idx in range(len(labelsdict['src_face_labels']))]+
                   [State('dst_img_'+ str(idx), 'checked') for idx in range(len(labelsdict['dst_face_labels']))])
                   
    
    def update_(n, *checked):
    
        if n:
            print (checked)
            global labelsdict
            
            src_n = len(labelsdict['src_face_labels'])
            dst_n = len(labelsdict['dst_face_labels'])
            
            for i,j in zip(checked[:src_n], labelsdict['src_face_labels'].keys()):


                if not i:
                
                    for k in labelsdict['src_face_labels'][j]:
                    
                        print (k)
                    
                        os.remove(k)
                        
                        
            for i,j in zip(checked[src_n:], labelsdict['dst_face_labels'].keys()):


                if not i:
                
                    for k in labelsdict['dst_face_labels'][j]:
                        print (k)
                        os.remove(k)




            return  ' '   





    
    
    @app.callback([Output('v_plus_size', 'disabled'),
                   Output('h_minus_size', 'disabled'),
                   Output('h_plus_size', 'disabled'),
                   Output('v_minus_size', 'disabled'),
                   Output('v_plus_shift', 'disabled'),
                   Output('h_minus_shift', 'disabled'),
                   Output('h_plus_shift', 'disabled'),
                   Output('v_minus_shift', 'disabled'),
             
                   Output('okay_merge', 'disabled'),

                   Output('refresh_img', 'disabled'),
                
                   Output('mask_mode_', 'disabled'),
                   Output('face_type_', 'disabled'),
                   Output('mode_', 'disabled'),
                   
                   Output('Erode_', 'disabled'),
                   Output('Blur_', 'disabled'),
                   Output('color_mode_', 'disabled'),
                   Output('motion_blur_power_', 'disabled'),
                   Output('blursharpen_amount_', 'disabled'),
                   Output('image_denoise_power_', 'disabled'),
                   Output('color_degrade_power_', 'disabled'),
                   Output('convert_load', 'children')],
                   [Input('interval-1', 'n_intervals')],
                   [State('convert_model_continue', 'n_clicks')]
                   )
                   
    def update_disabled(intval, n):
    
    
        npy_files = [i for i in os.listdir('/tmp') if i.endswith('.npy')]
    
            
        
        
        if len(npy_files)>5:
        
            isdisabled = False
            
            
        else:
        
            isdisabled = True
            
    
        if n:
        
            if len(npy_files)>5:
            
                msg = ""
                
            else:
            
                msg =  [html.Br(), "Loading. Please wait. ", dbc.Spinner(size="sm")]   
    
    
    
    
        else:
            
            msg = ""
            
            
        
        
        
        return [isdisabled]*20 + [msg]
        
        
    @app.callback([Output('convert_model_continue', 'disabled'),
                   Output('convert_model_id', 'disabled'),
                   
                  
                  ],
                   [Input('convert_model_continue', 'n_clicks')],
                   [State('convert_model_id', 'value')])
        
        
    def update_convert(n, model_id):
    
        global option_convert
        global npy_files
        
        if n:
            
            if model_id == '0':
            
                check = len(os.listdir('/content/workspace/model/'))>5 
                
                if check:
                    
                    os.system('echo | python DeepFaceLab/merger/Merger_preview.py')
                    
                    print ('dfggadgsg')
                    
                    #npy_files = [i for i in os.listdir('/tmp') if i.endswith('.npy')]
                    
                    #npy_ = npy_files[0]
                    
                    #img = Merger_tune.MergeMaskedFace_test(npy_, cfg)[0]
                    
                    return [True, True]
                    
                else:
                    
                    return [False, False]
                    
                    
            else:
            
                model = [i['label'] for i in option_convert if i['value'] == int(model_id)][0]
                convert_id = model.split('_')[-1].split('.')[0]
                model_name = 'workspace_'+convert_id + '.zip'
            
                if os.path.isdir('/content/workspace/'):
                    shutil.rmtree('/content/workspace/')    

                os.system('echo A | unzip /content/drive/My\ Drive/'+model_name)
                
                
                check = len(os.listdir('/content/workspace/model/'))>5 
                
                if check:
                    
                    os.system('echo | python DeepFaceLab/merger/Merger_preview.py')
                    
                    print ('dfggadgsg')
                    
                    
                    
                    #npy_files = [i for i in os.listdir('/tmp') if i.endswith('.npy')]
                    
                    #npy_ = npy_files[0]
                    
                    #img = Merger_tune.MergeMaskedFace_test(npy_, cfg)[0]
                    
                    
                    return [True, True]
                    
                else:
                    
                    return [False, False]
                    
                    
        else:
            
            return [False, False]    
        
        
        
    @app.callback([Output('Convert_Image', 'src'), Output('test_div', 'children')],
                   [
                   Input('v_plus_size', 'n_clicks'),
                   Input('h_minus_size', 'n_clicks'),
                   Input('h_plus_size', 'n_clicks'),
                   Input('v_minus_size', 'n_clicks'),
                   Input('v_plus_shift', 'n_clicks'),
                   Input('h_minus_shift', 'n_clicks'),
                   Input('h_plus_shift', 'n_clicks'),
                   Input('v_minus_shift', 'n_clicks'),
                   Input('refresh_img', 'n_clicks'),
                
                   Input('mask_mode_', 'value'),
                   Input('face_type_', 'value'),
                   Input('mode_', 'value'),
                   
                   Input('Erode_', 'value'),
                   Input('Blur_', 'value'),
                   Input('color_mode_', 'value'),
                   Input('motion_blur_power_', 'value'),
                   Input('blursharpen_amount_', 'value'),
                   Input('image_denoise_power_', 'value'),
                   Input('color_degrade_power_', 'value'),
                   Input('convert_model_continue', 'disabled')
           ], [State('size_step', 'value'),
                State('shift_step', 'value')]
                   )    
                   
    def update_convert_image(v_plus_size,h_minus_size, h_plus_size, v_minus_size , v_plus_shift, h_minus_shift, h_plus_shift, v_minus_shift,
                            refresh_img, mask_mode_, face_type_, mode_, Erode_,Blur_ ,color_mode_, motion_blur_power_, blursharpen_amount_,
                            image_denoise_power_,color_degrade_power_, stp_size, stp_shift, trigger):

        
        trigger_id = dash.callback_context.triggered[0]['prop_id']


        print (v_plus_size,h_minus_size, h_plus_size, v_minus_size , v_plus_shift, h_minus_shift, h_plus_shift, v_minus_shift,
                            refresh_img, mask_mode_, mode_, Erode_,Blur_ ,color_mode_, motion_blur_power_, blursharpen_amount_,
                            image_denoise_power_,color_degrade_power_)
        
        global horizontal_shear
        global vertical_shear
        global horizontal_shift
        global vertical_shift
        global ind_preview
        global npy_files
        global cfg_merge
        
        if trigger_id == 'v_plus_size.n_clicks':
        
            vertical_shear = vertical_shear + stp_size
            
        if trigger_id == 'h_minus_size.n_clicks':
        
            horizontal_shear = horizontal_shear - stp_size
            
            
        if trigger_id == 'v_minus_size.n_clicks':
        
            vertical_shear = vertical_shear - stp_size
            
        if trigger_id == 'h_plus_size.n_clicks':
        
            horizontal_shear = horizontal_shear + stp_size
            
            
            
        if trigger_id == 'v_plus_shift.n_clicks':
        
            vertical_shift = vertical_shift + stp_shift
            
        if trigger_id == 'h_minus_shift.n_clicks':
        
            horizontal_shift = horizontal_shift - stp_shift
            
            
        if trigger_id == 'v_minus_shift.n_clicks':
        
            vertical_shift = vertical_shift - stp_shift
            
        if trigger_id == 'h_plus_shift.n_clicks':
        
            horizontal_shift = horizontal_shift + stp_shift
            
            
        npy_files = [i for i in os.listdir('/tmp') if i.endswith('.npy')]
        
        
        if trigger_id == 'refresh_img.n_clicks':
        
            ind_preview = np.random.choice(20)
        
        
        
        
        if int(face_type_) == 0:
        
            face_type = FaceType.HEAD
            
        elif int(face_type_) == 1:
        
            face_type = FaceType.FULL
        
        elif int(face_type_) == 2:
        
            face_type = FaceType.WHOLE_FACE
            
        try:
        
            npy_ = os.path.join('/tmp', npy_files[ind_preview])
        
            
            #print (npy_)
            
            cfg_merge = merging_vars(
                   face_type = face_type,
                   mask_mode = int(mask_mode_),
                   mode = mode_,
                   erode_mask_modifier = Erode_,
                   blur_mask_modifier = Blur_,
                   color_transfer_mode = int(color_mode_),
                   masked_hist_match = True,
                   hist_match_threshold = 255,
                   motion_blur_power = motion_blur_power_,
                   blursharpen_amount = blursharpen_amount_,
                   image_denoise_power = image_denoise_power_,
                   bicubic_degrade_power = 0,
                   sharpen_mode = 1,
                   color_degrade_power = color_degrade_power_,
                   horizontal_shear = horizontal_shear,
                   vertical_shear = vertical_shear,
                   horizontal_shift = horizontal_shift,
                   vertical_shift = vertical_shift
                   )
                   
                   
            result, _ = Merger_tune.MergeMaskedFace_test(npy_, cfg_merge)
            result = imutils.resize(result*255, height=156)
            
            print (result.shape)
            
            ret, frame = cv2.imencode('.png',result )

            frame = base64.b64encode(frame)

            src = 'data:image/png;base64,{}'.format(frame.decode())
            
            return [src, ' ']
        
        
        except:
        
            return ["", ' ']
            
    @app.callback([Output('merge_progress', 'value'),Output('convert_result', 'children')],
                [Input('okay_merge', 'n_clicks'), Input('interval-1', 'n_intervals')])
                
          
    def update__(n, interval):
    
        trigger_id = dash.callback_context.triggered[0]['prop_id']
        global cfg_merge 
        done = 0
        global convert_id
        if n and trigger_id=='okay_merge.n_clicks':
        
            if os.path.isdir('/content/workspace/data_dst/merged'):
                shutil.rmtree('/content/workspace/data_dst/merged')
                os.mkdir ('/content/workspace/data_dst/merged')
                
                
            dict_1 = {'original':0, 'overlay':1, 'hist-match':2 ,'seamless':3 ,'seamless-hist-match':4 , 'raw-rgb':5 , 'raw-predict':6}
            
            dict_2 = {0: 'none', 1:'rct',2:'lct',3:'mkl',4:'mkl-m',5:'idt',6:'idt-m',7:'sot-m',8:'mix-m'}
            
            with open('/content/DeepFaceLab/settings.py', 'a') as f:

                f.write("\nmerging_mode = "+ str(dict_1[cfg_merge.mode]))
                f.write("\nmask_merging_mode = " + str(cfg_merge.mask_mode))
                f.write("\nblursharpen_amount = " + str(cfg_merge.blursharpen_amount))
                f.write("\nerode_mask_modifier = "+ str(cfg_merge.erode_mask_modifier))
                f.write("\nblur_mask_modifier ="+ str(cfg_merge.blur_mask_modifier))
                f.write("\nmotion_blur_power = "+ str(cfg_merge.motion_blur_power))
                #f.write("\noutput_face_scale = "+ cfg_merge)
                f.write("\ncolor_transfer_mode = '"+ dict_2[cfg_merge.color_transfer_mode]+"'")
                #f.write("\nsuper_resolution_power = "+ cfg_merge)
                f.write("\nimage_denoise_power = "+ str(cfg_merge.image_denoise_power))
                #f.write("\nbicubic_degrade_power = "+ cfg_merge)
                f.write("\ncolor_degrade_power = "+ str(cfg_merge.color_degrade_power))
                #f.write("\nmasked_hist_match = "+ cfg_merge)
                #f.write("\nhist_match_threshold ="+cfg_merge)
                f.write("\nhorizontal_shear = "+str(cfg_merge.horizontal_shear))
                f.write("\nvertical_shear = "+ str(cfg_merge.vertical_shear))
                f.write("\nhorizontal_shift = "+ str(cfg_merge.horizontal_shift))
                f.write("\nvertical_shift = "+ str(cfg_merge.vertical_shift))
                
                f.close()
                    
                    
                    
                    
            
            thr = Process(target = Convert, args=())
            thr.daemon=True   
            thr.start()
            
            return done, [html.Br(), "Converting frames ", dbc.Spinner(size="sm")]   
        
        if n and trigger_id=='interval-1.n_intervals':
            
            number_of_files = len(os.listdir('/content/workspace/data_dst/merged'))
            total_number_of_files = len(os.listdir('/content/workspace/data_dst/aligned'))
            
            done =  int((number_of_files/total_number_of_files)*100)
        
        
            if os.path.isfile('/content/drive/My Drive/result_' + convert_id + '.mp4'):
            
                done_ = "Completed. "
            
            else:
                done_ =  [html.Br(), "Converting frames ", dbc.Spinner(size="sm")]   
            
            
            return done,done_
        
        return done, ""
        
    app.run_server(debug=False, port =  8050)