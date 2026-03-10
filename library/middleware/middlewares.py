import json

def input_middleware(get_response):
    # get_response is the next layer (output_middleware)
    # this outer part runs once when server starts
    print('input_middleware')
    def middleware(request):
        # STEP 1: runs before view
        # request comes in from client, we add efe_new if not exists
        if not hasattr(request, 'efe_new'):
            request.efe_new = 'before_views_value'
        print('input_middleware_response_oncesi')
        # pass request to output_middleware and wait until everything inside finishes
        response = get_response(request)

        print('input_middleware_response_sonrasi')
        # STEP 5: runs after view, output_middleware already finished
        # response is ready, we just return it
        return response

    return middleware

def output_middleware(get_response):
    # get_response is the next layer (the view)
    # this outer part runs once when server starts
    print('output_middleware')
    def middleware(request):
        # STEP 2: runs before view
        # pass request to the view and wait
        print('output_middleware_response_oncesi')
        response = get_response(request)
        print('output_middleware_response_sonrasi')
        # STEP 4: runs after view returns the response
        # efe_new was set by input_middleware, we update it and add to response JSON
        if hasattr(request, 'efe_new'):
            data = json.loads(response.content)
            data['efe_new'] = 'updated_at_output_middleware'
            response.content = json.dumps(data)

        return response

    return middleware