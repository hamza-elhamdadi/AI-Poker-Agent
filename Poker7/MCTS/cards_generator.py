suits = ['A', 'B', 'C', 'D']
ranks = range(1, 14)

simulations_nb1 = 0  # count the number of simulations in different rounds
simulations_nb2 = 0
simulations_nb3 = 0
simulations_nb4 = 0

for r1 in ranks:  # card 1
    s1 = 'A'
    for r2 in range(r1, 14):  # card 2
        for s2 in ['A', 'B']:
            if s1 == s2 and r1 == r2:
                continue
            simulations_nb1 += 1
            #  use 2 cards to run simulations for Pre-Flop Round
            for r3 in range(1, 14):  # card 3
                for s3 in ['A', 'B', 'C']:
                    if (s3 == 'A' and s2 == 'C') or (r3 == r1 and s3 == s1) or (r3 == r2 and s3 == s2):
                        continue  # check
                    for r4 in range(r3, 14):  # generate card 4
                        for s4 in suits:
                            if (r4 == r1 and s4 == s1) or (r4 == r2 and s4 == s2) or (r4 == r3 and s4 == s3) or (
                                    s4 == 'D' and s3 != 'C') or (s4 == 'C' and s3 != 'B' and s2 != 'B') or (
                                    r4 == r3 and s4 == 'A' and s3 == 'B') or (r4 == r3 and s4 == 'B' and s3 == 'C') or (
                                    r4 == r3 and s4 == 'A' and s3 == 'C'):   # check
                                continue
                            for r5 in range(r4, 14):  # generate card 5
                                for s5 in suits:
                                    if (r5 == r1 and s5 == s1) or (r5 == r2 and s5 == s2) or (
                                            r5 == r3 and s5 == s3) or (r5 == r4 and s5 == s4):  # duplication check
                                        continue
                                    if s5 == 'D' and s4 != 'C' and s3 != 'C':  # jumping suits assignment check
                                        continue
                                    if r5 == r4:
                                        if (s5 == 'A') or (s5 == 'B' and s4 == 'C') or (s5 == 'C' and s4 == 'D') or (
                                                s5 == 'B' and s4 == 'D'):
                                            continue  # check suits order of same rank cards
                                    simulations_nb2 += 1
                                    #  use 2+3 cards to run simulations for Flop Round
                                    for r6 in range(r5, 14):  # card 6
                                        for s6 in suits:
                                            if (r6 == r1 and s5 == s1) or (r6 == r2 and s5 == s2) or (
                                                    r6 == r3 and s6 == s3) or (
                                                    r6 == r4 and s6 == s4) or (
                                                    r6 == r5 and s6 == s5):  # duplication check
                                                continue
                                            if s6 == 'D' and s5 != 'C' and s4 != 'C' and s3 != 'C':
                                                continue   # jumping suits assignment check
                                            if r6 == r5:
                                                if (s6 == 'A') or (s6 == 'B' and s5 == 'C') or (
                                                        s6 == 'C' and s5 == 'D') or (s6 == 'B' and s5 == 'D'):
                                                    continue  # check suits order of same rank cards
                                            simulations_nb3 += 1
                                            #  use 2+4 cards to run simulations for Turn Round
                                            for r7 in range(r6, 14):  # card 7
                                                for s7 in suits:
                                                    if (r7 == r1 and s7 == s1) or (r7 == r2 and s7 == s2) or (
                                                            r7 == r3 and s7 == s3) or (
                                                            r7 == r4 and s7 == s4) or (
                                                            r7 == r5 and s7 == s5) or (r7 == r6 and s7 == s6):
                                                        continue                           # duplication check
                                                    if (s7 == 'D' and s6 != 'C'
                                                            and s5 != 'C' and s4 != 'C' and s3 != 'C'):
                                                        continue  # jumping suits assignment check
                                                    if r7 == r6:
                                                        if (s7 == 'A') or (s7 == 'B' and s6 == 'C') or (
                                                                s7 == 'C' and s6 == 'D') or (s7 == 'B' and s6 == 'D'):
                                                            continue  # check suits order of same rank cards
                                                    simulations_nb4 += 1
                                                    #  use 2+5 cards to run simulations for River Round
print("We should run " + str(simulations_nb1)+" simulations in pre-flop round")
print("We should run " + str(simulations_nb2)+" simulations in flop round")
print("We should run " + str(simulations_nb3)+" simulations in turn round")
print("We should run " + str(simulations_nb4)+" simulations in river round")

# 1. NO repeating cards
# 2. r1 <= r2  r3 <= r4 <= r5
# 3. s1 = A s2 = A/B
