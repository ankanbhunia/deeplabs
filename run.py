#@markdown <br><center><img src='https://pbs.twimg.com/profile_images/552739703141588992/E3oZpVzB_400x400.png' height="200" alt="noMachine"/></center>
#@markdown <center>NoMachine<br><h3>Free Remote Desktop For Everybody</h3></center><br>
import os
import tarfile
import urllib.request
import shutil
import time
from IPython.display import HTML, clear_output
from subprocess import Popen

os.system('sudo apt-get clean')
os.system('sudo apt-get update')

#####################################
USE_FREE_TOKEN = False
TOKEN = "6HHRoYsgJ7hpZJvcF8syH_7aVenWciJrBDtUYkss7Mh" 
REGION = "IN"
APT_INSTALL = "apt install -y "
HOME = os.path.expanduser("~")
runW = get_ipython()

if not os.path.exists(f"{HOME}/.ipython/ocr.py"):
    hCode = "https://raw.githubusercontent.com/biplobsd/" \
                "OneClickRun/master/res/ocr.py"
    urllib.request.urlretrieve(hCode, f"{HOME}/.ipython/ocr.py")

from ocr import (
    runSh,
    loadingAn,
    PortForward_wrapper,
    findProcess,
    textAn,
)

loadingAn()

os.makedirs("tools/nomachine", exist_ok=True)
os.makedirs("/root/.icewm", exist_ok=True)

# password ganarate
try:
  print(f"Found old password! : {password}")
except:
  password = 'nomachine'
clear_output()

start = time.time()
if not os.path.exists("tools/nomachine/NX/bin/nxserver"):

  textAn("Wait for few seconds. It's doing for NoMachine ready ...")

  runW.system_raw('apt update --quiet --force-yes')

  os.system('sudo apt-get clean')
  os.system('sudo apt-get update')
  os.system('sudo apt-get install xfce4 firefox')

  # nomachine
  staticUrl = "https://github.com/biplobsd/temp/releases/download/6.9.2_1/nomachine_6.9.2_1_x86_64.tar.gz"
  configUrl = "https://raw.githubusercontent.com/biplobsd/OneClickRun/master/res/appdata/NoMachine/NXetc.tar.gz"
  
  output_file = 'tools/nomachine/nm.tar.gz'
  config_file = 'tools/nomachine/etc.tar.gz'
  urllib.request.urlretrieve(staticUrl, output_file)
  urllib.request.urlretrieve(configUrl, config_file)
  
  with tarfile.open(output_file, 'r:gz') as t:t.extractall('tools/nomachine')
  runSh('./nxserver --install', cd='tools/nomachine/NX', shell=True)
  runSh('./nxserver --stop', cd='tools/nomachine/NX/bin', shell=True)
  
  shutil.rmtree('tools/nomachine/NX/etc')
  with tarfile.open(config_file, 'r:gz') as t:t.extractall('tools/nomachine/NX')
  os.remove(config_file)
  
  os.remove(output_file)
  runSh('./nxserver --startup', cd='tools/nomachine/NX/bin', shell=True)
  runW.system_raw("echo root:$password | chpasswd")

end = time.time()
# START_SERVER
# Ngrok region 'us','eu','ap','au','sa','jp','in'
clear_output()
PORT_FORWARD = "ngrok"
Server = PortForward_wrapper(PORT_FORWARD, TOKEN, USE_FREE_TOKEN,
                             [['nomachine', 4000, 'tcp']], REGION.lower(), 
               [f"{HOME}/.ngrok2/nomachine.yml", 8459])

data = Server.start('nomachine', displayB=False)
clear_output()
host, port = data['url'][7:].split(':')
user = os.popen('whoami').read()

# Colors
bttxt = 'hsla(10, 50%, 85%, 1)'
btcolor = 'hsla(10, 86%, 56%, 1)'
btshado = 'hsla(10, 40%, 52%, .4)'
os.system('sudo apt-get install xarchiver')
display(HTML("""<style>@import url('https://fonts.googleapis.com/css?family=Source+Code+Pro:200,900');  :root {   --text-color: """+bttxt+""";   --shadow-color: """+btshado+""";   --btn-color: """+btcolor+""";   --bg-color: #141218; }  * {   box-sizing: border-box; } button { position:relative; padding: 10px 20px;     border: none;   background: none;      font-family: "Source Code Pro";   font-weight: 900;font-size: 100%;     color: var(--text-color);      background-color: var(--btn-color);   box-shadow: var(--shadow-color) 2px 2px 22px;   border-radius: 4px;    z-index: 0;overflow: hidden; -webkit-user-select: text;-moz-user-select: text;-ms-user-select: text;user-select: text;}  button:focus {   outline-color: transparent;   box-shadow: var(--btn-color) 2px 2px 22px; }  .right::after, button::after {   content: var(--content);   display: block;   position: absolute;   white-space: nowrap;   padding: 40px 40px;   pointer-events:none; }  button::after{   font-weight: 200;   top: -30px;   left: -20px; }   .right, .left {   position: absolute;   width: 100%;   height: 100%;   top: 0; } .right {   left: 66%; } .left {   right: 66%; } .right::after {   top: -30px;   left: calc(-66% - 20px);      background-color: var(--bg-color);   color:transparent;   transition: transform .4s ease-out;   transform: translate(0, -90%) rotate(0deg) }  button:hover .right::after {   transform: translate(0, -47%) rotate(0deg) }  button .right:hover::after {   transform: translate(0, -50%) rotate(-7deg) }  button .left:hover ~ .right::after {   transform: translate(0, -50%) rotate(7deg) }  /* bubbles */ button::before {   content: '';   pointer-events: none;   opacity: .6;   background:     radial-gradient(circle at 20% 35%,  transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),     radial-gradient(circle at 75% 44%, transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),     radial-gradient(circle at 46% 52%, transparent 0, transparent 4px, var(--text-color) 5px, var(--text-color) 6px, transparent 6px);    width: 100%;   height: 300%;   top: 0;   left: 0;   position: absolute;   animation: bubbles 5s linear infinite both; }  @keyframes bubbles {   from {     transform: translate();   }   to {     transform: translate(0, -66.666%);   } }.zui-table {    border: solid 1px #DDEEEE;    border-collapse: collapse;    border-spacing: 0;    font: normal 13px;}.zui-table thead th {    background-color: #DDEFEF;    border: solid 1px #DDEEEE;    color: #0000009e;    padding: 10px;    text-align: left;}.zui-table tbody td {border: solid 1px #effff97a;color: #ffffffd1;    padding: 10px;}</style><center><button><table class="zui-table blueBG"><p>NoMachine config<p><thead>        <tr><th>Username</th> <th>Password</th><th>Protocol</th>            <th>Host</th>            <th>Port</th>        </tr>    </thead>    <tbody>        <tr><td>"""+user+"""</td><td>"""+password+"""</td><td>NX</td><td>"""+host+"""</td><td>"""+port+"""</td></tr></tbody></table><a target="_blank" style="text-decoration: none;color: hsla(210, 50%, 85%, 1);font-size: 10px;" href="https://raw.githubusercontent.com/biplobsd/OneClickRun/master/img/NoMachine.gif">NB. How to setup this's config. [Click ME]</a></button><center>"""))
