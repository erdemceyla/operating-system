import numpy as np
import random

class Process:
    def __init__(self, pid, arrival, burst, ram_req, resource_req):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.ram_req = ram_req
        self.resource_req = np.array(resource_req)
        self.waiting_time = 0

def generate_workload(n, lam, mu_burst, sig_burst, mu_ram, sig_ram, max_resources):
    processes = []
    curr_time = 0.0
    
    inter_arrivals = np.random.exponential(1/lam, n)
    bursts = np.maximum(np.random.normal(mu_burst, sig_burst, n), 0.1)
    ram_reqs = np.maximum(np.random.normal(mu_ram, sig_ram, n), 10.0)
    
    for i in range(n):
        curr_time += inter_arrivals[i]
        res_req = []
        for res_capacity in max_resources:
            max_requestable = max(1, int(res_capacity * 0.6))
            res_req.append(random.randint(0, max_requestable))
            
        p = Process(i+1, curr_time, bursts[i], int(ram_reqs[i]), res_req)
        processes.append(p)
        
    return processes