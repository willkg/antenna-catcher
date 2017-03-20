# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import logging
import logging.config

import falcon


logger = logging.getLogger(__name__)


def setup_logging():
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'simple': {
                'format': '[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'loggers': {
            'catcher': {
                'handlers': ['console'],
                'level': 'DEBUG'
            }
        }
    })


PREFIX = 'CrashID=bp-'


class CrashIDResource:
    """Captures crash ids, stores them in memory and returns them when requested

    """
    def __init__(self):
        self.crashid_log = []

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = '\n'.join(self.crashid_log)

    def on_post(self, req, resp):
        crashid = req.params['crashid']
        if crashid.startswith(PREFIX):
            crashid = crashid[len(PREFIX):]

        crashid = crashid.strip()

        if len(crashid) == 36:
            # Append the timestamp and crashid to log
            self.crashid_log.append(
                '%s: %s' % (datetime.datetime.now(), crashid)
            )

            # Truncate log if we need to
            if len(self.crashid_log) > 2000000:
                self.crashid_log = self.crashid_log[500000:]

            resp.status = falcon.HTTP_200
            resp.body = 'Ok'

        else:
            logger.info('Bad crashid: %s' % crashid)
            resp.status = falcon.HTTP_400
            resp.body = 'Bad crashid: %s' % crashid


def get_app():
    setup_logging()

    app = falcon.API()
    app.add_route('/crashid', CrashIDResource())
    return app


app = get_app()
