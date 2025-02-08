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
    'UseAppOauthScopedToken',
]

@pulumi.output_type
class UseAppOauthScopedToken(dict):
    def __init__(__self__, *,
                 pd_client_id: Optional[str] = None,
                 pd_client_secret: Optional[str] = None,
                 pd_subdomain: Optional[str] = None):
        if pd_client_id is not None:
            pulumi.set(__self__, "pd_client_id", pd_client_id)
        if pd_client_secret is not None:
            pulumi.set(__self__, "pd_client_secret", pd_client_secret)
        if pd_subdomain is not None:
            pulumi.set(__self__, "pd_subdomain", pd_subdomain)

    @property
    @pulumi.getter(name="pdClientId")
    def pd_client_id(self) -> Optional[str]:
        return pulumi.get(self, "pd_client_id")

    @property
    @pulumi.getter(name="pdClientSecret")
    def pd_client_secret(self) -> Optional[str]:
        return pulumi.get(self, "pd_client_secret")

    @property
    @pulumi.getter(name="pdSubdomain")
    def pd_subdomain(self) -> Optional[str]:
        return pulumi.get(self, "pd_subdomain")


