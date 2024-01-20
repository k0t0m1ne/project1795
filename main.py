import matplotlib.pyplot as plt
import pandas as pd



df = pd.read_csv('Matrix_RC515.csv', delimiter=',')
time = df['pkeep']
sales = df['value_clr']
plt.plot(time, sales)

plt.grid()
plt.xlabel('pkeep')
plt.ylabel('value_clr')


plt.show()