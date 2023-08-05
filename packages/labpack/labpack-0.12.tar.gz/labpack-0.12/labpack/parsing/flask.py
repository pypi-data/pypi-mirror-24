__author__ = 'rcj1492'
__created__ = '2016.10'
__license__ = 'MIT'

'''
app.test_request_context(**kwargs):
# query_string=None,
# method='GET'
# input_stream=None
# content_type=None
# content_length=None
# errors_stream=None
# multithread=False,
# multiprocess=False
# run_once=False
# headers=None
# data=None
# environ_base=None
# environ_overrides=None
# charset='utf-8'
'''

def extract_request_details(request_object, session_object=None):

    '''
        a method for extracting request details from request and session objects

        NOTE:   method is also a placeholder funnel for future validation
                processes, request logging, request context building and
                counter-measures for the nasty web

    :param request_object: request object generated by flask from request route
    :param session_object: session object generated by flask from client cookie
    :return: dictionary with request details
    '''

    request_details = {
        'error': '',
        'status': 'ok',
        'code': 200,
        'method': request_object.method,
        'session': {},
        'root': request_object.url_root,
        'route': request_object.path,
        'headers': {},
        'form': {},
        'params': {},
        'json': {},
        'data': ''
    }

# automatically add header and query field data
    request_details['headers'].update(**request_object.headers)
    for key in request_object.args.keys():
        request_details['params'][key] = request_object.args.get(key)

# retrieve session details
    if session_object:
        request_details['session'].update(**session_object)

# add data based upon type
    if request_object.is_json:
        try:
            json_details = request_object.get_json(silent=True)
            if isinstance(json_details, dict):
                request_details['json'] = json_details
        except:
                pass
    else:
        try:
            from base64 import b64encode
            request_details['data'] = b64encode(request_object.data).decode()
        except:
            pass
        try:
            for key, value in request_object.form.items():
                request_details['form'][key] = value
        except:
            pass

# TODO: handle non-json data parsing (such as by mimetype and request.files)
# TODO: check content type against buffer values
# TODO: status code and error handling

    return request_details

def extract_session_details(request_headers, session_header, secret_key):

    '''
        a method to extract and validate jwt session token from request headers

    :param request_headers: dictionary with header fields from request
    :param session_header: string with name of session token header key
    :param secret_key: string with secret key to json web token encryption
    :return: dictionary with request details with session details or error coding
    '''

    session_details = {
        'error': '',
        'code': 200,
        'session': {}
    }

    if not session_header in request_headers.keys():
        session_details['error'] = '%s is missing.' % session_header
        session_details['code'] = 400
    else:
        import jwt
        session_token = request_headers[session_header]
        try:
            session_details['session'] = jwt.decode(session_token, secret_key)
        except jwt.DecodeError as err:
            session_details['error'] = 'Session token decoding error.'
            session_details['code'] = 400
        except jwt.ExpiredSignatureError as err:
            session_details['error'] = 'Session token has expired.'
            session_details['code'] = 400
        except Exception:
            session_details['error'] = 'Session token is invalid.'
            session_details['code'] = 400

    return session_details

def validate_request_content(request_content, request_model):
    
    '''
        a method to validate the content fields of a flask request
        
    :param request_content: dictionary with content fields to validate 
    :param request_model: object with jsonmodel class properties
    :return: dictionary with validation status details
    '''

# import dependencies
    from jsonmodel.validators import jsonModel
    from jsonmodel.exceptions import InputValidationError

    title = 'validate_request_content'

# validate inputs
    if not isinstance(request_content, dict):
        raise TypeError('%s(request_content={...}) must be a dictionary.' % title)
    elif not isinstance(request_model, jsonModel):
        raise TypeError('%s(request_model=<...>) must be a %s object.' % (title, jsonModel.__class__))

# construct default status details
    status_details = {
        'code': 200,
        'error': ''
    }

# validate request details
    for key, value in request_model.schema.items():
        comp_key = '.%s' % key
        if request_model.keyMap[comp_key]['required_field']:
            if not key in request_content.keys():
                status_details['code'] = 400
                status_details['error'] = "request is missing a value for required field '%s'" % key
                break
        elif key in request_content.keys():
            try:
                object_title = "request field '%s'" % key
                request_model.validate(request_content[key], '.%s' % key, object_title)
            except InputValidationError as err:
                status_details['error'] = err.message.replace('\n',' ').lstrip()
                status_details['code'] = 400
                break

    return status_details

if __name__ == '__main__':
# work around for namespace collision
    from sys import path as sys_path
    sys_path.append(sys_path.pop(0))
    from flask import Flask, jsonify, request
    sys_path.insert(0, sys_path.pop())
    app = Flask(import_name=__name__)
    @app.route('/test')
    def test_route():
        return jsonify({'status':'ok'}), 200
    import json
    request_kwargs = {
        'content_type': 'application/json',
        'data': json.dumps({'test':'request'}).encode('utf-8'),
        'query_string': 'test=yes'
    }
    with app.test_request_context('/test', **request_kwargs):
        request_details = extract_request_details(request)
        print(request_details)