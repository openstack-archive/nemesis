'''
Extend Flask Config to use `oslo.config`.

This module allows oslo.config itesm to be utilized in flask. It will
register all sqlalchemy options directly into flask for use with the
flask-sqlalchemy extension.
'''
from oslo_config import cfg


DEFAULT_OPT_GRP = cfg.OptGroup(name='DEFAULT')
DEFAULT_OPTS = [
    cfg.StrOpt('test_value', default="this is a value")
]

SQLALCHEMY_OPT_GRP = cfg.OptGroup(name='sqlalchemy')
SQLALCHEMY_OPTS = [
    cfg.StrOpt('database_uri'),
    cfg.BoolOpt('echo'),
    cfg.IntOpt('pool_size'),
    cfg.IntOpt('pool_timeout'),
    cfg.IntOpt('pool_recycle'),
    cfg.IntOpt('max_overflow'),
    cfg.BoolOpt('track_modifications'),
]

IDENTITY_OPT_GRP = cfg.OptGroup(name='identity')
IDENTITY_OPTS = [
    cfg.StrOpt('username'),
    cfg.StrOpt('password')
]


def register_opts(conf, config_file):
    '''
    Register Oslo Configuration Options from a provided config file.

    :param conf: oslo config to be populated.
    :type conf: :py:obj:`cfg.CONF`
    :param str config_file: Location of the config file to be used.
    '''
    conf(default_config_files=[config_file])
    conf.register_opts(DEFAULT_OPTS)
    conf.register_group(SQLALCHEMY_OPT_GRP)
    conf.register_opts(SQLALCHEMY_OPTS, SQLALCHEMY_OPT_GRP)
    conf.register_group(IDENTITY_OPT_GRP)
    conf.register_opts(IDENTITY_OPTS, IDENTITY_OPT_GRP)


def collect_sqlalchemy_opts(app, conf):
    """
    Collect sqlalchemy options from `oslo.config` and apply them.

    This function copies the configuration entries for sqlalchemy
    directly into the :py:class:`flask.Flask` object where the
    upstream Flask-SqlAlchemy extension expects to find them.

    :param app: The application object to which configuration should
                be applied.
    :type app: :py:class:`flask.Flask`
    :param conf: oslo config to be populated.
    :type conf: :py:obj:`cfg.CONF`
    """
    def _import_opt_from_oslo(flask_opt, oslo_opt):
        if conf.sqlalchemy[oslo_opt] is not None:
            app.config[flask_opt] = conf.sqlalchemy[oslo_opt]

    _import_opt_from_oslo('SQLALCHEMY_DATABASE_URI', 'database_uri')
    _import_opt_from_oslo('SQLALCHEMY_ECHO', 'echo')
    _import_opt_from_oslo('SQLALCHEMY_POOL_SIZE', 'pool_size')
    _import_opt_from_oslo('SQLALCHEMY_POOL_TIMEOUT', 'pool_timeout')
    _import_opt_from_oslo('SQLALCHEMY_POOL_RECYCLE', 'pool_recycle')
    _import_opt_from_oslo('SQLALCHEMY_MAX_OVERFLOW', 'max_overflow')
    _import_opt_from_oslo(
        'SQLALCHEMY_TRACK_MODIFICATIONS',
        'track_modifications'
    )
