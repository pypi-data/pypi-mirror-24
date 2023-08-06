import sys
import context
from ..api import *
from .. import __version__

import logging

logger = logging.getLogger(__name__)

try:
    from logging import NullHandler
except ImportError:
    from logging import Handler


    class NullHandler(Handler):
        def emit(self, record):
            pass


@click.group()
@click.option('--debug',
              is_flag=True,
              help='Debug mode',
              default=False)
@click.option('--loglevel',
              help='Log level',
              type=str,
              default='info')
@click.option('--settingsfile',
              help='Settings File',
              type=str,
              default=context.settings['settingsfile'])
@click.option('--backupdir',
              help='Backups Directory',
              type=str,
              required=False)
@click.option('--url', help='API URL', type=str)
@click.option('--org',
              help='Organization Name',
              type=str,
              required=False)
@click.option('--account',
              help='Account Name',
              type=str,
              required=False)
@click.option('--key',
              help='API Key',
              type=str,
              required=False)
@click.option('--timeout',
              help='Global request timeout',
              type=int,
              default=60,
              required=False)
@click.version_option(version=__version__)
def cli(settingsfile, url, org, account, key, backupdir, loglevel, debug, timeout):
    if debug:
        numeric_log_level = logging.DEBUG or loglevel.upper() == 'DEBUG'
        format_string = '%(asctime)s %(levelname)-9s %(name)22s %(funcName)22s:%(lineno)-4d %(message)s'
    else:
        numeric_log_level = getattr(logging, loglevel.upper(), None)
        format_string = '%(asctime)s %(levelname)-9s %(message)s'
        if not isinstance(numeric_log_level, int):
            raise ValueError('Invalid log level: {0}'.format(loglevel))

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(format_string))
    logging.root.addHandler(handler)
    logging.root.setLevel(numeric_log_level)

    if not debug:
        logging.getLogger("requests").setLevel(logging.WARN)

    try:
        # load some settings from file over the top of the defaults
        stream = open(settingsfile, 'r')
        file_settings = yaml.load(stream)
        context.settings.update({k: v for k, v in file_settings.iteritems() if v})
    except IOError:
        pass

    # command line options override defaults and settings file
    args = {
        'settingsfile': settingsfile,
        'url': url,
        'org': org,
        'account': account,
        'key': key,
        'backupdir': backupdir,
        'timeout': timeout
    }
    for arg, value in args.iteritems():
        if value:
            context.settings[arg] = value

    if (context.settings['key']) and (195 < len(context.settings['key']) < 204):
        print "Not a valid key! Please generate an API token at https://app.dataloop.io/#/user-account/api-tokens"
        sys.exit(2)


@click.command(short_help="status")
def status():
    url = context.settings['url']
    org = context.settings['org']
    account = context.settings['account']
    key = context.settings['key']
    timeout = context.settings['timeout']

    click.echo('URL: %s' % url)
    click.echo('Organization: %s' % org)
    click.echo('Account: %s' % account)
    click.echo('URI: %s/orgs/%s/accounts ' % (url, org))
    click.echo('Key: %s' % key)

    resp = requests.get(url + '/orgs/' + org + '/accounts/' + account,
                        headers={'Authorization': "Bearer " + key},
                        timeout=timeout).status_code
    if resp == 200:
        click.echo('Authenticated: %s' % click.style('True', fg='green'))
    else:
        click.echo(
            'Authenticated: %s, Status Code: %s' % (click.style('False', fg='red'), click.style(str(resp), fg='red')))


cli.add_command(status)
