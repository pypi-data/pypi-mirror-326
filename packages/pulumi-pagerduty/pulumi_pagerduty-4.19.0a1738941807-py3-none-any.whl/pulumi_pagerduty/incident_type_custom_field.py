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

__all__ = ['IncidentTypeCustomFieldArgs', 'IncidentTypeCustomField']

@pulumi.input_type
class IncidentTypeCustomFieldArgs:
    def __init__(__self__, *,
                 data_type: pulumi.Input[str],
                 display_name: pulumi.Input[str],
                 incident_type: pulumi.Input[str],
                 default_value: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 field_options: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 field_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a IncidentTypeCustomField resource.
        :param pulumi.Input[str] data_type: [Updating causes resource replacement] The type of the data of this custom field. Can be one of `string`, `integer`, `float`, `boolean`, `datetime`, or `url` when `data_type` is `single_value`, otherwise must be `string`. Update
        :param pulumi.Input[str] display_name: The display name of the custom Type.
        :param pulumi.Input[str] incident_type: [Updating causes resource replacement] The id of the incident type the custom field is associated with.
        :param pulumi.Input[str] default_value: The default value to set when new incidents are created. Always specified as a string.
        :param pulumi.Input[str] description: The description of the custom field.
        :param pulumi.Input[bool] enabled: Whether the custom field is enabled. Defaults to true if not provided.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] field_options: The options for the custom field. Can only be applied to fields with a type of `single_value_fixed` or `multi_value_fixed`.
        :param pulumi.Input[str] field_type: [Updating causes resource replacement] The field type of the field. Must be one of `single_value`, `single_value_fixed`, `multi_value`, or `multi_value_fixed`.
        :param pulumi.Input[str] name: [Updating causes resource replacement] The name of the custom field.
        """
        pulumi.set(__self__, "data_type", data_type)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "incident_type", incident_type)
        if default_value is not None:
            pulumi.set(__self__, "default_value", default_value)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if field_options is not None:
            pulumi.set(__self__, "field_options", field_options)
        if field_type is not None:
            pulumi.set(__self__, "field_type", field_type)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="dataType")
    def data_type(self) -> pulumi.Input[str]:
        """
        [Updating causes resource replacement] The type of the data of this custom field. Can be one of `string`, `integer`, `float`, `boolean`, `datetime`, or `url` when `data_type` is `single_value`, otherwise must be `string`. Update
        """
        return pulumi.get(self, "data_type")

    @data_type.setter
    def data_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "data_type", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The display name of the custom Type.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="incidentType")
    def incident_type(self) -> pulumi.Input[str]:
        """
        [Updating causes resource replacement] The id of the incident type the custom field is associated with.
        """
        return pulumi.get(self, "incident_type")

    @incident_type.setter
    def incident_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "incident_type", value)

    @property
    @pulumi.getter(name="defaultValue")
    def default_value(self) -> Optional[pulumi.Input[str]]:
        """
        The default value to set when new incidents are created. Always specified as a string.
        """
        return pulumi.get(self, "default_value")

    @default_value.setter
    def default_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_value", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the custom field.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the custom field is enabled. Defaults to true if not provided.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="fieldOptions")
    def field_options(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The options for the custom field. Can only be applied to fields with a type of `single_value_fixed` or `multi_value_fixed`.
        """
        return pulumi.get(self, "field_options")

    @field_options.setter
    def field_options(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "field_options", value)

    @property
    @pulumi.getter(name="fieldType")
    def field_type(self) -> Optional[pulumi.Input[str]]:
        """
        [Updating causes resource replacement] The field type of the field. Must be one of `single_value`, `single_value_fixed`, `multi_value`, or `multi_value_fixed`.
        """
        return pulumi.get(self, "field_type")

    @field_type.setter
    def field_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "field_type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        [Updating causes resource replacement] The name of the custom field.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _IncidentTypeCustomFieldState:
    def __init__(__self__, *,
                 data_type: Optional[pulumi.Input[str]] = None,
                 default_value: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 field_options: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 field_type: Optional[pulumi.Input[str]] = None,
                 incident_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 self: Optional[pulumi.Input[str]] = None,
                 summary: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering IncidentTypeCustomField resources.
        :param pulumi.Input[str] data_type: [Updating causes resource replacement] The type of the data of this custom field. Can be one of `string`, `integer`, `float`, `boolean`, `datetime`, or `url` when `data_type` is `single_value`, otherwise must be `string`. Update
        :param pulumi.Input[str] default_value: The default value to set when new incidents are created. Always specified as a string.
        :param pulumi.Input[str] description: The description of the custom field.
        :param pulumi.Input[str] display_name: The display name of the custom Type.
        :param pulumi.Input[bool] enabled: Whether the custom field is enabled. Defaults to true if not provided.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] field_options: The options for the custom field. Can only be applied to fields with a type of `single_value_fixed` or `multi_value_fixed`.
        :param pulumi.Input[str] field_type: [Updating causes resource replacement] The field type of the field. Must be one of `single_value`, `single_value_fixed`, `multi_value`, or `multi_value_fixed`.
        :param pulumi.Input[str] incident_type: [Updating causes resource replacement] The id of the incident type the custom field is associated with.
        :param pulumi.Input[str] name: [Updating causes resource replacement] The name of the custom field.
        :param pulumi.Input[str] self: The API show URL at which the object is accessible.
        :param pulumi.Input[str] summary: A short-form, server-generated string that provides succinct, important information about an object suitable for primary labeling of an entity in a client. In many cases, this will be identical to name, though it is not intended to be an identifier.
        """
        if data_type is not None:
            pulumi.set(__self__, "data_type", data_type)
        if default_value is not None:
            pulumi.set(__self__, "default_value", default_value)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if field_options is not None:
            pulumi.set(__self__, "field_options", field_options)
        if field_type is not None:
            pulumi.set(__self__, "field_type", field_type)
        if incident_type is not None:
            pulumi.set(__self__, "incident_type", incident_type)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if self is not None:
            pulumi.set(__self__, "self", self)
        if summary is not None:
            pulumi.set(__self__, "summary", summary)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="dataType")
    def data_type(self) -> Optional[pulumi.Input[str]]:
        """
        [Updating causes resource replacement] The type of the data of this custom field. Can be one of `string`, `integer`, `float`, `boolean`, `datetime`, or `url` when `data_type` is `single_value`, otherwise must be `string`. Update
        """
        return pulumi.get(self, "data_type")

    @data_type.setter
    def data_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_type", value)

    @property
    @pulumi.getter(name="defaultValue")
    def default_value(self) -> Optional[pulumi.Input[str]]:
        """
        The default value to set when new incidents are created. Always specified as a string.
        """
        return pulumi.get(self, "default_value")

    @default_value.setter
    def default_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_value", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the custom field.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name of the custom Type.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the custom field is enabled. Defaults to true if not provided.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="fieldOptions")
    def field_options(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The options for the custom field. Can only be applied to fields with a type of `single_value_fixed` or `multi_value_fixed`.
        """
        return pulumi.get(self, "field_options")

    @field_options.setter
    def field_options(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "field_options", value)

    @property
    @pulumi.getter(name="fieldType")
    def field_type(self) -> Optional[pulumi.Input[str]]:
        """
        [Updating causes resource replacement] The field type of the field. Must be one of `single_value`, `single_value_fixed`, `multi_value`, or `multi_value_fixed`.
        """
        return pulumi.get(self, "field_type")

    @field_type.setter
    def field_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "field_type", value)

    @property
    @pulumi.getter(name="incidentType")
    def incident_type(self) -> Optional[pulumi.Input[str]]:
        """
        [Updating causes resource replacement] The id of the incident type the custom field is associated with.
        """
        return pulumi.get(self, "incident_type")

    @incident_type.setter
    def incident_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "incident_type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        [Updating causes resource replacement] The name of the custom field.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def self(self) -> Optional[pulumi.Input[str]]:
        """
        The API show URL at which the object is accessible.
        """
        return pulumi.get(self, "self")

    @self.setter
    def self(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self", value)

    @property
    @pulumi.getter
    def summary(self) -> Optional[pulumi.Input[str]]:
        """
        A short-form, server-generated string that provides succinct, important information about an object suitable for primary labeling of an entity in a client. In many cases, this will be identical to name, though it is not intended to be an identifier.
        """
        return pulumi.get(self, "summary")

    @summary.setter
    def summary(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "summary", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class IncidentTypeCustomField(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_type: Optional[pulumi.Input[str]] = None,
                 default_value: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 field_options: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 field_type: Optional[pulumi.Input[str]] = None,
                 incident_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An [incident type custom fields](https://developer.pagerduty.com/api-reference/423b6701f3f1b-create-a-custom-field-for-an-incident-type)
        are a feature which will allow customers to extend Incidents with their own
        custom data, to provide additional context and support features such as
        customized filtering, search and analytics. Custom Fields can be applied to
        different incident types. Child types will inherit custom fields from their
        parent types.

        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_pagerduty as pagerduty

        alarm_time = pagerduty.IncidentTypeCustomField("alarm_time",
            name="alarm_time_minutes",
            display_name="Alarm Time",
            data_type="integer",
            field_type="single_value",
            default_value=json.dumps(5),
            incident_type="incident_default")
        foo = pagerduty.get_incident_type(display_name="Foo")
        level = pagerduty.IncidentTypeCustomField("level",
            name="level",
            incident_type=foo.id,
            display_name="Level",
            data_type="string",
            field_type="single_value_fixed",
            field_options=[
                "Trace",
                "Debug",
                "Info",
                "Warn",
                "Error",
                "Fatal",
            ])
        cs_impact = pagerduty.IncidentTypeCustomField("cs_impact",
            name="impact",
            incident_type=foo.id,
            display_name="Customer Impact",
            data_type="string",
            field_type="multi_value")
        ```

        ## Import

        Fields can be imported using the combination of `incident_type_id` and `field_id`, e.g.

        ```sh
        $ pulumi import pagerduty:index/incidentTypeCustomField:IncidentTypeCustomField cs_impact PT1234:PF1234
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_type: [Updating causes resource replacement] The type of the data of this custom field. Can be one of `string`, `integer`, `float`, `boolean`, `datetime`, or `url` when `data_type` is `single_value`, otherwise must be `string`. Update
        :param pulumi.Input[str] default_value: The default value to set when new incidents are created. Always specified as a string.
        :param pulumi.Input[str] description: The description of the custom field.
        :param pulumi.Input[str] display_name: The display name of the custom Type.
        :param pulumi.Input[bool] enabled: Whether the custom field is enabled. Defaults to true if not provided.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] field_options: The options for the custom field. Can only be applied to fields with a type of `single_value_fixed` or `multi_value_fixed`.
        :param pulumi.Input[str] field_type: [Updating causes resource replacement] The field type of the field. Must be one of `single_value`, `single_value_fixed`, `multi_value`, or `multi_value_fixed`.
        :param pulumi.Input[str] incident_type: [Updating causes resource replacement] The id of the incident type the custom field is associated with.
        :param pulumi.Input[str] name: [Updating causes resource replacement] The name of the custom field.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IncidentTypeCustomFieldArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An [incident type custom fields](https://developer.pagerduty.com/api-reference/423b6701f3f1b-create-a-custom-field-for-an-incident-type)
        are a feature which will allow customers to extend Incidents with their own
        custom data, to provide additional context and support features such as
        customized filtering, search and analytics. Custom Fields can be applied to
        different incident types. Child types will inherit custom fields from their
        parent types.

        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_pagerduty as pagerduty

        alarm_time = pagerduty.IncidentTypeCustomField("alarm_time",
            name="alarm_time_minutes",
            display_name="Alarm Time",
            data_type="integer",
            field_type="single_value",
            default_value=json.dumps(5),
            incident_type="incident_default")
        foo = pagerduty.get_incident_type(display_name="Foo")
        level = pagerduty.IncidentTypeCustomField("level",
            name="level",
            incident_type=foo.id,
            display_name="Level",
            data_type="string",
            field_type="single_value_fixed",
            field_options=[
                "Trace",
                "Debug",
                "Info",
                "Warn",
                "Error",
                "Fatal",
            ])
        cs_impact = pagerduty.IncidentTypeCustomField("cs_impact",
            name="impact",
            incident_type=foo.id,
            display_name="Customer Impact",
            data_type="string",
            field_type="multi_value")
        ```

        ## Import

        Fields can be imported using the combination of `incident_type_id` and `field_id`, e.g.

        ```sh
        $ pulumi import pagerduty:index/incidentTypeCustomField:IncidentTypeCustomField cs_impact PT1234:PF1234
        ```

        :param str resource_name: The name of the resource.
        :param IncidentTypeCustomFieldArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IncidentTypeCustomFieldArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_type: Optional[pulumi.Input[str]] = None,
                 default_value: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 field_options: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 field_type: Optional[pulumi.Input[str]] = None,
                 incident_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IncidentTypeCustomFieldArgs.__new__(IncidentTypeCustomFieldArgs)

            if data_type is None and not opts.urn:
                raise TypeError("Missing required property 'data_type'")
            __props__.__dict__["data_type"] = data_type
            __props__.__dict__["default_value"] = default_value
            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["field_options"] = field_options
            __props__.__dict__["field_type"] = field_type
            if incident_type is None and not opts.urn:
                raise TypeError("Missing required property 'incident_type'")
            __props__.__dict__["incident_type"] = incident_type
            __props__.__dict__["name"] = name
            __props__.__dict__["self"] = None
            __props__.__dict__["summary"] = None
            __props__.__dict__["type"] = None
        super(IncidentTypeCustomField, __self__).__init__(
            'pagerduty:index/incidentTypeCustomField:IncidentTypeCustomField',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            data_type: Optional[pulumi.Input[str]] = None,
            default_value: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            field_options: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            field_type: Optional[pulumi.Input[str]] = None,
            incident_type: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            self: Optional[pulumi.Input[str]] = None,
            summary: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'IncidentTypeCustomField':
        """
        Get an existing IncidentTypeCustomField resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_type: [Updating causes resource replacement] The type of the data of this custom field. Can be one of `string`, `integer`, `float`, `boolean`, `datetime`, or `url` when `data_type` is `single_value`, otherwise must be `string`. Update
        :param pulumi.Input[str] default_value: The default value to set when new incidents are created. Always specified as a string.
        :param pulumi.Input[str] description: The description of the custom field.
        :param pulumi.Input[str] display_name: The display name of the custom Type.
        :param pulumi.Input[bool] enabled: Whether the custom field is enabled. Defaults to true if not provided.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] field_options: The options for the custom field. Can only be applied to fields with a type of `single_value_fixed` or `multi_value_fixed`.
        :param pulumi.Input[str] field_type: [Updating causes resource replacement] The field type of the field. Must be one of `single_value`, `single_value_fixed`, `multi_value`, or `multi_value_fixed`.
        :param pulumi.Input[str] incident_type: [Updating causes resource replacement] The id of the incident type the custom field is associated with.
        :param pulumi.Input[str] name: [Updating causes resource replacement] The name of the custom field.
        :param pulumi.Input[str] self: The API show URL at which the object is accessible.
        :param pulumi.Input[str] summary: A short-form, server-generated string that provides succinct, important information about an object suitable for primary labeling of an entity in a client. In many cases, this will be identical to name, though it is not intended to be an identifier.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IncidentTypeCustomFieldState.__new__(_IncidentTypeCustomFieldState)

        __props__.__dict__["data_type"] = data_type
        __props__.__dict__["default_value"] = default_value
        __props__.__dict__["description"] = description
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["field_options"] = field_options
        __props__.__dict__["field_type"] = field_type
        __props__.__dict__["incident_type"] = incident_type
        __props__.__dict__["name"] = name
        __props__.__dict__["self"] = self
        __props__.__dict__["summary"] = summary
        __props__.__dict__["type"] = type
        return IncidentTypeCustomField(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dataType")
    def data_type(self) -> pulumi.Output[str]:
        """
        [Updating causes resource replacement] The type of the data of this custom field. Can be one of `string`, `integer`, `float`, `boolean`, `datetime`, or `url` when `data_type` is `single_value`, otherwise must be `string`. Update
        """
        return pulumi.get(self, "data_type")

    @property
    @pulumi.getter(name="defaultValue")
    def default_value(self) -> pulumi.Output[Optional[str]]:
        """
        The default value to set when new incidents are created. Always specified as a string.
        """
        return pulumi.get(self, "default_value")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the custom field.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name of the custom Type.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[bool]:
        """
        Whether the custom field is enabled. Defaults to true if not provided.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="fieldOptions")
    def field_options(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The options for the custom field. Can only be applied to fields with a type of `single_value_fixed` or `multi_value_fixed`.
        """
        return pulumi.get(self, "field_options")

    @property
    @pulumi.getter(name="fieldType")
    def field_type(self) -> pulumi.Output[Optional[str]]:
        """
        [Updating causes resource replacement] The field type of the field. Must be one of `single_value`, `single_value_fixed`, `multi_value`, or `multi_value_fixed`.
        """
        return pulumi.get(self, "field_type")

    @property
    @pulumi.getter(name="incidentType")
    def incident_type(self) -> pulumi.Output[str]:
        """
        [Updating causes resource replacement] The id of the incident type the custom field is associated with.
        """
        return pulumi.get(self, "incident_type")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        [Updating causes resource replacement] The name of the custom field.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def self(self) -> pulumi.Output[str]:
        """
        The API show URL at which the object is accessible.
        """
        return pulumi.get(self, "self")

    @property
    @pulumi.getter
    def summary(self) -> pulumi.Output[str]:
        """
        A short-form, server-generated string that provides succinct, important information about an object suitable for primary labeling of an entity in a client. In many cases, this will be identical to name, though it is not intended to be an identifier.
        """
        return pulumi.get(self, "summary")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "type")

