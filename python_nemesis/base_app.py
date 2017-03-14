import os
from flask import Flask
from oslo_config import cfg
from python_nemesis.config import collect_sqlalchemy_opts
from python_nemesis.config import register_opts
from python_nemesis.extensions import db
from python_nemesis.extensions import log


def configure_blueprints(app, blueprints):
    """
    Register configured blueprints into app object.

    :param app: The application object to which configuration should
                be applied.
    :type app: :py:class:`flask.Flask`
    :param blueprints: list of blueprints to be registered.
    :type blueprints: list(:py:class:`flask.Blueprint`)
    """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_app(app):
    """
    Retrieve App Configuration.

    configure_app first loads default configuration and then attempts
    to override defaults using a file specified in env:EXEQUOR_CONFIG.

    :param app: The application object to which configuration should
                be applied.
    :type app: :py:class:`flask.Flask`
    """
    app.config.from_object('python_nemesis.default_config')
    app.config["cfg"] = cfg.CONF
    config_file = os.environ.get(
        "NEMESIS_CONFIG",
        "/etc/nemesis/nemesis.conf")

    register_opts(app.config["cfg"], config_file)
    collect_sqlalchemy_opts(app, app.config["cfg"])


def configure_extensions(app):
    """
    Initialize extensions for Flask.

    This function is intended for use with the app factory style
    of Flask deployment.

    :param app: The application object to which configuration should
                be applied.
    :type app: :py:class:`flask.Flask`
    """
    db.init_app(app)
    log.init_app(app)


def create_app(app_name=None, blueprints=None):
    """
    Create the flask app.

    This function is intended to be used with the app factory
    style of Flask deployment.

    :param str app_name: Name to be used internally within flask.
    :param blueprints: Blueprints to be registered.
    :type blueprints: list(:py:class:`flask.Blueprint`)
    :returns: The created app.
    :rtype: :py:class:`flask.Flask`
    """
    app = Flask(app_name)

    configure_app(app)
    configure_extensions(app)

    return app


if __name__ == "__main__":  # pragma: no cover
    app = create_app('nemesis-api')
    app.run(threaded=True)

