import pandas as pd

df = pd.read_csv('RL_models/qtable_trained.csv')

vpip_low = 0
vpip_high = 0
af_low = 0
af_high = 0
total_keys = 1280
for hand in range(10):
    for street in range(4):
        for blind in range(2):
            for last_act in range(2):
                for af in range(2):
                    for vpip in range(2):
                        for winning in range(2):
                            key = f'H{hand}S{street}B{blind}L{last_act}A{af}V{vpip}W{winning}'
                            if sum(df[key]) != 0:
                                if vpip == 1:
                                    vpip_high += 1
                                else:
                                    vpip_low += 1
                                if af == 1:
                                    af_high += 1
                                else:
                                    af_low += 1
# print(vpip_low, vpip_high)
print(af_low, af_high)
