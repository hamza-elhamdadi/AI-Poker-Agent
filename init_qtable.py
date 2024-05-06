import pandas as pd

actions = ['fold', 'call', 'raise']
df = pd.DataFrame()
for hand in range(10):
    for blind in range(2):
        for last_act in range(2):
            for af in range(2):
                for vpip in range(2):
                    for winning in range(2):
                        key = f'H{hand}B{blind}L{last_act}A{af}V{vpip}W{winning}'
                        fold_rew = 0
                        call_rew = 1 if hand == 0 else hand - 1
                        raise_rew = hand
                        df[key] = pd.Series(dict(zip(actions,
                                                     [fold_rew, call_rew, raise_rew])))

df.to_csv('RL_models/qtable.csv')
