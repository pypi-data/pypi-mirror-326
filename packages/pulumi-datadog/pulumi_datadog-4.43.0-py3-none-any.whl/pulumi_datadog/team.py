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

__all__ = ['TeamArgs', 'Team']

@pulumi.input_type
class TeamArgs:
    def __init__(__self__, *,
                 description: pulumi.Input[str],
                 handle: pulumi.Input[str],
                 name: pulumi.Input[str]):
        """
        The set of arguments for constructing a Team resource.
        :param pulumi.Input[str] description: Free-form markdown description/content for the team's homepage.
        :param pulumi.Input[str] handle: The team's identifier
        :param pulumi.Input[str] name: The name of the team.
        """
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "handle", handle)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Input[str]:
        """
        Free-form markdown description/content for the team's homepage.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: pulumi.Input[str]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def handle(self) -> pulumi.Input[str]:
        """
        The team's identifier
        """
        return pulumi.get(self, "handle")

    @handle.setter
    def handle(self, value: pulumi.Input[str]):
        pulumi.set(self, "handle", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the team.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _TeamState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 handle: Optional[pulumi.Input[str]] = None,
                 link_count: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 summary: Optional[pulumi.Input[str]] = None,
                 user_count: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Team resources.
        :param pulumi.Input[str] description: Free-form markdown description/content for the team's homepage.
        :param pulumi.Input[str] handle: The team's identifier
        :param pulumi.Input[int] link_count: The number of links belonging to the team.
        :param pulumi.Input[str] name: The name of the team.
        :param pulumi.Input[str] summary: A brief summary of the team, derived from the `description`.
        :param pulumi.Input[int] user_count: The number of users belonging to the team.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if handle is not None:
            pulumi.set(__self__, "handle", handle)
        if link_count is not None:
            pulumi.set(__self__, "link_count", link_count)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if summary is not None:
            pulumi.set(__self__, "summary", summary)
        if user_count is not None:
            pulumi.set(__self__, "user_count", user_count)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Free-form markdown description/content for the team's homepage.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def handle(self) -> Optional[pulumi.Input[str]]:
        """
        The team's identifier
        """
        return pulumi.get(self, "handle")

    @handle.setter
    def handle(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "handle", value)

    @property
    @pulumi.getter(name="linkCount")
    def link_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of links belonging to the team.
        """
        return pulumi.get(self, "link_count")

    @link_count.setter
    def link_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "link_count", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the team.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def summary(self) -> Optional[pulumi.Input[str]]:
        """
        A brief summary of the team, derived from the `description`.
        """
        return pulumi.get(self, "summary")

    @summary.setter
    def summary(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "summary", value)

    @property
    @pulumi.getter(name="userCount")
    def user_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of users belonging to the team.
        """
        return pulumi.get(self, "user_count")

    @user_count.setter
    def user_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "user_count", value)


class Team(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 handle: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Datadog Team resource. This can be used to create and manage Datadog team.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        # Create new team resource
        foo = datadog.Team("foo",
            description="Team description",
            handle="example-team",
            name="Example Team")
        ```

        ## Import

        ```sh
        $ pulumi import datadog:index/team:Team foo "bf064c56-edb0-11ed-ae91-da7ad0900002"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Free-form markdown description/content for the team's homepage.
        :param pulumi.Input[str] handle: The team's identifier
        :param pulumi.Input[str] name: The name of the team.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TeamArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog Team resource. This can be used to create and manage Datadog team.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        # Create new team resource
        foo = datadog.Team("foo",
            description="Team description",
            handle="example-team",
            name="Example Team")
        ```

        ## Import

        ```sh
        $ pulumi import datadog:index/team:Team foo "bf064c56-edb0-11ed-ae91-da7ad0900002"
        ```

        :param str resource_name: The name of the resource.
        :param TeamArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TeamArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 handle: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TeamArgs.__new__(TeamArgs)

            if description is None and not opts.urn:
                raise TypeError("Missing required property 'description'")
            __props__.__dict__["description"] = description
            if handle is None and not opts.urn:
                raise TypeError("Missing required property 'handle'")
            __props__.__dict__["handle"] = handle
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            __props__.__dict__["link_count"] = None
            __props__.__dict__["summary"] = None
            __props__.__dict__["user_count"] = None
        super(Team, __self__).__init__(
            'datadog:index/team:Team',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            handle: Optional[pulumi.Input[str]] = None,
            link_count: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None,
            summary: Optional[pulumi.Input[str]] = None,
            user_count: Optional[pulumi.Input[int]] = None) -> 'Team':
        """
        Get an existing Team resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Free-form markdown description/content for the team's homepage.
        :param pulumi.Input[str] handle: The team's identifier
        :param pulumi.Input[int] link_count: The number of links belonging to the team.
        :param pulumi.Input[str] name: The name of the team.
        :param pulumi.Input[str] summary: A brief summary of the team, derived from the `description`.
        :param pulumi.Input[int] user_count: The number of users belonging to the team.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TeamState.__new__(_TeamState)

        __props__.__dict__["description"] = description
        __props__.__dict__["handle"] = handle
        __props__.__dict__["link_count"] = link_count
        __props__.__dict__["name"] = name
        __props__.__dict__["summary"] = summary
        __props__.__dict__["user_count"] = user_count
        return Team(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Free-form markdown description/content for the team's homepage.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def handle(self) -> pulumi.Output[str]:
        """
        The team's identifier
        """
        return pulumi.get(self, "handle")

    @property
    @pulumi.getter(name="linkCount")
    def link_count(self) -> pulumi.Output[int]:
        """
        The number of links belonging to the team.
        """
        return pulumi.get(self, "link_count")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the team.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def summary(self) -> pulumi.Output[str]:
        """
        A brief summary of the team, derived from the `description`.
        """
        return pulumi.get(self, "summary")

    @property
    @pulumi.getter(name="userCount")
    def user_count(self) -> pulumi.Output[int]:
        """
        The number of users belonging to the team.
        """
        return pulumi.get(self, "user_count")

