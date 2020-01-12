from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
TAG = 11

MAX_RANK = comm.Get_size() - 1

class Node:
    def __init__(self):
        self.dataRecv = []
        self.rank = comm.Get_rank()
        print("Rank:{0} Created".format(self.rank))

    def send(self, data):
        sendTo = self.rank + 1
        comm.send(data, dest=self.rank + 1)

    def waitForRequest(self):
        print("Rank:{0} Waiting".format(self.rank))
        while True:
            data = comm.recv(source=self.rank - 1)
            print("Rank:{0} Received:{1}".format(self.rank, data))
            self.dataRecv.append(data)
            if (self.rank < MAX_RANK):
                self.send(data + 1)

            # Finally exit once telling any followers of last data
            if (len(self.dataRecv) == 5):
                return


rank = comm.Get_rank()
if rank == 0:
    for itr in range(0,5):
        print("Rank:{0} Send:{1} To:{2}".format(rank, itr, 1))
        req = comm.send(itr, dest=1)
else:
    node = Node()
    node.waitForRequest()


print("===== END: " + str(rank) + "  =====")


