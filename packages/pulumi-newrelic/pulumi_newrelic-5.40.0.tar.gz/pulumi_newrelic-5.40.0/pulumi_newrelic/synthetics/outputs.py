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
    'BrokenLinksMonitorTag',
    'CertCheckMonitorTag',
    'MonitorCustomHeader',
    'MonitorTag',
    'MultiLocationAlertConditionCritical',
    'MultiLocationAlertConditionWarning',
    'ScriptMonitorLocationPrivate',
    'ScriptMonitorTag',
    'StepMonitorLocationPrivate',
    'StepMonitorStep',
    'StepMonitorTag',
]

@pulumi.output_type
class BrokenLinksMonitorTag(dict):
    def __init__(__self__, *,
                 key: str,
                 values: Sequence[str]):
        """
        :param str key: Name of the tag key.
        :param Sequence[str] values: Values associated with the tag key.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Name of the tag key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        Values associated with the tag key.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class CertCheckMonitorTag(dict):
    def __init__(__self__, *,
                 key: str,
                 values: Sequence[str]):
        """
        :param str key: Name of the tag key.
        :param Sequence[str] values: Values associated with the tag key.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Name of the tag key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        Values associated with the tag key.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class MonitorCustomHeader(dict):
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 value: Optional[str] = None):
        """
        :param str name: Header name.
        :param str value: Header Value.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Header name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        Header Value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class MonitorTag(dict):
    def __init__(__self__, *,
                 key: str,
                 values: Sequence[str]):
        """
        :param str key: Name of the tag key.
        :param Sequence[str] values: Values associated with the tag key.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Name of the tag key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        Values associated with the tag key.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class MultiLocationAlertConditionCritical(dict):
    def __init__(__self__, *,
                 threshold: int):
        """
        :param int threshold: The minimum number of monitor locations that must be concurrently failing before an incident is opened.
        """
        pulumi.set(__self__, "threshold", threshold)

    @property
    @pulumi.getter
    def threshold(self) -> int:
        """
        The minimum number of monitor locations that must be concurrently failing before an incident is opened.
        """
        return pulumi.get(self, "threshold")


@pulumi.output_type
class MultiLocationAlertConditionWarning(dict):
    def __init__(__self__, *,
                 threshold: int):
        """
        :param int threshold: The minimum number of monitor locations that must be concurrently failing before an incident is opened.
        """
        pulumi.set(__self__, "threshold", threshold)

    @property
    @pulumi.getter
    def threshold(self) -> int:
        """
        The minimum number of monitor locations that must be concurrently failing before an incident is opened.
        """
        return pulumi.get(self, "threshold")


@pulumi.output_type
class ScriptMonitorLocationPrivate(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "vsePassword":
            suggest = "vse_password"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScriptMonitorLocationPrivate. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScriptMonitorLocationPrivate.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScriptMonitorLocationPrivate.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 guid: str,
                 vse_password: Optional[str] = None):
        """
        :param str guid: The unique identifier for the Synthetics private location in New Relic.
        :param str vse_password: The location's Verified Script Execution password, Only necessary if Verified Script Execution is enabled for the location.
        """
        pulumi.set(__self__, "guid", guid)
        if vse_password is not None:
            pulumi.set(__self__, "vse_password", vse_password)

    @property
    @pulumi.getter
    def guid(self) -> str:
        """
        The unique identifier for the Synthetics private location in New Relic.
        """
        return pulumi.get(self, "guid")

    @property
    @pulumi.getter(name="vsePassword")
    def vse_password(self) -> Optional[str]:
        """
        The location's Verified Script Execution password, Only necessary if Verified Script Execution is enabled for the location.
        """
        return pulumi.get(self, "vse_password")


@pulumi.output_type
class ScriptMonitorTag(dict):
    def __init__(__self__, *,
                 key: str,
                 values: Sequence[str]):
        """
        :param str key: Name of the tag key.
        :param Sequence[str] values: Values associated with the tag key.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Name of the tag key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        Values associated with the tag key.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class StepMonitorLocationPrivate(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "vsePassword":
            suggest = "vse_password"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StepMonitorLocationPrivate. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StepMonitorLocationPrivate.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StepMonitorLocationPrivate.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 guid: str,
                 vse_password: Optional[str] = None):
        """
        :param str guid: The unique identifier for the Synthetics private location in New Relic.
        :param str vse_password: The location's Verified Script Execution password, only necessary if Verified Script Execution is enabled for the location.
        """
        pulumi.set(__self__, "guid", guid)
        if vse_password is not None:
            pulumi.set(__self__, "vse_password", vse_password)

    @property
    @pulumi.getter
    def guid(self) -> str:
        """
        The unique identifier for the Synthetics private location in New Relic.
        """
        return pulumi.get(self, "guid")

    @property
    @pulumi.getter(name="vsePassword")
    def vse_password(self) -> Optional[str]:
        """
        The location's Verified Script Execution password, only necessary if Verified Script Execution is enabled for the location.
        """
        return pulumi.get(self, "vse_password")


@pulumi.output_type
class StepMonitorStep(dict):
    def __init__(__self__, *,
                 ordinal: int,
                 type: str,
                 values: Optional[Sequence[str]] = None):
        """
        :param int ordinal: The position of the step within the script ranging from 0-100.
        :param str type: Name of the tag key. Valid values are `ASSERT_ELEMENT`, `ASSERT_MODAL`, `ASSERT_TEXT`, `ASSERT_TITLE`, `CLICK_ELEMENT`, `DISMISS_MODAL`, `DOUBLE_CLICK_ELEMENT`, `HOVER_ELEMENT`, `NAVIGATE`, `SECURE_TEXT_ENTRY`, `SELECT_ELEMENT`, `TEXT_ENTRY`.
        :param Sequence[str] values: The metadata values related to the step.
        """
        pulumi.set(__self__, "ordinal", ordinal)
        pulumi.set(__self__, "type", type)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def ordinal(self) -> int:
        """
        The position of the step within the script ranging from 0-100.
        """
        return pulumi.get(self, "ordinal")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Name of the tag key. Valid values are `ASSERT_ELEMENT`, `ASSERT_MODAL`, `ASSERT_TEXT`, `ASSERT_TITLE`, `CLICK_ELEMENT`, `DISMISS_MODAL`, `DOUBLE_CLICK_ELEMENT`, `HOVER_ELEMENT`, `NAVIGATE`, `SECURE_TEXT_ENTRY`, `SELECT_ELEMENT`, `TEXT_ENTRY`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        The metadata values related to the step.
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class StepMonitorTag(dict):
    def __init__(__self__, *,
                 key: str,
                 values: Sequence[str]):
        """
        :param str key: Name of the tag key.
        :param Sequence[str] values: Values associated with the tag key.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Name of the tag key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        Values associated with the tag key.
        """
        return pulumi.get(self, "values")


