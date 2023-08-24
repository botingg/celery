from flask import Flask, request
import config
from  config import config
from task import my_task_instance, long_running_task, celery
from flask_restx import Namespace, fields, Resource, Api

app = Flask(__name__)
app.config.from_object(config)

api = Api(app, version='0.0.1', title='celery_text', doc='/api/practice')
ns = Namespace("account", description="帳號管理")
api.add_namespace(ns)

base_output_payload = api.model('第一支', {
    'name': fields.String(required=True, description='名字', example='123'),
    'email': fields.String(required=True, description='信箱', example='123')})

@ns.route('/decorator_class')
class Test(Resource):
    @api.doc(params={'a': 'a', 'b': 'b'})
    def get(self):
        a = int(request.args.get('a', 0))
        b = int(request.args.get('b', 0))
        tasks = my_task_instance.delay(a, b)
    
        return dict(
            task_id=tasks.id,
            status=tasks.state
        )

@ns.route('/text')
class register(Resource):
    def post(self):
        tasks = long_running_task.delay()
        return dict(
            task_id=tasks.id,
            status=tasks.state,
        )

# get status and result value from task_id
@ns.route('/get_result/<string:task_id>')
class get_result(Resource):
    @api.expect(base_output_payload)
    def get(self, task_id):
        task = celery.AsyncResult(task_id)
        return dict(
            task_id=task.id,
            status=task.state,
            get_result=task.get(),
            # get_result=task.result
        )
if __name__ == "__main__":
    app.run(debug=True)