# Python Version: 3.x
import onlinejudge.service
import onlinejudge.problem
import onlinejudge.dispatch
import onlinejudge.implementation.utils as utils
import onlinejudge.implementation.logging as log
import re
import requests
import urllib.parse
import posixpath
import json


@utils.singleton
class CSAcademyService(onlinejudge.service.Service):

    def get_url(self):
        return 'https://csacademy.com/'

    def get_name(self):
        return 'csacademy'

    @classmethod
    def from_url(cls, s):
        # example: https://csacademy.com/
        result = urllib.parse.urlparse(s)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc in ('csacademy.com', 'www.csacademy.com'):
            return cls()


class CSAcademyProblem(onlinejudge.problem.Problem):
    def __init__(self, contest_name, task_name):
        self.contest_name = contest_name
        self.task_name = task_name

    def download(self, session=None):
        session = session or requests.Session()

        # get csrftoken
        url = self.get_url()
        log.status('GET: %s', url)
        resp = session.get(url)
        log.status(utils.describe_status_code(resp.status_code))
        resp.raise_for_status()
        csrftoken = None
        for cookie in session.cookies:
            if cookie.name == 'csrftoken' and cookie.domain == 'csacademy.com':
                csrftoken = cookie.value
        if csrftoken is None:
            log.error('csrftoken is not found')
            return []

        # get config
        headers = {
                'x-csrftoken': csrftoken,
                'x-requested-with': 'XMLHttpRequest',
            }
        contest_url = 'https://csacademy.com/contest/{}/'.format(self.contest_name)
        log.status('GET: %s', contest_url)
        resp = session.get(contest_url, headers=headers)
        log.status(utils.describe_status_code(resp.status_code))
        resp.raise_for_status()
        # parse config
        assert resp.encoding is None
        config = json.loads( resp.content.decode() ) # NOTE: Should I memoize this? Is the CSAcademyRound class required?
        task_config = None
        for it in config['state']['contesttask']:
            if it['name'] == self.task_name:
                task_config = it
        if task_config is None:
            log.error('no such task: %s', self.task_name)
            return []

        # get
        get_contest_task_url = 'https://csacademy.com/contest/get_contest_task/'
        payload = { 'contestTaskId': ( None, str(task_config['id']))  }
        headers = {
                'x-csrftoken': csrftoken,
                'x-requested-with': 'XMLHttpRequest',
                'Referer': url,
            }
        log.status('POST: %s', get_contest_task_url)
        resp = session.post(get_contest_task_url, files=payload, headers=headers)
        log.status(utils.describe_status_code(resp.status_code))
        resp.raise_for_status()
        # parse
        assert resp.encoding is None
        contest_task = json.loads( resp.content.decode() ) # NOTE: Should I memoize this?
        if contest_task.get('title') == 'Page not found':
            log.error('something wrong')
            return []
        samples = []
        for test_number, example_test in enumerate(contest_task['state']['EvalTask'][0]['exampleTests']):
            inname  = 'Input {}'.format(test_number)
            outname = 'Output {}'.format(test_number)
            samples += [[ ( example_test['input'], inname ), ( example_test['output'], outname ) ]]
        return samples


    def get_url(self):
        return 'https://csacademy.com/content/{}/task/{}/'.format(self.contest_name, self.task_name)

    def get_service(self):
        return CSAcademyService()

    @classmethod
    def from_url(cls, s):
        # example: https://csacademy.com/contest/round-38/task/path-union/
        # example: https://csacademy.com/contest/round-38/task/path-union/discussion/
        # example: https://csacademy.com/contest/archive/task/swap_permutation/
        # example: https://csacademy.com/contest/archive/task/swap_permutation/statement/
        result = urllib.parse.urlparse(s)
        if result.scheme in ('', 'http', 'https') \
                and result.netloc in ('csacademy.com', 'www.csacademy.com'):
            m = re.match(r'^/contest/([0-9A-Za-z_-]+)/task/([0-9A-Za-z_-]+)(|/statement|/solution|/discussion|/statistics|/submissions)/?$', utils.normpath(result.path))
            if m:
                return cls(m.group(1), m.group(2))

onlinejudge.dispatch.services += [ CSAcademyService ]
onlinejudge.dispatch.problems += [ CSAcademyProblem ]
