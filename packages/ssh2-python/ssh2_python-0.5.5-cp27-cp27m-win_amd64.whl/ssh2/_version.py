
import json

version_json = '''
{"date": "2017-08-30T23:30:36.463000", "full-revisionid": "bf460141156ca112c7a4d9bd26bc590d0e988af7", "dirty": false, "version": "0.5.5", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

