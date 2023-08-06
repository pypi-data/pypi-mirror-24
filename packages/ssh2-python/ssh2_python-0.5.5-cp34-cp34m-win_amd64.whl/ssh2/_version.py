
import json

version_json = '''
{"error": null, "version": "0.5.5", "dirty": false, "date": "2017-08-30T23:34:57.049162", "full-revisionid": "bf460141156ca112c7a4d9bd26bc590d0e988af7"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

