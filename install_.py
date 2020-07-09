
from google.colab import drive
drive.mount('/content/drive')

get_ipython().system_raw('pip3 install --upgrade moviepy')
get_ipython().system_raw('pip3 install dash')
get_ipython().system_raw('pip3 install dash_core_components')
get_ipython().system_raw('pip3 install dash_html_components')
get_ipython().system_raw('pip3 install dash_bootstrap_components')
get_ipython().system_raw('pip3 install flask')
get_ipython().system_raw('pip3 install youtube_dl')
get_ipython().system_raw('pip3 install mhyt')
get_ipython().system_raw('pip3 install dash_daq')
Mode = "install" 

from pathlib import Path
if (Mode == "install"):
  get_ipython().system_raw('git clone https://github.com/iperov/DeepFaceLab.git')

  # fix linux warning
  # /usr/lib/python3.6/multiprocessing/semaphore_tracker.py:143: UserWarning: semaphore_tracker: There appear to be 1 leaked semaphores to clean up at shutdown
  fin = open("/usr/lib/python3.6/multiprocessing/semaphore_tracker.py", "rt")
  data = fin.read()
  data = data.replace('if cache:', 'if False:')
  fin.close()

  fin = open("/usr/lib/python3.6/multiprocessing/semaphore_tracker.py", "wt")
  fin.write(data)
  fin.close()
else:

  get_ipython().system_raw('/content/DeepFaceLab | git pull')

get_ipython().system_raw('pip install -r /content/DeepFaceLab/requirements-colab.txt')
get_ipython().system_raw('pip install --upgrade scikit-image')
get_ipython().system_raw('apt-get install cuda-10-0')

if not Path("/content/pretrain").exists():
  print("Downloading CelebA faceset ... ")
  get_ipython().system_raw('wget -q --no-check-certificate -r https://github.com/chervonij/DFL-Colab/releases/download/pretrain-CelebA/pretrain_CelebA.zip -O /content/pretrain_CelebA.zip')
  get_ipython().system_raw('mkdir /content/pretrain')
  get_ipython().system_raw('unzip -q /content/pretrain_CelebA.zip -d /content/pretrain/')
  get_ipython().system_raw('rm /content/pretrain_CelebA.zip')

if not Path("/content/pretrain_Q96").exists():
  print("Downloading Q96 pretrained model ...")
  get_ipython().system_raw('wget -q --no-check-certificate -r https://github.com/chervonij/DFL-Colab/releases/download/Q96_model_pretrained/Q96_model_pretrained.zip -O /content/pretrain_Q96.zip')
  get_ipython().system_raw('mkdir /content/pretrain_Q96')
  get_ipython().system_raw('unzip -q /content/pretrain_Q96.zip -d /content/pretrain_Q96/')
  get_ipython().system_raw('rm /content/pretrain_Q96.zip')

if not Path("/content/workspace").exists():
  get_ipython().system_raw('mkdir /content/workspace; mkdir /content/workspace/data_src; mkdir /content/workspace/data_src/aligned; mkdir /content/workspace/data_dst; mkdir /content/workspace/data_dst/aligned; mkdir /content/workspace/model')  

import IPython
from google.colab import output

display(IPython.display.Javascript('''
 function ClickConnect(){
   btn = document.querySelector("colab-connect-button")
   if (btn != null){
     console.log("Click colab-connect-button"); 
     btn.click() 
     }
   
   btn = document.getElementById('ok')
   if (btn != null){
     console.log("Click reconnect"); 
     btn.click() 
     }
  }
  
setInterval(ClickConnect,60000)
'''))

print("\nDone!")
get_ipython().system_raw('wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip')
get_ipython().system_raw('unzip ngrok-stable-linux-amd64.zip')


get_ipython().system_raw('./ngrok authtoken 5vhWvAzJGtsJbnVp4V5di_6KNVTN8BpHMqKYyAaFFXQ')
print("Done!")