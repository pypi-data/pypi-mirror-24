#!/usr/bin/python3

# Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply

from argparse import ArgumentParser
import json
from dbus.mainloop.glib import DBusGMainLoop

from bjarkan.device_manager import DeviceManager
from bjarkan.list_devices import connected_devices, paired_devices, all_devices


def format_device_data(devices, format_json):
    if format_json:
        data = []
        for device in devices:
            device_data = {}
            device_data['address'] = device['address']
            device_data['rssi'] = device['rssi']
            device_data['icon'] = device['icon']
            device_data['paired'] = device['paired']
            device_data['connected'] = device['connected']
            device_data['alias'] = device['alias']
            data.append(device_data)

        print(json.dumps(data))
    else:
        for device in devices:
            print(
                '{!s} {!s} {!s} {!s} {!s} {!s}'.format(
                    device['address'],
                    device['rssi'],
                    device['paired'],
                    device['connected'],
                    device['icon'],
                    device['alias']
                )
            )


def format_results(results, format_json):
    if format_json:
        print(json.dumps({'result': results['result'], 'code': results['code']}))
    else:
        print('result: {}, code: {}'.format(results['result'], results['code']))


def pair(args):
    device_manager = DeviceManager(args.device)
    return format_results(device_manager.pair_device(), args.json)


def unpair(args):
    device_manager = DeviceManager(args.device)
    return format_results(device_manager.unpair_device(), args.json)


def connect(args):
    device_manager = DeviceManager(args.device)
    return format_results(device_manager.connect_device(), args.json)


def disconnect(args):
    device_manager = DeviceManager(args.device)
    return format_results(device_manager.disconnect_device(), args.json)


def connected(args):
    return format_device_data(connected_devices(), args.json)


def paired(args):
    return format_device_data(paired_devices(), args.json)


def scan(args):
    return format_device_data(all_devices(), args.json)


def main():
    DBusGMainLoop( set_as_default = True )

    parser = ArgumentParser(description = 'Connect to specifed BT device')
    parser.add_argument('-j', '--json', action = 'store_true', help = 'Change output format to json instead of plain text')
    subparsers = parser.add_subparsers(metavar = 'COMMAND')
    subparsers.required = True

    pair_parser = subparsers.add_parser('pair', help = 'Pair a device (pairing will also connect)')
    pair_parser.add_argument('-d', '--device', required = True, help = 'Specify the device to pair')
    pair_parser.set_defaults(func = pair)

    unpair_parser = subparsers.add_parser('unpair', help = 'Unpair a device')
    unpair_parser.add_argument('-d', '--device', required = True, help = 'Specify the device to unpair')
    unpair_parser.set_defaults(func = unpair)

    connect_parser = subparsers.add_parser('connect', help = 'Connect a new device')
    connect_parser.add_argument('-d', '--device', required = True, help = 'Specify the device to connect to')
    connect_parser.set_defaults(func = connect)

    disconnect_parser = subparsers.add_parser('disconnect', help = 'Disconnect a device')
    disconnect_parser.add_argument('-d', '--device', required = True, help = 'Specify the device to disconnect from')
    disconnect_parser.set_defaults(func = disconnect)

    paired_parser = subparsers.add_parser('paired-devices', help = 'Show all paired devices')
    paired_parser.set_defaults(func = paired)

    connected_parser = subparsers.add_parser('connected-devices', help = 'Show all connected devices')
    connected_parser.set_defaults( func = connected )

    list_parser = subparsers.add_parser('scan', help = 'Show all currently known devices')
    list_parser.set_defaults(func = scan)

    args = parser.parse_args()

    result = args.func(args)
    if result:
        return result

    return 0


if __name__ == '__main__':
    main()
