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

__all__ = [
    'GetPowerpackResult',
    'AwaitableGetPowerpackResult',
    'get_powerpack',
    'get_powerpack_output',
]

@pulumi.output_type
class GetPowerpackResult:
    """
    A collection of values returned by getPowerpack.
    """
    def __init__(__self__, id=None, name=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of this resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Powerpack to search for.
        """
        return pulumi.get(self, "name")


class AwaitableGetPowerpackResult(GetPowerpackResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPowerpackResult(
            id=self.id,
            name=self.name)


def get_powerpack(name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPowerpackResult:
    """
    Use this data source to retrieve information about an existing Datadog Powerpack.


    :param str name: The name of the Powerpack to search for.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('datadog:index/getPowerpack:getPowerpack', __args__, opts=opts, typ=GetPowerpackResult).value

    return AwaitableGetPowerpackResult(
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'))
def get_powerpack_output(name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPowerpackResult]:
    """
    Use this data source to retrieve information about an existing Datadog Powerpack.


    :param str name: The name of the Powerpack to search for.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('datadog:index/getPowerpack:getPowerpack', __args__, opts=opts, typ=GetPowerpackResult)
    return __ret__.apply(lambda __response__: GetPowerpackResult(
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name')))
