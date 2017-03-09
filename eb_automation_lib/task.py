from functools import total_ordering
from queue import PriorityQueue
from threading import Thread
from uuid import uuid1


class Queue(PriorityQueue):
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
            msg[task.id]['result'] = result
        if callback_result:
            msg[task.id]['callback_result'] = callback_result

        if msg.get(task.id):
            self.task_messages.append(msg)


@total_ordering
class Task:
    def __init__(self, todo, args=(), priority=3, description=None, on_complete=None, callback_args=()):
        if not callable(todo) and not callable(on_complete) and on_complete is not None:
            msg = 'Task todo, on_complete must be callable. Received: todo: {}, on_complete: {}'
            raise ValueError(msg.format(todo, on_complete))

        self.todo = todo
        self.args = args if hasattr(args, '__iter__') else (args,)
        self.priority = priority
        self.description = description or todo.__str__()
        self.on_complete = on_complete
        self.id = str(uuid1())
        self.callback_args = callback_args if hasattr(callback_args, '__iter__') else (callback_args,)

    def do(self):
        if self.on_complete:
            return self.todo(*self.args), self.on_complete(*self.callback_args)

        return self.todo(*self.args), None

    def __lt__(self, other):
        self.priority < other.priority

    def __eq__(self, other):
        self.priority == other.priority
