
import json

version_json = '''
{"full-revisionid": "6ee0997735ea2a8df48cd56afdd97ff9f3b05cce", "error": null, "dirty": false, "date": "2017-08-28T23:27:23.918321", "version": "0.5.4"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

