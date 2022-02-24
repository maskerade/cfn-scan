import logging
import json
import subprocess
from typing import Any, MutableMapping, Optional


from cloudformation_cli_python_lib import (
    BaseHookHandlerRequest,
    HandlerErrorCode,
    Hook,
    HookInvocationPoint,
    OperationStatus,
    ProgressEvent,
    SessionProxy,
    exceptions,
)

from .models import HookHandlerRequest, TypeConfigurationModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

TYPE_NAME = "Booking::Cloud::ScanHook"

hook = Hook(TYPE_NAME, TypeConfigurationModel)
test_entrypoint = hook.test_entrypoint

TMP_CFN_FILE = "/tmp/resource.json"
# CHECKOV_CHECKS = "CKV_AWS_19"

CFN_SCAN_CMD_CHECKOV = ["python",
                        "/var/task/booking_cloud_scanhook/checkrun",
                        "-f",
                        TMP_CFN_FILE,
                        "--output",
                        "json",
                        # "-c",
                        # CHECKOV_CHECKS
                        ]


@hook.handler(HookInvocationPoint.CREATE_PRE_PROVISION)
def pre_create_handler(
        session: Optional[SessionProxy],
        request: HookHandlerRequest,
        callback_context: MutableMapping[str, Any],
        type_configuration: TypeConfigurationModel
) -> ProgressEvent:
    target_model = request.hookContext.targetModel
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS
    )
    target_name = request.hookContext.targetName
    LOG.debug(request)
    enabled_checks = type_configuration.EnabledChecks

    CFN_SCAN_CMD_CHECKOV.append("-c")
    CFN_SCAN_CMD_CHECKOV.extend(enabled_checks)

    try:
        resource_properties = target_model.get("resourceProperties")

        temp_template = {
                            "Resources": {
                                "Resource": {
                                    "Type":  target_name,
                                    "Properties": resource_properties
                                }
                            }
        }

        with open(TMP_CFN_FILE, "w") as outfile:
            json.dump(temp_template, outfile)

        checkov_run = subprocess.run(CFN_SCAN_CMD_CHECKOV, capture_output=True, encoding='utf-8')

        if checkov_run.returncode == 0:
            # Setting Status to success will signal to cfn that the hook operation is complete
            progress.status = OperationStatus.SUCCESS
            progress.message = f"Successfully invoked HookHandler for target {target_name}. Resource passed compliance checks"
        else:
            LOG.debug("ERROR: 1 or more Template Compliance checks have failed, see below for details")
            LOG.debug(checkov_run.stdout)
            progress.status = OperationStatus.FAILED
            progress.message = f"Failed Hook due to compliance checks failing for {target_name} resource."
            progress.errorCode = HandlerErrorCode.NonCompliant
            progress.message = "One or more template compliance checks have failed, check logs for details"

    except TypeError as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        raise exceptions.InternalFailure(f"was not expecting type {e}")
        # this can also be done by returning a failed progress event
        # return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"was not expecting type {e}")

    return progress


@hook.handler(HookInvocationPoint.UPDATE_PRE_PROVISION)
def pre_update_handler(
        session: Optional[SessionProxy],
        request: BaseHookHandlerRequest,
        callback_context: MutableMapping[str, Any],
        type_configuration: TypeConfigurationModel
) -> ProgressEvent:
    target_model = request.hookContext.targetModel
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS
    )
    # TODO: put code here

    # Example:
    try:
        # A Hook that does not allow a resource's encryption algorithm to be modified

        # Reading the Resource Hook's target current properties and previous properties
        resource_properties = target_model.get("resourceProperties")
        previous_properties = target_model.get("previousResourceProperties")

        if resource_properties.get("encryptionAlgorithm") != previous_properties.get("encryptionAlgorithm"):
            progress.status = OperationStatus.FAILED
            progress.message = "Encryption algorithm can not be changed"
        else:
            progress.status = OperationStatus.SUCCESS
    except TypeError as e:
        progress = ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"was not expecting type {e}")

    return progress
