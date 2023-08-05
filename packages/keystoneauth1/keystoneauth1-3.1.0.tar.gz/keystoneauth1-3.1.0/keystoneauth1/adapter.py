# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import warnings

from positional import positional

from keystoneauth1 import session


class Adapter(object):
    """An instance of a session with local variables.

    A session is a global object that is shared around amongst many clients. It
    therefore contains state that is relevant to everyone. There is a lot of
    state such as the service type and region_name that are only relevant to a
    particular client that is using the session. An adapter provides a wrapper
    of client local data around the global session object.

    version, min_version, max_version and default_microversion can all be
    given either as a string or a tuple.

    :param session: The session object to wrap.
    :type session: keystoneauth1.session.Session
    :param str service_type: The default service_type for URL discovery.
    :param str service_name: The default service_name for URL discovery.
    :param str interface: The default interface for URL discovery.
    :param str region_name: The default region_name for URL discovery.
    :param str endpoint_override: Always use this endpoint URL for requests
                                  for this client.
    :param version: The minimum version restricted to a given Major API.
                    Mutually exclusive with min_version and max_version.
                    (optional)
    :param auth: An auth plugin to use instead of the session one.
    :type auth: keystoneauth1.plugin.BaseAuthPlugin
    :param str user_agent: The User-Agent string to set.
    :param int connect_retries: the maximum number of retries that should
                                be attempted for connection errors.
                                Default None - use session default which
                                is don't retry.
    :param logger: A logging object to use for requests that pass through this
                   adapter.
    :type logger: logging.Logger
    :param dict allow: Extra filters to pass when discovering API versions.
                       (optional)
    :param dict additional_headers: Additional headers that should be attached
                                    to every request passing through the
                                    adapter. Headers of the same name specified
                                    per request will take priority.
    :param str client_name: The name of the client that created the adapter.
                            This will be used to create the user_agent.
    :param str client_version: The version of the client that created the
                               adapter. This will be used to create the
                               user_agent.
    :param bool allow_version_hack: Allow keystoneauth to hack up catalog
                                    URLS to support older schemes.
                                    (optional, default True)
    :param str global_request_id: A global_request_id (in the form of
                                  ``req-$uuid``) that will be passed on all
                                  requests. Enables cross project request id
                                  tracking.
    :param min_version: The minimum major version of a given API, intended to
                        be used as the lower bound of a range with
                        max_version. Mutually exclusive with version.
                        If min_version is given with no max_version it is as
                        if max version is 'latest'. (optional)
    :param max_version: The maximum major version of a given API, intended to
                        be used as the upper bound of a range with min_version.
                        Mutually exclusive with version. (optional)
    :param default_microversion: The default microversion value to send
                                 with API requests. While microversions are
                                 a per-request feature, a user may know they
                                 want to default to sending a specific value.
                                 (optional)
    """

    client_name = None
    client_version = None

    @positional()
    def __init__(self, session, service_type=None, service_name=None,
                 interface=None, region_name=None, endpoint_override=None,
                 version=None, auth=None, user_agent=None,
                 connect_retries=None, logger=None, allow={},
                 additional_headers=None, client_name=None,
                 client_version=None, allow_version_hack=None,
                 global_request_id=None,
                 min_version=None, max_version=None,
                 default_microversion=None):
        if version and (min_version or max_version):
            raise TypeError(
                "version is mutually exclusive with min_version and"
                " max_version")
        # NOTE(jamielennox): when adding new parameters to adapter please also
        # add them to the adapter call in httpclient.HTTPClient.__init__ as
        # well as to load_adapter_from_argparse below if the argument is
        # intended to be something a user would reasonably expect to set on
        # a command line
        self.session = session
        self.service_type = service_type
        self.service_name = service_name
        self.interface = interface
        self.region_name = region_name
        self.endpoint_override = endpoint_override
        self.version = version
        self.user_agent = user_agent
        self.auth = auth
        self.connect_retries = connect_retries
        self.logger = logger
        self.allow = allow
        self.additional_headers = additional_headers or {}
        self.allow_version_hack = allow_version_hack
        self.min_version = min_version
        self.max_version = max_version
        self.default_microversion = default_microversion

        self.global_request_id = global_request_id

        if client_name:
            self.client_name = client_name
        if client_version:
            self.client_version = client_version

    def _set_endpoint_filter_kwargs(self, kwargs):
        if self.service_type:
            kwargs.setdefault('service_type', self.service_type)
        if self.service_name:
            kwargs.setdefault('service_name', self.service_name)
        if self.interface:
            kwargs.setdefault('interface', self.interface)
        if self.region_name:
            kwargs.setdefault('region_name', self.region_name)
        if self.version:
            kwargs.setdefault('version', self.version)
        if self.min_version:
            kwargs.setdefault('min_version', self.min_version)
        if self.max_version:
            kwargs.setdefault('max_version', self.max_version)
        if self.allow_version_hack is not None:
            kwargs.setdefault('allow_version_hack', self.allow_version_hack)

    def request(self, url, method, **kwargs):
        endpoint_filter = kwargs.setdefault('endpoint_filter', {})
        self._set_endpoint_filter_kwargs(endpoint_filter)

        if self.endpoint_override:
            kwargs.setdefault('endpoint_override', self.endpoint_override)

        if self.auth:
            kwargs.setdefault('auth', self.auth)
        if self.user_agent:
            kwargs.setdefault('user_agent', self.user_agent)
        if self.connect_retries is not None:
            kwargs.setdefault('connect_retries', self.connect_retries)
        if self.logger:
            kwargs.setdefault('logger', self.logger)
        if self.allow:
            kwargs.setdefault('allow', self.allow)
        if self.default_microversion is not None:
            kwargs.setdefault('microversion', self.default_microversion)

        if isinstance(self.session, (session.Session, Adapter)):
            # these things are unsupported by keystoneclient's session so be
            # careful with them until everyone has transitioned to ksa.
            # Allowing adapter allows adapter nesting that auth_token does.
            if self.client_name:
                kwargs.setdefault('client_name', self.client_name)
            if self.client_version:
                kwargs.setdefault('client_version', self.client_version)

        else:
            warnings.warn('Using keystoneclient sessions has been deprecated. '
                          'Please update your software to use keystoneauth1.')

        for k, v in self.additional_headers.items():
            kwargs.setdefault('headers', {}).setdefault(k, v)

        if self.global_request_id is not None:
            kwargs.setdefault('headers', {}).setdefault(
                "X-OpenStack-Request-ID", self.global_request_id)

        return self.session.request(url, method, **kwargs)

    def get_token(self, auth=None):
        """Return a token as provided by the auth plugin.

        :param auth: The auth plugin to use for token. Overrides the plugin
                     on the session. (optional)
        :type auth: keystoneauth1.plugin.BaseAuthPlugin

        :raises keystoneauth1.exceptions.auth.AuthorizationFailure: if a new
            token fetch fails.

        :returns: A valid token.
        :rtype: :class:`str`
        """
        return self.session.get_token(auth or self.auth)

    def get_endpoint(self, auth=None, **kwargs):
        """Get an endpoint as provided by the auth plugin.

        :param auth: The auth plugin to use for token. Overrides the plugin on
                     the session. (optional)
        :type auth: keystoneauth1.plugin.BaseAuthPlugin

        :raises keystoneauth1.exceptions.auth_plugins.MissingAuthPlugin: if a
            plugin is not available.

        :returns: An endpoint if available or None.
        :rtype: :class:`str`
        """
        if self.endpoint_override:
            return self.endpoint_override

        self._set_endpoint_filter_kwargs(kwargs)
        return self.session.get_endpoint(auth or self.auth, **kwargs)

    def get_endpoint_data(self, auth=None):
        """Get the endpoint data for this Adapter's endpoint.

        :param auth: The auth plugin to use for token. Overrides the plugin on
                     the session. (optional)
        :type auth: keystoneauth1.plugin.BaseAuthPlugin

        :raises keystoneauth1.exceptions.auth_plugins.MissingAuthPlugin: if a
            plugin is not available.
        :raises TypeError: If arguments are invalid

        :returns: Endpoint data if available or None.
        :rtype: keystoneauth1.discover.EndpointData
        """
        kwargs = {}
        self._set_endpoint_filter_kwargs(kwargs)
        if self.endpoint_override:
            kwargs['endpoint_override'] = self.endpoint_override

        return self.session.get_endpoint_data(auth or self.auth, **kwargs)

    def invalidate(self, auth=None):
        """Invalidate an authentication plugin."""
        return self.session.invalidate(auth or self.auth)

    def get_user_id(self, auth=None):
        """Return the authenticated user_id as provided by the auth plugin.

        :param auth: The auth plugin to use for token. Overrides the plugin
                     on the session. (optional)
        :type auth: keystoneauth1.plugin.BaseAuthPlugin

        :raises keystoneauth1.exceptions.auth.AuthorizationFailure:
            if a new token fetch fails.
        :raises keystoneauth1.exceptions.auth_plugins.MissingAuthPlugin:
            if a plugin is not available.

        :returns: Current `user_id` or None if not supported by plugin.
        :rtype: :class:`str`
        """
        return self.session.get_user_id(auth or self.auth)

    def get_project_id(self, auth=None):
        """Return the authenticated project_id as provided by the auth plugin.

        :param auth: The auth plugin to use for token. Overrides the plugin
                     on the session. (optional)
        :type auth: keystoneauth1.plugin.BaseAuthPlugin

        :raises keystoneauth1.exceptions.auth.AuthorizationFailure:
            if a new token fetch fails.
        :raises keystoneauth1.exceptions.auth_plugins.MissingAuthPlugin:
            if a plugin is not available.

        :returns: Current `project_id` or None if not supported by plugin.
        :rtype: :class:`str`
        """
        return self.session.get_project_id(auth or self.auth)

    def get(self, url, **kwargs):
        return self.request(url, 'GET', **kwargs)

    def head(self, url, **kwargs):
        return self.request(url, 'HEAD', **kwargs)

    def post(self, url, **kwargs):
        return self.request(url, 'POST', **kwargs)

    def put(self, url, **kwargs):
        return self.request(url, 'PUT', **kwargs)

    def patch(self, url, **kwargs):
        return self.request(url, 'PATCH', **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, 'DELETE', **kwargs)

    # TODO(efried): Move this to loading.adapter.Adapter
    @classmethod
    def register_argparse_arguments(cls, parser, service_type=None):
        """Attach arguments to a given argparse Parser for Adapters.

        :param parser: The argparse parser to attach options to.
        :type parser: argparse.ArgumentParser
        :param str service_type: Default service_type value. (optional)
        """
        adapter_group = parser.add_argument_group(
            'Service Options',
            'Options controlling the specialization of the API'
            ' Connection from information found in the catalog')

        adapter_group.add_argument(
            '--os-service-type',
            metavar='<name>',
            default=os.environ.get('OS_SERVICE_TYPE', service_type),
            help='Service type to request from the catalog')

        adapter_group.add_argument(
            '--os-service-name',
            metavar='<name>',
            default=os.environ.get('OS_SERVICE_NAME', None),
            help='Service name to request from the catalog')

        adapter_group.add_argument(
            '--os-interface',
            metavar='<name>',
            default=os.environ.get('OS_INTERFACE', 'public'),
            help='API Interface to use [public, internal, admin]')

        adapter_group.add_argument(
            '--os-region-name',
            metavar='<name>',
            default=os.environ.get('OS_REGION_NAME', None),
            help='Region of the cloud to use')

        adapter_group.add_argument(
            '--os-endpoint-override',
            metavar='<name>',
            default=os.environ.get('OS_ENDPOINT_OVERRIDE', None),
            help='Endpoint to use instead of the endpoint in the catalog')

        adapter_group.add_argument(
            '--os-api-version',
            metavar='<name>',
            default=os.environ.get('OS_API_VERSION', None),
            help='Which version of the service API to use')

    # TODO(efried): Move this to loading.adapter.Adapter
    @classmethod
    def register_service_argparse_arguments(cls, parser, service_type):
        """Attach arguments to a given argparse Parser for Adapters.

        :param parser: The argparse parser to attach options to.
        :type parser: argparse.ArgumentParser
        :param str service_type: Name of a service to generate additional
                                 arguments for.
        """
        service_env = service_type.upper().replace('-', '_')
        adapter_group = parser.add_argument_group(
            '{service_type} Service Options'.format(
                service_type=service_type.title()),
            'Options controlling the specialization of the {service_type}'
            ' API Connection from information found in the catalog'.format(
                service_type=service_type.title()))

        adapter_group.add_argument(
            '--os-{service_type}-service-type'.format(
                service_type=service_type),
            metavar='<name>',
            default=os.environ.get(
                'OS_{service_type}_SERVICE_TYPE'.format(
                    service_type=service_env), None),
            help=('Service type to request from the catalog for the'
                  ' {service_type} service'.format(
                      service_type=service_type)))

        adapter_group.add_argument(
            '--os-{service_type}-service-name'.format(
                service_type=service_type),
            metavar='<name>',
            default=os.environ.get(
                'OS_{service_type}_SERVICE_NAME'.format(
                    service_type=service_env), None),
            help=('Service name to request from the catalog for the'
                  ' {service_type} service'.format(
                      service_type=service_type)))

        adapter_group.add_argument(
            '--os-{service_type}-interface'.format(
                service_type=service_type),
            metavar='<name>',
            default=os.environ.get(
                'OS_{service_type}_INTERFACE'.format(
                    service_type=service_env), None),
            help=('API Interface to use for the {service_type} service'
                  ' [public, internal, admin]'.format(
                      service_type=service_type)))

        adapter_group.add_argument(
            '--os-{service_type}-api-version'.format(
                service_type=service_type),
            metavar='<name>',
            default=os.environ.get(
                'OS_{service_type}_API_VERSION'.format(
                    service_type=service_env), None),
            help=('Which version of the service API to use for'
                  ' the {service_type} service'.format(
                      service_type=service_type)))

        adapter_group.add_argument(
            '--os-{service_type}-endpoint-override'.format(
                service_type=service_type),
            metavar='<name>',
            default=os.environ.get(
                'OS_{service_type}_ENDPOINT_OVERRIDE'.format(
                    service_type=service_env), None),
            help=('Endpoint to use for the {service_type} service'
                  ' instead of the endpoint in the catalog'.format(
                      service_type=service_type)))


class LegacyJsonAdapter(Adapter):
    """Make something that looks like an old HTTPClient.

    A common case when using an adapter is that we want an interface similar to
    the HTTPClients of old which returned the body as JSON as well.

    You probably don't want this if you are starting from scratch.
    """

    def request(self, *args, **kwargs):
        headers = kwargs.setdefault('headers', {})
        headers.setdefault('Accept', 'application/json')

        try:
            kwargs['json'] = kwargs.pop('body')
        except KeyError:
            pass

        resp = super(LegacyJsonAdapter, self).request(*args, **kwargs)

        try:
            body = resp.json()
        except ValueError:
            body = None

        return resp, body


# TODO(efried): Deprecate this in favor of
#               loading.adapter.register_argparse_arguments
def register_adapter_argparse_arguments(*args, **kwargs):
    return Adapter.register_argparse_arguments(*args, **kwargs)


# TODO(efried): Deprecate this in favor of
#               loading.adapter.register_service_argparse_arguments
def register_service_adapter_argparse_arguments(*args, **kwargs):
    return Adapter.register_service_argparse_arguments(*args, **kwargs)
