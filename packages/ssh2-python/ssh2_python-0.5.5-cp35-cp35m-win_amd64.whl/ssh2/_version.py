
import json

version_json = '''
{"dirty": false, "error": null, "date": "2017-08-30T23:40:43.841888", "version": "0.5.5", "full-revisionid": "bf460141156ca112c7a4d9bd26bc590d0e988af7"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

