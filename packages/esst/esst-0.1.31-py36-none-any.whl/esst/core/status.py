# coding=utf-8
"""
Dummy class to facilitate the passing of information between other classes
"""


class Status:  # pylint: disable=too-few-public-methods
    """
    Represents DCS status
    """
    dcs_application = 'not running'
    dcs_version = 'unknown'
    dcs_cpu_usage = 'unknown'
    server_status = 'unknown'
    metar = 'unknown'
    mission_file = 'unknown'
    server_age = 'unknown'
    mission_time = 'unknown'
    paused = 'unknown'
    mission_name = 'unknown'
    players = []


class ServerStatus:
    """
    Represents server status
    """
    physical_cpus = 'unknown'
    logical_cpus = 'unknown'
    cpu_frequency = 'unknown'
    cpu_usage = 'unknown'
    total_memory = 'unknown'
    free_memory = 'unknown'
    swap_size = 'unknown'
    swap_used = 'unknown'
    boot_time = 'unknown'
