
import json

version_json = '''
{"date": "2017-08-28T23:16:09.222000", "full-revisionid": "6ee0997735ea2a8df48cd56afdd97ff9f3b05cce", "dirty": false, "version": "0.5.4", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

