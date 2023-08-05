# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import warnings

from keystoneclient import adapter
from keystoneclient import client as ks_client
from keystoneclient import discover
from keystoneclient import session

import manilaclient
from manilaclient.common import constants
from manilaclient.common import httpclient
from manilaclient import exceptions
from manilaclient.v2 import availability_zones
from manilaclient.v2 import limits
from manilaclient.v2 import messages
from manilaclient.v2 import quota_classes
from manilaclient.v2 import quotas
from manilaclient.v2 import scheduler_stats
from manilaclient.v2 import security_services
from manilaclient.v2 import services
from manilaclient.v2 import share_export_locations
from manilaclient.v2 import share_group_snapshots
from manilaclient.v2 import share_group_type_access
from manilaclient.v2 import share_group_types
from manilaclient.v2 import share_groups
from manilaclient.v2 import share_instance_export_locations
from manilaclient.v2 import share_instances
from manilaclient.v2 import share_networks
from manilaclient.v2 import share_replicas
from manilaclient.v2 import share_servers
from manilaclient.v2 import share_snapshot_export_locations
from manilaclient.v2 import share_snapshot_instance_export_locations
from manilaclient.v2 import share_snapshot_instances
from manilaclient.v2 import share_snapshots
from manilaclient.v2 import share_type_access
from manilaclient.v2 import share_types
from manilaclient.v2 import shares


class Client(object):
    """Top-level object to access the OpenStack Manila API.

    Create an instance with your creds::

        >>> client = Client(USERNAME, PASSWORD, PROJECT_ID, AUTH_URL)

    Or, alternatively, you can create a client instance using the
    keystoneclient.session API::

        >>> from keystoneclient.auth.identity import v2
        >>> from keystoneclient import session
        >>> from manilaclient import client
        >>> auth = v2.Password(auth_url=AUTH_URL,
                               username=USERNAME,
                               password=PASSWORD,
                               tenant_name=PROJECT_ID)
        >>> sess = session.Session(auth=auth)
        >>> manila = client.Client(VERSION, session=sess)

    Then call methods on its managers::

        >>> client.shares.list()
        ...
    """
    def __init__(self, username=None, api_key=None,
                 project_id=None, auth_url=None, insecure=False, timeout=None,
                 tenant_id=None, project_name=None, region_name=None,
                 endpoint_type='publicURL', extensions=None,
                 service_type=constants.V2_SERVICE_TYPE, service_name=None,
                 retries=None, http_log_debug=False, input_auth_token=None,
                 session=None, auth=None, cacert=None,
                 service_catalog_url=None, user_agent='python-manilaclient',
                 use_keyring=False, force_new_token=False,
                 cached_token_lifetime=300,
                 api_version=manilaclient.API_MIN_VERSION,
                 user_id=None,
                 user_domain_id=None,
                 user_domain_name=None,
                 project_domain_id=None,
                 project_domain_name=None,
                 cert=None,
                 password=None,
                 **kwargs):

        self.username = username
        self.password = password or api_key
        self.tenant_id = tenant_id or project_id
        self.tenant_name = project_name

        self.user_id = user_id
        self.project_id = project_id or tenant_id
        self.project_name = project_name
        self.user_domain_id = user_domain_id
        self.user_domain_name = user_domain_name
        self.project_domain_id = project_domain_id
        self.project_domain_name = project_domain_name

        self.endpoint_type = endpoint_type
        self.auth_url = auth_url
        self.region_name = region_name

        self.cacert = cacert
        self.cert = cert
        self.insecure = insecure

        self.use_keyring = use_keyring
        self.force_new_token = force_new_token
        self.cached_token_lifetime = cached_token_lifetime

        service_name = kwargs.get("share_service_name", service_name)

        def check_deprecated_arguments():
            deprecated = {
                'share_service_name': 'service_name',
                'proxy_tenant_id': None,
                'proxy_token': None,
                'os_cache': 'use_keyring',
                'api_key': 'password',
            }

            for arg, replacement in deprecated.items():
                if kwargs.get(arg, None) is None:
                    continue

                replacement_msg = ""

                if replacement is not None:
                    replacement_msg = " Use %s instead." % replacement

                msg = "Argument %(arg)s is deprecated.%(repl)s" % {
                    'arg': arg,
                    'repl': replacement_msg
                }
                warnings.warn(msg)

        check_deprecated_arguments()

        if input_auth_token and not service_catalog_url:
            msg = ("For token-based authentication you should "
                   "provide 'input_auth_token' and 'service_catalog_url'.")
            raise exceptions.ClientException(msg)

        self.project_id = tenant_id if tenant_id is not None else project_id
        self.keystone_client = None
        self.session = session

        # NOTE(u_glide): token authorization has highest priority.
        # That's why session and/or password will be ignored
        # if token is provided.
        if not input_auth_token:
            if session:
                self.keystone_client = adapter.LegacyJsonAdapter(
                    session=session,
                    auth=auth,
                    interface=endpoint_type,
                    service_type=service_type,
                    service_name=service_name,
                    region_name=region_name)
                input_auth_token = self.keystone_client.session.get_token(auth)

            else:
                self.keystone_client = self._get_keystone_client()
                input_auth_token = self.keystone_client.auth_token

        if not input_auth_token:
            raise RuntimeError("Not Authorized")

        if session and not service_catalog_url:
            service_catalog_url = self.keystone_client.session.get_endpoint(
                auth, interface=endpoint_type,
                service_type=service_type)
        elif not service_catalog_url:
            catalog = self.keystone_client.service_catalog.get_endpoints(
                service_type)
            for catalog_entry in catalog.get(service_type, []):
                if (catalog_entry.get("interface") == (
                        endpoint_type.lower().split("url")[0]) or
                        catalog_entry.get(endpoint_type)):
                    if (region_name and not region_name == (
                            catalog_entry.get(
                                "region",
                                catalog_entry.get("region_id")))):
                        continue
                    service_catalog_url = catalog_entry.get(
                        "url", catalog_entry.get(endpoint_type))
                    break

        if not service_catalog_url:
            raise RuntimeError("Could not find Manila endpoint in catalog")

        self.api_version = api_version
        self.client = httpclient.HTTPClient(service_catalog_url,
                                            input_auth_token,
                                            user_agent,
                                            insecure=insecure,
                                            cacert=cacert,
                                            timeout=timeout,
                                            retries=retries,
                                            http_log_debug=http_log_debug,
                                            api_version=self.api_version)

        self.availability_zones = availability_zones.AvailabilityZoneManager(
            self)
        self.limits = limits.LimitsManager(self)
        self.messages = messages.MessageManager(self)
        self.services = services.ServiceManager(self)
        self.security_services = security_services.SecurityServiceManager(self)
        self.share_networks = share_networks.ShareNetworkManager(self)

        self.quota_classes = quota_classes.QuotaClassSetManager(self)
        self.quotas = quotas.QuotaSetManager(self)

        self.shares = shares.ShareManager(self)
        self.share_export_locations = (
            share_export_locations.ShareExportLocationManager(self))
        self.share_groups = share_groups.ShareGroupManager(self)
        self.share_group_snapshots = (
            share_group_snapshots.ShareGroupSnapshotManager(self))
        self.share_group_type_access = (
            share_group_type_access.ShareGroupTypeAccessManager(self))
        self.share_group_types = share_group_types.ShareGroupTypeManager(self)
        self.share_instances = share_instances.ShareInstanceManager(self)
        self.share_instance_export_locations = (
            share_instance_export_locations.ShareInstanceExportLocationManager(
                self))
        self.share_snapshots = share_snapshots.ShareSnapshotManager(self)
        self.share_snapshot_instances = (
            share_snapshot_instances.ShareSnapshotInstanceManager(self))
        self.share_snapshot_export_locations = (
            share_snapshot_export_locations.ShareSnapshotExportLocationManager(
                self))
        self.share_snapshot_instance_export_locations = (
            share_snapshot_instance_export_locations.
            ShareSnapshotInstanceExportLocationManager(self))

        self.share_types = share_types.ShareTypeManager(self)
        self.share_type_access = share_type_access.ShareTypeAccessManager(self)
        self.share_servers = share_servers.ShareServerManager(self)
        self.share_replicas = share_replicas.ShareReplicaManager(self)
        self.pools = scheduler_stats.PoolManager(self)

        self._load_extensions(extensions)

    def _load_extensions(self, extensions):
        if not extensions:
            return

        for extension in extensions:
            if extension.manager_class:
                setattr(self, extension.name, extension.manager_class(self))

    def authenticate(self):
        """Authenticate against the server.

        Normally this is called automatically when you first access the API,
        but you can call this method to force authentication right now.

        Returns on success; raises :exc:`exceptions.Unauthorized` if the
        credentials are wrong.
        """
        warnings.warn("authenticate() method is deprecated. "
                      "Client automatically makes authentication call "
                      "in the constructor.")

    def _get_keystone_client(self):
        # First create a Keystone session
        if self.insecure:
            verify = False
        else:
            verify = self.cacert or True
        ks_session = session.Session(verify=verify, cert=self.cert)

        # Discover the supported keystone versions using the given url
        ks_discover = discover.Discover(
            session=ks_session, auth_url=self.auth_url)

        # Inspect the auth_url to see the supported version. If both v3 and v2
        # are supported, then use the highest version if possible.
        v2_auth_url = ks_discover.url_for('v2.0')
        v3_auth_url = ks_discover.url_for('v3.0')

        if v3_auth_url:
            keystone_client = ks_client.Client(
                session=ks_session,
                version=(3, 0),
                auth_url=v3_auth_url,
                username=self.username,
                password=self.password,
                user_id=self.user_id,
                user_domain_name=self.user_domain_name,
                user_domain_id=self.user_domain_id,
                project_id=self.project_id or self.tenant_id,
                project_name=self.project_name,
                project_domain_name=self.project_domain_name,
                project_domain_id=self.project_domain_id,
                region_name=self.region_name)
        elif v2_auth_url:
            keystone_client = ks_client.Client(
                session=ks_session,
                version=(2, 0),
                auth_url=v2_auth_url,
                username=self.username,
                password=self.password,
                tenant_id=self.tenant_id,
                tenant_name=self.tenant_name,
                region_name=self.region_name,
                cert=self.cert,
                use_keyring=self.use_keyring,
                force_new_token=self.force_new_token,
                stale_duration=self.cached_token_lifetime)
        else:
            raise exceptions.CommandError(
                'Unable to determine the Keystone version to authenticate '
                'with using the given auth_url.')
        keystone_client.authenticate()
        return keystone_client
