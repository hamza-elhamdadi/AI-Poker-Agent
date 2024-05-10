import pandas as pd
from warnings import simplefilter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

def gen_table(fname):
    actions = ['fold', 'call', 'raise']
    df = pd.DataFrame()
    for hand in range(10):
        for street in range(4):
            for blind in range(2):
                for last_act in range(2):
                    for af in range(2):
                        for vpip in range(2):
                            for winning in range(2):
                                key = f'H{hand}S{street}B{blind}L{last_act}A{af}V{vpip}W{winning}'
                                fold_rew = 0
                                call_rew = 1 if hand == 0 else hand - 1
                                raise_rew = hand
                                rewards = [fold_rew, call_rew, raise_rew]  # init with basic heuristics
                                # rewards = [0, 0, 0]  # initialize with all zeroes
                                df[key] = pd.Series(dict(zip(actions, rewards))).astype(float)
    df.to_csv(f'RL_models/{fname}')

gen_table('qtable.csv')
