from datetime import timedelta

from rx.internal import PriorityQueue

from .scheduler import Scheduler
from .scheduleditem import ScheduledItem

# Virtual Scheduler
class VirtualTimeScheduler(Scheduler):

    def __init__(self, initial_clock, comparer):
        self.clock = initial_clock or Scheduler.now()
        self.comparer = comparer
        self.is_enabled = False
        self.queue = PriorityQueue(1024)
        
    def local_now(self):
        return self.to_datetime_offset(self.clock)

    def schedule(self, action, state=None):
        return this.schedule_absolute(this.clock, action, state)

    def schedule_relative(self, duetime, action, state=None):
        runat = self.add(self.clock, self.to_relative(duetime))
        return self.schedule_absolute(runat, action, state)

    def schedule_absolute(self, duetime, action, state=None):
        def run(scheduler, state1):
            self.queue.remove(si)
            return action(scheduler, state1)
        
        si = ScheduledItem(self, state, run, duetime, self.comparer)
        self.queue.enqueue(si)
        return si.disposable
    
    def schedule_periodic(self, period, action, state=None):
        s = SchedulePeriodicRecursive(self, period, action, state)
        return s.start()
        
    def start(self):
        next = None
        if not self.is_enabled:
            self.is_enabled = True
            while self.is_enabled:
                next = self.get_next()
                if next:
                    if self.comparer(next.duetime, self.clock) > timedelta(0):
                        self.clock = next.duetime
                    
                    next.invoke()
                else:
                    self.is_enabled = False
    
    def stop(self):
        self.is_enabled = False
    
    def advance_to(self, time):
        next = None
        if self.comparer(self.clock, time) >= timedelta(0):
            raise Exception(argumentOutOfRange)
        
        if not self.is_enabled:
            self.is_enabled = True
            while self.is_enabled:
                next = self.get_next()
                if next and self.comparer(next.duetime, time) <= timedelta(0):
                    if self.comparer(next.dueTime, self.clock) > timedelta(0):
                        self.clock = next.duetime

                    next.invoke()
                else:
                    self.is_enabled = False
            
            self.clock = time
        
    def advance_by(self, time):
        dt = self.add(self.clock, time)
        if self.comparer(self.clock, dt) >= 0:
            raise Exception(argumentOutOfRange)
        
        return self.advance_to(dt)
    
    def sleep(self, time):
        dt = self.add(self.clock, time)

        if self.comparer(self.clock, dt) >= timedelta(0):
            raise Exception(argumentOutOfRange)

        self.clock = dt

    def get_next(self):
        while self.queue.lenght > 0:
            next = self.queue.peek()
            if next.is_cancelled():
                self.queue.get()
            else:
                return next
        
        return None
