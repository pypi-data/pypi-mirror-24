monitoring-plugins-apparmor
===========================

Python Nagios-compatible App Armor checks.

Description
===========

These Nagios-compatible checks aim to monitor apparmor-related
behaviours (status, profiles).

Usage
=====

Checks if App Armor is enabled:
``/usr/lib/nagios/plugins/check_aa_status``. This plugin requires a sudo
configuration, such as:

::

    User_Alias NAGIOS = nagios
    Cmd_Alias NAGIOS_CMD = /usr/sbin/aa-status --enabled
    NAGIOS ALL = (root) NOPASSWD: NOEXEC: NAGIOS_CMD

Checks if the given binary is enforced:
``/usr/lib/nagios/plugins/check_aa_profile --process=libvirtd``

Help
====

::

    /usr/lib/nagios/plugins/check_aa_status --help
    Usage: check_aa_status [options]

    Options:
      -v, --verbose         
      -H HOSTNAME, --hostname=HOSTNAME
      -w WARNING, --warning=WARNING
      -c CRITICAL, --critical=CRITICAL
      -t TIMEOUT, --timeout=TIMEOUT
      -h, --help            show this help message and exit

The process is mandatory.

::

    /usr/lib/nagios/plugins/check_aa_profile --help
    Usage: check_aa_profile [options]

    Options:
      --process=PROCESS     The name of the process to find
      -v, --verbose         
      -H HOSTNAME, --hostname=HOSTNAME
      -w WARNING, --warning=WARNING
      -c CRITICAL, --critical=CRITICAL
      -t TIMEOUT, --timeout=TIMEOUT
      -h, --help            show this help message and exit

