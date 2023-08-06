import click
import os
import sys
import subprocess

from . import command, docker, package_utils
from .configreader import Config
from clint.textui import colored, puts, columns


class StakkrActions():
    """Main class that does actions asked in the cli"""

    _services_to_display = {
        'apache': {'name': 'Web Server', 'url': 'http://{}'},
        'mailcatcher': {'name': 'Mailcatcher (fake SMTP)', 'url': 'http://{}', 'extra_port': 25},
        'maildev': {'name': 'Maildev (Fake SMTP)', 'url': 'http://{}', 'extra_port': 25},
        'portainer': {'name': 'Portainer (Docker GUI)', 'url': 'http://{}'},
        'phpmyadmin': {'name': 'PhpMyAdmin', 'url': 'http://{}'},
        'xhgui': {'name': 'XHGui (PHP Profiling)', 'url': 'http://{}'}
    }


    def __init__(self, base_dir: str, ctx: dict):
        # Work with directories and move to the right place
        self.stakkr_base_dir = base_dir
        self.context = ctx
        self.current_dir = os.getcwd()
        self.current_dir_relative = self._get_relative_dir()
        os.chdir(self.stakkr_base_dir)

        # Set some general variables
        self.dns_container_name = 'docker_dns'
        self.config_file = ctx['CONFIG']
        self.compose_base_cmd = self._get_compose_base_cmd()

        # Get info from config
        self.config = self._get_config()
        self.main_config = self.config['main']
        self.project_name = self.main_config.get('project_name')


    def console(self, ct: str, user: str, tty: bool):
        """Enter a container (stakkr allows only apache / php and mysql)"""

        docker.check_cts_are_running(self.project_name, self.config_file)

        tty = 't' if tty is True else ''
        cmd = ['docker', 'exec', '-u', user, '-i' + tty, docker.get_ct_name(ct), docker.guess_shell(ct)]
        subprocess.call(cmd)

        self._verbose('Command : "' + ' '.join(cmd) + '"')


    def get_services_ports(self):
        """Once started, stakkr displays a message with the list of launched containers."""

        dns_started = docker.container_running('docker_dns')

        running_cts, cts = docker.get_running_containers(self.project_name)

        text = ''
        for ct, ct_info in cts.items():
            if ct_info['compose_name'] not in self._services_to_display:
                continue
            options = self._services_to_display[ct_info['compose_name']]
            url = self._get_url(options['url'], ct_info['compose_name'], dns_started)
            text += '  - For {}'.format(colored.yellow(options['name'])).ljust(55, ' ') + ' : ' + url + '\n'

            if 'extra_port' in options:
                text += ' '*3 + ' ... in your containers use the port {}\n'.format(options['extra_port'])

        return text


    def exec(self, container: str, user: str, args: tuple, tty: bool):
        """Run a command from outside to any container. Wrapped into /bin/sh"""

        docker.check_cts_are_running(self.project_name, self.config_file)

        # Protect args to avoid strange behavior in exec
        args = ['"{}"'.format(arg) for arg in args]

        tty = 't' if tty is True else ''
        cmd = ['docker', 'exec', '-u', user, '-i' + tty, docker.get_ct_name(container), 'sh', '-c']
        cmd += ["""test -d "/var/{0}" && cd "/var/{0}" ; exec {1}""".format(self.current_dir_relative, ' '.join(args))]
        self._verbose('Command : "' + ' '.join(cmd) + '"')
        subprocess.call(cmd, stdin=sys.stdin)


    def manage_dns(self, action: str):
        """Starts or stop the DNS forwarder"""

        dns_started = docker.container_running(self.dns_container_name)
        if dns_started is True and action == 'stop':
            dns = docker.client.containers.get('docker_dns')
            return dns.stop()

        elif action == 'start':
            self._docker_run_dns()
            return

        click.echo(click.style('[ERROR]', fg='red') + " DNS already stopped")
        sys.exit(1)


    def start(self, pull: bool, recreate: bool):
        """If not started, start the containers defined in config"""

        verb = self.context['VERBOSE']
        debug = self.context['DEBUG']

        try:
            docker.check_cts_are_running(self.project_name, self.config_file)
            puts(colored.yellow('[INFO]') + ' stakkr is already started ...')
            sys.exit(0)
        except Exception:
            pass

        if pull is True:
            command.launch_cmd_displays_output(self.compose_base_cmd + ['pull'], verb, debug, True)

        recreate_param = '--force-recreate' if recreate is True else '--no-recreate'
        cmd = self.compose_base_cmd + ['up', '-d', recreate_param, '--remove-orphans']
        self._verbose('Command: ' + ' '.join(cmd))
        command.launch_cmd_displays_output(cmd, verb, debug, True)

        self.running_cts, self.cts = docker.get_running_containers(self.project_name)
        if self.running_cts is 0:
            raise SystemError("Couldn't start the containers, run the start with '-v' and '-d'")

        self._patch_oses_start()
        self._run_iptables_rules()
        self._run_services_post_scripts()


    def status(self):
        """Returns a nice table with the list of started containers"""

        try:
            self.running_cts, self.cts = docker.check_cts_are_running(self.project_name, self.config_file)
        except Exception:
            puts(colored.yellow('[INFO]') + ' stakkr is currently stopped')
            sys.exit(0)

        dns_started = docker.container_running('docker_dns')

        self._print_status_headers(dns_started)
        self._print_status_body(dns_started)


    def stop(self):
        """If started, stop the containers defined in config. Else throw an error"""

        verb = self.context['VERBOSE']
        debug = self.context['DEBUG']

        docker.check_cts_are_running(self.project_name, self.config_file)
        command.launch_cmd_displays_output(self.compose_base_cmd + ['stop'], verb, debug, True)
        self._patch_oses_stop()

        self.running_cts, self.cts = docker.get_running_containers(self.project_name)
        if self.running_cts is not 0:
            raise SystemError("Couldn't stop services ...")


    def _call_service_post_script(self, service: str):
        service_script = package_utils.get_file('static', 'services/{}.sh'.format(service))
        if os.path.isfile(service_script) is True:
            cmd = ['bash', service_script, docker.get_ct_item(service, 'name')]
            subprocess.call(cmd)
            self._verbose('Service Script : ' + ' '.join(cmd))


    def _docker_run_dns(self):
        network = self.project_name + '_stakkr'

        # Started ? Only attach it to the current network
        if docker.container_running(self.dns_container_name) is True:
            docker.add_container_to_network(self.dns_container_name, network)
            self._verbose('{} attached to network {}'.format(self.dns_container_name, network))
            return

        # Not started ? Create it and add it to the network
        try:
            volumes = ['/var/run/docker.sock:/tmp/docker.sock', '/etc/resolv.conf:/tmp/resolv.conf']
            docker.client.containers.run(
                'mgood/resolvable', remove=True, detach=True, network=network,
                hostname='docker-dns', name=self.dns_container_name, volumes=volumes)
        except Exception as e:
            click.echo(click.style('[ERROR]', fg='red') + " Can't start the DNS ...")
            click.echo('       -> {}'.format(e))
            sys.exit(1)


    def _get_compose_base_cmd(self):
        if self.context['CONFIG'] is None:
            return ['stakkr-compose']

        return ['stakkr-compose', '-c', self.context['CONFIG']]


    def _get_config(self):
        config = Config(self.config_file)
        main_config = config.read()
        if main_config is False:
            config.display_errors()
            sys.exit(1)

        return main_config


    def _get_relative_dir(self):
        if self.current_dir.startswith(self.stakkr_base_dir):
            return self.current_dir[len(self.stakkr_base_dir):].lstrip('/')

        return ''


    def _get_url(self, service_url: str, service: str, dns_started: bool):
        name = docker.get_ct_name(service) if dns_started else docker.get_ct_item(service, 'ip')

        return service_url.format(name)


    def _patch_oses_start(self):
        """For Windows we need to do a few manipulations to be able to access
        our dev environment from the host ...

        Found here: https://github.com/docker/for-win/issues/221#issuecomment-270576243"""

        if os.name not in ['nt']:
            return

        docker.client.containers.run(
            'justincormack/nsenter1', remove=True, tty=True, privileged=True, network_mode='none',
            pid_mode='host', command='bin/sh -c "iptables -A FORWARD -j ACCEPT"')

        subnet = docker.get_subnet(self.project_name)
        switch_ip = docker.get_switch_ip()
        msg = 'We need to create a route for the network {} via {} to work...'
        click.secho(msg.format(subnet, switch_ip), fg='yellow', nl=False)
        subprocess.call(['route', 'add', subnet, 'MASK', '255.255.255.0', switch_ip])
        print()


    def _patch_oses_stop(self):
        """Opposite actions than _patch_oses_start()"""

        if os.name not in ['nt']:
            return

        subnet = docker.get_subnet(self.project_name)
        click.secho("Let's remove the route that has been added for {}...".format(subnet), fg='yellow', nl=False)
        subprocess.call(['route', 'delete', subnet])
        print()


    def _print_status_headers(self, dns_started: bool):
        host_ip = (colored.green('HostName' if dns_started else 'IP'))

        puts(columns(
            [(colored.green('Container')), 16], [host_ip, 25], [(colored.green('Ports')), 25],
            [(colored.green('Image')), 32],
            [(colored.green('Docker ID')), 15], [(colored.green('Docker Name')), 25]
            ))

        puts(columns(
            ['-'*16, 16], ['-'*25, 25], ['-'*25, 25],
            ['-'*32, 32],
            ['-'*15, 15], ['-'*25, 25]
            ))


    def _print_status_body(self, dns_started: bool):
        for ct in sorted(self.cts.keys()):
            ct_data = self.cts[ct]
            if ct_data['ip'] == '':
                continue

            host_ip = ct_data['name'] if dns_started else ct_data['ip']

            puts(columns(
                [ct_data['compose_name'], 16], [host_ip, 25], [', '.join(ct_data['ports']), 25],
                [ct_data['image'], 32],
                [ct_data['id'][:12], 15], [ct_data['name'], 25]
                ))


    def _run_iptables_rules(self):
        """For some containers we need to add iptables rules added from the config"""

        block_config = self.config['network-block']
        for service, ports in block_config.items():
            error, msg = docker.block_ct_ports(service, ports, self.project_name)
            if error is True:
                click.secho(msg, fg='red')
                continue

            self._verbose(msg)


    def _run_services_post_scripts(self):
        """A service can have a .sh file that will be executed once it's started.
        Useful to override some actions of the classical /run.sh

        """

        if os.name == 'nt':
            click.secho('Could not run service post scripts under Windows', fg='red')
            return

        for service in self.main_config.get('services'):
            self._call_service_post_script(service)


    def _verbose(self, message: str):
        if self.context['VERBOSE'] is True:
            print(colored.green('[VERBOSE]') + ' {}'.format(message), file=sys.stderr)
