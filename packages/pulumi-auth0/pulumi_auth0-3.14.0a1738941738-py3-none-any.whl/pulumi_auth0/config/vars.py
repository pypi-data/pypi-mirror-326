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

import types

__config__ = pulumi.Config('auth0')


class _ExportableConfig(types.ModuleType):
    @property
    def api_token(self) -> Optional[str]:
        """
        Your Auth0 [management api access
        token](https://auth0.com/docs/security/tokens/access-tokens/management-api-access-tokens). It can also be sourced from
        the `AUTH0_API_TOKEN` environment variable. It can be used instead of `client_id` + `client_secret`. If both are
        specified, `api_token` will be used over `client_id` + `client_secret` fields.
        """
        return __config__.get('apiToken')

    @property
    def audience(self) -> Optional[str]:
        """
        Your Auth0 audience when using a custom domain. It can also be sourced from the `AUTH0_AUDIENCE` environment variable.
        """
        return __config__.get('audience')

    @property
    def client_id(self) -> Optional[str]:
        """
        Your Auth0 client ID. It can also be sourced from the `AUTH0_CLIENT_ID` environment variable.
        """
        return __config__.get('clientId')

    @property
    def client_secret(self) -> Optional[str]:
        """
        Your Auth0 client secret. It can also be sourced from the `AUTH0_CLIENT_SECRET` environment variable.
        """
        return __config__.get('clientSecret')

    @property
    def debug(self) -> Optional[bool]:
        """
        Indicates whether to turn on debug mode.
        """
        return __config__.get_bool('debug') or _utilities.get_env_bool('AUTH0_DEBUG')

    @property
    def domain(self) -> Optional[str]:
        """
        Your Auth0 domain name. It can also be sourced from the `AUTH0_DOMAIN` environment variable.
        """
        return __config__.get('domain')

