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

__all__ = ['AwsGovcloudLinkAccountArgs', 'AwsGovcloudLinkAccount']

@pulumi.input_type
class AwsGovcloudLinkAccountArgs:
    def __init__(__self__, *,
                 arn: pulumi.Input[str],
                 account_id: Optional[pulumi.Input[str]] = None,
                 metric_collection_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AwsGovcloudLinkAccount resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the IAM role.
               
               > **NOTE:** Altering the `account_id` (or) `metric_collection_mode` of an already applied `cloud.AwsGovcloudLinkAccount` resource shall trigger a recreation of the resource, instead of an update.
        :param pulumi.Input[str] account_id: The New Relic account ID to operate on. This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`, if not specified in the configuration.
        :param pulumi.Input[str] metric_collection_mode: The mode by which metric data is to be collected from the linked AWS GovCloud account. Defaults to `PULL`, if not specified in the configuration.
               - Use `PUSH` for Metric Streams and `PULL` for API Polling based metric collection respectively.
        :param pulumi.Input[str] name: The name/identifier of the AWS GovCloud - New Relic 'linked' account.
        """
        pulumi.set(__self__, "arn", arn)
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if metric_collection_mode is not None:
            pulumi.set(__self__, "metric_collection_mode", metric_collection_mode)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role.

        > **NOTE:** Altering the `account_id` (or) `metric_collection_mode` of an already applied `cloud.AwsGovcloudLinkAccount` resource shall trigger a recreation of the resource, instead of an update.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The New Relic account ID to operate on. This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`, if not specified in the configuration.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="metricCollectionMode")
    def metric_collection_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The mode by which metric data is to be collected from the linked AWS GovCloud account. Defaults to `PULL`, if not specified in the configuration.
        - Use `PUSH` for Metric Streams and `PULL` for API Polling based metric collection respectively.
        """
        return pulumi.get(self, "metric_collection_mode")

    @metric_collection_mode.setter
    def metric_collection_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_collection_mode", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name/identifier of the AWS GovCloud - New Relic 'linked' account.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _AwsGovcloudLinkAccountState:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 metric_collection_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AwsGovcloudLinkAccount resources.
        :param pulumi.Input[str] account_id: The New Relic account ID to operate on. This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`, if not specified in the configuration.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the IAM role.
               
               > **NOTE:** Altering the `account_id` (or) `metric_collection_mode` of an already applied `cloud.AwsGovcloudLinkAccount` resource shall trigger a recreation of the resource, instead of an update.
        :param pulumi.Input[str] metric_collection_mode: The mode by which metric data is to be collected from the linked AWS GovCloud account. Defaults to `PULL`, if not specified in the configuration.
               - Use `PUSH` for Metric Streams and `PULL` for API Polling based metric collection respectively.
        :param pulumi.Input[str] name: The name/identifier of the AWS GovCloud - New Relic 'linked' account.
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if metric_collection_mode is not None:
            pulumi.set(__self__, "metric_collection_mode", metric_collection_mode)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The New Relic account ID to operate on. This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`, if not specified in the configuration.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the IAM role.

        > **NOTE:** Altering the `account_id` (or) `metric_collection_mode` of an already applied `cloud.AwsGovcloudLinkAccount` resource shall trigger a recreation of the resource, instead of an update.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="metricCollectionMode")
    def metric_collection_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The mode by which metric data is to be collected from the linked AWS GovCloud account. Defaults to `PULL`, if not specified in the configuration.
        - Use `PUSH` for Metric Streams and `PULL` for API Polling based metric collection respectively.
        """
        return pulumi.get(self, "metric_collection_mode")

    @metric_collection_mode.setter
    def metric_collection_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_collection_mode", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name/identifier of the AWS GovCloud - New Relic 'linked' account.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class AwsGovcloudLinkAccount(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 metric_collection_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Use this resource to link an AWS GovCloud account to New Relic.

        ## Prerequisite

        To link an AWS GovCloud account to New Relic, you need an AWS GovCloud account. AWS GovCloud is designed to address the specific regulatory needs of United States federal, state, and local agencies, educational institutions, and their supporting ecosystem. It is an isolated AWS region designed to host sensitive data and regulated workloads in the cloud, helping customers support their US government compliance requirements.

        To pull data from AWS GovCloud, follow the [steps outlined here](https://docs.newrelic.com/docs/infrastructure/amazon-integrations/get-started/connect-aws-govcloud-new-relic).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        foo = newrelic.cloud.AwsGovcloudLinkAccount("foo",
            account_id="1234567",
            name="My New Relic - AWS GovCloud Linked Account",
            metric_collection_mode="PUSH",
            arn="arn:aws:service:region:account-id:resource-id")
        ```

        ## Import

        Linked AWS GovCloud accounts can be imported using the `id`, e.g.

        bash

        ```sh
        $ pulumi import newrelic:cloud/awsGovcloudLinkAccount:AwsGovcloudLinkAccount foo <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The New Relic account ID to operate on. This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`, if not specified in the configuration.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the IAM role.
               
               > **NOTE:** Altering the `account_id` (or) `metric_collection_mode` of an already applied `cloud.AwsGovcloudLinkAccount` resource shall trigger a recreation of the resource, instead of an update.
        :param pulumi.Input[str] metric_collection_mode: The mode by which metric data is to be collected from the linked AWS GovCloud account. Defaults to `PULL`, if not specified in the configuration.
               - Use `PUSH` for Metric Streams and `PULL` for API Polling based metric collection respectively.
        :param pulumi.Input[str] name: The name/identifier of the AWS GovCloud - New Relic 'linked' account.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AwsGovcloudLinkAccountArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Use this resource to link an AWS GovCloud account to New Relic.

        ## Prerequisite

        To link an AWS GovCloud account to New Relic, you need an AWS GovCloud account. AWS GovCloud is designed to address the specific regulatory needs of United States federal, state, and local agencies, educational institutions, and their supporting ecosystem. It is an isolated AWS region designed to host sensitive data and regulated workloads in the cloud, helping customers support their US government compliance requirements.

        To pull data from AWS GovCloud, follow the [steps outlined here](https://docs.newrelic.com/docs/infrastructure/amazon-integrations/get-started/connect-aws-govcloud-new-relic).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        foo = newrelic.cloud.AwsGovcloudLinkAccount("foo",
            account_id="1234567",
            name="My New Relic - AWS GovCloud Linked Account",
            metric_collection_mode="PUSH",
            arn="arn:aws:service:region:account-id:resource-id")
        ```

        ## Import

        Linked AWS GovCloud accounts can be imported using the `id`, e.g.

        bash

        ```sh
        $ pulumi import newrelic:cloud/awsGovcloudLinkAccount:AwsGovcloudLinkAccount foo <id>
        ```

        :param str resource_name: The name of the resource.
        :param AwsGovcloudLinkAccountArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AwsGovcloudLinkAccountArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 metric_collection_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AwsGovcloudLinkAccountArgs.__new__(AwsGovcloudLinkAccountArgs)

            __props__.__dict__["account_id"] = account_id
            if arn is None and not opts.urn:
                raise TypeError("Missing required property 'arn'")
            __props__.__dict__["arn"] = arn
            __props__.__dict__["metric_collection_mode"] = metric_collection_mode
            __props__.__dict__["name"] = name
        super(AwsGovcloudLinkAccount, __self__).__init__(
            'newrelic:cloud/awsGovcloudLinkAccount:AwsGovcloudLinkAccount',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_id: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            metric_collection_mode: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'AwsGovcloudLinkAccount':
        """
        Get an existing AwsGovcloudLinkAccount resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The New Relic account ID to operate on. This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`, if not specified in the configuration.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the IAM role.
               
               > **NOTE:** Altering the `account_id` (or) `metric_collection_mode` of an already applied `cloud.AwsGovcloudLinkAccount` resource shall trigger a recreation of the resource, instead of an update.
        :param pulumi.Input[str] metric_collection_mode: The mode by which metric data is to be collected from the linked AWS GovCloud account. Defaults to `PULL`, if not specified in the configuration.
               - Use `PUSH` for Metric Streams and `PULL` for API Polling based metric collection respectively.
        :param pulumi.Input[str] name: The name/identifier of the AWS GovCloud - New Relic 'linked' account.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AwsGovcloudLinkAccountState.__new__(_AwsGovcloudLinkAccountState)

        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["arn"] = arn
        __props__.__dict__["metric_collection_mode"] = metric_collection_mode
        __props__.__dict__["name"] = name
        return AwsGovcloudLinkAccount(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        The New Relic account ID to operate on. This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`, if not specified in the configuration.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role.

        > **NOTE:** Altering the `account_id` (or) `metric_collection_mode` of an already applied `cloud.AwsGovcloudLinkAccount` resource shall trigger a recreation of the resource, instead of an update.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="metricCollectionMode")
    def metric_collection_mode(self) -> pulumi.Output[Optional[str]]:
        """
        The mode by which metric data is to be collected from the linked AWS GovCloud account. Defaults to `PULL`, if not specified in the configuration.
        - Use `PUSH` for Metric Streams and `PULL` for API Polling based metric collection respectively.
        """
        return pulumi.get(self, "metric_collection_mode")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name/identifier of the AWS GovCloud - New Relic 'linked' account.
        """
        return pulumi.get(self, "name")

