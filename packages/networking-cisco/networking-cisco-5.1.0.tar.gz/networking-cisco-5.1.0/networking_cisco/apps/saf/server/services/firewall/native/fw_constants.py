# Copyright 2014 Cisco Systems, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Service Constants

import networking_cisco.apps.saf.server.services.constants as services_const

AUTO_NWK_CREATE = True
DEVICE = ''
SCHED_POLICY = 'max_sched'
VLAN_ID_MIN = services_const.VLAN_ID_MIN
VLAN_ID_MAX = services_const.VLAN_ID_MAX
MOB_DOMAIN_NAME = 'md0'
HOST_PROF = 'serviceNetworkUniversalDynamicRoutingESProfile'
HOST_FWD_MODE = 'proxy-gateway'
PART_PROF = 'vrf-common-universal-external-dynamic-ES'
EXT_PROF = 'externalNetworkUniversalDynamicRoutingESProfile'
EXT_FWD_MODE = 'anycast-gateway'
IN_IP_START = '100.100.2.0/24'
IN_IP_END = '100.100.20.0/24'
OUT_IP_START = '200.200.2.0/24'
OUT_IP_END = '200.200.20.0/24'
DUMMY_IP_SUBNET = '9.9.9.0/24'
SERVICE_NAME_EXTRA_LEN = 8

IN_SERVICE_SUBNET = 'FwServiceInSub'
IN_SERVICE_NWK = 'FwServiceInNwk'
SERV_PART_NAME = 'CTX-ext'
OUT_SERVICE_SUBNET = 'FwServiceOutSub'
OUT_SERVICE_NWK = 'FwServiceOutNwk'
DUMMY_SERVICE_RTR = 'DUMMY_SRVC_RTR'
DUMMY_SERVICE_NWK = 'DUMMY_SRVC_NWK'
TENANT_EDGE_RTR = 'Cisco_TenantEdge'
FW_TENANT_EDGE = 'TE'

FW_CR_OP = 'CREATE'
FW_DEL_OP = 'DELETE'

RESULT_FW_CREATE_INIT = 'FAB_CREATE_PEND'
RESULT_FW_CREATE_DONE = 'FAB_CREATE_DONE'
RESULT_FW_DELETE_INIT = 'FAB_DELETE_PEND'
RESULT_FW_DELETE_DONE = 'FAB_DELETE_DONE'

FW_CONST = 'Firewall'
INIT_STATE_STR = 'INIT'

OS_IN_NETWORK_CREATE_FAIL = 'OS_IN_NETWORK_CREATE_FAIL'
OS_INIT_STATE = OS_IN_NETWORK_CREATE_FAIL
OS_IN_NETWORK_CREATE_SUCCESS = 'OS_IN_NETWORK_CREATE_SUCCESS'
OS_OUT_NETWORK_CREATE_FAIL = 'OS_OUT_NETWORK_CREATE_FAIL'
OS_OUT_NETWORK_CREATE_SUCCESS = 'OS_OUT_NETWORK_CREATE_SUCCESS'
OS_DUMMY_RTR_CREATE_FAIL = 'OS_DUMMY_RTR_CREATE_FAIL'
OS_DUMMY_RTR_CREATE_SUCCESS = 'OS_DUMMY_RTR_CREATE_SUCCESS'
OS_CREATE_SUCCESS = OS_DUMMY_RTR_CREATE_SUCCESS
DCNM_IN_NETWORK_CREATE_FAIL = 'DCNM_IN_NETWORK_CREATE_FAIL'
DCNM_INIT_STATE = DCNM_IN_NETWORK_CREATE_FAIL
DCNM_IN_NETWORK_CREATE_SUCCESS = 'DCNM_IN_NETWORK_CREATE_SUCCESS'
DCNM_IN_PART_UPDATE_FAIL = 'DCNM_IN_PART_UPDATE_FAIL'
DCNM_IN_PART_UPDATE_SUCCESS = 'DCNM_IN_PART_UPDATE_SUCCESS'
DCNM_OUT_PART_CREATE_FAIL = 'DCNM_OUT_PART_CREATE_FAIL'
DCNM_OUT_PART_CREATE_SUCCESS = 'DCNM_OUT_PART_CREATE_SUCCESS'
DCNM_OUT_NETWORK_CREATE_FAIL = 'DCNM_OUT_NETWORK_CREATE_FAIL'
DCNM_OUT_NETWORK_CREATE_SUCCESS = 'DCNM_OUT_NETWORK_CREATE_SUCCESS'
DCNM_OUT_PART_UPDATE_FAIL = 'DCNM_OUT_PART_UPDATE_FAIL'
DCNM_OUT_PART_UPDATE_SUCCESS = 'DCNM_OUT_PART_UPDATE_SUCCESS'
DCNM_CREATE_SUCCESS = DCNM_OUT_PART_UPDATE_SUCCESS
# FABRIC_PREPARE_SUCCESS = DCNM_OUT_PART_UPDATE_SUCCESS
FABRIC_PREPARE_SUCCESS = 'FABRIC_PREPARE_SUCCESS'

OS_IN_NETWORK_DEL_FAIL = 'OS_IN_NETWORK_DEL_FAIL'
OS_IN_NETWORK_DEL_SUCCESS = 'OS_IN_NETWORK_DEL_SUCCESS'
OS_OUT_NETWORK_DEL_FAIL = 'OS_OUT_NETWORK_DEL_FAIL'
OS_OUT_NETWORK_DEL_SUCCESS = 'OS_OUT_NETWORK_DEL_SUCCESS'
OS_DUMMY_RTR_DEL_FAIL = 'OS_DUMMY_RTR_DEL_FAIL'
OS_DUMMY_RTR_DEL_SUCCESS = 'OS_DUMMY_RTR_DEL_SUCCESS'
OS_DEL_SUCCESS = 'OS_DUMMY_RTR_DEL_SUCCESS'
DCNM_IN_NETWORK_DEL_FAIL = 'DCNM_IN_NETWORK_DEL_FAIL'
DCNM_IN_NETWORK_DEL_SUCCESS = 'DCNM_IN_NETWORK_DEL_SUCCESS'
DCNM_IN_PART_UPDDEL_FAIL = 'DCNM_IN_PART_UPDDEL_FAIL'
DCNM_IN_PART_UPDDEL_SUCCESS = 'DCNM_IN_PART_UPDDEL_SUCCESS'
DCNM_OUT_PART_DEL_FAIL = 'DCNM_OUT_PART_DEL_FAIL'
DCNM_OUT_PART_DEL_SUCCESS = 'DCNM_OUT_PART_DEL_SUCCESS'
DCNM_OUT_NETWORK_DEL_FAIL = 'DCNM_OUT_NETWORK_DEL_FAIL'
DCNM_OUT_NETWORK_DEL_SUCCESS = 'DCNM_OUT_NETWORK_DEL_SUCCESS'
DCNM_OUT_PART_UPDDEL_FAIL = 'DCNM_OUT_PART_UPDDEL_FAIL'
DCNM_OUT_PART_UPDDEL_SUCCESS = 'DCNM_OUT_PART_UPDDEL_SUCCESS'
DCNM_DELETE_SUCCESS = DCNM_IN_NETWORK_DEL_SUCCESS
INIT = 0
MAX_STATE = FABRIC_PREPARE_SUCCESS  # 17

INIT_STATE = 100
OS_IN_NETWORK_STATE = INIT_STATE + 1
OS_OUT_NETWORK_STATE = OS_IN_NETWORK_STATE + 1
OS_DUMMY_RTR_STATE = OS_OUT_NETWORK_STATE + 1
OS_COMPL_STATE = OS_DUMMY_RTR_STATE
DCNM_IN_NETWORK_STATE = OS_DUMMY_RTR_STATE + 1
DCNM_IN_PART_UPDATE_STATE = DCNM_IN_NETWORK_STATE + 1
DCNM_OUT_PART_STATE = DCNM_IN_PART_UPDATE_STATE + 1
DCNM_OUT_NETWORK_STATE = DCNM_OUT_PART_STATE + 1
DCNM_OUT_PART_UPDATE_STATE = DCNM_OUT_NETWORK_STATE + 1
FABRIC_PREPARE_DONE_STATE = DCNM_OUT_PART_UPDATE_STATE + 1

# The below is for debug display
fw_state_fn_dict = {}
fw_state_fn_dict[INIT_STATE] = 'INIT_STATE'
fw_state_fn_dict[OS_IN_NETWORK_STATE] = 'OS_IN_NETWORK_CREATE_STATE'
fw_state_fn_dict[OS_OUT_NETWORK_STATE] = 'OS_OUT_NETWORK_CREATE_STATE'
fw_state_fn_dict[OS_DUMMY_RTR_STATE] = 'OS_DUMMY_RTR_CREATE_STATE'
fw_state_fn_dict[DCNM_IN_NETWORK_STATE] = 'DCNM_IN_NETWORK_CREATE_STATE'
fw_state_fn_dict[DCNM_IN_PART_UPDATE_STATE] = 'DCNM_IN_PART_UPDATE_STATE'
fw_state_fn_dict[DCNM_OUT_PART_STATE] = 'DCNM_OUT_PART_CREATE_STATE'
fw_state_fn_dict[DCNM_OUT_NETWORK_STATE] = 'DCNM_OUT_NETWORK_CREATE_STATE'
fw_state_fn_dict[DCNM_OUT_PART_UPDATE_STATE] = 'DCNM_OUT_PART_UPDATE_STATE'
fw_state_fn_dict[FABRIC_PREPARE_DONE_STATE] = 'FABRIC_PREPARE_DONE_STATE'

fw_state_fn_del_dict = {}
fw_state_fn_del_dict[INIT_STATE] = 'INIT_STATE'
fw_state_fn_del_dict[OS_IN_NETWORK_STATE] = 'OS_IN_NETWORK_DELETE_STATE'
fw_state_fn_del_dict[OS_OUT_NETWORK_STATE] = 'OS_OUT_NETWORK_DELETE_STATE'
fw_state_fn_del_dict[OS_DUMMY_RTR_STATE] = 'OS_DUMMY_RTR_DELETE_STATE'
fw_state_fn_del_dict[DCNM_IN_NETWORK_STATE] = 'DCNM_IN_NETWORK_DELETE_STATE'
fw_state_fn_del_dict[DCNM_IN_PART_UPDATE_STATE] = 'DCNM_IN_PART_UPDDEL_STATE'
fw_state_fn_del_dict[DCNM_OUT_PART_STATE] = 'DCNM_OUT_PART_DELETE_STATE'
fw_state_fn_del_dict[DCNM_OUT_NETWORK_STATE] = 'DCNM_OUT_NETWORK_DELETE_STATE'
fw_state_fn_del_dict[DCNM_OUT_PART_UPDATE_STATE] = 'DCNM_OUT_PART_UPDDEL_STATE'
fw_state_fn_del_dict[FABRIC_PREPARE_DONE_STATE] = 'FABRIC_PREPARE_DONE_STATE'
