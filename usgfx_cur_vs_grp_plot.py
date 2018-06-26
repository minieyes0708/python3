import matplotlib.pyplot as plt
import numpy as np
path = r'C:\Users\minieyes\AppData\Roaming\MetaQuotes\Terminal\5A590048FA8C0D1558C5BA77A5A1447F\MQL4\Files\\'
with open(path + 'CurData.txt', 'r') as file:
    line = file.read()
cur_data = [float(bar) for bar in line.split(',')[:-1]]
with open(path + 'GrpData.txt', 'r') as file:
    line = file.read()
grp_data = [float(bar) for bar in line.split(',')[:-1]]
with open(path + 'Groups.txt', 'r') as file:
    lines = file.readlines()

grp_data1 = [float(bar) for bar in lines[1].split(',')[2:-1]]
grp_data2 = [float(bar) for bar in lines[2].split(',')[2:-1]]
grp_data3 = [float(bar) for bar in lines[3].split(',')[2:-1]]
grp_data4 = [float(bar) for bar in lines[4].split(',')[2:-1]]
grp_data5 = [float(bar) for bar in lines[5].split(',')[2:-1]]

plt.figure
plt.plot(np.array(grp_data1) - np.mean(grp_data1), 'g-')
plt.plot(np.array(grp_data2) - np.mean(grp_data2), 'g--')
plt.plot(np.array(grp_data3) - np.mean(grp_data3), 'go')
plt.plot(np.array(grp_data4) - np.mean(grp_data4), 'g.')
plt.plot(np.array(grp_data5) - np.mean(grp_data5), 'gv')
plt.plot(np.array(cur_data)  - np.mean(cur_data),  'b')
plt.plot(np.array(grp_data)  - np.mean(grp_data),  'r')
plt.ylim([-5,5])
plt.show()
