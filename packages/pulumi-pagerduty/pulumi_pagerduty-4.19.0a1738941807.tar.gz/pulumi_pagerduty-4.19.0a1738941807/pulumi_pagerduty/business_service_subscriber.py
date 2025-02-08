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

__all__ = ['BusinessServiceSubscriberArgs', 'BusinessServiceSubscriber']

@pulumi.input_type
class BusinessServiceSubscriberArgs:
    def __init__(__self__, *,
                 business_service_id: pulumi.Input[str],
                 subscriber_id: pulumi.Input[str],
                 subscriber_type: pulumi.Input[str]):
        """
        The set of arguments for constructing a BusinessServiceSubscriber resource.
        :param pulumi.Input[str] business_service_id: The ID of the business service to subscribe to.
        :param pulumi.Input[str] subscriber_id: The ID of the subscriber entity.
        :param pulumi.Input[str] subscriber_type: Type of subscriber entity in the subscriber assignment. Possible values can be `user` and `team`.
        """
        pulumi.set(__self__, "business_service_id", business_service_id)
        pulumi.set(__self__, "subscriber_id", subscriber_id)
        pulumi.set(__self__, "subscriber_type", subscriber_type)

    @property
    @pulumi.getter(name="businessServiceId")
    def business_service_id(self) -> pulumi.Input[str]:
        """
        The ID of the business service to subscribe to.
        """
        return pulumi.get(self, "business_service_id")

    @business_service_id.setter
    def business_service_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "business_service_id", value)

    @property
    @pulumi.getter(name="subscriberId")
    def subscriber_id(self) -> pulumi.Input[str]:
        """
        The ID of the subscriber entity.
        """
        return pulumi.get(self, "subscriber_id")

    @subscriber_id.setter
    def subscriber_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subscriber_id", value)

    @property
    @pulumi.getter(name="subscriberType")
    def subscriber_type(self) -> pulumi.Input[str]:
        """
        Type of subscriber entity in the subscriber assignment. Possible values can be `user` and `team`.
        """
        return pulumi.get(self, "subscriber_type")

    @subscriber_type.setter
    def subscriber_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "subscriber_type", value)


@pulumi.input_type
class _BusinessServiceSubscriberState:
    def __init__(__self__, *,
                 business_service_id: Optional[pulumi.Input[str]] = None,
                 subscriber_id: Optional[pulumi.Input[str]] = None,
                 subscriber_type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BusinessServiceSubscriber resources.
        :param pulumi.Input[str] business_service_id: The ID of the business service to subscribe to.
        :param pulumi.Input[str] subscriber_id: The ID of the subscriber entity.
        :param pulumi.Input[str] subscriber_type: Type of subscriber entity in the subscriber assignment. Possible values can be `user` and `team`.
        """
        if business_service_id is not None:
            pulumi.set(__self__, "business_service_id", business_service_id)
        if subscriber_id is not None:
            pulumi.set(__self__, "subscriber_id", subscriber_id)
        if subscriber_type is not None:
            pulumi.set(__self__, "subscriber_type", subscriber_type)

    @property
    @pulumi.getter(name="businessServiceId")
    def business_service_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the business service to subscribe to.
        """
        return pulumi.get(self, "business_service_id")

    @business_service_id.setter
    def business_service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "business_service_id", value)

    @property
    @pulumi.getter(name="subscriberId")
    def subscriber_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the subscriber entity.
        """
        return pulumi.get(self, "subscriber_id")

    @subscriber_id.setter
    def subscriber_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subscriber_id", value)

    @property
    @pulumi.getter(name="subscriberType")
    def subscriber_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of subscriber entity in the subscriber assignment. Possible values can be `user` and `team`.
        """
        return pulumi.get(self, "subscriber_type")

    @subscriber_type.setter
    def subscriber_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subscriber_type", value)


class BusinessServiceSubscriber(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 business_service_id: Optional[pulumi.Input[str]] = None,
                 subscriber_id: Optional[pulumi.Input[str]] = None,
                 subscriber_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A [business service subscriber](https://developer.pagerduty.com/api-reference/b3A6NDUwNDgxOQ-list-business-service-subscribers) allows you to subscribe users or teams to automatically receive updates about key business services.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_pagerduty as pagerduty

        example = pagerduty.BusinessService("example",
            name="My Web App",
            description="A very descriptive description of this business service",
            point_of_contact="PagerDuty Admin",
            team="P37RSRS")
        engteam = pagerduty.Team("engteam", name="Engineering")
        example_user = pagerduty.User("example",
            name="Earline Greenholt",
            email="125.greenholt.earline@graham.name")
        team_example = pagerduty.BusinessServiceSubscriber("team_example",
            subscriber_id=engteam.id,
            subscriber_type="team",
            business_service_id=example.id)
        user_example = pagerduty.BusinessServiceSubscriber("user_example",
            subscriber_id=example_user.id,
            subscriber_type="user",
            business_service_id=example.id)
        ```

        ## Import

        Services can be imported using the `id` using the related business service ID, the subscriber type and the subscriber ID separated by a dot, e.g.

        ```sh
        $ pulumi import pagerduty:index/businessServiceSubscriber:BusinessServiceSubscriber main PLBP09X.team.PLBP09X
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] business_service_id: The ID of the business service to subscribe to.
        :param pulumi.Input[str] subscriber_id: The ID of the subscriber entity.
        :param pulumi.Input[str] subscriber_type: Type of subscriber entity in the subscriber assignment. Possible values can be `user` and `team`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BusinessServiceSubscriberArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A [business service subscriber](https://developer.pagerduty.com/api-reference/b3A6NDUwNDgxOQ-list-business-service-subscribers) allows you to subscribe users or teams to automatically receive updates about key business services.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_pagerduty as pagerduty

        example = pagerduty.BusinessService("example",
            name="My Web App",
            description="A very descriptive description of this business service",
            point_of_contact="PagerDuty Admin",
            team="P37RSRS")
        engteam = pagerduty.Team("engteam", name="Engineering")
        example_user = pagerduty.User("example",
            name="Earline Greenholt",
            email="125.greenholt.earline@graham.name")
        team_example = pagerduty.BusinessServiceSubscriber("team_example",
            subscriber_id=engteam.id,
            subscriber_type="team",
            business_service_id=example.id)
        user_example = pagerduty.BusinessServiceSubscriber("user_example",
            subscriber_id=example_user.id,
            subscriber_type="user",
            business_service_id=example.id)
        ```

        ## Import

        Services can be imported using the `id` using the related business service ID, the subscriber type and the subscriber ID separated by a dot, e.g.

        ```sh
        $ pulumi import pagerduty:index/businessServiceSubscriber:BusinessServiceSubscriber main PLBP09X.team.PLBP09X
        ```

        :param str resource_name: The name of the resource.
        :param BusinessServiceSubscriberArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BusinessServiceSubscriberArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 business_service_id: Optional[pulumi.Input[str]] = None,
                 subscriber_id: Optional[pulumi.Input[str]] = None,
                 subscriber_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BusinessServiceSubscriberArgs.__new__(BusinessServiceSubscriberArgs)

            if business_service_id is None and not opts.urn:
                raise TypeError("Missing required property 'business_service_id'")
            __props__.__dict__["business_service_id"] = business_service_id
            if subscriber_id is None and not opts.urn:
                raise TypeError("Missing required property 'subscriber_id'")
            __props__.__dict__["subscriber_id"] = subscriber_id
            if subscriber_type is None and not opts.urn:
                raise TypeError("Missing required property 'subscriber_type'")
            __props__.__dict__["subscriber_type"] = subscriber_type
        super(BusinessServiceSubscriber, __self__).__init__(
            'pagerduty:index/businessServiceSubscriber:BusinessServiceSubscriber',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            business_service_id: Optional[pulumi.Input[str]] = None,
            subscriber_id: Optional[pulumi.Input[str]] = None,
            subscriber_type: Optional[pulumi.Input[str]] = None) -> 'BusinessServiceSubscriber':
        """
        Get an existing BusinessServiceSubscriber resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] business_service_id: The ID of the business service to subscribe to.
        :param pulumi.Input[str] subscriber_id: The ID of the subscriber entity.
        :param pulumi.Input[str] subscriber_type: Type of subscriber entity in the subscriber assignment. Possible values can be `user` and `team`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BusinessServiceSubscriberState.__new__(_BusinessServiceSubscriberState)

        __props__.__dict__["business_service_id"] = business_service_id
        __props__.__dict__["subscriber_id"] = subscriber_id
        __props__.__dict__["subscriber_type"] = subscriber_type
        return BusinessServiceSubscriber(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="businessServiceId")
    def business_service_id(self) -> pulumi.Output[str]:
        """
        The ID of the business service to subscribe to.
        """
        return pulumi.get(self, "business_service_id")

    @property
    @pulumi.getter(name="subscriberId")
    def subscriber_id(self) -> pulumi.Output[str]:
        """
        The ID of the subscriber entity.
        """
        return pulumi.get(self, "subscriber_id")

    @property
    @pulumi.getter(name="subscriberType")
    def subscriber_type(self) -> pulumi.Output[str]:
        """
        Type of subscriber entity in the subscriber assignment. Possible values can be `user` and `team`.
        """
        return pulumi.get(self, "subscriber_type")

