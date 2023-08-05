# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class AssignedAddOnExtensionList(ListResource):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, account_sid, resource_sid, assigned_add_on_sid):
        """
        Initialize the AssignedAddOnExtensionList

        :param Version version: Version that contains the resource
        :param account_sid: The Account id that has installed this Add-on
        :param resource_sid: The Phone Number id that has installed this Add-on
        :param assigned_add_on_sid: A string that uniquely identifies the assigned Add-on installation

        :returns: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionList
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionList
        """
        super(AssignedAddOnExtensionList, self).__init__(version)

        # Path Solution
        self._solution = {
            'account_sid': account_sid,
            'resource_sid': resource_sid,
            'assigned_add_on_sid': assigned_add_on_sid,
        }
        self._uri = '/Accounts/{account_sid}/IncomingPhoneNumbers/{resource_sid}/AssignedAddOns/{assigned_add_on_sid}/Extensions.json'.format(**self._solution)

    def stream(self, limit=None, page_size=None):
        """
        Streams AssignedAddOnExtensionInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, limit=None, page_size=None):
        """
        Lists AssignedAddOnExtensionInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionInstance]
        """
        return list(self.stream(
            limit=limit,
            page_size=page_size,
        ))

    def page(self, page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of AssignedAddOnExtensionInstance records from the API.
        Request is executed immediately

        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of AssignedAddOnExtensionInstance
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionPage
        """
        params = values.of({
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return AssignedAddOnExtensionPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of AssignedAddOnExtensionInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of AssignedAddOnExtensionInstance
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return AssignedAddOnExtensionPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a AssignedAddOnExtensionContext

        :param sid: The unique Extension Sid

        :returns: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionContext
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionContext
        """
        return AssignedAddOnExtensionContext(
            self._version,
            account_sid=self._solution['account_sid'],
            resource_sid=self._solution['resource_sid'],
            assigned_add_on_sid=self._solution['assigned_add_on_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a AssignedAddOnExtensionContext

        :param sid: The unique Extension Sid

        :returns: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionContext
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionContext
        """
        return AssignedAddOnExtensionContext(
            self._version,
            account_sid=self._solution['account_sid'],
            resource_sid=self._solution['resource_sid'],
            assigned_add_on_sid=self._solution['assigned_add_on_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.AssignedAddOnExtensionList>'


class AssignedAddOnExtensionPage(Page):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, response, solution):
        """
        Initialize the AssignedAddOnExtensionPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The Account id that has installed this Add-on
        :param resource_sid: The Phone Number id that has installed this Add-on
        :param assigned_add_on_sid: A string that uniquely identifies the assigned Add-on installation

        :returns: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionPage
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionPage
        """
        super(AssignedAddOnExtensionPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of AssignedAddOnExtensionInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionInstance
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionInstance
        """
        return AssignedAddOnExtensionInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            resource_sid=self._solution['resource_sid'],
            assigned_add_on_sid=self._solution['assigned_add_on_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.AssignedAddOnExtensionPage>'


class AssignedAddOnExtensionContext(InstanceContext):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, account_sid, resource_sid, assigned_add_on_sid,
                 sid):
        """
        Initialize the AssignedAddOnExtensionContext

        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param resource_sid: The resource_sid
        :param assigned_add_on_sid: The assigned_add_on_sid
        :param sid: The unique Extension Sid

        :returns: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionContext
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionContext
        """
        super(AssignedAddOnExtensionContext, self).__init__(version)

        # Path Solution
        self._solution = {
            'account_sid': account_sid,
            'resource_sid': resource_sid,
            'assigned_add_on_sid': assigned_add_on_sid,
            'sid': sid,
        }
        self._uri = '/Accounts/{account_sid}/IncomingPhoneNumbers/{resource_sid}/AssignedAddOns/{assigned_add_on_sid}/Extensions/{sid}.json'.format(**self._solution)

    def fetch(self):
        """
        Fetch a AssignedAddOnExtensionInstance

        :returns: Fetched AssignedAddOnExtensionInstance
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionInstance
        """
        params = values.of({})

        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )

        return AssignedAddOnExtensionInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            resource_sid=self._solution['resource_sid'],
            assigned_add_on_sid=self._solution['assigned_add_on_sid'],
            sid=self._solution['sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.AssignedAddOnExtensionContext {}>'.format(context)


class AssignedAddOnExtensionInstance(InstanceResource):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, payload, account_sid, resource_sid,
                 assigned_add_on_sid, sid=None):
        """
        Initialize the AssignedAddOnExtensionInstance

        :returns: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionInstance
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionInstance
        """
        super(AssignedAddOnExtensionInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'sid': payload['sid'],
            'account_sid': payload['account_sid'],
            'resource_sid': payload['resource_sid'],
            'assigned_add_on_sid': payload['assigned_add_on_sid'],
            'friendly_name': payload['friendly_name'],
            'product_name': payload['product_name'],
            'unique_name': payload['unique_name'],
            'uri': payload['uri'],
            'enabled': payload['enabled'],
        }

        # Context
        self._context = None
        self._solution = {
            'account_sid': account_sid,
            'resource_sid': resource_sid,
            'assigned_add_on_sid': assigned_add_on_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: AssignedAddOnExtensionContext for this AssignedAddOnExtensionInstance
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionContext
        """
        if self._context is None:
            self._context = AssignedAddOnExtensionContext(
                self._version,
                account_sid=self._solution['account_sid'],
                resource_sid=self._solution['resource_sid'],
                assigned_add_on_sid=self._solution['assigned_add_on_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def sid(self):
        """
        :returns: A string that uniquely identifies this Extension
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def account_sid(self):
        """
        :returns: The Account id that has installed this Add-on
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def resource_sid(self):
        """
        :returns: The Phone Number id that has installed this Add-on
        :rtype: unicode
        """
        return self._properties['resource_sid']

    @property
    def assigned_add_on_sid(self):
        """
        :returns: A string that uniquely identifies the assigned Add-on installation
        :rtype: unicode
        """
        return self._properties['assigned_add_on_sid']

    @property
    def friendly_name(self):
        """
        :returns: A human-readable description of this Extension
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def product_name(self):
        """
        :returns: A human-readable description of the Extension's Product
        :rtype: unicode
        """
        return self._properties['product_name']

    @property
    def unique_name(self):
        """
        :returns: The string that uniquely identifies this Extension
        :rtype: unicode
        """
        return self._properties['unique_name']

    @property
    def uri(self):
        """
        :returns: The uri
        :rtype: unicode
        """
        return self._properties['uri']

    @property
    def enabled(self):
        """
        :returns: A Boolean indicating if the Extension will be invoked
        :rtype: bool
        """
        return self._properties['enabled']

    def fetch(self):
        """
        Fetch a AssignedAddOnExtensionInstance

        :returns: Fetched AssignedAddOnExtensionInstance
        :rtype: twilio.rest.api.v2010.account.incoming_phone_number.assigned_add_on.assigned_add_on_extension.AssignedAddOnExtensionInstance
        """
        return self._proxy.fetch()

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.AssignedAddOnExtensionInstance {}>'.format(context)
