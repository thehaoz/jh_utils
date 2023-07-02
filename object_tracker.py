import numpy as np
import time

class State:
    Idle = 1
    Active = 2
    Tentative = 3

class StateTracker(object):
    def __init__(self):
        self.runtime = 0

    @property
    def getState(self):
        raise NotImplementedError

    @property
    def getRunTime(self):
        return self.runtime

    def startRunTime(self):
        self.runtime = time.time()
    
    def getTimeDelta(self):
        return time.time() - self.runtime
    
    def __repr__(self):
        return f"{self.__class__.__name__} runtime : {self.getTimeDelta()}"

class Idle(StateTracker):
    def __init__(self):
        super().__init__()
        self.state = State.Idle
        self.startRunTime()

    @property
    def getState(self):
        return self.state
    
class Active(StateTracker):
    def __init__(self):
        super().__init__()
        self.state = State.Active
        self.startRunTime()

    @property
    def getState(self):
        return self.state
    
class Activity:
    def __init__(self, idx, timeout):
        self.idx = idx
        self.state = None
        self.stateTrack = None
        self.timeout = timeout
        self.timer = 0
        self.setState(State.Idle)
        
    def setState(self, state):
        if state == State.Idle:
            self.stateTrack = Idle()
            self.state = state
        elif state == State.Active:
            if self.state == State.Tentative:
                self.state = State.Active
            else:
                self.stateTrack = Active()
                self.state = state
        elif state == State.Tentative:
            self.state = state
        else:
            raise ValueError("Invalid State")
        
    @property
    def getState(self):
        return self.state, self.stateTrack
    
    def reset(self):
        self.timer = 0
        self.setState(State.Idle)

    def markActive(self):
        self.setState(State.Active)
        # print(f"{self.idx} is active")

    def markMissed(self):
        self.setState(State.Tentative)
        self.timer = time.time()
        # print(f"{self.idx} is missed")

    def markIdle(self):
        if self.state == State.Tentative:
            if time.time() - self.timer > self.timeout:
                self.setState(State.Idle)
                self.timer = 0
                # print(f"{self.idx} is idle")

    def __repr__(self):
        return f"Activity({self.idx}, {self.stateTrack})"

class ArrayObserver:
    def __init__(self, array, timeout, observer=[]):
        self.timeout = timeout
        array = np.ones_like(array)
        x,y=np.nonzero(array)
        self.XY = tuple(map(lambda x : tuple(x), np.hstack([x.reshape(-1,1),y.reshape(-1,1)])))
        self.array_tracker = dict(zip(self.XY,[Activity(xy, timeout) for xy in self.XY]))
        self.observers = observer

    def refresh(self, array):
        x,y=np.nonzero(array)
        xy = tuple(map(lambda x : tuple(x), np.hstack([x.reshape(-1,1),y.reshape(-1,1)])))
        # print(xy)
        for k in self.array_tracker.keys():
            if k in xy:
                self.array_tracker[k].markActive()

        remaining = set(self.array_tracker.keys()) - set(xy)

        for k in remaining:
            if self.array_tracker[k].getState[0] == State.Active:
                self.array_tracker[k].markMissed()

        for k in self.array_tracker.keys():
            self.array_tracker[k].markIdle()

    def reset(self):
        for k in self.array_tracker.keys():
            self.array_tracker[k].reset()

    def observe(self):
        try:
            for obs in self.observers:
                obs(self.array_tracker)
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    def getState(array_tracker):
        for k in array_tracker.keys():
            state, stateTrack = array_tracker[k].getState
            print(stateTrack)
    def getActive(array_tracker):
        for k in array_tracker.keys():
            state, stateTrack = array_tracker[k].getState
            if stateTrack.getState == State.Active and stateTrack.getTimeDelta() > 0.5:
                print(f"{k} is active for more than 30s")

    def getIdle(array_tracker):
        for k in array_tracker.keys():
            state, stateTrack = array_tracker[k].getState
            if stateTrack.getState == State.Idle and stateTrack.getTimeDelta() > 0.5:
                print(f"{k} is idle for more than 30s")


    # a = np.random.randint(0,1,(10,10))
    a = np.zeros(shape=(10,10))
    a[0,0] = 1
    a[2,2] = 1
    a[1,5] = 1
    a[3,3] = 1
    
    arrayO = ArrayObserver(a, 5, observer=[getActive,getIdle])

    randlist = [(0,0), (5,3), (3,2), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (1,1)]
    for i in range(10):
        print("-------------")
        print(a)
        # a = np.random.randint(0,2,(10,10))
        a[randlist[i]] = 1
        arrayO.refresh(a)
        arrayO.observe()
        time.sleep(1)

    # print(arrayO.getArray)
    # print(a)
    # a = Idle()
    # b = Active()
    # print(a)
    # time.sleep(5)
    # print(a)
    # time.sleep(1)
    # print(a)

