from collections import namedtuple
import requests

from .tasks import Task

DEFAULT_FIELDS = {'callback_url', 'instruction', 'urgency', 'metadata'}
ALLOWED_FIELDS = {'categorization': {'attachment', 'attachment_type', 'categories',
                                     'category_ids', 'allow_multiple', 'layers'},
                  'transcription': {'attachment', 'attachment_type',
                                    'fields', 'repeatable_fields'},
                  'phonecall': {'attachment', 'attachment_type', 'phone_number',
                                'script', 'entity_name', 'fields', 'choices'},
                  'comparison': {'attachments', 'attachment_type',
                                 'fields', 'choices'},
                  'annotation': {'attachment', 'attachment_type', 'instruction',
                                 'objects_to_annotate', 'with_labels', 'examples',
                                 'min_width', 'min_height', 'layers'},
                  'polygonannotation': {'attachment', 'attachment_type', 'instruction',
                                 'objects_to_annotate', 'with_labels', 'layers'},
                  'cuboidannotation': {'attachment', 'attachment_type', 'instruction',
                                 'objects_to_annotate', 'min_width', 'min_height', 'with_labels', 'layers'},
                  'audiotranscription': {'attachment', 'attachment_type', 'verbatim', 'phrases'},
                  'annotation': {'attachment', 'attachment_type', 'instruction', 'objects_to_annotate', 'with_labels', 'examples', 'min_width', 'min_height', 'layers', 'annotation_attributes'},
                  'polygonannotation': {'attachment', 'attachment_type', 'instruction', 'objects_to_annotate', 'with_labels', 'examples', 'layers', 'annotation_attributes'},
                  'lineannotation':
                    {'attachment', 'attachment_type', 'instruction', 'objects_to_annotate', 'with_labels', 'examples', 'splines', 'layers', 'annotation_attributes'},
                  'datacollection': {'attachment', 'attachment_type', 'fields'},
                  'pointannotation': {'attachment_type','attachment', 'objects_to_annotate','with_labels', 'examples', 'layers','annotation_attributes'},
                  'segmentannotation': {'attachment_type','attachment', 'labels', 'allow_unlabeled'}}
SCALE_ENDPOINT = 'https://api.scaleapi.com/v1/'
DEFAULT_LIMIT = 100
DEFAULT_OFFSET = 0


def validate_payload(task_type, kwargs):
    allowed_fields = DEFAULT_FIELDS | ALLOWED_FIELDS[task_type]
    for k in kwargs:
        if k not in allowed_fields:
            raise ScaleInvalidRequest('Illegal parameter %s for task_type %s'
                                      % (k, task_type), None)


class ScaleException(Exception):
    def __init__(self, message, errcode):
        super(ScaleException, self).__init__(message)
        self.code = errcode


class ScaleInvalidRequest(ScaleException, ValueError):
    pass


class Tasklist(list):
    def __init__(self, docs, total, limit, offset, has_more):
        super(Tasklist, self).__init__(docs)
        self.docs = docs
        self.total = total
        self.limit = limit
        self.offset = offset
        self.has_more = has_more


class ScaleClient(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def _getrequest(self, endpoint, params={}):
        """Makes a get request to an endpoint.

        If an error occurs, assumes that endpoint returns JSON as:
            { 'status_code': XXX,
              'error': 'I failed' }
        """
        r = requests.get(SCALE_ENDPOINT + endpoint,
                         headers={"Content-Type": "application/json"},
                         auth=(self.api_key, ''), params=params)

        if r.status_code == 200:
            return r.json()
        raise ScaleException(r.json()['error'], r.status_code)

    def _postrequest(self, endpoint, payload=None):
        """Makes a post request to an endpoint.

        If an error occurs, assumes that endpoint returns JSON as:
            { 'status_code': XXX,
              'error': 'I failed' }
        """
        payload = payload or {}
        r = requests.post(SCALE_ENDPOINT + endpoint, json=payload,
                          headers={"Content-Type": "application/json"},
                          auth=(self.api_key, ''))

        if r.status_code == 200:
            return r.json()
        if r.status_code == 400:
            raise ScaleInvalidRequest(r.json()['error'], r.status_code)
        raise ScaleException(r.json()['error'], r.status_code)

    def fetch_task(self, task_id):
        """Fetches a task.

        Returns the associated task.
        """
        return Task(self._getrequest('task/%s' % task_id), self)

    def cancel_task(self, task_id):
        """Cancels a task.

        Returns the associated task.
        Raises a ScaleException if it has already been canceled.
        """
        return Task(self._postrequest('task/%s/cancel' % task_id), self)

    def tasks(self, **kwargs):
        """Returns a list of your tasks.
        Returns up to 100 at a time, to get more use the offset param.

        start/end_time are ISO8601 dates, the time range of tasks to fetch.
        status can be 'completed', 'pending', or 'canceled'.
        type is the task type.
        limit is the max number of results to display per page,
        offset is the number of results to skip (for showing more pages).
        """
        allowed_kwargs = {'start_time', 'end_time', 'status', 'type', 'limit', 'offset'}
        for key in kwargs:
            if key not in allowed_kwargs:
                raise ScaleInvalidRequest('Illegal parameter %s for ScaleClient.tasks()'
                                          % key, None)
        response = self._getrequest('tasks', params=kwargs)
        docs = [Task(json, self) for json in response['docs']]
        return Tasklist(docs, response['total'], response['limit'],
                        response['offset'], response['has_more'])

    def create_categorization_task(self, **kwargs):
        validate_payload('categorization', kwargs)
        taskdata = self._postrequest('task/categorize', payload=kwargs)
        return Task(taskdata, self)

    def create_transcription_task(self, **kwargs):
        validate_payload('transcription', kwargs)
        taskdata = self._postrequest('task/transcription', payload=kwargs)
        return Task(taskdata, self)

    def create_phonecall_task(self, **kwargs):
        raise ScaleException('Phone call tasks have been deprecated and are no longer available.', 400)

    def create_comparison_task(self, **kwargs):
        validate_payload('comparison', kwargs)
        taskdata = self._postrequest('task/comparison', payload=kwargs)
        return Task(taskdata, self)

    def create_annotation_task(self, **kwargs):
        validate_payload('annotation', kwargs)
        taskdata = self._postrequest('task/annotation', payload=kwargs)
        return Task(taskdata, self)

    def create_polygonannotation_task(self, **kwargs):
        validate_payload('polygonannotation', kwargs)
        taskdata = self._postrequest('task/polygonannotation', payload=kwargs)
        return Task(taskdata, self)

    def create_lineannotation_task(self, **kwargs):
        validate_payload('lineannotation', kwargs)
        taskdata = self._postrequest('task/lineannotation', payload=kwargs)
        return Task(taskdata, self)

    def create_datacollection_task(self, **kwargs):
        validate_payload('datacollection', kwargs)
        taskdata = self._postrequest('task/datacollection', payload=kwargs)
        return Task(taskdata, self)

    def create_audiotranscription_task(self, **kwargs):
        validate_payload('audiotranscription', kwargs)
        taskdata = self._postrequest('task/audiotranscription', payload=kwargs)
        return Task(taskdata, self)

    def create_pointannotation_task(self, **kwargs):
        validate_payload('pointannotation', kwargs)
        taskdata = self._postrequest('task/pointannotation', payload=kwargs)
        return Task(taskdata, self)

    def create_segmentannotation_task(self, **kwargs):
        validate_payload('segmentannotation', kwargs)
        taskdata = self._postrequest('task/segmentannotation', payload=kwargs)
        return Task(taskdata, self)
