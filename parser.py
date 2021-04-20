import subprocess
from datetime import datetime
from collections import Counter, defaultdict

d_proc = defaultdict(dict)
ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

for proc in ps.split('\n')[1:-1]:
    plist = proc.split()
    pid = int(plist[1])
    user = plist[0]
    cpu = float(plist[2])
    mem = float(plist[3])
    command = plist[10]

    d_proc[pid]["user"] = user
    d_proc[pid]["cpu"] = cpu
    d_proc[pid]["mem"] = mem
    d_proc[pid]["command"] = user

counter_proc_by_name = Counter([val["user"] for _, val in d_proc.items()])
filename = datetime.now().strftime('%d-%m-%Y-%H:%M-scan.txt')

with open(filename, 'w') as f:
    f.write(f"Пользователи системы: {list(counter_proc_by_name)}\n")
    f.write(f"Процессов запущено: {len(d_proc)}\n")
    f.write(
        "Процессы по пользователям: " + " ".join(u + ":" + str(cnt) for u, cnt in counter_proc_by_name.items()) + "\n")
    f.write(f"Всего памяти используется: {sum(v['mem'] for k, v in d_proc.items())}\n")
    f.write(f"Всего CPU используется: {sum(v['cpu'] for k, v in d_proc.items())} %\n")
    f.write(f"Больше всего памяти ест: {max(d_proc.items(), key=lambda x: x[1]['mem'])[1]['command']}\n")
    f.write(f"Больше всего CPU ест: {max(d_proc.items(), key=lambda x: x[1]['cpu'])[1]['command']}\n")
