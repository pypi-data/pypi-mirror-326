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

__all__ = [
    'IntegrationAccountAuthConfigArgs',
    'IntegrationAccountAuthConfigArgsDict',
    'IntegrationAccountAuthConfigAwsAuthConfigKeysArgs',
    'IntegrationAccountAuthConfigAwsAuthConfigKeysArgsDict',
    'IntegrationAccountAuthConfigAwsAuthConfigRoleArgs',
    'IntegrationAccountAuthConfigAwsAuthConfigRoleArgsDict',
    'IntegrationAccountAwsRegionsArgs',
    'IntegrationAccountAwsRegionsArgsDict',
    'IntegrationAccountLogsConfigArgs',
    'IntegrationAccountLogsConfigArgsDict',
    'IntegrationAccountLogsConfigLambdaForwarderArgs',
    'IntegrationAccountLogsConfigLambdaForwarderArgsDict',
    'IntegrationAccountMetricsConfigArgs',
    'IntegrationAccountMetricsConfigArgsDict',
    'IntegrationAccountMetricsConfigNamespaceFiltersArgs',
    'IntegrationAccountMetricsConfigNamespaceFiltersArgsDict',
    'IntegrationAccountMetricsConfigTagFilterArgs',
    'IntegrationAccountMetricsConfigTagFilterArgsDict',
    'IntegrationAccountResourcesConfigArgs',
    'IntegrationAccountResourcesConfigArgsDict',
    'IntegrationAccountTracesConfigArgs',
    'IntegrationAccountTracesConfigArgsDict',
    'IntegrationAccountTracesConfigXrayServicesArgs',
    'IntegrationAccountTracesConfigXrayServicesArgsDict',
]

MYPY = False

if not MYPY:
    class IntegrationAccountAuthConfigArgsDict(TypedDict):
        aws_auth_config_keys: NotRequired[pulumi.Input['IntegrationAccountAuthConfigAwsAuthConfigKeysArgsDict']]
        """
        Datadog will use the provided AWS Access Key ID and Secret Access Key to authenticate to your account.
        """
        aws_auth_config_role: NotRequired[pulumi.Input['IntegrationAccountAuthConfigAwsAuthConfigRoleArgsDict']]
elif False:
    IntegrationAccountAuthConfigArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountAuthConfigArgs:
    def __init__(__self__, *,
                 aws_auth_config_keys: Optional[pulumi.Input['IntegrationAccountAuthConfigAwsAuthConfigKeysArgs']] = None,
                 aws_auth_config_role: Optional[pulumi.Input['IntegrationAccountAuthConfigAwsAuthConfigRoleArgs']] = None):
        """
        :param pulumi.Input['IntegrationAccountAuthConfigAwsAuthConfigKeysArgs'] aws_auth_config_keys: Datadog will use the provided AWS Access Key ID and Secret Access Key to authenticate to your account.
        """
        if aws_auth_config_keys is not None:
            pulumi.set(__self__, "aws_auth_config_keys", aws_auth_config_keys)
        if aws_auth_config_role is not None:
            pulumi.set(__self__, "aws_auth_config_role", aws_auth_config_role)

    @property
    @pulumi.getter(name="awsAuthConfigKeys")
    def aws_auth_config_keys(self) -> Optional[pulumi.Input['IntegrationAccountAuthConfigAwsAuthConfigKeysArgs']]:
        """
        Datadog will use the provided AWS Access Key ID and Secret Access Key to authenticate to your account.
        """
        return pulumi.get(self, "aws_auth_config_keys")

    @aws_auth_config_keys.setter
    def aws_auth_config_keys(self, value: Optional[pulumi.Input['IntegrationAccountAuthConfigAwsAuthConfigKeysArgs']]):
        pulumi.set(self, "aws_auth_config_keys", value)

    @property
    @pulumi.getter(name="awsAuthConfigRole")
    def aws_auth_config_role(self) -> Optional[pulumi.Input['IntegrationAccountAuthConfigAwsAuthConfigRoleArgs']]:
        return pulumi.get(self, "aws_auth_config_role")

    @aws_auth_config_role.setter
    def aws_auth_config_role(self, value: Optional[pulumi.Input['IntegrationAccountAuthConfigAwsAuthConfigRoleArgs']]):
        pulumi.set(self, "aws_auth_config_role", value)


if not MYPY:
    class IntegrationAccountAuthConfigAwsAuthConfigKeysArgsDict(TypedDict):
        access_key_id: NotRequired[pulumi.Input[str]]
        """
        AWS Access Key ID
        """
        secret_access_key: NotRequired[pulumi.Input[str]]
elif False:
    IntegrationAccountAuthConfigAwsAuthConfigKeysArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountAuthConfigAwsAuthConfigKeysArgs:
    def __init__(__self__, *,
                 access_key_id: Optional[pulumi.Input[str]] = None,
                 secret_access_key: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] access_key_id: AWS Access Key ID
        """
        if access_key_id is not None:
            pulumi.set(__self__, "access_key_id", access_key_id)
        if secret_access_key is not None:
            pulumi.set(__self__, "secret_access_key", secret_access_key)

    @property
    @pulumi.getter(name="accessKeyId")
    def access_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        AWS Access Key ID
        """
        return pulumi.get(self, "access_key_id")

    @access_key_id.setter
    def access_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_key_id", value)

    @property
    @pulumi.getter(name="secretAccessKey")
    def secret_access_key(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "secret_access_key")

    @secret_access_key.setter
    def secret_access_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret_access_key", value)


if not MYPY:
    class IntegrationAccountAuthConfigAwsAuthConfigRoleArgsDict(TypedDict):
        external_id: NotRequired[pulumi.Input[str]]
        """
        AWS IAM external ID for associated role. If omitted, one is generated.
        """
        role_name: NotRequired[pulumi.Input[str]]
        """
        AWS IAM role name.
        """
elif False:
    IntegrationAccountAuthConfigAwsAuthConfigRoleArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountAuthConfigAwsAuthConfigRoleArgs:
    def __init__(__self__, *,
                 external_id: Optional[pulumi.Input[str]] = None,
                 role_name: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] external_id: AWS IAM external ID for associated role. If omitted, one is generated.
        :param pulumi.Input[str] role_name: AWS IAM role name.
        """
        if external_id is not None:
            pulumi.set(__self__, "external_id", external_id)
        if role_name is not None:
            pulumi.set(__self__, "role_name", role_name)

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> Optional[pulumi.Input[str]]:
        """
        AWS IAM external ID for associated role. If omitted, one is generated.
        """
        return pulumi.get(self, "external_id")

    @external_id.setter
    def external_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "external_id", value)

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> Optional[pulumi.Input[str]]:
        """
        AWS IAM role name.
        """
        return pulumi.get(self, "role_name")

    @role_name.setter
    def role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_name", value)


if not MYPY:
    class IntegrationAccountAwsRegionsArgsDict(TypedDict):
        include_all: NotRequired[pulumi.Input[bool]]
        """
        Include all regions. Defaults to `true`.
        """
        include_onlies: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Include only these regions.
        """
elif False:
    IntegrationAccountAwsRegionsArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountAwsRegionsArgs:
    def __init__(__self__, *,
                 include_all: Optional[pulumi.Input[bool]] = None,
                 include_onlies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[bool] include_all: Include all regions. Defaults to `true`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] include_onlies: Include only these regions.
        """
        if include_all is not None:
            pulumi.set(__self__, "include_all", include_all)
        if include_onlies is not None:
            pulumi.set(__self__, "include_onlies", include_onlies)

    @property
    @pulumi.getter(name="includeAll")
    def include_all(self) -> Optional[pulumi.Input[bool]]:
        """
        Include all regions. Defaults to `true`.
        """
        return pulumi.get(self, "include_all")

    @include_all.setter
    def include_all(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_all", value)

    @property
    @pulumi.getter(name="includeOnlies")
    def include_onlies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Include only these regions.
        """
        return pulumi.get(self, "include_onlies")

    @include_onlies.setter
    def include_onlies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "include_onlies", value)


if not MYPY:
    class IntegrationAccountLogsConfigArgsDict(TypedDict):
        lambda_forwarder: NotRequired[pulumi.Input['IntegrationAccountLogsConfigLambdaForwarderArgsDict']]
        """
        Leave empty to omit logs config.
        """
elif False:
    IntegrationAccountLogsConfigArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountLogsConfigArgs:
    def __init__(__self__, *,
                 lambda_forwarder: Optional[pulumi.Input['IntegrationAccountLogsConfigLambdaForwarderArgs']] = None):
        """
        :param pulumi.Input['IntegrationAccountLogsConfigLambdaForwarderArgs'] lambda_forwarder: Leave empty to omit logs config.
        """
        if lambda_forwarder is not None:
            pulumi.set(__self__, "lambda_forwarder", lambda_forwarder)

    @property
    @pulumi.getter(name="lambdaForwarder")
    def lambda_forwarder(self) -> Optional[pulumi.Input['IntegrationAccountLogsConfigLambdaForwarderArgs']]:
        """
        Leave empty to omit logs config.
        """
        return pulumi.get(self, "lambda_forwarder")

    @lambda_forwarder.setter
    def lambda_forwarder(self, value: Optional[pulumi.Input['IntegrationAccountLogsConfigLambdaForwarderArgs']]):
        pulumi.set(self, "lambda_forwarder", value)


if not MYPY:
    class IntegrationAccountLogsConfigLambdaForwarderArgsDict(TypedDict):
        lambdas: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        List of Datadog Lambda Log Forwarder ARNs in your AWS account. Defaults to `[]`.
        """
        sources: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        List of service IDs set to enable automatic log collection. Use `aws_get_integration_available_logs_services` data source to get allowed values. Defaults to `[]`.
        """
elif False:
    IntegrationAccountLogsConfigLambdaForwarderArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountLogsConfigLambdaForwarderArgs:
    def __init__(__self__, *,
                 lambdas: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 sources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] lambdas: List of Datadog Lambda Log Forwarder ARNs in your AWS account. Defaults to `[]`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] sources: List of service IDs set to enable automatic log collection. Use `aws_get_integration_available_logs_services` data source to get allowed values. Defaults to `[]`.
        """
        if lambdas is not None:
            pulumi.set(__self__, "lambdas", lambdas)
        if sources is not None:
            pulumi.set(__self__, "sources", sources)

    @property
    @pulumi.getter
    def lambdas(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of Datadog Lambda Log Forwarder ARNs in your AWS account. Defaults to `[]`.
        """
        return pulumi.get(self, "lambdas")

    @lambdas.setter
    def lambdas(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "lambdas", value)

    @property
    @pulumi.getter
    def sources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of service IDs set to enable automatic log collection. Use `aws_get_integration_available_logs_services` data source to get allowed values. Defaults to `[]`.
        """
        return pulumi.get(self, "sources")

    @sources.setter
    def sources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "sources", value)


if not MYPY:
    class IntegrationAccountMetricsConfigArgsDict(TypedDict):
        automute_enabled: NotRequired[pulumi.Input[bool]]
        """
        Enable EC2 automute for AWS metrics Defaults to `true`.
        """
        collect_cloudwatch_alarms: NotRequired[pulumi.Input[bool]]
        """
        Enable CloudWatch alarms collection Defaults to `false`.
        """
        collect_custom_metrics: NotRequired[pulumi.Input[bool]]
        """
        Enable custom metrics collection Defaults to `false`.
        """
        enabled: NotRequired[pulumi.Input[bool]]
        """
        Enable AWS metrics collection Defaults to `true`.
        """
        namespace_filters: NotRequired[pulumi.Input['IntegrationAccountMetricsConfigNamespaceFiltersArgsDict']]
        """
        AWS metrics namespace filters. Defaults to a pre-set `exclude_only` list if block is empty.
        """
        tag_filters: NotRequired[pulumi.Input[Sequence[pulumi.Input['IntegrationAccountMetricsConfigTagFilterArgsDict']]]]
        """
        AWS Metrics Collection tag filters list. The array of custom AWS resource tags (in the form `key:value`) defines a filter that Datadog uses when collecting metrics from a specified service. Wildcards, such as `?` (match a single character) and `*` (match multiple characters), and exclusion using `!` before the tag are supported. For EC2, only hosts that match one of the defined tags will be imported into Datadog. The rest will be ignored. For example, `env:production,instance-type:c?.*,!region:us-east-1`.
        """
elif False:
    IntegrationAccountMetricsConfigArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountMetricsConfigArgs:
    def __init__(__self__, *,
                 automute_enabled: Optional[pulumi.Input[bool]] = None,
                 collect_cloudwatch_alarms: Optional[pulumi.Input[bool]] = None,
                 collect_custom_metrics: Optional[pulumi.Input[bool]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 namespace_filters: Optional[pulumi.Input['IntegrationAccountMetricsConfigNamespaceFiltersArgs']] = None,
                 tag_filters: Optional[pulumi.Input[Sequence[pulumi.Input['IntegrationAccountMetricsConfigTagFilterArgs']]]] = None):
        """
        :param pulumi.Input[bool] automute_enabled: Enable EC2 automute for AWS metrics Defaults to `true`.
        :param pulumi.Input[bool] collect_cloudwatch_alarms: Enable CloudWatch alarms collection Defaults to `false`.
        :param pulumi.Input[bool] collect_custom_metrics: Enable custom metrics collection Defaults to `false`.
        :param pulumi.Input[bool] enabled: Enable AWS metrics collection Defaults to `true`.
        :param pulumi.Input['IntegrationAccountMetricsConfigNamespaceFiltersArgs'] namespace_filters: AWS metrics namespace filters. Defaults to a pre-set `exclude_only` list if block is empty.
        :param pulumi.Input[Sequence[pulumi.Input['IntegrationAccountMetricsConfigTagFilterArgs']]] tag_filters: AWS Metrics Collection tag filters list. The array of custom AWS resource tags (in the form `key:value`) defines a filter that Datadog uses when collecting metrics from a specified service. Wildcards, such as `?` (match a single character) and `*` (match multiple characters), and exclusion using `!` before the tag are supported. For EC2, only hosts that match one of the defined tags will be imported into Datadog. The rest will be ignored. For example, `env:production,instance-type:c?.*,!region:us-east-1`.
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
    def automute_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable EC2 automute for AWS metrics Defaults to `true`.
        """
        return pulumi.get(self, "automute_enabled")

    @automute_enabled.setter
    def automute_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "automute_enabled", value)

    @property
    @pulumi.getter(name="collectCloudwatchAlarms")
    def collect_cloudwatch_alarms(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable CloudWatch alarms collection Defaults to `false`.
        """
        return pulumi.get(self, "collect_cloudwatch_alarms")

    @collect_cloudwatch_alarms.setter
    def collect_cloudwatch_alarms(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "collect_cloudwatch_alarms", value)

    @property
    @pulumi.getter(name="collectCustomMetrics")
    def collect_custom_metrics(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable custom metrics collection Defaults to `false`.
        """
        return pulumi.get(self, "collect_custom_metrics")

    @collect_custom_metrics.setter
    def collect_custom_metrics(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "collect_custom_metrics", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable AWS metrics collection Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="namespaceFilters")
    def namespace_filters(self) -> Optional[pulumi.Input['IntegrationAccountMetricsConfigNamespaceFiltersArgs']]:
        """
        AWS metrics namespace filters. Defaults to a pre-set `exclude_only` list if block is empty.
        """
        return pulumi.get(self, "namespace_filters")

    @namespace_filters.setter
    def namespace_filters(self, value: Optional[pulumi.Input['IntegrationAccountMetricsConfigNamespaceFiltersArgs']]):
        pulumi.set(self, "namespace_filters", value)

    @property
    @pulumi.getter(name="tagFilters")
    def tag_filters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IntegrationAccountMetricsConfigTagFilterArgs']]]]:
        """
        AWS Metrics Collection tag filters list. The array of custom AWS resource tags (in the form `key:value`) defines a filter that Datadog uses when collecting metrics from a specified service. Wildcards, such as `?` (match a single character) and `*` (match multiple characters), and exclusion using `!` before the tag are supported. For EC2, only hosts that match one of the defined tags will be imported into Datadog. The rest will be ignored. For example, `env:production,instance-type:c?.*,!region:us-east-1`.
        """
        return pulumi.get(self, "tag_filters")

    @tag_filters.setter
    def tag_filters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IntegrationAccountMetricsConfigTagFilterArgs']]]]):
        pulumi.set(self, "tag_filters", value)


if not MYPY:
    class IntegrationAccountMetricsConfigNamespaceFiltersArgsDict(TypedDict):
        exclude_onlies: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Exclude only these namespaces from metrics collection. Use `aws_get_integration_available_namespaces` data source to get allowed values. Defaults to `["AWS/SQS", "AWS/ElasticMapReduce"]`. `AWS/SQS` and `AWS/ElasticMapReduce` are excluded by default to reduce your AWS CloudWatch costs from `GetMetricData` API calls.
        """
        include_onlies: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Include only these namespaces for metrics collection. Use `aws_get_integration_available_namespaces` data source to get allowed values.
        """
elif False:
    IntegrationAccountMetricsConfigNamespaceFiltersArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountMetricsConfigNamespaceFiltersArgs:
    def __init__(__self__, *,
                 exclude_onlies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 include_onlies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] exclude_onlies: Exclude only these namespaces from metrics collection. Use `aws_get_integration_available_namespaces` data source to get allowed values. Defaults to `["AWS/SQS", "AWS/ElasticMapReduce"]`. `AWS/SQS` and `AWS/ElasticMapReduce` are excluded by default to reduce your AWS CloudWatch costs from `GetMetricData` API calls.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] include_onlies: Include only these namespaces for metrics collection. Use `aws_get_integration_available_namespaces` data source to get allowed values.
        """
        if exclude_onlies is not None:
            pulumi.set(__self__, "exclude_onlies", exclude_onlies)
        if include_onlies is not None:
            pulumi.set(__self__, "include_onlies", include_onlies)

    @property
    @pulumi.getter(name="excludeOnlies")
    def exclude_onlies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Exclude only these namespaces from metrics collection. Use `aws_get_integration_available_namespaces` data source to get allowed values. Defaults to `["AWS/SQS", "AWS/ElasticMapReduce"]`. `AWS/SQS` and `AWS/ElasticMapReduce` are excluded by default to reduce your AWS CloudWatch costs from `GetMetricData` API calls.
        """
        return pulumi.get(self, "exclude_onlies")

    @exclude_onlies.setter
    def exclude_onlies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "exclude_onlies", value)

    @property
    @pulumi.getter(name="includeOnlies")
    def include_onlies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Include only these namespaces for metrics collection. Use `aws_get_integration_available_namespaces` data source to get allowed values.
        """
        return pulumi.get(self, "include_onlies")

    @include_onlies.setter
    def include_onlies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "include_onlies", value)


if not MYPY:
    class IntegrationAccountMetricsConfigTagFilterArgsDict(TypedDict):
        namespace: pulumi.Input[str]
        """
        The AWS service for which the tag filters defined in `tags` will be applied.
        """
        tags: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        The AWS resource tags to filter on for the service specified by `namespace`. Defaults to `[]`.
        """
elif False:
    IntegrationAccountMetricsConfigTagFilterArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountMetricsConfigTagFilterArgs:
    def __init__(__self__, *,
                 namespace: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] namespace: The AWS service for which the tag filters defined in `tags` will be applied.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: The AWS resource tags to filter on for the service specified by `namespace`. Defaults to `[]`.
        """
        pulumi.set(__self__, "namespace", namespace)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Input[str]:
        """
        The AWS service for which the tag filters defined in `tags` will be applied.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The AWS resource tags to filter on for the service specified by `namespace`. Defaults to `[]`.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


if not MYPY:
    class IntegrationAccountResourcesConfigArgsDict(TypedDict):
        cloud_security_posture_management_collection: NotRequired[pulumi.Input[bool]]
        """
        Enable Cloud Security Management to scan AWS resources for vulnerabilities, misconfigurations, identity risks, and compliance violations. Requires `extended_collection` to be set to `true`. Defaults to `false`.
        """
        extended_collection: NotRequired[pulumi.Input[bool]]
        """
        Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for `cloud_security_posture_management_collection`. Defaults to `true`.
        """
elif False:
    IntegrationAccountResourcesConfigArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountResourcesConfigArgs:
    def __init__(__self__, *,
                 cloud_security_posture_management_collection: Optional[pulumi.Input[bool]] = None,
                 extended_collection: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[bool] cloud_security_posture_management_collection: Enable Cloud Security Management to scan AWS resources for vulnerabilities, misconfigurations, identity risks, and compliance violations. Requires `extended_collection` to be set to `true`. Defaults to `false`.
        :param pulumi.Input[bool] extended_collection: Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for `cloud_security_posture_management_collection`. Defaults to `true`.
        """
        if cloud_security_posture_management_collection is not None:
            pulumi.set(__self__, "cloud_security_posture_management_collection", cloud_security_posture_management_collection)
        if extended_collection is not None:
            pulumi.set(__self__, "extended_collection", extended_collection)

    @property
    @pulumi.getter(name="cloudSecurityPostureManagementCollection")
    def cloud_security_posture_management_collection(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable Cloud Security Management to scan AWS resources for vulnerabilities, misconfigurations, identity risks, and compliance violations. Requires `extended_collection` to be set to `true`. Defaults to `false`.
        """
        return pulumi.get(self, "cloud_security_posture_management_collection")

    @cloud_security_posture_management_collection.setter
    def cloud_security_posture_management_collection(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cloud_security_posture_management_collection", value)

    @property
    @pulumi.getter(name="extendedCollection")
    def extended_collection(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for `cloud_security_posture_management_collection`. Defaults to `true`.
        """
        return pulumi.get(self, "extended_collection")

    @extended_collection.setter
    def extended_collection(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "extended_collection", value)


if not MYPY:
    class IntegrationAccountTracesConfigArgsDict(TypedDict):
        xray_services: NotRequired[pulumi.Input['IntegrationAccountTracesConfigXrayServicesArgsDict']]
        """
        AWS X-Ray services to collect traces from. Defaults to `include_only`.
        """
elif False:
    IntegrationAccountTracesConfigArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountTracesConfigArgs:
    def __init__(__self__, *,
                 xray_services: Optional[pulumi.Input['IntegrationAccountTracesConfigXrayServicesArgs']] = None):
        """
        :param pulumi.Input['IntegrationAccountTracesConfigXrayServicesArgs'] xray_services: AWS X-Ray services to collect traces from. Defaults to `include_only`.
        """
        if xray_services is not None:
            pulumi.set(__self__, "xray_services", xray_services)

    @property
    @pulumi.getter(name="xrayServices")
    def xray_services(self) -> Optional[pulumi.Input['IntegrationAccountTracesConfigXrayServicesArgs']]:
        """
        AWS X-Ray services to collect traces from. Defaults to `include_only`.
        """
        return pulumi.get(self, "xray_services")

    @xray_services.setter
    def xray_services(self, value: Optional[pulumi.Input['IntegrationAccountTracesConfigXrayServicesArgs']]):
        pulumi.set(self, "xray_services", value)


if not MYPY:
    class IntegrationAccountTracesConfigXrayServicesArgsDict(TypedDict):
        include_all: NotRequired[pulumi.Input[bool]]
        """
        Include all services.
        """
        include_onlies: NotRequired[pulumi.Input[Sequence[pulumi.Input[str]]]]
        """
        Include only these services. Defaults to `[]`.
        """
elif False:
    IntegrationAccountTracesConfigXrayServicesArgsDict: TypeAlias = Mapping[str, Any]

@pulumi.input_type
class IntegrationAccountTracesConfigXrayServicesArgs:
    def __init__(__self__, *,
                 include_all: Optional[pulumi.Input[bool]] = None,
                 include_onlies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[bool] include_all: Include all services.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] include_onlies: Include only these services. Defaults to `[]`.
        """
        if include_all is not None:
            pulumi.set(__self__, "include_all", include_all)
        if include_onlies is not None:
            pulumi.set(__self__, "include_onlies", include_onlies)

    @property
    @pulumi.getter(name="includeAll")
    def include_all(self) -> Optional[pulumi.Input[bool]]:
        """
        Include all services.
        """
        return pulumi.get(self, "include_all")

    @include_all.setter
    def include_all(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_all", value)

    @property
    @pulumi.getter(name="includeOnlies")
    def include_onlies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Include only these services. Defaults to `[]`.
        """
        return pulumi.get(self, "include_onlies")

    @include_onlies.setter
    def include_onlies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "include_onlies", value)


