

# https://blog.ipswitch.com/managing-windows-system-administration-with-wmi-and-python
# https://stackoverflow.com/questions/20171392/python-pprint-dictionary-on-multiple-lines
# https://topnetworkguide.com/python-script-to-get-windows-system-information-using-wmi/

# netsh advfirewall firewall set rule group="windows management instrumentation (wmi)" new enable=yes

import wmi
import re


def connect_windows(host=None):
    if host:
        connection = None
    else:
        connection = wmi.WMI()
    return connection


def get_windows_users(connection):
    user_list = {}
    for group in connection.Win32_Group():
        machine_group = re.search(r'(\S+)\\(\S+)', group.Caption)
        machine_name = machine_group.group(1)
        group_name = machine_group.group(2)
        user_list[group_name] = dict(machine=machine_name, users=[])

        for user in group.associators(wmi_result_class="Win32_UserAccount"):
            machine_user = re.search(r'(\S+)\\(\S+)', user.Caption)
            # machine_name = machine_user.group(1)
            user_name = machine_user.group(2)
            user_list[group_name]['users'].append(user_name)

    return user_list


def connect_get_win_users(host=None):
    connection = connect_windows(host)
    return get_windows_users(connection)


print(connect_get_win_users())



