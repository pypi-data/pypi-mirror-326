# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities
from . import outputs

__all__ = [
    'IntegrationAccountAuthConfig',
    'IntegrationAccountAuthConfigAwsAuthConfigKeys',
    'IntegrationAccountAuthConfigAwsAuthConfigRole',
    'IntegrationAccountAwsRegions',
    'IntegrationAccountLogsConfig',
    'IntegrationAccountLogsConfigLambdaForwarder',
    'IntegrationAccountMetricsConfig',
    'IntegrationAccountMetricsConfigNamespaceFilters',
    'IntegrationAccountMetricsConfigTagFilter',
    'IntegrationAccountResourcesConfig',
    'IntegrationAccountTracesConfig',
    'IntegrationAccountTracesConfigXrayServices',
    'GetIntegrationLogsServicesAwsLogsServiceResult',
]

@pulumi.output_type
class IntegrationAccountAuthConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "awsAuthConfigKeys":
            suggest = "aws_auth_config_keys"
        elif key == "awsAuthConfigRole":
            suggest = "aws_auth_config_role"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationAccountAuthConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationAccountAuthConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationAccountAuthConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 aws_auth_config_keys: Optional['outputs.IntegrationAccountAuthConfigAwsAuthConfigKeys'] = None,
                 aws_auth_config_role: Optional['outputs.IntegrationAccountAuthConfigAwsAuthConfigRole'] = None):
        """
        :param 'IntegrationAccountAuthConfigAwsAuthConfigKeysArgs' aws_auth_config_keys: Datadog will use the provided AWS Access Key ID and Secret Access Key to authenticate to your account.
        """
        if aws_auth_config_keys is not None:
            pulumi.set(__self__, "aws_auth_config_keys", aws_auth_config_keys)
        if aws_auth_config_role is not None:
            pulumi.set(__self__, "aws_auth_config_role", aws_auth_config_role)

    @property
    @pulumi.getter(name="awsAuthConfigKeys")
    def aws_auth_config_keys(self) -> Optional['outputs.IntegrationAccountAuthConfigAwsAuthConfigKeys']:
        """
        Datadog will use the provided AWS Access Key ID and Secret Access Key to authenticate to your account.
        """
        return pulumi.get(self, "aws_auth_config_keys")

    @property
    @pulumi.getter(name="awsAuthConfigRole")
    def aws_auth_config_role(self) -> Optional['outputs.IntegrationAccountAuthConfigAwsAuthConfigRole']:
        return pulumi.get(self, "aws_auth_config_role")


@pulumi.output_type
class IntegrationAccountAuthConfigAwsAuthConfigKeys(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accessKeyId":
            suggest = "access_key_id"
        elif key == "secretAccessKey":
            suggest = "secret_access_key"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationAccountAuthConfigAwsAuthConfigKeys. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationAccountAuthConfigAwsAuthConfigKeys.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationAccountAuthConfigAwsAuthConfigKeys.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 access_key_id: Optional[str] = None,
                 secret_access_key: Optional[str] = None):
        """
        :param str access_key_id: AWS Access Key ID
        """
        if access_key_id is not None:
            pulumi.set(__self__, "access_key_id", access_key_id)
        if secret_access_key is not None:
            pulumi.set(__self__, "secret_access_key", secret_access_key)

    @property
    @pulumi.getter(name="accessKeyId")
    def access_key_id(self) -> Optional[str]:
        """
        AWS Access Key ID
        """
        return pulumi.get(self, "access_key_id")

    @property
    @pulumi.getter(name="secretAccessKey")
    def secret_access_key(self) -> Optional[str]:
        return pulumi.get(self, "secret_access_key")


@pulumi.output_type
class IntegrationAccountAuthConfigAwsAuthConfigRole(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "externalId":
            suggest = "external_id"
        elif key == "roleName":
            suggest = "role_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationAccountAuthConfigAwsAuthConfigRole. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationAccountAuthConfigAwsAuthConfigRole.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationAccountAuthConfigAwsAuthConfigRole.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 external_id: Optional[str] = None,
                 role_name: Optional[str] = None):
        """
        :param str external_id: AWS IAM external ID for associated role. If omitted, one is generated.
        :param str role_name: AWS IAM role name.
        """
        if external_id is not None:
            pulumi.set(__self__, "external_id", external_id)
        if role_name is not None:
            pulumi.set(__self__, "role_name", role_name)

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> Optional[str]:
        """
        AWS IAM external ID for associated role. If omitted, one is generated.
        """
        return pulumi.get(self, "external_id")

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> Optional[str]:
        """
        AWS IAM role name.
        """
        return pulumi.get(self, "role_name")


@pulumi.output_type
class IntegrationAccountAwsRegions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "includeAll":
            suggest = "include_all"
        elif key == "includeOnlies":
            suggest = "include_onlies"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationAccountAwsRegions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationAccountAwsRegions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationAccountAwsRegions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 include_all: Optional[bool] = None,
                 include_onlies: Optional[Sequence[str]] = None):
        """
        :param bool include_all: Include all regions. Defaults to `true`.
        :param Sequence[str] include_onlies: Include only these regions.
        """
        if include_all is not None:
            pulumi.set(__self__, "include_all", include_all)
        if include_onlies is not None:
            pulumi.set(__self__, "include_onlies", include_onlies)

    @property
    @pulumi.getter(name="includeAll")
    def include_all(self) -> Optional[bool]:
        """
        Include all regions. Defaults to `true`.
        """
        return pulumi.get(self, "include_all")

    @property
    @pulumi.getter(name="includeOnlies")
    def include_onlies(self) -> Optional[Sequence[str]]:
        """
        Include only these regions.
        """
        return pulumi.get(self, "include_onlies")


@pulumi.output_type
class IntegrationAccountLogsConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "lambdaForwarder":
            suggest = "lambda_forwarder"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationAccountLogsConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationAccountLogsConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationAccountLogsConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 lambda_forwarder: Optional['outputs.IntegrationAccountLogsConfigLambdaForwarder'] = None):
        """
        :param 'IntegrationAccountLogsConfigLambdaForwarderArgs' lambda_forwarder: Leave empty to omit logs config.
        """
        if lambda_forwarder is not None:
            pulumi.set(__self__, "lambda_forwarder", lambda_forwarder)

    @property
    @pulumi.getter(name="lambdaForwarder")
    def lambda_forwarder(self) -> Optional['outputs.IntegrationAccountLogsConfigLambdaForwarder']:
        """
        Leave empty to omit logs config.
        """
        return pulumi.get(self, "lambda_forwarder")


@pulumi.output_type
class IntegrationAccountLogsConfigLambdaForwarder(dict):
    def __init__(__self__, *,
                 lambdas: Optional[Sequence[str]] = None,
                 sources: Optional[Sequence[str]] = None):
        """
        :param Sequence[str] lambdas: List of Datadog Lambda Log Forwarder ARNs in your AWS account. Defaults to `[]`.
        :param Sequence[str] sources: List of service IDs set to enable automatic log collection. Use `aws_get_integration_available_logs_services` data source to get allowed values. Defaults to `[]`.
        """
        if lambdas is not None:
            pulumi.set(__self__, "lambdas", lambdas)
        if sources is not None:
            pulumi.set(__self__, "sources", sources)

    @property
    @pulumi.getter
    def lambdas(self) -> Optional[Sequence[str]]:
        """
        List of Datadog Lambda Log Forwarder ARNs in your AWS account. Defaults to `[]`.
        """
        return pulumi.get(self, "lambdas")

    @property
    @pulumi.getter
    def sources(self) -> Optional[Sequence[str]]:
        """
        List of service IDs set to enable automatic log collection. Use `aws_get_integration_available_logs_services` data source to get allowed values. Defaults to `[]`.
        """
        return pulumi.get(self, "sources")


@pulumi.output_type
class IntegrationAccountMetricsConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "automuteEnabled":
            suggest = "automute_enabled"
        elif key == "collectCloudwatchAlarms":
            suggest = "collect_cloudwatch_alarms"
        elif key == "collectCustomMetrics":
            suggest = "collect_custom_metrics"
        elif key == "namespaceFilters":
            suggest = "namespace_filters"
        elif key == "tagFilters":
            suggest = "tag_filters"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationAccountMetricsConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationAccountMetricsConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationAccountMetricsConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 automute_enabled: Optional[bool] = None,
                 collect_cloudwatch_alarms: Optional[bool] = None,
                 collect_custom_metrics: Optional[bool] = None,
                 enabled: Optional[bool] = None,
                 namespace_filters: Optional['outputs.IntegrationAccountMetricsConfigNamespaceFilters'] = None,
                 tag_filters: Optional[Sequence['outputs.IntegrationAccountMetricsConfigTagFilter']] = None):
        """
        :param bool automute_enabled: Enable EC2 automute for AWS metrics Defaults to `true`.
        :param bool collect_cloudwatch_alarms: Enable CloudWatch alarms collection Defaults to `false`.
        :param bool collect_custom_metrics: Enable custom metrics collection Defaults to `false`.
        :param bool enabled: Enable AWS metrics collection Defaults to `true`.
        :param 'IntegrationAccountMetricsConfigNamespaceFiltersArgs' namespace_filters: AWS metrics namespace filters. Defaults to a pre-set `exclude_only` list if block is empty.
        :param Sequence['IntegrationAccountMetricsConfigTagFilterArgs'] tag_filters: AWS Metrics Collection tag filters list. The array of custom AWS resource tags (in the form `key:value`) defines a filter that Datadog uses when collecting metrics from a specified service. Wildcards, such as `?` (match a single character) and `*` (match multiple characters), and exclusion using `!` before the tag are supported. For EC2, only hosts that match one of the defined tags will be imported into Datadog. The rest will be ignored. For example, `env:production,instance-type:c?.*,!region:us-east-1`.
        """
        if automute_enabled is not None:
            pulumi.set(__self__, "automute_enabled", automute_enabled)
        if collect_cloudwatch_alarms is not None:
            pulumi.set(__self__, "collect_cloudwatch_alarms", collect_cloudwatch_alarms)
        if collect_custom_metrics is not None:
            pulumi.set(__self__, "collect_custom_metrics", collect_custom_metrics)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if namespace_filters is not None:
            pulumi.set(__self__, "namespace_filters", namespace_filters)
        if tag_filters is not None:
            pulumi.set(__self__, "tag_filters", tag_filters)

    @property
    @pulumi.getter(name="automuteEnabled")
    def automute_enabled(self) -> Optional[bool]:
        """
        Enable EC2 automute for AWS metrics Defaults to `true`.
        """
        return pulumi.get(self, "automute_enabled")

    @property
    @pulumi.getter(name="collectCloudwatchAlarms")
    def collect_cloudwatch_alarms(self) -> Optional[bool]:
        """
        Enable CloudWatch alarms collection Defaults to `false`.
        """
        return pulumi.get(self, "collect_cloudwatch_alarms")

    @property
    @pulumi.getter(name="collectCustomMetrics")
    def collect_custom_metrics(self) -> Optional[bool]:
        """
        Enable custom metrics collection Defaults to `false`.
        """
        return pulumi.get(self, "collect_custom_metrics")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Enable AWS metrics collection Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="namespaceFilters")
    def namespace_filters(self) -> Optional['outputs.IntegrationAccountMetricsConfigNamespaceFilters']:
        """
        AWS metrics namespace filters. Defaults to a pre-set `exclude_only` list if block is empty.
        """
        return pulumi.get(self, "namespace_filters")

    @property
    @pulumi.getter(name="tagFilters")
    def tag_filters(self) -> Optional[Sequence['outputs.IntegrationAccountMetricsConfigTagFilter']]:
        """
        AWS Metrics Collection tag filters list. The array of custom AWS resource tags (in the form `key:value`) defines a filter that Datadog uses when collecting metrics from a specified service. Wildcards, such as `?` (match a single character) and `*` (match multiple characters), and exclusion using `!` before the tag are supported. For EC2, only hosts that match one of the defined tags will be imported into Datadog. The rest will be ignored. For example, `env:production,instance-type:c?.*,!region:us-east-1`.
        """
        return pulumi.get(self, "tag_filters")


@pulumi.output_type
class IntegrationAccountMetricsConfigNamespaceFilters(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "excludeOnlies":
            suggest = "exclude_onlies"
        elif key == "includeOnlies":
            suggest = "include_onlies"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationAccountMetricsConfigNamespaceFilters. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationAccountMetricsConfigNamespaceFilters.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationAccountMetricsConfigNamespaceFilters.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 exclude_onlies: Optional[Sequence[str]] = None,
                 include_onlies: Optional[Sequence[str]] = None):
        """
        :param Sequence[str] exclude_onlies: Exclude only these namespaces from metrics collection. Use `aws_get_integration_available_namespaces` data source to get allowed values. Defaults to `["AWS/SQS", "AWS/ElasticMapReduce"]`. `AWS/SQS` and `AWS/ElasticMapReduce` are excluded by default to reduce your AWS CloudWatch costs from `GetMetricData` API calls.
        :param Sequence[str] include_onlies: Include only these namespaces for metrics collection. Use `aws_get_integration_available_namespaces` data source to get allowed values.
        """
        if exclude_onlies is not None:
            pulumi.set(__self__, "exclude_onlies", exclude_onlies)
        if include_onlies is not None:
            pulumi.set(__self__, "include_onlies", include_onlies)

    @property
    @pulumi.getter(name="excludeOnlies")
    def exclude_onlies(self) -> Optional[Sequence[str]]:
        """
        Exclude only these namespaces from metrics collection. Use `aws_get_integration_available_namespaces` data source to get allowed values. Defaults to `["AWS/SQS", "AWS/ElasticMapReduce"]`. `AWS/SQS` and `AWS/ElasticMapReduce` are excluded by default to reduce your AWS CloudWatch costs from `GetMetricData` API calls.
        """
        return pulumi.get(self, "exclude_onlies")

    @property
    @pulumi.getter(name="includeOnlies")
    def include_onlies(self) -> Optional[Sequence[str]]:
        """
        Include only these namespaces for metrics collection. Use `aws_get_integration_available_namespaces` data source to get allowed values.
        """
        return pulumi.get(self, "include_onlies")


@pulumi.output_type
class IntegrationAccountMetricsConfigTagFilter(dict):
    def __init__(__self__, *,
                 namespace: str,
                 tags: Optional[Sequence[str]] = None):
        """
        :param str namespace: The AWS service for which the tag filters defined in `tags` will be applied.
        :param Sequence[str] tags: The AWS resource tags to filter on for the service specified by `namespace`. Defaults to `[]`.
        """
        pulumi.set(__self__, "namespace", namespace)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def namespace(self) -> str:
        """
        The AWS service for which the tag filters defined in `tags` will be applied.
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence[str]]:
        """
        The AWS resource tags to filter on for the service specified by `namespace`. Defaults to `[]`.
        """
        return pulumi.get(self, "tags")


@pulumi.output_type
class IntegrationAccountResourcesConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cloudSecurityPostureManagementCollection":
            suggest = "cloud_security_posture_management_collection"
        elif key == "extendedCollection":
            suggest = "extended_collection"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationAccountResourcesConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationAccountResourcesConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationAccountResourcesConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cloud_security_posture_management_collection: Optional[bool] = None,
                 extended_collection: Optional[bool] = None):
        """
        :param bool cloud_security_posture_management_collection: Enable Cloud Security Management to scan AWS resources for vulnerabilities, misconfigurations, identity risks, and compliance violations. Requires `extended_collection` to be set to `true`. Defaults to `false`.
        :param bool extended_collection: Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for `cloud_security_posture_management_collection`. Defaults to `true`.
        """
        if cloud_security_posture_management_collection is not None:
            pulumi.set(__self__, "cloud_security_posture_management_collection", cloud_security_posture_management_collection)
        if extended_collection is not None:
            pulumi.set(__self__, "extended_collection", extended_collection)

    @property
    @pulumi.getter(name="cloudSecurityPostureManagementCollection")
    def cloud_security_posture_management_collection(self) -> Optional[bool]:
        """
        Enable Cloud Security Management to scan AWS resources for vulnerabilities, misconfigurations, identity risks, and compliance violations. Requires `extended_collection` to be set to `true`. Defaults to `false`.
        """
        return pulumi.get(self, "cloud_security_posture_management_collection")

    @property
    @pulumi.getter(name="extendedCollection")
    def extended_collection(self) -> Optional[bool]:
        """
        Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for `cloud_security_posture_management_collection`. Defaults to `true`.
        """
        return pulumi.get(self, "extended_collection")


@pulumi.output_type
class IntegrationAccountTracesConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "xrayServices":
            suggest = "xray_services"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationAccountTracesConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationAccountTracesConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationAccountTracesConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 xray_services: Optional['outputs.IntegrationAccountTracesConfigXrayServices'] = None):
        """
        :param 'IntegrationAccountTracesConfigXrayServicesArgs' xray_services: AWS X-Ray services to collect traces from. Defaults to `include_only`.
        """
        if xray_services is not None:
            pulumi.set(__self__, "xray_services", xray_services)

    @property
    @pulumi.getter(name="xrayServices")
    def xray_services(self) -> Optional['outputs.IntegrationAccountTracesConfigXrayServices']:
        """
        AWS X-Ray services to collect traces from. Defaults to `include_only`.
        """
        return pulumi.get(self, "xray_services")


@pulumi.output_type
class IntegrationAccountTracesConfigXrayServices(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "includeAll":
            suggest = "include_all"
        elif key == "includeOnlies":
            suggest = "include_onlies"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IntegrationAccountTracesConfigXrayServices. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IntegrationAccountTracesConfigXrayServices.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IntegrationAccountTracesConfigXrayServices.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 include_all: Optional[bool] = None,
                 include_onlies: Optional[Sequence[str]] = None):
        """
        :param bool include_all: Include all services.
        :param Sequence[str] include_onlies: Include only these services. Defaults to `[]`.
        """
        if include_all is not None:
            pulumi.set(__self__, "include_all", include_all)
        if include_onlies is not None:
            pulumi.set(__self__, "include_onlies", include_onlies)

    @property
    @pulumi.getter(name="includeAll")
    def include_all(self) -> Optional[bool]:
        """
        Include all services.
        """
        return pulumi.get(self, "include_all")

    @property
    @pulumi.getter(name="includeOnlies")
    def include_onlies(self) -> Optional[Sequence[str]]:
        """
        Include only these services. Defaults to `[]`.
        """
        return pulumi.get(self, "include_onlies")


@pulumi.output_type
class GetIntegrationLogsServicesAwsLogsServiceResult(dict):
    def __init__(__self__, *,
                 id: str,
                 label: str):
        """
        :param str id: The id of the AWS log service.
        :param str label: The name of the AWS log service.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "label", label)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The id of the AWS log service.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def label(self) -> str:
        """
        The name of the AWS log service.
        """
        return pulumi.get(self, "label")


