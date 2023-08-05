#!/bin/bash

# This script will be executed inside pre_test_hook function in devstack gate

set -ex

DIR=${BASH_SOURCE%/*}
source $DIR/commons $@

# Enable LBaaS V2 Neutron plugin
DEVSTACK_LOCAL_CONFIG+=$'\n'"enable_plugin neutron-lbaas https://git.openstack.org/openstack/neutron-lbaas"
ENABLED_SERVICES+=",q-lbaasv2"
DISABLED_SERVICES+="q-lbaas"

# Enable default recommended implementation for LBaaS v2, Octavia
ENABLED_SERVICES+=",octavia,o-cw,o-hk,o-hm,o-api"
DEVSTACK_LOCAL_CONFIG+=$'\n'"enable_plugin octavia https://git.openstack.org/openstack/octavia"
DEVSTACK_LOCAL_CONFIG+=$'\n'"[[post-config|/etc/octavia/octavia.conf]]"
DEVSTACK_LOCAL_CONFIG+=$'\n'"[controller_worker]"
DEVSTACK_LOCAL_CONFIG+=$'\n'"amphora_driver = amphora_noop_driver"
DEVSTACK_LOCAL_CONFIG+=$'\n'"compute_driver = compute_noop_driver"
DEVSTACK_LOCAL_CONFIG+=$'\n'"network_driver = network_noop_driver"

# Enable LBaaS v2 Horizon plugin
DEVSTACK_LOCAL_CONFIG+=$'\n'"enable_plugin neutron-lbaas-dashboard https://git.openstack.org/openstack/neutron-lbaas-dashboard"

export DEVSTACK_LOCAL_CONFIG
export ENABLED_SERVICES
export DISABLED_SERVICES

