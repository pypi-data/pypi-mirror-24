from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import argparse
import logging
import os
from functools import wraps

from flask import Flask
from flask import current_app
from flask import jsonify
from flask import request
from gevent.wsgi import WSGIServer

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.data_router import DataRouter, InvalidModelError
from rasa_nlu.version import __version__

logger = logging.getLogger(__name__)


def create_argparser():
    parser = argparse.ArgumentParser(description='parse incoming text')
    parser.add_argument('-c', '--config',
                        help="config file, all the command line options can also be passed via a (json-formatted) " +
                             "config file. NB command line args take precedence")
    parser.add_argument('-d', '--server_model_dirs',
                        help='directory containing model to for parser to use')
    parser.add_argument('-e', '--emulate', choices=['wit', 'luis', 'api'],
                        help='which service to emulate (default: None i.e. use simple built in format)')
    parser.add_argument('-l', '--language', choices=['de', 'en'], help="model and data language")
    parser.add_argument('-m', '--mitie_file',
                        help='file with mitie total_word_feature_extractor')
    parser.add_argument('-p', '--path', help="path where model files will be saved")
    parser.add_argument('--pipeline', help="The pipeline to use. Either a pipeline template name or a list of " +
                                           "components separated by comma")
    parser.add_argument('-P', '--port', type=int, help='port on which to run server')
    parser.add_argument('-t', '--token',
                        help="auth token. If set, reject requests which don't provide this token as a query parameter")
    parser.add_argument('-w', '--write', help='file where logs will be saved')

    return parser


def requires_auth(f):
    """Wraps a request handler with token authentication."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token', '')
        if current_app.data_router.token is None or token == current_app.data_router.token:
            return f(*args, **kwargs)
        return "unauthorized", 401

    return decorated


def create_app(config, component_builder=None):
    rasa_nlu_app = Flask(__name__)

    @rasa_nlu_app.route("/parse", methods=['GET', 'POST'])
    @requires_auth
    def parse_get():
        if request.method == 'GET':
            request_params = request.args
        else:
            request_params = request.get_json(force=True)
        if 'q' not in request_params:
            return jsonify(error="Invalid parse parameter specified"), 404
        else:
            try:
                data = current_app.data_router.extract(request_params)
                response = current_app.data_router.parse(data)
                return jsonify(response)
            except InvalidModelError as e:
                return jsonify({"error": "{}".format(e)}), 404

    @rasa_nlu_app.route("/version", methods=['GET'])
    @requires_auth
    def version():
        return jsonify({'version': __version__})

    @rasa_nlu_app.route("/config", methods=['GET'])
    @requires_auth
    def rasaconfig():
        return jsonify(config.as_dict())

    @rasa_nlu_app.route("/status", methods=['GET'])
    @requires_auth
    def status():
        return jsonify(current_app.data_router.get_status())

    @rasa_nlu_app.route("/", methods=['GET'])
    def hello():
        return "hello from Rasa NLU: " + __version__

    @rasa_nlu_app.route("/train", methods=['POST'])
    @requires_auth
    def train():
        data_string = request.get_data(as_text=True)
        current_app.data_router.start_train_process(data_string, request.args)
        return jsonify(info="training started.", training_process_ids=current_app.data_router.train_proc_ids())

    logging.basicConfig(filename=config['log_file'], level=config['log_level'])
    logging.captureWarnings(True)
    logger.info("Configuration: " + config.view())

    logger.debug("Creating a new data router")
    rasa_nlu_app.data_router = DataRouter(config, component_builder)
    return rasa_nlu_app


if __name__ == '__main__':
    # Running as standalone python application
    arg_parser = create_argparser()
    cmdline_args = {key: val for key, val in list(vars(arg_parser.parse_args()).items()) if val is not None}
    rasa_nlu_config = RasaNLUConfig(cmdline_args.get("config"), os.environ, cmdline_args)
    app = WSGIServer(('0.0.0.0', rasa_nlu_config['port']), create_app(rasa_nlu_config))
    logger.info('Started http server on port %s' % rasa_nlu_config['port'])
    app.serve_forever()
