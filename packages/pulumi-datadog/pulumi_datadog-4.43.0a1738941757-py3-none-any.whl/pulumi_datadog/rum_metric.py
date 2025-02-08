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
from . import outputs
from ._inputs import *

__all__ = ['RumMetricArgs', 'RumMetric']

@pulumi.input_type
class RumMetricArgs:
    def __init__(__self__, *,
                 event_type: pulumi.Input[str],
                 name: pulumi.Input[str],
                 compute: Optional[pulumi.Input['RumMetricComputeArgs']] = None,
                 filter: Optional[pulumi.Input['RumMetricFilterArgs']] = None,
                 group_bies: Optional[pulumi.Input[Sequence[pulumi.Input['RumMetricGroupByArgs']]]] = None,
                 uniqueness: Optional[pulumi.Input['RumMetricUniquenessArgs']] = None):
        """
        The set of arguments for constructing a RumMetric resource.
        :param pulumi.Input[str] event_type: The type of RUM events to filter on.
        :param pulumi.Input[str] name: The name of the RUM-based metric. This field can't be updated after creation.
        """
        pulumi.set(__self__, "event_type", event_type)
        pulumi.set(__self__, "name", name)
        if compute is not None:
            pulumi.set(__self__, "compute", compute)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if group_bies is not None:
            pulumi.set(__self__, "group_bies", group_bies)
        if uniqueness is not None:
            pulumi.set(__self__, "uniqueness", uniqueness)

    @property
    @pulumi.getter(name="eventType")
    def event_type(self) -> pulumi.Input[str]:
        """
        The type of RUM events to filter on.
        """
        return pulumi.get(self, "event_type")

    @event_type.setter
    def event_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "event_type", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the RUM-based metric. This field can't be updated after creation.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def compute(self) -> Optional[pulumi.Input['RumMetricComputeArgs']]:
        return pulumi.get(self, "compute")

    @compute.setter
    def compute(self, value: Optional[pulumi.Input['RumMetricComputeArgs']]):
        pulumi.set(self, "compute", value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['RumMetricFilterArgs']]:
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['RumMetricFilterArgs']]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter(name="groupBies")
    def group_bies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RumMetricGroupByArgs']]]]:
        return pulumi.get(self, "group_bies")

    @group_bies.setter
    def group_bies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RumMetricGroupByArgs']]]]):
        pulumi.set(self, "group_bies", value)

    @property
    @pulumi.getter
    def uniqueness(self) -> Optional[pulumi.Input['RumMetricUniquenessArgs']]:
        return pulumi.get(self, "uniqueness")

    @uniqueness.setter
    def uniqueness(self, value: Optional[pulumi.Input['RumMetricUniquenessArgs']]):
        pulumi.set(self, "uniqueness", value)


@pulumi.input_type
class _RumMetricState:
    def __init__(__self__, *,
                 compute: Optional[pulumi.Input['RumMetricComputeArgs']] = None,
                 event_type: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input['RumMetricFilterArgs']] = None,
                 group_bies: Optional[pulumi.Input[Sequence[pulumi.Input['RumMetricGroupByArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 uniqueness: Optional[pulumi.Input['RumMetricUniquenessArgs']] = None):
        """
        Input properties used for looking up and filtering RumMetric resources.
        :param pulumi.Input[str] event_type: The type of RUM events to filter on.
        :param pulumi.Input[str] name: The name of the RUM-based metric. This field can't be updated after creation.
        """
        if compute is not None:
            pulumi.set(__self__, "compute", compute)
        if event_type is not None:
            pulumi.set(__self__, "event_type", event_type)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if group_bies is not None:
            pulumi.set(__self__, "group_bies", group_bies)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if uniqueness is not None:
            pulumi.set(__self__, "uniqueness", uniqueness)

    @property
    @pulumi.getter
    def compute(self) -> Optional[pulumi.Input['RumMetricComputeArgs']]:
        return pulumi.get(self, "compute")

    @compute.setter
    def compute(self, value: Optional[pulumi.Input['RumMetricComputeArgs']]):
        pulumi.set(self, "compute", value)

    @property
    @pulumi.getter(name="eventType")
    def event_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of RUM events to filter on.
        """
        return pulumi.get(self, "event_type")

    @event_type.setter
    def event_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_type", value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['RumMetricFilterArgs']]:
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['RumMetricFilterArgs']]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter(name="groupBies")
    def group_bies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RumMetricGroupByArgs']]]]:
        return pulumi.get(self, "group_bies")

    @group_bies.setter
    def group_bies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RumMetricGroupByArgs']]]]):
        pulumi.set(self, "group_bies", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the RUM-based metric. This field can't be updated after creation.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def uniqueness(self) -> Optional[pulumi.Input['RumMetricUniquenessArgs']]:
        return pulumi.get(self, "uniqueness")

    @uniqueness.setter
    def uniqueness(self, value: Optional[pulumi.Input['RumMetricUniquenessArgs']]):
        pulumi.set(self, "uniqueness", value)


class RumMetric(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compute: Optional[pulumi.Input[Union['RumMetricComputeArgs', 'RumMetricComputeArgsDict']]] = None,
                 event_type: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[Union['RumMetricFilterArgs', 'RumMetricFilterArgsDict']]] = None,
                 group_bies: Optional[pulumi.Input[Sequence[pulumi.Input[Union['RumMetricGroupByArgs', 'RumMetricGroupByArgsDict']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 uniqueness: Optional[pulumi.Input[Union['RumMetricUniquenessArgs', 'RumMetricUniquenessArgsDict']]] = None,
                 __props__=None):
        """
        Provides a Datadog RumMetric resource. This can be used to create and manage Datadog rum_metric.

        ## Import

        ```sh
        $ pulumi import datadog:index/rumMetric:RumMetric testing_rum_metric "testing.rum.metric"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] event_type: The type of RUM events to filter on.
        :param pulumi.Input[str] name: The name of the RUM-based metric. This field can't be updated after creation.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RumMetricArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog RumMetric resource. This can be used to create and manage Datadog rum_metric.

        ## Import

        ```sh
        $ pulumi import datadog:index/rumMetric:RumMetric testing_rum_metric "testing.rum.metric"
        ```

        :param str resource_name: The name of the resource.
        :param RumMetricArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RumMetricArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compute: Optional[pulumi.Input[Union['RumMetricComputeArgs', 'RumMetricComputeArgsDict']]] = None,
                 event_type: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[Union['RumMetricFilterArgs', 'RumMetricFilterArgsDict']]] = None,
                 group_bies: Optional[pulumi.Input[Sequence[pulumi.Input[Union['RumMetricGroupByArgs', 'RumMetricGroupByArgsDict']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 uniqueness: Optional[pulumi.Input[Union['RumMetricUniquenessArgs', 'RumMetricUniquenessArgsDict']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RumMetricArgs.__new__(RumMetricArgs)

            __props__.__dict__["compute"] = compute
            if event_type is None and not opts.urn:
                raise TypeError("Missing required property 'event_type'")
            __props__.__dict__["event_type"] = event_type
            __props__.__dict__["filter"] = filter
            __props__.__dict__["group_bies"] = group_bies
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            __props__.__dict__["uniqueness"] = uniqueness
        super(RumMetric, __self__).__init__(
            'datadog:index/rumMetric:RumMetric',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            compute: Optional[pulumi.Input[Union['RumMetricComputeArgs', 'RumMetricComputeArgsDict']]] = None,
            event_type: Optional[pulumi.Input[str]] = None,
            filter: Optional[pulumi.Input[Union['RumMetricFilterArgs', 'RumMetricFilterArgsDict']]] = None,
            group_bies: Optional[pulumi.Input[Sequence[pulumi.Input[Union['RumMetricGroupByArgs', 'RumMetricGroupByArgsDict']]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            uniqueness: Optional[pulumi.Input[Union['RumMetricUniquenessArgs', 'RumMetricUniquenessArgsDict']]] = None) -> 'RumMetric':
        """
        Get an existing RumMetric resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] event_type: The type of RUM events to filter on.
        :param pulumi.Input[str] name: The name of the RUM-based metric. This field can't be updated after creation.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RumMetricState.__new__(_RumMetricState)

        __props__.__dict__["compute"] = compute
        __props__.__dict__["event_type"] = event_type
        __props__.__dict__["filter"] = filter
        __props__.__dict__["group_bies"] = group_bies
        __props__.__dict__["name"] = name
        __props__.__dict__["uniqueness"] = uniqueness
        return RumMetric(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def compute(self) -> pulumi.Output[Optional['outputs.RumMetricCompute']]:
        return pulumi.get(self, "compute")

    @property
    @pulumi.getter(name="eventType")
    def event_type(self) -> pulumi.Output[str]:
        """
        The type of RUM events to filter on.
        """
        return pulumi.get(self, "event_type")

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Output[Optional['outputs.RumMetricFilter']]:
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter(name="groupBies")
    def group_bies(self) -> pulumi.Output[Optional[Sequence['outputs.RumMetricGroupBy']]]:
        return pulumi.get(self, "group_bies")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the RUM-based metric. This field can't be updated after creation.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def uniqueness(self) -> pulumi.Output[Optional['outputs.RumMetricUniqueness']]:
        return pulumi.get(self, "uniqueness")

