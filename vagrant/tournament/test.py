def get_sorted_matches(matches):
    sorted_matches = []
    for match in matches:
        sorted_matches.append(sorted(match))
    return sorted_matches

order = [i for i in range(8)]
matches = [(8,6),(5,3),(2,4),(7,1)]
i = 0
matches = get_sorted_matches(matches)
standings = [8,6,5,3,2,7,4,1]

for i in range(0,7,2):
    pair = (standings[i],standings[i+1])
    if sorted(pair) in matches:
	temp = order[i+1]
	order[i+1] = order[i+2]
	order[i+2] = temp

print order
