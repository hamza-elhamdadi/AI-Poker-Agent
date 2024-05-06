suits = ['A', 'B', 'C', 'D']
ranks = range(1,14)

case_nb = 0  # count the number of simulations

for r1 in ranks:  # generate card 1
    s1 = 'A'
    for r2 in range(r1,14):  # generate card 2
        for s2 in ['A', 'B']:
            if s1 == s2 and r1 == r2:
                continue
            for r3 in range(1,14):  # generate card 3
                for s3 in ['A', 'B', 'C']:
                    if (s3 == 'A' and s2 == 'C') or (r3 == r1 and s3 == s1) or (r3 == r2 and s3 == s2):
                        continue
                    for r4 in range(r3,14):  # generate card 4
                        for s4 in suits:
                            if (r4 == r1 and s4 == s1) or (r4 == r2 and s4 == s2) or (r4 == r3 and s4 == s3) or (s4 == 'D' and s3 != 'C') or (s4 == 'C' and s3 != 'B' and s2 != 'B') or (r4 == r3 and s4 == 'A' and s3 == 'B'):
                                continue
                            for r5 in range(r4,14):  # generate card 5
                                for s5 in suits:
                                    if (r5 == r1 and s5 == s1) or (r5 == r2 and s5 == s2) or (r5 == r3 and s5 == s3) or (r5 == r4 and s5 == s4):  # duplication check
                                        continue
                                    if s5 == 'D' and s4 != 'C' and s3 != 'C':  # jumping suits assignment check
                                        continue
                                    if r5 == r4:
                                        if (s5 == 'A') or (s5 == 'B' and s4 == 'C') or (s5 == 'C' and s4 == 'D'):
                                            continue
                                    case_nb += 1
                                    # useful assignment, run the simulation
print(case_nb)
