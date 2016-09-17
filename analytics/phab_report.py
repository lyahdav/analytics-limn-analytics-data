#!/usr/bin/env python

import json
import subprocess
import argparse

def conduit_projPHID(project):
    result = execute_apicall(
        'project.query',
        {
            'names' : [project]
        }
    )

    projPHID = result['response']['data'].keys()[0]

    return projPHID

def conduit_tasktransactions(taskids):
    result = execute_apicall(
        'maniphest.gettasktransactions',
        {
            'ids': taskids
        }
    )

    tasktransactions = result['response']

    return tasktransactions

def conduit_phidlookup(phids):
    result = execute_apicall(
        'phid.lookup',
        {
            'names': phids
        }
    )

    phidlookup = { x: result['response'][x]['fullName'] for x in result['response'].keys() }

    return phidlookup

def find_first(iterable, f):
    for x in iterable:
        if f(x):
            yield x
            raise StopIteration
    raise StopIteration

def conduit_tasks(projPHID):
    result = execute_apicall(
        'maniphest.query',
        {
            'projectPHIDs': [projPHID],
            'order': 'order-priority'
        }
    )

    taskPHIDs = result['response'].keys()

    all_tasktransactions = conduit_tasktransactions(
        [int(x['id']) for x in result['response'].values()]
    )

    all_values = all_tasktransactions.values()

    all_columnPHIDs = set()
    for tasktransactions in all_values:
        first_column_move_transaction = find_first(
            tasktransactions,
            lambda x: x['transactionType'] == 'projectcolumn' and \
            x['newValue']['projectPHID'] == projPHID
        )
        latest_column_id = [x['newValue']['columnPHIDs'][0] for x in first_column_move_transaction]
        if len(latest_column_id) > 0:
            all_columnPHIDs.add(latest_column_id[0])

    columnPHID_lookup = conduit_phidlookup(list(all_columnPHIDs))

    tasks = []

    for taskPHID in result['response'].keys():

        this_tasktransactions = all_tasktransactions[result['response'][taskPHID]['id']]

        first_column_move_transaction = find_first(
            this_tasktransactions,
            lambda x: x['transactionType'] == 'projectcolumn' and \
            x['newValue']['projectPHID'] == projPHID
        )
        columnPHID = [
            x['newValue']['columnPHIDs'][0] for x in first_column_move_transaction
        ]
        if len(columnPHID) > 0:
            column_name = columnPHID_lookup[columnPHID[0]]
        else:
            column_name = 'Unknown'

        task = {
            'title': result['response'][taskPHID]['title'],
            'status': result['response'][taskPHID]['status'],
            'phid': taskPHID,
            'column': column_name
        }

        tasks.append(task)

    return tasks

def execute_apicall(apicall, query):
    p = subprocess.Popen(
        ['arc', 'call-conduit', apicall],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    p.stdin.write(json.dumps(query))
    stdout = p.communicate()[0]
    p.stdin.close()
    p.wait()

    if p.returncode != 0:
        raise Exception(stdout)
    return json.loads(stdout)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate report of Phabricator workboard column')
    parser.add_argument('--column',
        help='Name of workboard column to report on',
        required=True)
    parser.add_argument('--project',
        help='Name of project to report on',
        required=True)
    return parser.parse_args()

def main():
    args = parse_arguments()
    project_name = args.project
    column_name = args.column

    # get project PHID
    projPHID = conduit_projPHID(project_name)

    # get task PHIDs for project
    tasks = conduit_tasks(projPHID)

    # prune to tasks in certain column
    tasks = filter(lambda x: x['column'] == column_name, tasks)

    # group tasks by status
    by_status = {}
    for t in tasks:
        if t['status'] in by_status:
            by_status[t['status']].append(t)
        else:
            by_status[t['status']] = [t]

    # print report
    for status, tasks in by_status.items():
        print '%s:' % status
        for t in tasks:
            print '\t* %s' % t['title']
        print

if __name__ == '__main__':
    main()
