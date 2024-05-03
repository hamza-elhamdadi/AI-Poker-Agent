import json

with open('MCTS_params.json', 'r') as file:
    data = json.load(file)

print(data.keys())

for key in data.keys():
    with open(f'MCTS_params_{key}.json', 'w') as file:
        json.dump(data[key], file)

# with open('MCTS_params.pkl', 'wb') as file:
#     pickle.dump(data, file)