"""
Log paging for django applications

Because logs are dynamically increase it is impossible to page through them using conventional methods.
This code use log entry id for limiting number of entries in a page.

params: (query string GET method)
    - after::int (specify starting log id)
    - before::int (specify ending log id)
    - after_dt::datetime (specify starting datetime)
    - before_dt::datetime (specify ending datetime)
    - reverse::<value does not matter> (send entries in reverse order)
    - number::int (specify number of entries in a page)

output:
    - log entries in json format


author:
    - name: Mohammad Javad Beheshtian
    - email: beheshtraya@gmail.com
    - github: https://github.com/beheshtraya

date: 2016.11.06
version: 1.0
license: MIT

"""


from django.http.response import HttpResponse
from django.utils.dateparse import parse_datetime
from django.core import serializers
import json
# from [app.models] import Log

LOGS_PER_PAGE = 15

# DB schema: Log(id, datetime, severity, message::json(id, text, additional fields ...))


class LogsView(View):
    def get(self, request):
        logs = Log.objects.using('[db name]')  # optional if using default database
        logs = logs.order_by('datetime')

        # other filters will be done here

        output_list = paging(logs, request)

        if isinstance(output_list, HttpResponse):
            return output_list

        return HttpResponse(status=200,
                            content=response_string(output_list, 'Logs loaded successfully', 'Ok', 200, 'null'),
                            content_type='application/json')


def paging(logs, request):
    has_new = False
    has_old = False

    if 'source' in request.GET:
        logs = logs.filter(source=request.GET['source'])

        if not logs:
            return HttpResponse(status=404,
                                content=response_string([], 'No logs found', 'Error!', 404, 'null'),
                                content_type='application/json')

    if 'before_dt' in request.GET:
        before_datetime = request.GET['before_dt']
        before_datetime = parse_datetime(before_datetime)
        if not before_datetime:
            return HttpResponse(status=400,
                                content=response_string([],
                                                        'before value should be datetime. sample: 2016-11-05T13:13:28.669',
                                                        'Error!', 400, 'null'),
                                content_type='application/json')

        total_len = len(logs)
        logs = logs.filter(datetime__lt=before_datetime)

        if total_len != len(logs):
            has_new = True

        if not logs:
            return HttpResponse(status=404,
                                content=response_string([], 'No logs found', 'Error!', 404, 'null'),
                                content_type='application/json')

    if 'after_dt' in request.GET:
        after_datetime = request.GET['after_dt']
        after_datetime = parse_datetime(after_datetime)
        if not after_datetime:
            return HttpResponse(status=400,
                                content=response_string([],
                                                        'after value should be datetime. sample: 2016-11-05T13:13:28.669',
                                                        'Error!', 400, 'null'),
                                content_type='application/json')

        total_len = len(logs)
        logs = logs.filter(datetime__gt=after_datetime)
        if total_len != len(logs):
            has_old = True
        if not logs:
            return HttpResponse(status=404,
                                content=response_string([], 'No logs found', 'Error!', 404, 'null'),
                                content_type='application/json')

    if 'before' in request.GET:
        before = request.GET['before']
        total_len = len(logs)
        logs = logs.filter(id__lt=before)

        if total_len != len(logs):
            has_new = True

        if not logs:
            return HttpResponse(status=404,
                                content=response_string([], 'No logs found', 'Error!', 404, 'null'),
                                content_type='application/json')

    if 'after' in request.GET:
        after = request.GET['after']

        total_len = len(logs)
        logs = logs.filter(id__gt=after)
        if total_len != len(logs):
            has_old = True

        if not logs:
            return HttpResponse(status=404,
                                content=response_string([], 'No logs found', 'Error!', 404, 'null'),
                                content_type='application/json')

    if 'number' in request.GET:
        limit = int(request.GET['number'])
    else:
        limit = LOGS_PER_PAGE

    total_len = len(logs)

    if 'reverse' in request.GET:
        logs = logs[:limit]
        if total_len != len(logs):
            has_new = True
    else:
        logs = logs[::-1][:limit][::-1]
        if total_len != len(logs):
            has_old = True

    list_items = list()
    for item in logs:
        serialized_tender = serializers.serialize('json', [item])
        each_item = json.loads(serialized_tender)

        # convert text to unicode-escape to display correctly
        if 'text' in each_item[0]['fields']['message']:
            each_item[0]['fields']['message']['text'] = each_item[0]['fields']['message']['text'].encode().decode(
                'unicode-escape')

        list_items.append(each_item[0])

    output_list = list()
    output_list.append(list_items)

    paging_info = {
        'has_new': has_new,
        'has_old': has_old
    }

    output_list.append(paging_info)

    return output_list


def response_string(body, message, status, code, redirect):
    response = {'body': body, 'message': message, 'status': status, 'code': code, 'redirect': redirect}
    return json.dumps(response)

