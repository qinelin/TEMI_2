import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import IsolationForest
df_dict = json.loads(r.get(key))
#df_train = pd.DataFrame(list(df_dict), columns=['batteryPercentage'])
df_train = pd.DataFrame.from_dict(df_dict)
df_train.info()
df_train.head()

#Change to anomaly data
for i in range(0,99):
    df_train.loc[i,'batteryPercentage']=500

#boxplot
sns.boxplot(df_train['batteryPercentage'])

#training model
random_state = np.random.RandomState(42)
model=IsolationForest(n_estimators=100,max_samples='auto',contamination=float(0.2),random_state=random_state)
model.fit(df_train[['batteryPercentage']])
print(model.get_params())

#Increase score
df_train['scores'] = model.decision_function(df_train[['batteryPercentage']])
df_train['anomaly_score'] = model.predict(df_train[['batteryPercentage']])
df_train[df_train['anomaly_score']==-1].head(50)

#Result
count = df_train.shape[0]
anomaly_count = 100
anomaly_count_wrong = 0
for i in range(100):
    if list(df_train['anomaly_score'])[i] == -1:
        anomaly_count_wrong += 0
    else:
        anomaly_count_wrong += 1
accuracy_a = 100*(1-(anomaly_count_wrong/anomaly_count))
accuracy_n = (count-list(df_train['anomaly_score']).count(-1))/count*100
#accuracy = 100*list(df_train['anomaly_score']).count(-1)/(anomaly_count)
print("Accuracy of the model(in_anomaly):", accuracy_a)
print("Accuracy of the model(in_normal):", accuracy_n)
print("Anomaly count:",list(df_train['anomaly_score']).count(-1))
print("count:",df_train.shape[0])
