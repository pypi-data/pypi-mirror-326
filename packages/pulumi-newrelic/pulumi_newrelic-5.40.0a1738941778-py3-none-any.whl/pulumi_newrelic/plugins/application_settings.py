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

__all__ = ['ApplicationSettingsArgs', 'ApplicationSettings']

@pulumi.input_type
class ApplicationSettingsArgs:
    def __init__(__self__, *,
                 app_apdex_threshold: pulumi.Input[float],
                 enable_real_user_monitoring: pulumi.Input[bool],
                 end_user_apdex_threshold: pulumi.Input[float],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ApplicationSettings resource.
        :param pulumi.Input[float] app_apdex_threshold: The apdex threshold for the New Relic application.
        :param pulumi.Input[bool] enable_real_user_monitoring: Enable or disable real user monitoring for the New Relic application.
               
               ```
               Warning: This resource will use the account ID linked to your API key. At the moment it is not possible to dynamically set the account ID.
               ```
        :param pulumi.Input[float] end_user_apdex_threshold: The user's apdex threshold for the New Relic application.
        :param pulumi.Input[str] name: The name of the application in New Relic APM.
        """
        pulumi.set(__self__, "app_apdex_threshold", app_apdex_threshold)
        pulumi.set(__self__, "enable_real_user_monitoring", enable_real_user_monitoring)
        pulumi.set(__self__, "end_user_apdex_threshold", end_user_apdex_threshold)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="appApdexThreshold")
    def app_apdex_threshold(self) -> pulumi.Input[float]:
        """
        The apdex threshold for the New Relic application.
        """
        return pulumi.get(self, "app_apdex_threshold")

    @app_apdex_threshold.setter
    def app_apdex_threshold(self, value: pulumi.Input[float]):
        pulumi.set(self, "app_apdex_threshold", value)

    @property
    @pulumi.getter(name="enableRealUserMonitoring")
    def enable_real_user_monitoring(self) -> pulumi.Input[bool]:
        """
        Enable or disable real user monitoring for the New Relic application.

        ```
        Warning: This resource will use the account ID linked to your API key. At the moment it is not possible to dynamically set the account ID.
        ```
        """
        return pulumi.get(self, "enable_real_user_monitoring")

    @enable_real_user_monitoring.setter
    def enable_real_user_monitoring(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enable_real_user_monitoring", value)

    @property
    @pulumi.getter(name="endUserApdexThreshold")
    def end_user_apdex_threshold(self) -> pulumi.Input[float]:
        """
        The user's apdex threshold for the New Relic application.
        """
        return pulumi.get(self, "end_user_apdex_threshold")

    @end_user_apdex_threshold.setter
    def end_user_apdex_threshold(self, value: pulumi.Input[float]):
        pulumi.set(self, "end_user_apdex_threshold", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the application in New Relic APM.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ApplicationSettingsState:
    def __init__(__self__, *,
                 app_apdex_threshold: Optional[pulumi.Input[float]] = None,
                 enable_real_user_monitoring: Optional[pulumi.Input[bool]] = None,
                 end_user_apdex_threshold: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ApplicationSettings resources.
        :param pulumi.Input[float] app_apdex_threshold: The apdex threshold for the New Relic application.
        :param pulumi.Input[bool] enable_real_user_monitoring: Enable or disable real user monitoring for the New Relic application.
               
               ```
               Warning: This resource will use the account ID linked to your API key. At the moment it is not possible to dynamically set the account ID.
               ```
        :param pulumi.Input[float] end_user_apdex_threshold: The user's apdex threshold for the New Relic application.
        :param pulumi.Input[str] name: The name of the application in New Relic APM.
        """
        if app_apdex_threshold is not None:
            pulumi.set(__self__, "app_apdex_threshold", app_apdex_threshold)
        if enable_real_user_monitoring is not None:
            pulumi.set(__self__, "enable_real_user_monitoring", enable_real_user_monitoring)
        if end_user_apdex_threshold is not None:
            pulumi.set(__self__, "end_user_apdex_threshold", end_user_apdex_threshold)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="appApdexThreshold")
    def app_apdex_threshold(self) -> Optional[pulumi.Input[float]]:
        """
        The apdex threshold for the New Relic application.
        """
        return pulumi.get(self, "app_apdex_threshold")

    @app_apdex_threshold.setter
    def app_apdex_threshold(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "app_apdex_threshold", value)

    @property
    @pulumi.getter(name="enableRealUserMonitoring")
    def enable_real_user_monitoring(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable or disable real user monitoring for the New Relic application.

        ```
        Warning: This resource will use the account ID linked to your API key. At the moment it is not possible to dynamically set the account ID.
        ```
        """
        return pulumi.get(self, "enable_real_user_monitoring")

    @enable_real_user_monitoring.setter
    def enable_real_user_monitoring(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_real_user_monitoring", value)

    @property
    @pulumi.getter(name="endUserApdexThreshold")
    def end_user_apdex_threshold(self) -> Optional[pulumi.Input[float]]:
        """
        The user's apdex threshold for the New Relic application.
        """
        return pulumi.get(self, "end_user_apdex_threshold")

    @end_user_apdex_threshold.setter
    def end_user_apdex_threshold(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "end_user_apdex_threshold", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the application in New Relic APM.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class ApplicationSettings(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_apdex_threshold: Optional[pulumi.Input[float]] = None,
                 enable_real_user_monitoring: Optional[pulumi.Input[bool]] = None,
                 end_user_apdex_threshold: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        > **NOTE:** Applications are not created by this resource, but are created by
        a reporting agent.

        Use this resource to manage configuration for an application that already
        exists in New Relic.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        app = newrelic.plugins.ApplicationSettings("app",
            name="my-app",
            app_apdex_threshold=0.7,
            end_user_apdex_threshold=0.8,
            enable_real_user_monitoring=False)
        ```

        ## Notes

        > **NOTE:** Applications that have reported data in the last twelve hours
        cannot be deleted.

        ## Import

        Applications can be imported using notation `application_id`, e.g.

        ```sh
        $ pulumi import newrelic:plugins/applicationSettings:ApplicationSettings main 6789012345
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] app_apdex_threshold: The apdex threshold for the New Relic application.
        :param pulumi.Input[bool] enable_real_user_monitoring: Enable or disable real user monitoring for the New Relic application.
               
               ```
               Warning: This resource will use the account ID linked to your API key. At the moment it is not possible to dynamically set the account ID.
               ```
        :param pulumi.Input[float] end_user_apdex_threshold: The user's apdex threshold for the New Relic application.
        :param pulumi.Input[str] name: The name of the application in New Relic APM.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplicationSettingsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        > **NOTE:** Applications are not created by this resource, but are created by
        a reporting agent.

        Use this resource to manage configuration for an application that already
        exists in New Relic.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        app = newrelic.plugins.ApplicationSettings("app",
            name="my-app",
            app_apdex_threshold=0.7,
            end_user_apdex_threshold=0.8,
            enable_real_user_monitoring=False)
        ```

        ## Notes

        > **NOTE:** Applications that have reported data in the last twelve hours
        cannot be deleted.

        ## Import

        Applications can be imported using notation `application_id`, e.g.

        ```sh
        $ pulumi import newrelic:plugins/applicationSettings:ApplicationSettings main 6789012345
        ```

        :param str resource_name: The name of the resource.
        :param ApplicationSettingsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationSettingsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_apdex_threshold: Optional[pulumi.Input[float]] = None,
                 enable_real_user_monitoring: Optional[pulumi.Input[bool]] = None,
                 end_user_apdex_threshold: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationSettingsArgs.__new__(ApplicationSettingsArgs)

            if app_apdex_threshold is None and not opts.urn:
                raise TypeError("Missing required property 'app_apdex_threshold'")
            __props__.__dict__["app_apdex_threshold"] = app_apdex_threshold
            if enable_real_user_monitoring is None and not opts.urn:
                raise TypeError("Missing required property 'enable_real_user_monitoring'")
            __props__.__dict__["enable_real_user_monitoring"] = enable_real_user_monitoring
            if end_user_apdex_threshold is None and not opts.urn:
                raise TypeError("Missing required property 'end_user_apdex_threshold'")
            __props__.__dict__["end_user_apdex_threshold"] = end_user_apdex_threshold
            __props__.__dict__["name"] = name
        super(ApplicationSettings, __self__).__init__(
            'newrelic:plugins/applicationSettings:ApplicationSettings',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            app_apdex_threshold: Optional[pulumi.Input[float]] = None,
            enable_real_user_monitoring: Optional[pulumi.Input[bool]] = None,
            end_user_apdex_threshold: Optional[pulumi.Input[float]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'ApplicationSettings':
        """
        Get an existing ApplicationSettings resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] app_apdex_threshold: The apdex threshold for the New Relic application.
        :param pulumi.Input[bool] enable_real_user_monitoring: Enable or disable real user monitoring for the New Relic application.
               
               ```
               Warning: This resource will use the account ID linked to your API key. At the moment it is not possible to dynamically set the account ID.
               ```
        :param pulumi.Input[float] end_user_apdex_threshold: The user's apdex threshold for the New Relic application.
        :param pulumi.Input[str] name: The name of the application in New Relic APM.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ApplicationSettingsState.__new__(_ApplicationSettingsState)

        __props__.__dict__["app_apdex_threshold"] = app_apdex_threshold
        __props__.__dict__["enable_real_user_monitoring"] = enable_real_user_monitoring
        __props__.__dict__["end_user_apdex_threshold"] = end_user_apdex_threshold
        __props__.__dict__["name"] = name
        return ApplicationSettings(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appApdexThreshold")
    def app_apdex_threshold(self) -> pulumi.Output[float]:
        """
        The apdex threshold for the New Relic application.
        """
        return pulumi.get(self, "app_apdex_threshold")

    @property
    @pulumi.getter(name="enableRealUserMonitoring")
    def enable_real_user_monitoring(self) -> pulumi.Output[bool]:
        """
        Enable or disable real user monitoring for the New Relic application.

        ```
        Warning: This resource will use the account ID linked to your API key. At the moment it is not possible to dynamically set the account ID.
        ```
        """
        return pulumi.get(self, "enable_real_user_monitoring")

    @property
    @pulumi.getter(name="endUserApdexThreshold")
    def end_user_apdex_threshold(self) -> pulumi.Output[float]:
        """
        The user's apdex threshold for the New Relic application.
        """
        return pulumi.get(self, "end_user_apdex_threshold")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the application in New Relic APM.
        """
        return pulumi.get(self, "name")

