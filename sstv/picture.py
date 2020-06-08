import subprocess, time as t
filename = t.strftime('%x_%X').replace("/", "-")
cmd = f"raspistill -vf -o ./pics/{filename}.jpeg"
subprocess.call(cmd, shell=True)
