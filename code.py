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