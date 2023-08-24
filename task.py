from celery import Celery, Task

celery = Celery(__name__, broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')

@celery.task(bind=True)
def long_running_task(self):
    total_steps = 100
    for i in range(total_steps):
        self.update_state(state='PROGRESS', meta={'current': i, 'total': total_steps})
    return 1

class MyTask(Task):
    def run(self, arg1, arg2):
        print(arg1 ,arg2)
        result = arg1 * arg2
        self.update_state(state='PROGRESS', meta={'current': result, 'total': 100})
        return result


my_task_instance = celery.register_task(MyTask())
AsyncResult = celery.AsyncResult