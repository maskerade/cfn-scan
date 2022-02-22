import logging
from pythonjsonlogger import jsonlogger
import json
import subprocess
from typing import Any, MutableMapping, Optional
from checkov.main import run as checkovrun
import pathlib

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

jsonLogger = logging.getLogger()
jsonLogger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
jsonLogger.addHandler(logHandler)


hook = Hook(TYPE_NAME, TypeConfigurationModel)
test_entrypoint = hook.test_entrypoint


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


    try:

        # LOG.debug(pathlib.Path(__file__).parent.resolve())
        # LOG.debug(pathlib.Path().parent.resolve())
        #
        # # Reading the Resource Hook's target properties
        # checkov_run = subprocess.run(
        #     ["pwd"],
        #     capture_output=True)
        # LOG.debug(checkov_run.returncode)
        # LOG.debug(checkov_run.stdout)
        #
        # checkov_run = subprocess.run(
        #     ["ls", "-la"],
        #     capture_output=True)
        # LOG.debug(checkov_run.returncode)
        # LOG.debug(checkov_run.stdout)
        #
        # checkov_run = subprocess.run(
        #     ["ls", "-la", "../"],
        #     capture_output=True)
        # LOG.debug(checkov_run.returncode)
        # LOG.debug(checkov_run.stdout)
        #
        # checkov_run = subprocess.run(
        #     ["ls", "-la", "/var/task/cloudformation_cli_python_lib/"],
        #     capture_output=True)
        # LOG.debug(checkov_run.returncode)
        # LOG.debug(checkov_run.stdout)
        #
        # checkov_run = subprocess.run(
        #     ["ls", "-la", "/var/task/booking_cloud_scanhook"],
        #     capture_output=True)
        # LOG.debug(checkov_run.returncode)
        # LOG.debug(checkov_run.stdout)
        #

        checkov_run = subprocess.run(
            ["python", "/var/task/booking_cloud_scanhook/checkrun", "--version"],
            capture_output=True)
        LOG.debug(checkov_run.returncode)
        LOG.debug(checkov_run.stdout)
        LOG.debug(checkov_run.stderr)

        resource_properties = target_model.get("resourceProperties")

        temp_template = {
                            "Resources": {
                                "Resource": {
                                    "Type":  target_name,
                                    "Properties": resource_properties
                                }
                            }
        }


        with open('/tmp/resource.json', 'w') as outfile:
            json.dump(temp_template, outfile)

        # f = open("/tmp/resource.yaml", "w")
        #
        # f.write(resource_properties)
        # f.close()

        checkov_run = subprocess.run(
            ["cat", "/tmp/resource.json"],
            capture_output=True)
        LOG.debug(checkov_run.returncode)
        LOG.debug(checkov_run.stdout)
        LOG.debug(checkov_run.stderr)


        checkov_run = subprocess.run(
            ["python", "/var/task/booking_cloud_scanhook/checkrun", "-f", "/tmp/resource.json", "--quiet", "--compact", "--output", "cli", "-c", "CKV_AWS_19"],
            capture_output=True)
        LOG.debug(checkov_run.returncode)
        LOG.debug(checkov_run.stdout)
        LOG.debug(checkov_run.stderr)

        checkov_run = subprocess.run(
            ["python", "/var/task/booking_cloud_scanhook/checkrun", "-f", "/tmp/resource.json", "--quiet", "--compact", "--output", "json", "-c", "CKV_AWS_19"],
            capture_output=True)
        LOG.debug(checkov_run.returncode)
        jsonLogger.debug(checkov_run.stdout)
        LOG.debug(checkov_run.stderr)

        # list_files = subprocess.run(["ls", "-l"])

        # checkov_run = subprocess.run (["checkov", "-f", "s3noecryption.yaml", "--quiet", "--compact", "--output", "cli", "-c", "CKV_AWS_19"], capture_output=True)
        # print("The exit code was: %d" % checkov_run.returncode)
        # print("The output was: %s" % checkov_run.stdout)

        # run(banner="Bannertime",argv=[ "-f", "s3noecryption.yaml", "--quiet", "--compact", "--output", "cli", "-c", "CKV_AWS_19"])

        #checkovrun()
        #checkovrun(argv=["--version"])

        # Setting Status to success will signal to cfn that the hook operation is complete
        progress.status = OperationStatus.SUCCESS
    except TypeError as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        raise exceptions.InternalFailure(f"was not expecting type {e}")
        # this can also be done by returning a failed progress event
        # return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"was not expecting type {e}")


    # print("The exit code was: %d" % checkov_run.returncode)
    # print("The output was: %s" % checkov_run.stdout)

    # TODO: put code here

    # Example:
    try:
        # Reading the Resource Hook's target properties
        resource_properties = target_model.get("resourceProperties")

        if isinstance(session, SessionProxy):
            client = session.client("s3")
        # Setting Status to success will signal to cfn that the hook operation is complete
        progress.status = OperationStatus.SUCCESS
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

