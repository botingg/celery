from flask_restx import Namespace, fields, Resource
import ast

from db import Database as db

api = Namespace("account", description="帳號管理")

base_output_payload = api.model('基本輸出', {
    'status': fields.String(required=True, default=0),
    'message': fields.String(required=True, default="")
})

account_register_input_payload = api.model('註冊帳號input', {
    'email': fields.String(required=True, example="test01@gmail.com"),
    'password': fields.String(required=True, example="test")
})

account_register_output_payload = api.clone('註冊帳號output', base_output_payload)

@api.route('/register')
class register(Resource):
    @api.expect(account_register_input_payload)
    @api.marshal_with(account_register_output_payload)
    def post(self):
        data = api.payload
        try:
            nums = str(db.length('users'))
            data = str({'email': data['email'], 'password': data['password']})
            db.insert('users', nums, data)
        except Exception:
            message = {'status': 1, 'message': 'error'}
        else:
            message = {'status': 0, 'message': ''}
        finally:
            return message