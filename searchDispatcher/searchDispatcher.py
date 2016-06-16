import sys
from flask import Flask
from flask_restful import request, reqparse, abort, Api, Resource
import os
import json

sys.path.append('..')
from common.textMatcher import TextMatcher
from common.indexMatcher import IndexMatcher



#matcher.....
textMatcher = TextMatcher()
indexMatcher = IndexMatcher()
    

#dispatch text
#url  http://unified.eng.vmware.com:8000/text
# action: post
# field name:text
class TextDispatcher(Resource):
    

    def get(self):
        #self.m = TextMatcher()
        return 'This is text get'
 
    def post(self):
        if request.form.haskey['text']:
            text = request.form['text']
            print text
            return 'Not text founded in request', 400

        #by default max result is 10
        size = 10
        #by default minscore is 0.5
        minscore = 0.5

        if request.form.haskey['size']:
            size = request.form['size']
        if request.form.haskey['minscore']:
            minscore = request.form['minscore']
        ret = textMatcher.match(text, size, minscore)

        #return 'text received', 200
        return ret

  
#dispatch file
#url  http://unified.eng.vmware.com:8000/file 
#action:post
#fieldname:file
class FileDispatcher(Resource):
    def post(self):
        file = request.files['file']
        if file:
            f_name = file.filename
            print f_name
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





class Service:
    def __init__(self):
        self.createApp()
        
    def createApp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
 
        self.api.add_resource(TextDispatcher, '/text')
        self.api.add_resource(FileDispatcher, '/file')
        self.api.add_resource(TaskDispatcher, '/task')
        self.api.add_resource(PRDispatcher, '/pr')
        self.api.add_resource(SRDispatcher, '/sr')
 

    def start(self):
        self.app.run(host='0.0.0.0', port=8000,debug=True)
        #self.app.run(host='0.0.0.0', port=8000)



       


if __name__ == '__main__':
    #textMatcher = TextMatcher()
    s = Service()
    s.start()

