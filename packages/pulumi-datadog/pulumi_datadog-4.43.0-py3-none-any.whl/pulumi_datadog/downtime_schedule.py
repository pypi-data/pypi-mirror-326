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

__all__ = ['DowntimeScheduleArgs', 'DowntimeSchedule']

@pulumi.input_type
class DowntimeScheduleArgs:
    def __init__(__self__, *,
                 scope: pulumi.Input[str],
                 display_timezone: Optional[pulumi.Input[str]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 monitor_identifier: Optional[pulumi.Input['DowntimeScheduleMonitorIdentifierArgs']] = None,
                 mute_first_recovery_notification: Optional[pulumi.Input[bool]] = None,
                 notify_end_states: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 notify_end_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 one_time_schedule: Optional[pulumi.Input['DowntimeScheduleOneTimeScheduleArgs']] = None,
                 recurring_schedule: Optional[pulumi.Input['DowntimeScheduleRecurringScheduleArgs']] = None):
        """
        The set of arguments for constructing a DowntimeSchedule resource.
        :param pulumi.Input[str] scope: The scope to which the downtime applies. Must follow the [common search syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/).
        :param pulumi.Input[str] display_timezone: The timezone in which to display the downtime's start and end times in Datadog applications. This is not used as an offset for scheduling.
        :param pulumi.Input[str] message: A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same `@username` notation as events.
        :param pulumi.Input[bool] mute_first_recovery_notification: If the first recovery notification during a downtime should be muted.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_end_states: States that will trigger a monitor notification when the `notify_end_types` action occurs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_end_types: Actions that will trigger a monitor notification if the downtime is in the `notify_end_types` state.
        """
        pulumi.set(__self__, "scope", scope)
        if display_timezone is not None:
            pulumi.set(__self__, "display_timezone", display_timezone)
        if message is not None:
            pulumi.set(__self__, "message", message)
        if monitor_identifier is not None:
            pulumi.set(__self__, "monitor_identifier", monitor_identifier)
        if mute_first_recovery_notification is not None:
            pulumi.set(__self__, "mute_first_recovery_notification", mute_first_recovery_notification)
        if notify_end_states is not None:
            pulumi.set(__self__, "notify_end_states", notify_end_states)
        if notify_end_types is not None:
            pulumi.set(__self__, "notify_end_types", notify_end_types)
        if one_time_schedule is not None:
            pulumi.set(__self__, "one_time_schedule", one_time_schedule)
        if recurring_schedule is not None:
            pulumi.set(__self__, "recurring_schedule", recurring_schedule)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        The scope to which the downtime applies. Must follow the [common search syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/).
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter(name="displayTimezone")
    def display_timezone(self) -> Optional[pulumi.Input[str]]:
        """
        The timezone in which to display the downtime's start and end times in Datadog applications. This is not used as an offset for scheduling.
        """
        return pulumi.get(self, "display_timezone")

    @display_timezone.setter
    def display_timezone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_timezone", value)

    @property
    @pulumi.getter
    def message(self) -> Optional[pulumi.Input[str]]:
        """
        A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same `@username` notation as events.
        """
        return pulumi.get(self, "message")

    @message.setter
    def message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message", value)

    @property
    @pulumi.getter(name="monitorIdentifier")
    def monitor_identifier(self) -> Optional[pulumi.Input['DowntimeScheduleMonitorIdentifierArgs']]:
        return pulumi.get(self, "monitor_identifier")

    @monitor_identifier.setter
    def monitor_identifier(self, value: Optional[pulumi.Input['DowntimeScheduleMonitorIdentifierArgs']]):
        pulumi.set(self, "monitor_identifier", value)

    @property
    @pulumi.getter(name="muteFirstRecoveryNotification")
    def mute_first_recovery_notification(self) -> Optional[pulumi.Input[bool]]:
        """
        If the first recovery notification during a downtime should be muted.
        """
        return pulumi.get(self, "mute_first_recovery_notification")

    @mute_first_recovery_notification.setter
    def mute_first_recovery_notification(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "mute_first_recovery_notification", value)

    @property
    @pulumi.getter(name="notifyEndStates")
    def notify_end_states(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        States that will trigger a monitor notification when the `notify_end_types` action occurs.
        """
        return pulumi.get(self, "notify_end_states")

    @notify_end_states.setter
    def notify_end_states(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "notify_end_states", value)

    @property
    @pulumi.getter(name="notifyEndTypes")
    def notify_end_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Actions that will trigger a monitor notification if the downtime is in the `notify_end_types` state.
        """
        return pulumi.get(self, "notify_end_types")

    @notify_end_types.setter
    def notify_end_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "notify_end_types", value)

    @property
    @pulumi.getter(name="oneTimeSchedule")
    def one_time_schedule(self) -> Optional[pulumi.Input['DowntimeScheduleOneTimeScheduleArgs']]:
        return pulumi.get(self, "one_time_schedule")

    @one_time_schedule.setter
    def one_time_schedule(self, value: Optional[pulumi.Input['DowntimeScheduleOneTimeScheduleArgs']]):
        pulumi.set(self, "one_time_schedule", value)

    @property
    @pulumi.getter(name="recurringSchedule")
    def recurring_schedule(self) -> Optional[pulumi.Input['DowntimeScheduleRecurringScheduleArgs']]:
        return pulumi.get(self, "recurring_schedule")

    @recurring_schedule.setter
    def recurring_schedule(self, value: Optional[pulumi.Input['DowntimeScheduleRecurringScheduleArgs']]):
        pulumi.set(self, "recurring_schedule", value)


@pulumi.input_type
class _DowntimeScheduleState:
    def __init__(__self__, *,
                 display_timezone: Optional[pulumi.Input[str]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 monitor_identifier: Optional[pulumi.Input['DowntimeScheduleMonitorIdentifierArgs']] = None,
                 mute_first_recovery_notification: Optional[pulumi.Input[bool]] = None,
                 notify_end_states: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 notify_end_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 one_time_schedule: Optional[pulumi.Input['DowntimeScheduleOneTimeScheduleArgs']] = None,
                 recurring_schedule: Optional[pulumi.Input['DowntimeScheduleRecurringScheduleArgs']] = None,
                 scope: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DowntimeSchedule resources.
        :param pulumi.Input[str] display_timezone: The timezone in which to display the downtime's start and end times in Datadog applications. This is not used as an offset for scheduling.
        :param pulumi.Input[str] message: A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same `@username` notation as events.
        :param pulumi.Input[bool] mute_first_recovery_notification: If the first recovery notification during a downtime should be muted.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_end_states: States that will trigger a monitor notification when the `notify_end_types` action occurs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_end_types: Actions that will trigger a monitor notification if the downtime is in the `notify_end_types` state.
        :param pulumi.Input[str] scope: The scope to which the downtime applies. Must follow the [common search syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/).
        """
        if display_timezone is not None:
            pulumi.set(__self__, "display_timezone", display_timezone)
        if message is not None:
            pulumi.set(__self__, "message", message)
        if monitor_identifier is not None:
            pulumi.set(__self__, "monitor_identifier", monitor_identifier)
        if mute_first_recovery_notification is not None:
            pulumi.set(__self__, "mute_first_recovery_notification", mute_first_recovery_notification)
        if notify_end_states is not None:
            pulumi.set(__self__, "notify_end_states", notify_end_states)
        if notify_end_types is not None:
            pulumi.set(__self__, "notify_end_types", notify_end_types)
        if one_time_schedule is not None:
            pulumi.set(__self__, "one_time_schedule", one_time_schedule)
        if recurring_schedule is not None:
            pulumi.set(__self__, "recurring_schedule", recurring_schedule)
        if scope is not None:
            pulumi.set(__self__, "scope", scope)

    @property
    @pulumi.getter(name="displayTimezone")
    def display_timezone(self) -> Optional[pulumi.Input[str]]:
        """
        The timezone in which to display the downtime's start and end times in Datadog applications. This is not used as an offset for scheduling.
        """
        return pulumi.get(self, "display_timezone")

    @display_timezone.setter
    def display_timezone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_timezone", value)

    @property
    @pulumi.getter
    def message(self) -> Optional[pulumi.Input[str]]:
        """
        A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same `@username` notation as events.
        """
        return pulumi.get(self, "message")

    @message.setter
    def message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message", value)

    @property
    @pulumi.getter(name="monitorIdentifier")
    def monitor_identifier(self) -> Optional[pulumi.Input['DowntimeScheduleMonitorIdentifierArgs']]:
        return pulumi.get(self, "monitor_identifier")

    @monitor_identifier.setter
    def monitor_identifier(self, value: Optional[pulumi.Input['DowntimeScheduleMonitorIdentifierArgs']]):
        pulumi.set(self, "monitor_identifier", value)

    @property
    @pulumi.getter(name="muteFirstRecoveryNotification")
    def mute_first_recovery_notification(self) -> Optional[pulumi.Input[bool]]:
        """
        If the first recovery notification during a downtime should be muted.
        """
        return pulumi.get(self, "mute_first_recovery_notification")

    @mute_first_recovery_notification.setter
    def mute_first_recovery_notification(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "mute_first_recovery_notification", value)

    @property
    @pulumi.getter(name="notifyEndStates")
    def notify_end_states(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        States that will trigger a monitor notification when the `notify_end_types` action occurs.
        """
        return pulumi.get(self, "notify_end_states")

    @notify_end_states.setter
    def notify_end_states(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "notify_end_states", value)

    @property
    @pulumi.getter(name="notifyEndTypes")
    def notify_end_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Actions that will trigger a monitor notification if the downtime is in the `notify_end_types` state.
        """
        return pulumi.get(self, "notify_end_types")

    @notify_end_types.setter
    def notify_end_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "notify_end_types", value)

    @property
    @pulumi.getter(name="oneTimeSchedule")
    def one_time_schedule(self) -> Optional[pulumi.Input['DowntimeScheduleOneTimeScheduleArgs']]:
        return pulumi.get(self, "one_time_schedule")

    @one_time_schedule.setter
    def one_time_schedule(self, value: Optional[pulumi.Input['DowntimeScheduleOneTimeScheduleArgs']]):
        pulumi.set(self, "one_time_schedule", value)

    @property
    @pulumi.getter(name="recurringSchedule")
    def recurring_schedule(self) -> Optional[pulumi.Input['DowntimeScheduleRecurringScheduleArgs']]:
        return pulumi.get(self, "recurring_schedule")

    @recurring_schedule.setter
    def recurring_schedule(self, value: Optional[pulumi.Input['DowntimeScheduleRecurringScheduleArgs']]):
        pulumi.set(self, "recurring_schedule", value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input[str]]:
        """
        The scope to which the downtime applies. Must follow the [common search syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/).
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "scope", value)


class DowntimeSchedule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_timezone: Optional[pulumi.Input[str]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 monitor_identifier: Optional[pulumi.Input[Union['DowntimeScheduleMonitorIdentifierArgs', 'DowntimeScheduleMonitorIdentifierArgsDict']]] = None,
                 mute_first_recovery_notification: Optional[pulumi.Input[bool]] = None,
                 notify_end_states: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 notify_end_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 one_time_schedule: Optional[pulumi.Input[Union['DowntimeScheduleOneTimeScheduleArgs', 'DowntimeScheduleOneTimeScheduleArgsDict']]] = None,
                 recurring_schedule: Optional[pulumi.Input[Union['DowntimeScheduleRecurringScheduleArgs', 'DowntimeScheduleRecurringScheduleArgsDict']]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Datadog DowntimeSchedule resource. This can be used to create and manage Datadog downtimes.

        ## Import

        ```sh
        $ pulumi import datadog:index/downtimeSchedule:DowntimeSchedule new_list "00e000000-0000-1234-0000-000000000000"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_timezone: The timezone in which to display the downtime's start and end times in Datadog applications. This is not used as an offset for scheduling.
        :param pulumi.Input[str] message: A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same `@username` notation as events.
        :param pulumi.Input[bool] mute_first_recovery_notification: If the first recovery notification during a downtime should be muted.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_end_states: States that will trigger a monitor notification when the `notify_end_types` action occurs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_end_types: Actions that will trigger a monitor notification if the downtime is in the `notify_end_types` state.
        :param pulumi.Input[str] scope: The scope to which the downtime applies. Must follow the [common search syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DowntimeScheduleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog DowntimeSchedule resource. This can be used to create and manage Datadog downtimes.

        ## Import

        ```sh
        $ pulumi import datadog:index/downtimeSchedule:DowntimeSchedule new_list "00e000000-0000-1234-0000-000000000000"
        ```

        :param str resource_name: The name of the resource.
        :param DowntimeScheduleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DowntimeScheduleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_timezone: Optional[pulumi.Input[str]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 monitor_identifier: Optional[pulumi.Input[Union['DowntimeScheduleMonitorIdentifierArgs', 'DowntimeScheduleMonitorIdentifierArgsDict']]] = None,
                 mute_first_recovery_notification: Optional[pulumi.Input[bool]] = None,
                 notify_end_states: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 notify_end_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 one_time_schedule: Optional[pulumi.Input[Union['DowntimeScheduleOneTimeScheduleArgs', 'DowntimeScheduleOneTimeScheduleArgsDict']]] = None,
                 recurring_schedule: Optional[pulumi.Input[Union['DowntimeScheduleRecurringScheduleArgs', 'DowntimeScheduleRecurringScheduleArgsDict']]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DowntimeScheduleArgs.__new__(DowntimeScheduleArgs)

            __props__.__dict__["display_timezone"] = display_timezone
            __props__.__dict__["message"] = message
            __props__.__dict__["monitor_identifier"] = monitor_identifier
            __props__.__dict__["mute_first_recovery_notification"] = mute_first_recovery_notification
            __props__.__dict__["notify_end_states"] = notify_end_states
            __props__.__dict__["notify_end_types"] = notify_end_types
            __props__.__dict__["one_time_schedule"] = one_time_schedule
            __props__.__dict__["recurring_schedule"] = recurring_schedule
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
        super(DowntimeSchedule, __self__).__init__(
            'datadog:index/downtimeSchedule:DowntimeSchedule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            display_timezone: Optional[pulumi.Input[str]] = None,
            message: Optional[pulumi.Input[str]] = None,
            monitor_identifier: Optional[pulumi.Input[Union['DowntimeScheduleMonitorIdentifierArgs', 'DowntimeScheduleMonitorIdentifierArgsDict']]] = None,
            mute_first_recovery_notification: Optional[pulumi.Input[bool]] = None,
            notify_end_states: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            notify_end_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            one_time_schedule: Optional[pulumi.Input[Union['DowntimeScheduleOneTimeScheduleArgs', 'DowntimeScheduleOneTimeScheduleArgsDict']]] = None,
            recurring_schedule: Optional[pulumi.Input[Union['DowntimeScheduleRecurringScheduleArgs', 'DowntimeScheduleRecurringScheduleArgsDict']]] = None,
            scope: Optional[pulumi.Input[str]] = None) -> 'DowntimeSchedule':
        """
        Get an existing DowntimeSchedule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_timezone: The timezone in which to display the downtime's start and end times in Datadog applications. This is not used as an offset for scheduling.
        :param pulumi.Input[str] message: A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same `@username` notation as events.
        :param pulumi.Input[bool] mute_first_recovery_notification: If the first recovery notification during a downtime should be muted.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_end_states: States that will trigger a monitor notification when the `notify_end_types` action occurs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_end_types: Actions that will trigger a monitor notification if the downtime is in the `notify_end_types` state.
        :param pulumi.Input[str] scope: The scope to which the downtime applies. Must follow the [common search syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DowntimeScheduleState.__new__(_DowntimeScheduleState)

        __props__.__dict__["display_timezone"] = display_timezone
        __props__.__dict__["message"] = message
        __props__.__dict__["monitor_identifier"] = monitor_identifier
        __props__.__dict__["mute_first_recovery_notification"] = mute_first_recovery_notification
        __props__.__dict__["notify_end_states"] = notify_end_states
        __props__.__dict__["notify_end_types"] = notify_end_types
        __props__.__dict__["one_time_schedule"] = one_time_schedule
        __props__.__dict__["recurring_schedule"] = recurring_schedule
        __props__.__dict__["scope"] = scope
        return DowntimeSchedule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="displayTimezone")
    def display_timezone(self) -> pulumi.Output[str]:
        """
        The timezone in which to display the downtime's start and end times in Datadog applications. This is not used as an offset for scheduling.
        """
        return pulumi.get(self, "display_timezone")

    @property
    @pulumi.getter
    def message(self) -> pulumi.Output[Optional[str]]:
        """
        A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same `@username` notation as events.
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter(name="monitorIdentifier")
    def monitor_identifier(self) -> pulumi.Output[Optional['outputs.DowntimeScheduleMonitorIdentifier']]:
        return pulumi.get(self, "monitor_identifier")

    @property
    @pulumi.getter(name="muteFirstRecoveryNotification")
    def mute_first_recovery_notification(self) -> pulumi.Output[bool]:
        """
        If the first recovery notification during a downtime should be muted.
        """
        return pulumi.get(self, "mute_first_recovery_notification")

    @property
    @pulumi.getter(name="notifyEndStates")
    def notify_end_states(self) -> pulumi.Output[Sequence[str]]:
        """
        States that will trigger a monitor notification when the `notify_end_types` action occurs.
        """
        return pulumi.get(self, "notify_end_states")

    @property
    @pulumi.getter(name="notifyEndTypes")
    def notify_end_types(self) -> pulumi.Output[Sequence[str]]:
        """
        Actions that will trigger a monitor notification if the downtime is in the `notify_end_types` state.
        """
        return pulumi.get(self, "notify_end_types")

    @property
    @pulumi.getter(name="oneTimeSchedule")
    def one_time_schedule(self) -> pulumi.Output[Optional['outputs.DowntimeScheduleOneTimeSchedule']]:
        return pulumi.get(self, "one_time_schedule")

    @property
    @pulumi.getter(name="recurringSchedule")
    def recurring_schedule(self) -> pulumi.Output[Optional['outputs.DowntimeScheduleRecurringSchedule']]:
        return pulumi.get(self, "recurring_schedule")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[str]:
        """
        The scope to which the downtime applies. Must follow the [common search syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/).
        """
        return pulumi.get(self, "scope")

