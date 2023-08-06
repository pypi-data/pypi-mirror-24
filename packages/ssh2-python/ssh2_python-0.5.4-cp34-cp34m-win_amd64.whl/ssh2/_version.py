
import json

version_json = '''
{"error": null, "date": "2017-08-28T23:20:57.153638", "version": "0.5.4", "full-revisionid": "6ee0997735ea2a8df48cd56afdd97ff9f3b05cce", "dirty": false}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

