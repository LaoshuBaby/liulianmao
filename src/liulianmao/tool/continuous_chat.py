# main.py

import subprocess

def communicate():
    ai1_process = subprocess.Popen(['python', 'AI1.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    ai2_process = subprocess.Popen(['python', 'AI2.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    while True:
        ai1_output = ai1_process.stdout.readline().strip()
        if ai1_output:
            print("AI1 says:", ai1_output)
            ai2_process.stdin.write(ai1_output + '\n')
            ai2_process.stdin.flush()

        ai2_output = ai2_process.stdout.readline().strip()
        if ai2_output:
            print("AI2 says:", ai2_output)
            ai1_process.stdin.write(ai2_output + '\n')
            ai1_process.stdin.flush()

communicate()