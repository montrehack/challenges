from bottle import run, route, get, post, request, template, static_file
import os
import sys
import hashlib
import license_validator

PINNED_LICENSE_VALIDATOR_FILE_MD5_HASH='8280b4a5ea2300582e4590225ba415e4'

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/')
    
@get('/')
def index():
    print request.query.c
    license_key_validation_result = license_validator.validate_license_key(request.query.c)
    return template('index', support=request.query.support, debug=request.query.debug, debug_output=license_key_validation_result)
    
@post('/upload_new_license_file')
def upload():
    new_license_file = request.files.get('new_license_file')
    new_license_file_data = new_license_file.file.read()
    new_license_file.file.seek(0) # Reset file pointer so we can read twice
    new_license_file_hash = hashlib.md5(new_license_file_data).hexdigest()
    license_upload_error = None
    
    print 'Uploaded filename: ' + new_license_file.filename
    print 'Uploaded file hash: ' + new_license_file_hash
    
    if new_license_file.filename != 'license_validator.py' or new_license_file_hash != PINNED_LICENSE_VALIDATOR_FILE_MD5_HASH:
        license_upload_error = 'License file MUST be named license_validator.py AND have a MD5 hash of ' + PINNED_LICENSE_VALIDATOR_FILE_MD5_HASH
    else:
        new_license_save_path = os.path.dirname(os.path.abspath(__file__)) + '/'
        new_license_file.save(new_license_save_path, overwrite=True)
        print 'Succesfully updated license file at: ' + new_license_save_path
    return template('index', support=request.forms.get('support'), debug=request.forms.get('debug'), debug_output=license_upload_error)
    
run(host='0.0.0.0', port=8080, debug=True, reloader=True)