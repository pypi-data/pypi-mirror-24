import os
import paramiko
import textfsm
from djangolg import methods, settings


class LookingGlass(object):
    def __init__(self, router=None, port=22):
        self.router = router
        self.credentials = router.credentials
        try:
            self.dialect = methods.Dialect(router.dialect)
        except KeyError:
            self.dialect = None
        self.defaults = {
            'ssh_host_key_policy': paramiko.WarningPolicy(),
            'ssh_port': port,
        }

    def _connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(
            self.defaults['ssh_host_key_policy']
        )
        try:
            self.ssh.connect(
                hostname=self.router.hostname,
                port=self.defaults['ssh_port'],
                username=self.credentials.username,
                password=self.credentials.password,
            )
        except Exception:
            raise
        return self

    def _disconnect(self):
        if self.ssh:
            try:
                self.ssh.close()
            except Exception:
                raise
            del self.ssh
        else:
            raise ValueError
        return self

    def _exec(self, cmd=None):
        if self.ssh:
            try:
                stdin, stdout, stderr = self.ssh.exec_command(cmd)
                output = stdout.read()
            except Exception:
                raise
        else:
            raise ValueError
        return output

    def _build_cmd(self, method, target=None, option=None):
        if self.dialect:
            try:
                method.dialect = self.dialect
            except NotImplementedError:
                pass
        if method.options and isinstance(option, int):
            cmd = method.options[option]['cmd'](target)
        else:
            cmd = method.cmd(target)
        return cmd

    def _parse(self, raw, method, option=None):
        templates_dir = settings.TEXTFSM_TEMPLATES_DIR
        if self.dialect:
            templates_dir = os.path.join(templates_dir, str(self.dialect))
            try:
                method.dialect = self.dialect
            except NotImplementedError:
                pass
        try:
            if method.options and isinstance(option, int):
                template = method.options[option]['template']
            else:
                template = method.template
        except KeyError:
            return None
        try:
            f = os.path.join(templates_dir, template)
            t = open(f)
        except:
            raise
        parser = textfsm.TextFSM(t)
        parsed = {
            'header': parser.header,
            'data': parser.ParseText(raw)
        }
        return parsed

    def execute(self, method=None, target=None, option=None, parse=False):
        cmd = self._build_cmd(method, target=target, option=option)
        output = {}
        try:
            raw = self._connect()._exec(cmd)
            output['raw'] = raw
        except Exception:
            raise
        finally:
            self._disconnect()
        if parse:
            parsed = self._parse(raw=raw, method=method, option=option)
            output['parsed'] = parsed
        return output
