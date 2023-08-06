import os
import glob
import logging
import yaml
import json
import accounts
import agents
import plugins
import dashboards
import rules
import links
import orgs
import click
import errno
import urllib
from terminaltables import SingleTable
from termcolor import colored

logger = logging.getLogger(__name__)


def flatten(d, result=None):
    if result is None:
        result = {}
    for key in d:
        value = d[key]
        if isinstance(value, dict):
            value1 = {}
            for keyIn in value:
                value1[".".join([key, keyIn])] = value[keyIn]
            flatten(value1, result)
        elif isinstance(value, (list, tuple)):
            for indexB, element in enumerate(value):
                if isinstance(element, dict):
                    value1 = {}
                    index = 0
                    for keyIn in element:
                        newkey = ".".join([key, keyIn])
                        value1[".".join([key, keyIn])] = value[indexB][keyIn]
                        index += 1
                    for keyA in value1:
                        flatten(value1, result)
        else:
            result[key] = value
    return result


def print_command_output(command_data):
    for row in command_data:
        if row[1] == 0:
            print colored(str(row[0]), 'green')
        else:
            print colored(str(row[0]), 'red')
        print row[2]


def print_run_table(table_data):
    table = SingleTable(table_data)
    table.justify_columns = {0: 'left', 1: 'center', 2: 'left'}
    table.inner_heading_row_border = False
    table.inner_column_border = False
    table.outer_border = False
    max_width = table.column_max_width(2)
    for index, row in enumerate(table_data):
        table.table_data[index][2] = str(row[2][0:max_width].splitlines()[0])
        if row[1] == 0:
            table.table_data[index][1] = colored(str(row[1]), 'green')
        elif row[1] == 1:
            table.table_data[index][2] = colored(str(row[1]), 'yellow')
        elif row[1] == 3:
            table.table_data[index][2] = colored(str(row[1]), 'grey')
        else:
            table.table_data[index][2] = colored(str(row[1]), 'red')
    print table.table


def save_setting(setting='', value='', settings_file=''):
    try:
        stream = open(settings_file, 'r')
        data = yaml.load(stream)
    except IOError:
        data = {}
    data[setting] = value
    with open(settings_file, 'w') as yaml_file:
        yaml_file.write(yaml.safe_dump(data, default_flow_style=False, explicit_start=True))


def build_api_url(url,
                  org,
                  account,
                  endpoint='',
                  org_level=False,
                  account_level=False):
    if org_level:
        return url + '/orgs'
    elif account_level:
        return url + '/orgs/' + org + '/accounts'
    else:
        return url + '/orgs/' + org + '/accounts/' + account + '/' + endpoint


def create_dir(path, directory):
    new_directory = os.path.join(path, directory)
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
    return new_directory


# noinspection PyUnusedLocal
def backup_account(url='', org='', key='', account='', backup_dir='', **kwargs):
    #  create directory structure
    backup_dir = create_dir(os.getcwd(), backup_dir)
    org_dir = create_dir(backup_dir, org)
    account_dir = create_dir(org_dir, account)

    # backup agents
    agent_dir = create_dir(account_dir, 'agents')
    for agent in agents.get_agents(url=url, org=org, account=account, key=key):
        logging.debug('Exporting JSON for agent "%s"', agent['name'])
        # some agents can have a name 'http://...' encode name before writing a dir
        agent_path = os.path.join(agent_dir, str(urllib.quote(agent['name'], safe='')) + '.json')
        remove_keys = ['presence_state', 'created', 'modified', 'heartbeat']
        for k in remove_keys:
            if k in agent:
                del agent[k]
        with open(agent_path, 'w') as f:
            f.write(json.dumps(agent, indent=4))

    # backup dashboards
    dashboard_dir = create_dir(account_dir, 'dashboards')
    for dash in dashboards.get_dashboards(url=url, org=org, account=account, key=key):
        logging.debug('Exporting YAML for dashboard "%s"', dash['name'])
        dashboard_path = os.path.join(dashboard_dir, str(dash['name']) + '.yaml')
        with open(dashboard_path, 'w') as f:
            f.write(yaml.safe_dump(dash, default_flow_style=False, explicit_start=True))

    # backup plugins
    plugin_dir = create_dir(account_dir, 'plugins')
    for plugin in plugins.get_plugins(url=url, org=org, account=account, key=key):
        logging.debug('Exporting plugin "%s"', plugin['name'])
        plugin_path = os.path.join(plugin_dir, str(plugin['name']) + '.' + str(plugin['extension']))
        with open(plugin_path, 'w') as f:
            f.write(plugins.export_plugin(plugin=plugin['name'], url=url, org=org, account=account, key=key))


    # backup rules
    rule_dir = create_dir(account_dir, 'rules')
    for rule in rules.get_rules(url=url, org=org, account=account, key=key):
        logging.debug('Exporting YAML for rule "%s" with id %s', rule['name'], rule['id'])
        rule_path = os.path.join(rule_dir, str(rule['name']) + '.yaml')
        with open(rule_path, 'w') as f:
            rule_yaml = rules.export_rule(rule=rule['id'], url=url, org=org, account=account, key=key)
            try:
                rule_content = yaml.safe_load(rule_yaml)
                if rule_content['actions']:
                    action_count = len(rule_content['actions'])
                    for i in range(action_count):
                        try:
                            del rule_content['actions'][i]['details']['status']
                        except KeyError:
                            continue
                f.write(yaml.safe_dump(rule_content, default_flow_style=False, explicit_start=True))
            except yaml.YAMLError as e:
                logging.warn('Unable to parse YAML for rule %s: %s', rule['name'], e.problem)
                f.write(rule_yaml)

    # backup links
    link_dir = create_dir(account_dir, 'links')
    for link in links.get_links(url=url, org=org, account=account, key=key):
        logging.debug('Exporting JSON for pack "%s" with id %s', link['plugin'], link['id'])
        link_path = os.path.join(link_dir, link['id'] + '.json')
        link_json = links.export_link(link_id=link['id'], url=url, org=org, account=account, key=key)
        with open(link_path, 'w') as f:
            f.write(json.dumps(link_json, indent=4))


# noinspection PyUnusedLocal
def backup_org(url='', org='', key='', backup_dir='', **kwargs):
    click.echo(click.style('Backing up accounts in %s...' % org, 'white', bold=True))
    for a in accounts.get_accounts(url=url, org=org, key=key):
        click.echo(click.style(' * Backing up account: ', 'white', bold=True) + click.style(a['name'], 'green'))
        backup_account(url=url, key=key, org=org, account=a['name'], backup_dir=backup_dir)


def read_file_content(file_path):
    try:
        with open(file_path) as f:
            return f.read()
    except IOError as exc:
        if exc.errno != os.errno.EISDIR:
            raise


# noinspection PyUnusedLocal
def restore_account(url='', key='', org='', account='', backup_dir='', **kwargs):

    agents_dir = os.path.join(backup_dir, org, account, 'agents')
    dashboards_dir = os.path.join(backup_dir, org, account, 'dashboards')
    plugins_dir = os.path.join(backup_dir, org, account, 'plugins')
    rules_dir = os.path.join(backup_dir, org, account, 'rules')
    links_dir = os.path.join(backup_dir, org, account, 'links')

    # restore agents

    agent_files = glob.glob(agents_dir + '/*.json')
    for agent_path in agent_files:
        agent_json = json.loads(read_file_content(agent_path))
        payload = {
            "fingerprint": agent_json['id'],
            "name": agent_json['name'],
            "hostname": agent_json['hostname'],
            "tag_names": ",".join(agent_json['tags']),
            "mac": agent_json['mac'],
            "os_name": agent_json['osName'],
            "container_name": agent_json['container_name'],
            "mode": agent_json['mode'],
            "status": agent_json['status']
        }
        agents.register_agent(url=url, org=org, account=account, key=key, payload=payload, finger=agent_json['id'])


    # restore dashboards
    try:
        dashboard_files = glob.glob(dashboards_dir + '/*.yaml')
        for dashboard_path in dashboard_files:
            dashboards.import_dashboard(file_path=dashboard_path, url=url, key=key,
                                        org=org, account=account, backup_dir=backup_dir)

    except Exception, e:
        print e

    # restore plugins
    plugin_files = glob.glob(plugins_dir + '/*')
    for plugin_path in plugin_files:
        plugins.import_plugin(plugin_path=plugin_path, url=url, key=key,
                              org=org, account=account, backup_dir=backup_dir)

    # restore rules
    rule_files = glob.glob(rules_dir + '/*.yaml')
    for rule_path in rule_files:
        rules.import_rule(rule_path=rule_path, url=url, key=key,
                          org=org, account=account, backup_dir=backup_dir)

    # restore links
    link_files = glob.glob(links_dir + '/*.json')
    for link_path in link_files:
        links.import_link(link_path=link_path, url=url, key=key,
                          org=org, account=account, backup_dir=backup_dir)


# noinspection PyUnusedLocal
def restore_org(url='', key='', org='', backup_dir='', **kwargs):
    for a in accounts.get_accounts():
        restore_account(url, key, org, a['name'], backup_dir)


def agent_status_check(agent, status):
    if status == 'all':
        if agent['presence_state'] == 'online':
            click.echo(click.style(agent['name'], fg='green'))
        else:
            click.echo(click.style(agent['name'], fg='red'))
    if status == 'up':
        if agent['presence_state'] == 'online':
            click.echo(click.style(agent['name'], fg='green'))
    if status == 'down':
        if agent['presence_state'] != 'online':
            click.echo(click.style(agent['name'], fg='red'))


# noinspection PyUnusedLocal
def search_agent(url='', key='', org='', account='', agent='', **kwargs):
    org_list = orgs.get_orgs(url=url, org=org, account=account, key=key)
    for o in org_list:
        account_list = accounts.get_accounts(url=url, org=o['name'], key=key)
        for acc in account_list:
            agent_list = agents.get_agents(url=url, org=org, account=acc['name'], key=key)
            for ag in agent_list:
                if ag['name'] == agent:
                    click.echo('Organization: %s Account: %s Agent: %s' % (o['name'], acc['name'], ag['name']))


# noinspection PyUnusedLocal
def search_fingerprint(url='', key='', org='', account='', fingerprint='', **kwargs):
    org_list = orgs.get_orgs(url=url, org=org, account=account, key=key)
    for o in org_list:
        account_list = accounts.get_accounts(url=url, org=o['name'], key=key)
        for acc in account_list:
            agent_list = agents.get_agents(url=url, org=org, account=acc['name'], key=key)
            for ag in agent_list:
                if ag['id'] == fingerprint:
                    click.echo('Organization: %s Account: %s Agent: %s' % (o['name'], acc['name'], ag['name']))


# noinspection PyUnusedLocal
def search_metadata(url='', key='', org='', account='', metadata='', **kwargs):
    agent_names = []
    org_list = orgs.get_orgs(url=url, org=org, account=account, key=key)
    for o in org_list:
        account_list = accounts.get_accounts(url=url, org=o['name'], key=key)
        for acc in account_list:
            agent_list = agents.get_agents(url=url, org=org, account=acc['name'], key=key)
            for summary in agent_list:
                agent_names.append(summary['name'])
            for agent in agent_names:
                try:
                    search_hash = flatten(agents.get_agent(url=url, org=org, account=acc['name'],
                                                           key=key, agent_name=agent))
                    if metadata in search_hash.keys() or metadata in search_hash.values():
                        click.echo('Organization: %s Account: %s Agent: %s' % (o['name'], acc['name'], agent))
                except:
                    continue


def make_node(node):
    try:
        os.makedirs(node)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise


def create_node(f, times=None):
    with open(f, 'a'):
        os.utime(f, times)


def create_tree(h, c):
    for path, files in c.iteritems():
        parent = os.path.join(h, path)
        make_node(parent)
        children = c[path]
        for child in children:
            child = os.path.join(parent, child)
            create_node(child)
