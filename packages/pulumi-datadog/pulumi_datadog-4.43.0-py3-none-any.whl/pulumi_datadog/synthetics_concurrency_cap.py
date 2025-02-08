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
from . import _utilities

__all__ = ['SyntheticsConcurrencyCapArgs', 'SyntheticsConcurrencyCap']

@pulumi.input_type
class SyntheticsConcurrencyCapArgs:
    def __init__(__self__, *,
                 on_demand_concurrency_cap: pulumi.Input[int]):
        """
        The set of arguments for constructing a SyntheticsConcurrencyCap resource.
        :param pulumi.Input[int] on_demand_concurrency_cap: Value of the on-demand concurrency cap, customizing the number of Synthetic tests run in parallel.
        """
        pulumi.set(__self__, "on_demand_concurrency_cap", on_demand_concurrency_cap)

    @property
    @pulumi.getter(name="onDemandConcurrencyCap")
    def on_demand_concurrency_cap(self) -> pulumi.Input[int]:
        """
        Value of the on-demand concurrency cap, customizing the number of Synthetic tests run in parallel.
        """
        return pulumi.get(self, "on_demand_concurrency_cap")

    @on_demand_concurrency_cap.setter
    def on_demand_concurrency_cap(self, value: pulumi.Input[int]):
        pulumi.set(self, "on_demand_concurrency_cap", value)


@pulumi.input_type
class _SyntheticsConcurrencyCapState:
    def __init__(__self__, *,
                 on_demand_concurrency_cap: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering SyntheticsConcurrencyCap resources.
        :param pulumi.Input[int] on_demand_concurrency_cap: Value of the on-demand concurrency cap, customizing the number of Synthetic tests run in parallel.
        """
        if on_demand_concurrency_cap is not None:
            pulumi.set(__self__, "on_demand_concurrency_cap", on_demand_concurrency_cap)

    @property
    @pulumi.getter(name="onDemandConcurrencyCap")
    def on_demand_concurrency_cap(self) -> Optional[pulumi.Input[int]]:
        """
        Value of the on-demand concurrency cap, customizing the number of Synthetic tests run in parallel.
        """
        return pulumi.get(self, "on_demand_concurrency_cap")

    @on_demand_concurrency_cap.setter
    def on_demand_concurrency_cap(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "on_demand_concurrency_cap", value)


class SyntheticsConcurrencyCap(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 on_demand_concurrency_cap: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides a Datadog Synthetics On Demand Concurrency Cap API resource. This can be used to manage the Concurrency Cap for Synthetic tests.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        # Example Usage (Synthetics Concurrency Cap Configuration)
        this = datadog.SyntheticsConcurrencyCap("this", on_demand_concurrency_cap=1)
        ```

        ## Import

        The Synthetics concurrency cap can be imported. <name> can be whatever you specify in your code. Datadog does not store the name on the server.

        ```sh
        $ pulumi import datadog:index/syntheticsConcurrencyCap:SyntheticsConcurrencyCap this <name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] on_demand_concurrency_cap: Value of the on-demand concurrency cap, customizing the number of Synthetic tests run in parallel.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SyntheticsConcurrencyCapArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog Synthetics On Demand Concurrency Cap API resource. This can be used to manage the Concurrency Cap for Synthetic tests.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        # Example Usage (Synthetics Concurrency Cap Configuration)
        this = datadog.SyntheticsConcurrencyCap("this", on_demand_concurrency_cap=1)
        ```

        ## Import

        The Synthetics concurrency cap can be imported. <name> can be whatever you specify in your code. Datadog does not store the name on the server.

        ```sh
        $ pulumi import datadog:index/syntheticsConcurrencyCap:SyntheticsConcurrencyCap this <name>
        ```

        :param str resource_name: The name of the resource.
        :param SyntheticsConcurrencyCapArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SyntheticsConcurrencyCapArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 on_demand_concurrency_cap: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SyntheticsConcurrencyCapArgs.__new__(SyntheticsConcurrencyCapArgs)

            if on_demand_concurrency_cap is None and not opts.urn:
                raise TypeError("Missing required property 'on_demand_concurrency_cap'")
            __props__.__dict__["on_demand_concurrency_cap"] = on_demand_concurrency_cap
        super(SyntheticsConcurrencyCap, __self__).__init__(
            'datadog:index/syntheticsConcurrencyCap:SyntheticsConcurrencyCap',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            on_demand_concurrency_cap: Optional[pulumi.Input[int]] = None) -> 'SyntheticsConcurrencyCap':
        """
        Get an existing SyntheticsConcurrencyCap resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] on_demand_concurrency_cap: Value of the on-demand concurrency cap, customizing the number of Synthetic tests run in parallel.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SyntheticsConcurrencyCapState.__new__(_SyntheticsConcurrencyCapState)

        __props__.__dict__["on_demand_concurrency_cap"] = on_demand_concurrency_cap
        return SyntheticsConcurrencyCap(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="onDemandConcurrencyCap")
    def on_demand_concurrency_cap(self) -> pulumi.Output[int]:
        """
        Value of the on-demand concurrency cap, customizing the number of Synthetic tests run in parallel.
        """
        return pulumi.get(self, "on_demand_concurrency_cap")

