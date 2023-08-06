
import json

version_json = '''
{"date": "2017-08-30T23:46:52.813441", "dirty": false, "error": null, "full-revisionid": "bf460141156ca112c7a4d9bd26bc590d0e988af7", "version": "0.5.5"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

