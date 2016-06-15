from flask import Flask
from flask_restful import request, reqparse, abort, Api, Resource
import os
import json

app = Flask(__name__)
api = Api(app)



parser = reqparse.RequestParser()
parser.add_argument('text')
parser.add_argument('file')


#dispatch text
#url  http://unified.eng.vmware.com:8000/text
# action: post
# field name:text
class TextDispatcher(Resource):
    def get(self):
        return 'This is text get'
 
    def post(self):
        args = parser.parse_args()
        text = args['text']
        print text
        #####Todo...

        return 'text received', 200

  
#dispatch file
#url  http://unified.eng.vmware.com:8000/file 
#action:post
#fieldname:file
class FileDispatcher(Resource):
    def post(self):
        #args = parser.parse_args()
        #file = args['file']
        file = request.files['file']
        if file:
            f_name = file.filename
            print f_name
            #f_name = str(uuid.uuid4()) + extension
            file.save(os.path.join('/tmp/', f_name))
            return json.dumps({'filename':f_name})
        return 'upload failed', 500

   



#dispatch task
#url http://unified.eng.vmware.com:8000/task
#action post
#fieldname:task

class TaskDispatcher(Resource):
    def get(self):
        return 'This is text get'
 
    def post(self):
        args = parser.parse_args()
        task = args['task']
        #####Todo...

        return 'task received', 200

#dispatch pr
#url http://unified.eng.vmware.com:8000/pr
#action post
#fieldname:pr

class PRDispatcher(Resource):
    def get(self):
        return 'This is text get'
 
    def post(self):
        args = parser.parse_args()
        pr = args['pr']
        #####Todo...

        return 'pr received', 200



#dispatch sr
#url http://unified.eng.vmware.com:8000/sr
#action post
#fieldname:sr

class SRDispatcher(Resource):
    def get(self):
        return 'This is text get'
 
    def post(self):
        args = parser.parse_args()
        sr = args['sr']
        #####Todo...

        return 'sr received', 200






api.add_resource(TextDispatcher, '/text')
api.add_resource(FileDispatcher, '/file')
api.add_resource(TaskDispatcher, '/task')
api.add_resource(PRDispatcher, '/pr')
api.add_resource(SRDispatcher, '/sr')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)
