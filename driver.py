
import json
import random
import sched
import sys
import time
from mpi4py import MPI

NUM_TICKS = 5
DELAY = 0.01

COMM = MPI.COMM_WORLD
NUM_NODES = COMM.Get_size()
RANK = COMM.Get_rank()

def createId():
    return random.randint(1000, 1000000)

def createNodes():
    node1 = {}
    node1["id"] = createId()
    node2 = {}
    node2["id"] = createId()
    node3 = {}
    node3["id"] = createId()

    return [
        node1,
        node2,
        node3,
    ]

class Node:
    def __init__(self):
        self.__running = True
        pass
    def __init(self, data):
        self.__id = data["id"]
        print("Create id:{0}".format(self.__id))
    def run(self):
        # Schedule ticks
        self.__sched = sched.scheduler(time.time, time.sleep)
        self.__sched.enter(0, 1, self.tick, ())
        self.__sched.run(blocking=True)
        while self.__running:
            pass



    def tick(self):
        recv = COMM.irecv(source=MPI.ANY_SOURCE)
        if recv.test():
            msg = recv.wait()
            if msg:
                if msg["key"] == "end":
                    self.__running = False
                    return # RETURN

                if msg["key"] == "init":
                    self.__init(msg["data"])

        self.__sched.enter(DELAY, 1, self.tick, ())
        self.__sched.run(blocking=True)

class MasterNode:
    def __init__(self):
        self.__tick = 0

    def run(self):
        for i in range(1, NUM_NODES):
            msg = {}
            msg["key"] = "init"
            msg["source"] = 0
            msg["data"] = {}
            msg["data"]["id"] = createId()
            COMM.send(msg, dest=i)

        # Instead each node will have its own schedule
        self.__sched = sched.scheduler(time.time, time.sleep)
        self.__sched.enter(5, 1, self.tick, ())
        self.__sched.run(blocking=True)



    def tick(self):
        for i in range(1, NUM_NODES):
            msg = {}
            msg["key"] = "end"
            msg["source"] = 0
            COMM.send(msg, dest=i)

if RANK == 0:
    mNode = MasterNode()
    mNode.run()
else:
    node = Node()
    node.run()

print("========== DONE {0} ==========".format(RANK))