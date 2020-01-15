from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
TAG = 11

NUM_NODES = comm.Get_size()
MAX_RANK = NUM_NODES - 1
rank = comm.Get_rank()

MASTER_DEST = 0

COMM_KEYS = {};
COMM_KEYS["log"] = "log"
COMM_KEYS["end"] = "end"

def sendData(data, dest):
    commData = {}
    commData["key"] = "data"
    commData["data"] = data
    comm.send(commData, dest=dest)

def sendEnd(selfRank):
    endMsg = {}
    endMsg["key"] = "end"
    endMsg["data"] = selfRank
    comm.send(endMsg, dest=MASTER_DEST)

def log(message):
    if rank == MASTER_DEST:
        print(message)
    else:
        data = {}
        data["key"] = "log"
        data["data"] = message
        comm.send(data, dest=MASTER_DEST)

class Node:
    # Input and output weights - too general of a node (highly connected) won't
    # get triggered for everything when not that important
    # Activation threshold
    # "Analyze this website" - use Puppeteer to go to website
    # Nodes combine and strengthen (like muscles) and die over time
    # Some nodes are action outputs inputs feelings thoughts choices imagination
    def __init__(self):
        self.dataRecv = []
        self.rank = comm.Get_rank()
        log("Rank:{0} Created".format(self.rank))

    def send(self, data):
        sendTo = self.rank + 1
        sendData(data, dest=self.rank + 1)

    def waitForRequest(self):
        log("Rank:{0} Waiting".format(self.rank))
        while True:
            data = comm.recv(source=self.rank - 1)
            log("Rank:{0} Received:{1}".format(self.rank, data["data"]))
            self.dataRecv.append(data["data"])
            if (self.rank < MAX_RANK):
                self.send(data["data"] + 1)

            # Finally exit once telling any followers of last data
            if (len(self.dataRecv) == NUM_NODES):
                sendEnd(self.rank)
                return

class MasterNode:
    def __init__(self):
        pass
    def start(self):
        for itr in range(0,NUM_NODES):
            log("Rank:{0} Send:{1} To:{2}".format(rank, itr, 1))
            sendData(itr, dest=1)

        endCount = 0
        while True:
            data = comm.recv(source=MPI.ANY_SOURCE)
            if data["key"] == "end":
                endCount += 1
                if endCount == MAX_RANK:
                    break
            if data["key"] == "log":
                log(data["data"])


if rank == 0:
    masterNode = MasterNode()
    masterNode.start()
else:
    node = Node()
    node.waitForRequest()


print("===== END: " + str(rank) + "  =====")


