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

__all__ = ['OrganizationMembersArgs', 'OrganizationMembers']

@pulumi.input_type
class OrganizationMembersArgs:
    def __init__(__self__, *,
                 members: pulumi.Input[Sequence[pulumi.Input[str]]],
                 organization_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a OrganizationMembers resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] members: Add user ID(s) directly from the tenant to become members of the organization.
        :param pulumi.Input[str] organization_id: The ID of the organization to assign the members to.
        """
        pulumi.set(__self__, "members", members)
        pulumi.set(__self__, "organization_id", organization_id)

    @property
    @pulumi.getter
    def members(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Add user ID(s) directly from the tenant to become members of the organization.
        """
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> pulumi.Input[str]:
        """
        The ID of the organization to assign the members to.
        """
        return pulumi.get(self, "organization_id")

    @organization_id.setter
    def organization_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "organization_id", value)


@pulumi.input_type
class _OrganizationMembersState:
    def __init__(__self__, *,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 organization_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OrganizationMembers resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] members: Add user ID(s) directly from the tenant to become members of the organization.
        :param pulumi.Input[str] organization_id: The ID of the organization to assign the members to.
        """
        if members is not None:
            pulumi.set(__self__, "members", members)
        if organization_id is not None:
            pulumi.set(__self__, "organization_id", organization_id)

    @property
    @pulumi.getter
    def members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Add user ID(s) directly from the tenant to become members of the organization.
        """
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "members", value)

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the organization to assign the members to.
        """
        return pulumi.get(self, "organization_id")

    @organization_id.setter
    def organization_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organization_id", value)


class OrganizationMembers(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 organization_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource is used to manage members of an organization.

        !> This resource manages all the members assigned to an organization. In contrast, the `OrganizationMember`
        resource only appends a member to an organization. To avoid potential issues, it is recommended not to use this
        resource in conjunction with the `OrganizationMember` resource when managing members for the same organization
        id.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_auth0 as auth0

        user1 = auth0.User("user_1",
            connection_name="Username-Password-Authentication",
            email="myuser1@auth0.com",
            password="MyPass123$")
        user2 = auth0.User("user_2",
            connection_name="Username-Password-Authentication",
            email="myuser2@auth0.com",
            password="MyPass123$")
        my_org = auth0.Organization("my_org",
            name="some-org",
            display_name="Some Organization")
        my_members = auth0.OrganizationMembers("my_members",
            organization_id=my_org.id,
            members=[
                user1.id,
                user2.id,
            ])
        ```

        ## Import

        This resource can be imported by specifying the organization ID.

        # 

        Example:

        ```sh
        $ pulumi import auth0:index/organizationMembers:OrganizationMembers my_org_members "org_XXXXX"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] members: Add user ID(s) directly from the tenant to become members of the organization.
        :param pulumi.Input[str] organization_id: The ID of the organization to assign the members to.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OrganizationMembersArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource is used to manage members of an organization.

        !> This resource manages all the members assigned to an organization. In contrast, the `OrganizationMember`
        resource only appends a member to an organization. To avoid potential issues, it is recommended not to use this
        resource in conjunction with the `OrganizationMember` resource when managing members for the same organization
        id.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_auth0 as auth0

        user1 = auth0.User("user_1",
            connection_name="Username-Password-Authentication",
            email="myuser1@auth0.com",
            password="MyPass123$")
        user2 = auth0.User("user_2",
            connection_name="Username-Password-Authentication",
            email="myuser2@auth0.com",
            password="MyPass123$")
        my_org = auth0.Organization("my_org",
            name="some-org",
            display_name="Some Organization")
        my_members = auth0.OrganizationMembers("my_members",
            organization_id=my_org.id,
            members=[
                user1.id,
                user2.id,
            ])
        ```

        ## Import

        This resource can be imported by specifying the organization ID.

        # 

        Example:

        ```sh
        $ pulumi import auth0:index/organizationMembers:OrganizationMembers my_org_members "org_XXXXX"
        ```

        :param str resource_name: The name of the resource.
        :param OrganizationMembersArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OrganizationMembersArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 organization_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OrganizationMembersArgs.__new__(OrganizationMembersArgs)

            if members is None and not opts.urn:
                raise TypeError("Missing required property 'members'")
            __props__.__dict__["members"] = members
            if organization_id is None and not opts.urn:
                raise TypeError("Missing required property 'organization_id'")
            __props__.__dict__["organization_id"] = organization_id
        super(OrganizationMembers, __self__).__init__(
            'auth0:index/organizationMembers:OrganizationMembers',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            organization_id: Optional[pulumi.Input[str]] = None) -> 'OrganizationMembers':
        """
        Get an existing OrganizationMembers resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] members: Add user ID(s) directly from the tenant to become members of the organization.
        :param pulumi.Input[str] organization_id: The ID of the organization to assign the members to.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OrganizationMembersState.__new__(_OrganizationMembersState)

        __props__.__dict__["members"] = members
        __props__.__dict__["organization_id"] = organization_id
        return OrganizationMembers(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def members(self) -> pulumi.Output[Sequence[str]]:
        """
        Add user ID(s) directly from the tenant to become members of the organization.
        """
        return pulumi.get(self, "members")

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> pulumi.Output[str]:
        """
        The ID of the organization to assign the members to.
        """
        return pulumi.get(self, "organization_id")

