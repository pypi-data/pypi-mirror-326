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

__all__ = ['ServiceObjectArgs', 'ServiceObject']

@pulumi.input_type
class ServiceObjectArgs:
    def __init__(__self__, *,
                 service_key: pulumi.Input[str],
                 service_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a ServiceObject resource.
        :param pulumi.Input[str] service_name: Your Service name in PagerDuty.
        """
        pulumi.set(__self__, "service_key", service_key)
        pulumi.set(__self__, "service_name", service_name)

    @property
    @pulumi.getter(name="serviceKey")
    def service_key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "service_key")

    @service_key.setter
    def service_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_key", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        Your Service name in PagerDuty.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)


@pulumi.input_type
class _ServiceObjectState:
    def __init__(__self__, *,
                 service_key: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServiceObject resources.
        :param pulumi.Input[str] service_name: Your Service name in PagerDuty.
        """
        if service_key is not None:
            pulumi.set(__self__, "service_key", service_key)
        if service_name is not None:
            pulumi.set(__self__, "service_name", service_name)

    @property
    @pulumi.getter(name="serviceKey")
    def service_key(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "service_key")

    @service_key.setter
    def service_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_key", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> Optional[pulumi.Input[str]]:
        """
        Your Service name in PagerDuty.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_name", value)


class ServiceObject(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 service_key: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides access to individual Service Objects of Datadog - PagerDuty integrations. Note that the Datadog - PagerDuty integration must be activated in the Datadog UI in order for this resource to be usable.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        testing_foo = datadog.pagerduty.ServiceObject("testing_foo",
            service_name="testing_foo",
            service_key="9876543210123456789")
        testing_bar = datadog.pagerduty.ServiceObject("testing_bar",
            service_name="testing_bar",
            service_key="54321098765432109876")
        ```

        ## Import

        Pagerduty service object can be imported using the service_name, while the service_key should be passed by setting the environment variable SERVICE_KEY

        ```sh
        $ pulumi import datadog:pagerduty/serviceObject:ServiceObject SERVICE_KEY=${service_key} datadog_integration_pagerduty_service_object.foo ${service_name}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] service_name: Your Service name in PagerDuty.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceObjectArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides access to individual Service Objects of Datadog - PagerDuty integrations. Note that the Datadog - PagerDuty integration must be activated in the Datadog UI in order for this resource to be usable.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        testing_foo = datadog.pagerduty.ServiceObject("testing_foo",
            service_name="testing_foo",
            service_key="9876543210123456789")
        testing_bar = datadog.pagerduty.ServiceObject("testing_bar",
            service_name="testing_bar",
            service_key="54321098765432109876")
        ```

        ## Import

        Pagerduty service object can be imported using the service_name, while the service_key should be passed by setting the environment variable SERVICE_KEY

        ```sh
        $ pulumi import datadog:pagerduty/serviceObject:ServiceObject SERVICE_KEY=${service_key} datadog_integration_pagerduty_service_object.foo ${service_name}
        ```

        :param str resource_name: The name of the resource.
        :param ServiceObjectArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceObjectArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 service_key: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceObjectArgs.__new__(ServiceObjectArgs)

            if service_key is None and not opts.urn:
                raise TypeError("Missing required property 'service_key'")
            __props__.__dict__["service_key"] = None if service_key is None else pulumi.Output.secret(service_key)
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__["service_name"] = service_name
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["serviceKey"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(ServiceObject, __self__).__init__(
            'datadog:pagerduty/serviceObject:ServiceObject',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            service_key: Optional[pulumi.Input[str]] = None,
            service_name: Optional[pulumi.Input[str]] = None) -> 'ServiceObject':
        """
        Get an existing ServiceObject resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] service_name: Your Service name in PagerDuty.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceObjectState.__new__(_ServiceObjectState)

        __props__.__dict__["service_key"] = service_key
        __props__.__dict__["service_name"] = service_name
        return ServiceObject(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="serviceKey")
    def service_key(self) -> pulumi.Output[str]:
        return pulumi.get(self, "service_key")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Output[str]:
        """
        Your Service name in PagerDuty.
        """
        return pulumi.get(self, "service_name")

