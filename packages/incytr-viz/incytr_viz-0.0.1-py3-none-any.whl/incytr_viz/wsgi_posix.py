import sys
import time

import gunicorn.app.base
from gunicorn.arbiter import Arbiter

from incytr_viz.app import create_app
from incytr_viz.util import ascii, create_logger

logger = create_logger(__name__)


class CustomArbiter(Arbiter):

    def handle_hup(self):
        self.handle_term()


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    def run(self):
        bind = self.cfg.settings.get("bind").value

        # should always be pointing to a single port on localhost
        if isinstance(bind, list) and len(bind) == 1:
            location = "http://" + bind[0]
        else:
            location = bind

        logger.info(f"Running incytr-viz with gunicorn at {location}")

        try:
            CustomArbiter(self).run()
        except RuntimeError as e:
            print("\nError: %s\n" % e, file=sys.stderr)
            sys.stderr.flush()
            sys.exit(1)


def run_gunicorn(pathways, clusters):

    print(ascii())
    time.sleep(1)
    app = create_app(pathways_file=pathways, clusters_file=clusters)

    g_app = StandaloneApplication(app=app)

    try:
        g_app.cfg.settings["loglevel"].value = "warning"
    except:
        logger.warning("Could not set gunicorn loglevel")

    g_app.run()
