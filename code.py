import math


Nmax = 64 
peers = [1, 8, 14, 21, 32, 38, 42, 48, 51, 56] 

def successor(key, peers=peers):
    sorted_peers = sorted(peers) # We need to ensure we are checking in order

    for peer in sorted_peers:
        if peer > key:
            return peer
    return sorted_peers[0] # We are returing 1, we wrap around to the smallest peer (first in the sorted list)

def predecessor(key, peers=peers):
    sorted_peers = sorted(peers)
    
    if key <= sorted_peers[0]:
        return sorted_peers[-1] # We return to the largest peer (It's circle don't forget that)
                                # In case the peer is 1 or anything smaller than that, we should go to the peer before 1 ( whihc is 56)
    
    for i in range(len(sorted_peers)):
        if sorted_peers[i] >= key:
            return sorted_peers[i-1]

print('\n'.join(f"The successor of the key {p} is the peer {successor(p)}." for p in [30, 42, 60]))
print('\n'.join(f"The predecessor of the key {p} is the peer {predecessor(p)}." for p in [37, 1]))

# Question 1.2

def make_dht(peers=peers):
    dht_dict = {}
    m = int(math.log2(Nmax)) # m : is the number of bits to write the keyspace (64)

    for peer in peers:
        finger_table = []

        for i in range(m):
            value = (peer + 2**i) % Nmax
            finger_entry = successor(value)

            if finger_entry not in finger_table:
                finger_table.append(finger_entry)

        dht_dict[peer] = {
            'key': peer,
            'succ': successor(peer),
            'pred': predecessor(peer),
            'finger': finger_table
        }
    return dht_dict

dht = make_dht(peers)
print({peer: {'key': peer, 'succ': info['succ'], 'pred': info['pred'], 'finger': info['finger']} for peer, info in dht.items()})

# Question 2.1

#Question 2.1 : 

def isincharge(dht_i, key):
    # It is important to understand this:
    # A peer is responsible for a key 'K' if:
    # The key K lies in the interval between the predecessor of p and P itself
    # We can express this as:
    # if predecessor(p) < K <= P, then P is responsible for K.

    current_key = dht_i['key']      #38
    predecessor_key = dht_i['pred'] # from one to 64

    if predecessor_key < current_key:
        return predecessor_key <= key < current_key  # return true, if the valuated condition is correct else return false
    else:
        return key >= predecessor_key or key < current_key

i = 1; k = 56
value = isincharge(dht[i], k)
print(value)

k = 55
value = isincharge(dht[i], k)
print(value)
i = 38
responsible_keys = [k for k in range(Nmax) if isincharge(dht[i], k)]
print(responsible_keys)


# Question 2.2

def lookup(i, key, dht=dht):
    current_peer = dht[i]
    peer_key = current_peer['key']
    
    # To build a recursion we need a base case
    # this is where the loop should end, otherwise we end up with infinite loop
    #if pred_key < key <= peer_key or (pred_key > peer_key and (key > pred_key or key <= peer_key)):
    if isincharge(dht[i], key):
        return [i] # Why would i add '[]', because otherwise you will sum up numbers (look in the 3rd return)
    
    successor = current_peer['succ']
    predecessor = current_peer['pred']
    # Added after exo 3, to handle the unique situation where dht contains only one peer responsible for everything
    if successor == peer_key and predecessor == peer_key:
        return [i]
    
    finger_table = current_peer['finger']
    # Case 2: Use the finger table to find the closest peer
    for finger in reversed(finger_table): # the reversed function is very important to our search
                                            # if we dont reverse the order = > This could lead to inefficient routing with unnecessary intermediate hops.
                                            # I noticed when i didnt use it that the path was long and it is not prioritizing
                                            # the largest valid finger 
        if finger > peer_key and finger <= key:
            return [i] + lookup(finger, key, dht)
    
    # If no finger is valid, move to the successor
    return [i] + lookup(successor, key, dht)

result = lookup(56, 2, dht)
print(result)

new_dht = {1: {'key': 1, 'succ': 1, 'pred': 1, 'finger': []}}
result = lookup(1, 42, dht=new_dht)
print(result)

# Question 3
def build_finger(i, candidates):
    # Initialisation de la table des doigts
    finger_table = []

    # Trier les candidats
    sorted_candidates = sorted(candidates)

    # Déterminer la taille maximale du finger table (log2(Nmax))
    m = int(math.log2(Nmax))  # Nmax doit être défini (par exemple, 64)

    # Construction de la table des doigts
    for k in range(m):
        target = (i + 2**k) % Nmax  # Calcul du point cible pour l'entrée k
        for candidate in sorted_candidates:
            if candidate >= target and candidate != i:  # Exclure i (le nœud lui-même)
                finger_table.append(candidate)
                break
        else:
            # Si aucun candidat ne correspond, prendre le premier (cycle de l'anneau)
            if sorted_candidates[0] != i:  # Exclure i s'il est le premier
                finger_table.append(sorted_candidates[0])

    # Retourner la table des doigts sans doublons et respectant l'ordre
    return sorted(set(finger_table), key=finger_table.index)


