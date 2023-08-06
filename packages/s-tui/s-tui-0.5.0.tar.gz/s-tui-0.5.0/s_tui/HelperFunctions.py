#!/usr/bin/env python
#
# Copyright (C) 2017 Alex Manuskin, Gil Tsuker
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


""" Reads the value of the msr containing information on Turbo Boost on intel CPUs
"""
import os
import logging
import signal
import platform
import subprocess
import re

__version__ = "0.5.0"
TURBO_MSR = 429


def get_avarage_cpu_freq():
    with open("/proc/cpuinfo") as cpuinfo:
        cores_freq = []
        for line in cpuinfo:
            if "cpu MHz" in line:
                core_freq = re.findall("\d+\.\d+", line)
                cores_freq += core_freq
        return round(reduce(lambda x, y: float(x) + float(y), cores_freq) / len(cores_freq), 1)



def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
         return subprocess.check_output(['/usr/sbin/sysctl', "-n", "machdep.cpu.brand_string"]).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return ""


def read_msr(msr, cpu=0):
    if not os.path.exists("/dev/cpu/0/msr"):
        try:
            os.system("/sbin/modprobe msr")
            logging.debug("Ran modprobe sucessfully")
        except:
            pass
            return None
    msr_file = '/dev/cpu/%d/msr' % (cpu,)
    try:
        with open(msr_file, 'r') as f:
            f.seek(msr)
            read_res = f.read(8)
        s_decoded = [ord(c) for c in read_res]
        return s_decoded
    except IOError as e:
        e.message = e.message + "Unable to read file " + msr_file
        raise e
    except OSError as e:
        e.message = e.message + "File " + msr_file + " does not exist"
        raise e


def kill_child_processes(parent_proc, sig=signal.SIGTERM):
    try:
        for proc in parent_proc.children(recursive=True):
            logging.debug('Killing' + str(proc))
            proc.kill()
        parent_proc.kill()
    except:
        logging.debug('No such process')


PALETTE = [
    ('body',                    'black',          'light gray',   'standout'),
    ('header',                  'white',          'dark red',     'bold'),
    ('screen edge',             'light blue',     'brown'),
    ('main shadow',             'dark gray',      'black'),
    ('line',                    'black',          'light gray',   'standout'),
    ('menu button',             'light gray',     'black'),
    ('bg background',           'light gray',     'black'),
    ('util light',              'black',          'dark green',   'standout'),
    ('util light smooth',       'dark green',     'black'),
    ('util dark',               'dark red',       'light green',  'standout'),
    ('util dark smooth',        'light green',    'black'),
    ('high temp dark',          'light red',      'dark red',     'standout'),
    ('overheat dark',           'black',          'light red',     'standout'),
    ('high temp dark smooth',   'dark red',       'black'),
    ('high temp light',         'dark red',       'light red',    'standout'),
    ('high temp light smooth',  'light red',      'black'),
    ('power dark',               'dark gray',          'dark cyan',    'standout'),
    ('power dark smooth',        'dark gray',      'black'),
    ('power light',              'light gray',       'light cyan',   'standout'),
    ('temp dark',               'black',          'dark cyan',    'standout'),
    ('temp dark smooth',        'dark cyan',      'black'),
    ('temp light',              'dark red',       'light cyan',   'standout'),
    ('temp light smooth',       'light cyan',     'black'),
    ('freq dark',               'dark red',       'dark magenta', 'standout'),
    ('freq dark smooth',        'dark magenta',   'black'),
    ('freq light',              'dark red',       'light magenta', 'standout'),
    ('freq light smooth',       'light magenta',  'black'),
    ('button normal',           'de gray',     'dark blue',    'standout'),
    ('button select',           'white',          'dark green'),
    ('line',                    'black',          'light gray',   'standout'),
    ('pg normal',               'white',          'black',        'standout'),
    ('pg complete',             'white',          'dark magenta'),
    ('high temp txt',           'light red',      'light gray'),
    ('pg smooth',               'dark magenta',   'black')
    ]

DEFAULT_PALETTE = [
    ('body',                    'default',        'default',   'standout'),
    ('header',                  'default',        'dark red',     ),
    ('screen edge',             'light blue',     'brown'),
    ('main shadow',             'dark gray',      'black'),
    ('line',                    'default',          'light gray',   'standout'),
    ('menu button',             'light gray',     'black'),
    ('bg background',           'default',         'default'),
    ('overheat dark',           'white',          'light red',     'standout'),

    ('util light',              'default',          'dark green',   'standout'),
    ('util light smooth',       'dark green',     'default'),
    ('util dark',               'dark red',       'light green',  'standout'),
    ('util dark smooth',        'light green',    'default'),

    ('high temp dark',          'default',       'dark red',     'standout'),
    ('high temp dark smooth',   'dark red',      'default'),
    ('high temp light',         'default',       'light red',    'standout'),
    ('high temp light smooth',  'light red',     'default'),

    ('power dark',               'default',      'black',    'standout'),
    ('power dark smooth',        'black',        'default'),
    ('power light',              'default',      'light gray',   'standout'),
    ('power light smooth',       'light gray',   'default'),

    ('temp dark',               'default',        'dark cyan',    'standout'),
    ('temp dark smooth',        'dark cyan',      'default'),
    ('temp light',              'default',       'light cyan',   'standout'),
    ('temp light smooth',       'light cyan',     'default'),

    ('freq dark',               'default',        'dark magenta', 'standout'),
    ('freq dark smooth',        'dark magenta',   'default'),
    ('freq light',              'default',        'light magenta', 'standout'),
    ('freq light smooth',       'light magenta',  'default'),

    ('button normal',           'dark green',     'default',    'standout'),
    ('button select',           'white',          'dark green'),
    ('line',                    'default',        'default',      'standout'),
    ('pg normal',               'white',          'default',        'standout'),
    ('pg complete',             'white',          'dark magenta'),
    ('high temp txt',           'light red',      'default'),
    ('pg smooth',               'dark magenta',   'default')
    ]

if '__main__' == __name__:
    avg = get_avarage_cpu_freq()
    print(avg)
