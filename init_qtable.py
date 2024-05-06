import pandas as pd

actions = ['call', 'raise', 'fold']
df = pd.DataFrame()
for hand in range(10):
    for blind in range(2):
        for last_act in range(2):
            for af in range(2):
                for vpip in range(2):
                    for winning in range(2):
                        key = f'H{hand}B{blind}L{last_act}A{af}V{vpip}W{winning}'
                        df[key] = pd.Series([0, 0, 0])

df.to_csv('RL_models/qtable.csv')
