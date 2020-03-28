'''
tickets
=====
The following methods allow for interaction into the Tenable.sc
:sc-api:`Ticket <Ticket.html>` API.  These items are typically seen under the
Worklow --> Tickets section of Tenable.sc.
Methods available on ``sc.tickets``:
.. rst-class:: hide-signature
.. autoclass:: TicketAPI
    .. automethod:: create
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
    Note: you cannot delete tickets, must set them to resolved and they will be auto-purged via system configured retention period
'''
from .base import SCEndpoint

class TicketAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a ticket document
        '''

        if 'assigned_to' in kw:
            # Validate as int and pass to assignee
            kw['assignee'] = self._check('assigned_to', kw['assigned_to'], int)
            del(kw['assigned_to'])

        # all of the following keys are string values and do not require any
        # case conversion.  We will simply iterate through them and verify that
        # they are in-fact strings.
        keys = [
            'name', 'description', 'notes'
        ]
        for k in keys:
            if k in kw:
                self._check(k, kw[k], str)

        if 'classification' in kw:
            # Verify that classification is one of the correct possible values.
            kw['classification'] = self._check(
                'classification', kw['classification'], str, choices=['information', 'configuration', 'patch', 'disable', 'firewall', 'schedule', 'ids', 'accept risk', 'recast risk', 're-scan request', 'false positive', 'system probe', 'external probe', 'investigation needed', 'compromised system', 'virus incident', 'bad credentials', 'unauthorized software', 'unauthorized system', 'unauthorized user', 'other'])

        if 'status' in kw:
            # Verify that status is one of the correct possible values
            kw['status'] = self._check('status', kw['status'], str,
                choices=['assigned', 'resolved', 'more information', 'not applicable', 'duplicate', 'closed'])

        return kw

    def create(self, name, assignee, **kw):
        '''
        Creates a ticket.
        :sc-api:`ticket: create <Ticket.html#ticket_POST>`
        Args:
            name (str):
                The name for the ticket
            assignee (int):
                The ID for the user the ticket is being assigned to
            status (str, optional):
                Optional status of the ticket: assigned, resolved, etc.
            classification (str, optional):
                Optional classification of the ticket type, i.e. Information, Other, etc.
            description (str, optional):
                Optional description for the ticket
            notes (str, optional):
                Optional notes associated with the ticket
            queries (list, optional):
                Optional list of IDs of queries to associate with the ticket
            query (object, optional):
                Optional query object
        Returns:
            :obj:`dict`:
                The newly created ticket.
        Examples:
            >>> ticket = sc.tickets.create('INC123456', 1, status='assigned', classification='information', description='This is a sample ticket', notes='Sample notes')
        '''
        kw['name'] = name
        kw['assignee'] = assignee
        kw['status'] = status
        kw['classification'] = classification
        kw['description'] = description
        kw['notes'] = notes
        kw['queries'] = queries
        kw['query'] = query
#        kw.get('auth_type', 'tns')
        payload = self._constructor(**kw)
        return self._api.post('ticket', json=payload).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific ticket.
        :sc-api:`tiket: details <Ticket.html#TicketRESTReference-/ticket/{id}>`
        Args:
            id (int): The identifier for the ticket.
            fields (list, optional): A list of attributes to return.
        Returns:
            :obj:`dict`:
                The ticket resource record.
        Examples:
            >>> ticket = sc.tickets.details(1)
            >>> pprint(ticket)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('ticket/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def edit(self, id, **kw):
        '''
        Edits a ticket.
        :sc-api:`ticket: edit <Ticket.html#ticket_id_PATCH>`
        Args:
            name (str):
                Optional name for the ticket. Must not be blank.
            assignee (int):
                Optional ID for the user the ticket is being assigned to
            status (str, optional):
                Optional status of the ticket: assigned, resolved, etc. Must not be blank.
            classification (str, optional):
                Optional classification of the ticket type, i.e. Information, Other, etc. Must not be blank.
            description (str, optional):
                Optional description for the ticket
            notes (str, optional):
                Optional notes associated with the ticket
            queries (list, optional):
                Optional list of IDs of queries to associate with the ticket
            query (object, optional):
                Optional query object

        Returns:
            :obj:`dict`:
                The newly updated ticket.
        Examples:
            >>> ticket = sc.tickets.edit(1, status='Resolved', notes='ran updates')
        '''
        payload = self._constructor(**kw)
        return self._api.patch('ticket/{}'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def list(self, fields=None):
        '''
        Outputs a dictionary of usable and manageable tickets, within which is a list of tickets.
        :sc-api:`ticket: list <Ticket.html#ticket_GET>`
        Args:
            fields (list, optional):
                A list of attributes to return for each ticket, e.g. ["name","description"]. If not specified, only a list of ticket IDs will return
        Returns:
            :obj:`dict`:
                A dictionary with two lists of ticket resources.
        Examples:
            >>> for ticket in sc.tickets.list():
            ...     pprint(ticket)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('ticket', params=params).json()['response']
