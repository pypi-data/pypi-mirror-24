''' Utility functions that gather statistical information on a Workflow
'''


def count_logs(workflow):
    ''' Number of logs for Workflow '''
    return workflow.workflowlog_set.count()


def response_time(workflow_log):
    ''' Log execution time as a timedelta object '''
    diff = workflow_log.date_finished - workflow_log.date_started
    return diff.total_seconds()


def _executed_logs(workflow, quantity=None):
    ''' Filter logs with start and end time '''
    if quantity:
        return workflow.workflowlog_set.exclude(date_finished__isnull=True, date_started__isnull=True)[:quantity]
    return workflow.workflowlog_set.exclude(date_finished__isnull=True, date_started__isnull=True)


def average_response_time(workflow):
    ''' Calculates the average response time for a given workflow '''
    times = [response_time(log) for log in _executed_logs(workflow, quantity=100)]
    if times:
        return sum(times) / float(len(times))
    return 0


def response_time_series(workflow, n=10):
    ''' Response times of last n logs in seconds, as a list '''
    recent_logs = list(_executed_logs(workflow).order_by('date_finished'))[-n:]
    return [response_time(log) for log in recent_logs]


def impact(workflow):
    ''' Total of seconds the Workflow has run '''
    logs = _executed_logs(workflow)
    seconds = sum([response_time(log) for log in logs])
    return seconds
