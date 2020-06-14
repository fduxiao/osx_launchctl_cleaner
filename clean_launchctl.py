#!/usr/bin/env python3
import inspect
import os
import re
import stat
import subprocess
import sys


class WithSource:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

    @property
    def source(self):
        return inspect.getsource(self.f)


@WithSource
def read_command(*args):
    with subprocess.Popen(*args, stdout=subprocess.PIPE) as proc:
        return proc.stdout.read()


@WithSource
def launchctl_list(service_name=None):
    args = ["launchctl", "list"]
    if service_name is not None:
        args.append(service_name)
    return read_command(args)


@WithSource
def all_list():
    for one in launchctl_list().rstrip(b"\n").split(b"\n"):
        yield one.split(b"\t")[2]


@WithSource
def read_one(name):
    info = launchctl_list(name)
    program = re.findall(rb'"[pP]rogram"\s=\s"(.*?)";', info)
    if program:
        return program[0]


@WithSource
def read_diff(healthy_list):
    targets = set(all_list()) - set(healthy_list)
    for name in targets:
        print()
        print(name.decode())
        print(launchctl_list(name).decode())
        print()
        print()


if __name__ == '__main__':
    # run in a healthy system
    health = all_list()
    output_code = f"""#!/usr/bin/env python3
import inspect
import os
import re
import stat
import subprocess
import sys

{inspect.getsource(WithSource)}
{read_command.source}
{launchctl_list.source}
{all_list.source}
{read_one.source}
{read_diff.source}

read_diff({list(all_list())})
    """
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath, 'w') as f:
            f.write(output_code)
        st = os.stat(filepath)
        os.chmod(filepath, st.st_mode | stat.S_IEXEC)
    else:
        print(output_code)
