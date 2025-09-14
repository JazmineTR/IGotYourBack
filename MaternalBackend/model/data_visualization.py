import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("model/lumbar_bipe_only.xlsx")
print(df['label'].value_counts())  # see how balanced it is

plt.hist(df[df['label']==0]['lumbar_bipe'], bins=15, alpha=0.5, label='Healthy')
plt.hist(df[df['label']==1]['lumbar_bipe'], bins=15, alpha=0.5, label='Dangerous')
plt.xlabel("Lumbar Angle (°)")
plt.ylabel("Count")
plt.legend()
plt.show()

df.boxplot(column="lumbar_bipe", by="label")
plt.title("Lumbar Angle by Health Label")
plt.suptitle("")
plt.show()

df = pd.read_excel("model/hip_bipe_only.xlsx")
print(df['label'].value_counts())  # see how balanced it is

plt.hist(df[df['label']==0]['hip_bipe'], bins=15, alpha=0.5, label='Healthy')
plt.hist(df[df['label']==1]['hip_bipe'], bins=15, alpha=0.5, label='Dangerous')
plt.xlabel("hip Angle (°)")
plt.ylabel("Count")
plt.legend()
plt.show()

df.boxplot(column="hip_bipe", by="label")
plt.title("Hip Angle by Health Label")
plt.suptitle("")
plt.show()