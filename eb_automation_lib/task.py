from functools import total_ordering
from queue import PriorityQueue
from threading import Thread
from uuid import uuid1


class Queue(PriorityQueue):
    """Queue is a subclass of PriorityQueue, with a few extra methods and a
    worker pool of daemon threads that will work on Tasks in the queue. Can only add
    objects of type Task to the queue.
    >>>q = Queue()
    >>>q.start_work()
    >>>q.put(Task(some_func))
    # This task is being worked on now
    """
    def __init__(self, maxsize=0, max_workers=8):
        PriorityQueue.__init__(self, maxsize=maxsize)
        self.max_workers = max_workers
        self.task_messages = []

    def put(self, item, block=True, timeout=None):
        if isinstance(item, Task):
            PriorityQueue.put(self, item, block=block, timeout=timeout)
        else:
            raise ValueError('Only Task objects can be put into Queue. Received {}'.format(item))

    def start_work(self):
        for i in range(self.max_workers):
            worker = Thread(target=self._worker_target, daemon=True)
            worker.start()

    def _worker_target(self):
        task = self.get()
        result, callback_result = task.do()
        msg = {task.id: {}}
        if result:
            msg[task.id]['todo'] = result
        if callback_result:
            msg[task.id]['callback'] = callback_result

        if msg.get(task.id):
            self.task_messages.append(msg)


@total_ordering
class Task:
    """Meant to be added to Queue class in the module. A Task added to a Queue
    will have it's todo and callback functions executed asynchronously. Return values
    from todo, callback can be accesed in Queue.task_messages[task.id]. You can get the task id like so
    task = Task()
    task_id = task.id
    """
    def __init__(self, todo, args=(), priority=3, description=None, callback=None, callback_args=()):
        if not callable(todo) and not callable(callback) and callback is not None:
            msg = 'Task todo, callback must be callable. Received: todo: {}, callback: {}'
            raise ValueError(msg.format(todo, callback))

        self.todo = todo
        self.args = args if hasattr(args, '__iter__') else (args,)
        self.priority = priority
        self.description = description or todo.__str__()
        self.callback = callback
        self.id = str(uuid1())
        self.callback_args = callback_args if hasattr(callback_args, '__iter__') else (callback_args,)

    def do(self):
        if self.callback:
            return self.todo(*self.args), self.callback(*self.callback_args)

        return self.todo(*self.args), None

    def __lt__(self, other):
        self.priority < other.priority

    def __eq__(self, other):
        self.priority == other.priority
