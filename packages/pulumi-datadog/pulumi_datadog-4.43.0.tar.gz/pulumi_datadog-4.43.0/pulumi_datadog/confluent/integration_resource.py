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

__all__ = ['IntegrationResourceArgs', 'IntegrationResource']

@pulumi.input_type
class IntegrationResourceArgs:
    def __init__(__self__, *,
                 account_id: pulumi.Input[str],
                 resource_id: pulumi.Input[str],
                 enable_custom_metrics: Optional[pulumi.Input[bool]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a IntegrationResource resource.
        :param pulumi.Input[str] account_id: Confluent Account ID.
        :param pulumi.Input[str] resource_id: The ID associated with a Confluent resource.
        :param pulumi.Input[bool] enable_custom_metrics: Enable the `custom.consumer_lag_offset` metric, which contains extra metric tags. Defaults to `false`.
        :param pulumi.Input[str] resource_type: The resource type of the Resource. Can be `kafka`, `connector`, `ksql`, or `schema_registry`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of strings representing tags. Can be a single key, or key-value pairs separated by a colon.
        """
        pulumi.set(__self__, "account_id", account_id)
        pulumi.set(__self__, "resource_id", resource_id)
        if enable_custom_metrics is not None:
            pulumi.set(__self__, "enable_custom_metrics", enable_custom_metrics)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Input[str]:
        """
        Confluent Account ID.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Input[str]:
        """
        The ID associated with a Confluent resource.
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_id", value)

    @property
    @pulumi.getter(name="enableCustomMetrics")
    def enable_custom_metrics(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable the `custom.consumer_lag_offset` metric, which contains extra metric tags. Defaults to `false`.
        """
        return pulumi.get(self, "enable_custom_metrics")

    @enable_custom_metrics.setter
    def enable_custom_metrics(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_custom_metrics", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        The resource type of the Resource. Can be `kafka`, `connector`, `ksql`, or `schema_registry`.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of strings representing tags. Can be a single key, or key-value pairs separated by a colon.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _IntegrationResourceState:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[str]] = None,
                 enable_custom_metrics: Optional[pulumi.Input[bool]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering IntegrationResource resources.
        :param pulumi.Input[str] account_id: Confluent Account ID.
        :param pulumi.Input[bool] enable_custom_metrics: Enable the `custom.consumer_lag_offset` metric, which contains extra metric tags. Defaults to `false`.
        :param pulumi.Input[str] resource_id: The ID associated with a Confluent resource.
        :param pulumi.Input[str] resource_type: The resource type of the Resource. Can be `kafka`, `connector`, `ksql`, or `schema_registry`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of strings representing tags. Can be a single key, or key-value pairs separated by a colon.
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if enable_custom_metrics is not None:
            pulumi.set(__self__, "enable_custom_metrics", enable_custom_metrics)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        Confluent Account ID.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="enableCustomMetrics")
    def enable_custom_metrics(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable the `custom.consumer_lag_offset` metric, which contains extra metric tags. Defaults to `false`.
        """
        return pulumi.get(self, "enable_custom_metrics")

    @enable_custom_metrics.setter
    def enable_custom_metrics(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_custom_metrics", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID associated with a Confluent resource.
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        The resource type of the Resource. Can be `kafka`, `connector`, `ksql`, or `schema_registry`.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of strings representing tags. Can be a single key, or key-value pairs separated by a colon.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class IntegrationResource(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 enable_custom_metrics: Optional[pulumi.Input[bool]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a Datadog IntegrationConfluentResource resource. This can be used to create and manage Datadog integration_confluent_resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        foo = datadog.confluent.IntegrationAccount("foo",
            api_key="TESTAPIKEY123",
            api_secret="test-api-secret-123",
            tags=[
                "mytag",
                "mytag2:myvalue",
            ])
        # Create new integration_confluent_resource resource
        foo_integration_resource = datadog.confluent.IntegrationResource("foo",
            account_id=foo.id,
            resource_id="123456",
            resource_type="kafka",
            tags=[
                "mytag",
                "mytag2:myvalue",
            ])
        ```

        ## Import

        ```sh
        $ pulumi import datadog:confluent/integrationResource:IntegrationResource new_list "confluent_account_id:confluent_resource_id"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: Confluent Account ID.
        :param pulumi.Input[bool] enable_custom_metrics: Enable the `custom.consumer_lag_offset` metric, which contains extra metric tags. Defaults to `false`.
        :param pulumi.Input[str] resource_id: The ID associated with a Confluent resource.
        :param pulumi.Input[str] resource_type: The resource type of the Resource. Can be `kafka`, `connector`, `ksql`, or `schema_registry`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of strings representing tags. Can be a single key, or key-value pairs separated by a colon.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IntegrationResourceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog IntegrationConfluentResource resource. This can be used to create and manage Datadog integration_confluent_resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        foo = datadog.confluent.IntegrationAccount("foo",
            api_key="TESTAPIKEY123",
            api_secret="test-api-secret-123",
            tags=[
                "mytag",
                "mytag2:myvalue",
            ])
        # Create new integration_confluent_resource resource
        foo_integration_resource = datadog.confluent.IntegrationResource("foo",
            account_id=foo.id,
            resource_id="123456",
            resource_type="kafka",
            tags=[
                "mytag",
                "mytag2:myvalue",
            ])
        ```

        ## Import

        ```sh
        $ pulumi import datadog:confluent/integrationResource:IntegrationResource new_list "confluent_account_id:confluent_resource_id"
        ```

        :param str resource_name: The name of the resource.
        :param IntegrationResourceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IntegrationResourceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 enable_custom_metrics: Optional[pulumi.Input[bool]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IntegrationResourceArgs.__new__(IntegrationResourceArgs)

            if account_id is None and not opts.urn:
                raise TypeError("Missing required property 'account_id'")
            __props__.__dict__["account_id"] = account_id
            __props__.__dict__["enable_custom_metrics"] = enable_custom_metrics
            if resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'resource_id'")
            __props__.__dict__["resource_id"] = resource_id
            __props__.__dict__["resource_type"] = resource_type
            __props__.__dict__["tags"] = tags
        super(IntegrationResource, __self__).__init__(
            'datadog:confluent/integrationResource:IntegrationResource',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_id: Optional[pulumi.Input[str]] = None,
            enable_custom_metrics: Optional[pulumi.Input[bool]] = None,
            resource_id: Optional[pulumi.Input[str]] = None,
            resource_type: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'IntegrationResource':
        """
        Get an existing IntegrationResource resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: Confluent Account ID.
        :param pulumi.Input[bool] enable_custom_metrics: Enable the `custom.consumer_lag_offset` metric, which contains extra metric tags. Defaults to `false`.
        :param pulumi.Input[str] resource_id: The ID associated with a Confluent resource.
        :param pulumi.Input[str] resource_type: The resource type of the Resource. Can be `kafka`, `connector`, `ksql`, or `schema_registry`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of strings representing tags. Can be a single key, or key-value pairs separated by a colon.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IntegrationResourceState.__new__(_IntegrationResourceState)

        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["enable_custom_metrics"] = enable_custom_metrics
        __props__.__dict__["resource_id"] = resource_id
        __props__.__dict__["resource_type"] = resource_type
        __props__.__dict__["tags"] = tags
        return IntegrationResource(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        Confluent Account ID.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="enableCustomMetrics")
    def enable_custom_metrics(self) -> pulumi.Output[bool]:
        """
        Enable the `custom.consumer_lag_offset` metric, which contains extra metric tags. Defaults to `false`.
        """
        return pulumi.get(self, "enable_custom_metrics")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Output[str]:
        """
        The ID associated with a Confluent resource.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Output[Optional[str]]:
        """
        The resource type of the Resource. Can be `kafka`, `connector`, `ksql`, or `schema_registry`.
        """
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of strings representing tags. Can be a single key, or key-value pairs separated by a colon.
        """
        return pulumi.get(self, "tags")

