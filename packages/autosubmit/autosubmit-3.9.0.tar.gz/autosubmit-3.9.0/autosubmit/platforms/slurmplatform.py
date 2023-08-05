#!/usr/bin/env python

# Copyright 2017 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

import os

from xml.dom.minidom import parseString

from autosubmit.platforms.paramiko_platform import ParamikoPlatform
from autosubmit.platforms.headers.slurm_header import SlurmHeader
from autosubmit.platforms.wrappers.slurm_wrapper import SlurmWrapper


class SlurmPlatform(ParamikoPlatform):
    """
    Class to manage jobs to host using SLURM scheduler

    :param expid: experiment's identifier
    :type expid: str
    """

    def __init__(self, expid, name, config):
        ParamikoPlatform.__init__(self, expid, name, config)
        self._header = SlurmHeader()
        self._wrapper = SlurmWrapper()
        self.job_status = dict()
        self.job_status['COMPLETED'] = ['COMPLETED']
        self.job_status['RUNNING'] = ['RUNNING']
        self.job_status['QUEUING'] = ['PENDING', 'CONFIGURING', 'RESIZING']
        self.job_status['FAILED'] = ['FAILED', 'CANCELLED', 'NODE_FAIL', 'PREEMPTED', 'SUSPENDED', 'TIMEOUT']
        self._pathdir = "\$HOME/LOG_" + self.expid
        self._allow_arrays = False
        self._allow_wrappers = True
        self.update_cmds()

    def update_cmds(self):
        """
        Updates commands for platforms
        """
        self.root_dir = os.path.join(self.scratch, self.project, self.user, self.expid)
        self.remote_log_dir = os.path.join(self.root_dir, "LOG_" + self.expid)
        self.cancel_cmd = "scancel"
        self._checkhost_cmd = "echo 1"
        self._submit_cmd = 'sbatch -D {1} {1}/'.format(self.host, self.remote_log_dir)
        self.put_cmd = "scp"
        self.get_cmd = "scp"
        self.mkdir_cmd = "mkdir -p " + self.remote_log_dir

    def get_checkhost_cmd(self):
        return self._checkhost_cmd

    def get_mkdir_cmd(self):
        return self.mkdir_cmd

    def get_remote_log_dir(self):
        return self.remote_log_dir

    def parse_job_output(self, output):
        return output.strip().split(' ')[0].strip()

    def get_submitted_job_id(self, output):
        return output.split(' ')[3]

    def jobs_in_queue(self):
        dom = parseString('')
        jobs_xml = dom.getElementsByTagName("JB_job_number")
        return [int(element.firstChild.nodeValue) for element in jobs_xml]

    def get_submit_cmd(self, job_script, job):
        return self._submit_cmd + job_script

    def get_checkjob_cmd(self, job_id):
        return 'sacct -n -j {1} -o "State"'.format(self.host, job_id)
