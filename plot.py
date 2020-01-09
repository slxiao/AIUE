from matplotlib import pyplot as pl
import numpy as np


with open("r.log", "r") as f:
    random = eval(f.read())

with open("e.log", "r") as f:
    qlearning = eval(f.read())

random_points = [[] for i in range(1000)]
for i in random:
    for j in i[1]:
        random_points[j[0]-1].append(j[1]-1)

qlearning_points = [[] for i in range(1000)]
for i in qlearning:
    for j in i[1]:
        qlearning_points[j[0]-1].append(j[1]-1)

mean_r = np.mean(random_points, axis=1)
standard_dev_r = np.std(random_points, axis=1)

mean_q = np.mean(qlearning_points, axis=1)
standard_dev_q = np.std(qlearning_points, axis=1)

pl.plot(mean_r, label="random")
pl.fill_between(range(1000), mean_r-standard_dev_r, mean_r+standard_dev_r, alpha = 0.5)
pl.plot(mean_q, label="q-learning")
pl.fill_between(range(1000), mean_q-standard_dev_q, mean_q+standard_dev_q, alpha = 0.5)
pl.legend(loc="upper left")
#pl.show()
pl.xlabel("Actions")
pl.ylabel("Unique States")
pl.savefig("random.png")