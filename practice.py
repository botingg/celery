from task import long_running_task, my_task_instance
tasks = my_task_instance.delay(5,10)
print(tasks.id)
print(tasks.get())
print(tasks.status)