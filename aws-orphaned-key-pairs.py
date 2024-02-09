#!/usr/bin/env python3

import boto3


def main():
    ec2_client = boto3.client('ec2')

    all_keys = []
    instance_keys = set()
    orphaned_keys = []

    banner_outline = '-'*40

    key_data = ec2_client.describe_key_pairs()

    for item in key_data.get('KeyPairs'):
        key_name = item.get('KeyName')
        all_keys.append(key_name)

    instance_data = ec2_client.describe_instances()

    reservations = instance_data.get('Reservations')

    for item in reservations:
        instance_keys.add(item.get('Instances')[0].get('KeyName'))

    instance_keys = list(instance_keys)

    for key in all_keys:
        if key not in instance_keys:
            orphaned_keys.append(key)

    orphan_key_count = len(orphaned_keys)

    if orphan_key_count > 0:
        print(f'{banner_outline}\n{orphan_key_count} orphaned key pairs found!\n{banner_outline}')
        for key in orphaned_keys:
            print(key)


if __name__ == '__main__':
    main()
