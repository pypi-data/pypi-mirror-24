"""
Overview
========

Used to spawn processes and send/receive data. It is useful to talk with extern processes like interpreters.

Key-Commands
============

Namespace: shell

Mode: NORMAL
Event: <F2>
Description: Send the cursor line to the process.

Mode: INSERT
Event: <F2>
Description: Send the cursor line to the process and insert a line down.
"""

from untwisted.expect import Expect, LOAD, CLOSE
from untwisted.network import xmap
from vyapp.exe import exec_quiet
from tkinter import TclError
from vyapp.plugins import ENV
from vyapp.areavi import AreaVi
from vyapp.app import root
from os import environ 

import signal
import shlex

class Shell(object):
    def __init__(self, data, area, output):
        self.area = area
        self.output = output

        try:
            self.expect = Expect(*shlex.split(data), env=environ)
        except Exception as e:
            root.status.set_msg(e)
        else:
            self.install_events()
        
    def install_events(self):
        """

        """

        # When one of the AreaVi instances are destroyed then
        # the process is killed.
        self.output.hook('shell', -1, '<Destroy>', lambda event: 
        self.terminate_process())
        self.area.hook('shell', -1, '<Destroy>', lambda event: 
        self.terminate_process())

        # self.output.hook('shell', 'NORMAL', '<Control-F2>', lambda event: 
        # self.map_process_input())

        self.map_process_input()
        # When call.terminnate is called it may happen of having still data to be
        # processed. It would attempt to write on an AreaVi instance that no more exist.
        # So, it executes quietly the AreaVi.append method.
        xmap(self.expect, LOAD, lambda expect, data: 
        exec_quiet(self.output.append, data))

        xmap(self.expect, CLOSE, self.handle_close)

    def map_process_input(self):
        self.area.hook('shell', 'NORMAL', '<F1>', lambda event: 
        self.dump_line(), add=False)

        self.area.hook('shell', 'INSERT', '<F1>', lambda event: 
        self.dump_line(), add=False)

        self.area.hook('shell', 'NORMAL', '<Control-c>', lambda event: 
        self.dump_signal(signal.SIGINT), add=False)

        self.area.hook('shell', 'NORMAL', '<Control-backslash>', lambda event: 
        self.dump_signal(signal.SIGQUIT), add=False)

        root.status.set_msg('%s -> %s' % (self.area.filename, self.output.filename))

    def dump_signal(self, num):
        self.expect.child.send_signal(num)

    def terminate_process(self):
        try:
            self.expect.terminate()
        except Exception:
            pass
        root.status.set_msg('Killed process!')

    def dump_line(self):
        data = self.area.curline().encode(self.area.charset)
        self.expect.send(data)
        self.area.down()

    def handle_close(self, expect):
        root.status.set_msg('Killed process!')
        expect.destroy()


ENV['Shell']  = Shell
ENV['hshell'] = lambda data: Shell(data, AreaVi.ACTIVE, AreaVi.ACTIVE.master.master.create())
ENV['vshell'] = lambda data: Shell(data, AreaVi.ACTIVE, AreaVi.ACTIVE.master.master.master.create())
ENV['vbash']  = lambda : Shell('bash -i',AreaVi.ACTIVE, AreaVi.ACTIVE.master.master.master.create())
ENV['hbash'] = lambda : Shell('bash -i', AreaVi.ACTIVE, AreaVi.ACTIVE.master.master.create())




