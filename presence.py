import subprocess, pypresence, time, datetime, re, psutil, os
from datetime import timedelta
from cpuinfo import get_cpu_info

rpc = pypresence.Presence('your_game_id')
rpc.connect()

kernel = os.uname().release
actions = {'Firefox': 'browsing the web', 'Minecraft': 'playing minecraft', 'Xonotic': 'playing xonotic', 'term': 'in a terminal', 'Discord': 'chatting', 'Visual': 'coding', 'Wine': 'playing a shit rythm game'}
action2 = ''

def windowname():
    return re.findall(r'Firefox|Xonotic|term|Discord|Visual|Wine|Minecraft', subprocess.check_output(['xdotool', 'getwindowfocus', 'getwindowname']).decode('utf-8'))[0]
    
def getuptime():
    with open('/proc/uptime', 'r') as f:
        return str(timedelta(seconds=float(f.read().split()[0]))).split('.')[0]

while True:
    try:
        try:
            name = windowname()
            if name in actions:
                action = actions[name]
        except IndexError:
            action = 'petting catgirls'
        if action != action2:
            action2 = action
            apptime = datetime.datetime.now().timestamp()
        else:
            pass
        print(rpc.update(
            start=apptime,
            state="cpu: " + str(psutil.cpu_percent()) + "%, ram: " + str(round(psutil.virtual_memory().used / 1024 / 1024 / 1024, 1)) + "GB of " + str(round(psutil.virtual_memory().total / 1024 / 1024 / 1024, 1)) + "GB", 
            details="currently " + action, 
            large_image="yeaha", 
            large_text="uptime: " + getuptime(),
            small_image=action.lower(), 
            small_text="on kernel " + kernel))
        time.sleep(15)
    except KeyboardInterrupt:
        print('\nexitting')
        exit(0)
    except(pypresence.exceptions.InvalidID, pypresence.exceptions.PyPresenceException, pypresence.exceptions.ServerError, pypresence.exceptions.DiscordError):
        print('connection error, retrying in 10 seconds')
        time.sleep(10)
        rpc.connect()
