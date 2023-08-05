# -*- coding: utf-8 -*-
from aiohttp.web_exceptions import HTTPUnauthorized
from calendar import timegm
from datetime import datetime
from guillotina import app_settings
from guillotina import configure
from guillotina.async import IAsyncUtility
from guillotina.auth.users import GuillotinaUser
from guillotina.component import getUtility
from guillotina.exceptions import Unauthorized
from guillotina.interfaces import Allow
from guillotina.interfaces import IApplication
from guillotina.interfaces import IContainer

import aiohttp
import asyncio
import json
import jwt
import logging
import time


logger = logging.getLogger('guillotina_oauth')

# Asyncio Utility
NON_IAT_VERIFY = {
    'verify_iat': False,
}


class IOAuth(IAsyncUtility):
    """Marker interface for OAuth Utility."""

    pass


REST_API = {
    'get_authorization_code': ['POST', True],
    'get_service_token': ['POST', True],
    'valid_token': ['POST', True],
    'get_user': ['POST', False],
    'get_users': ['POST', False],
    'search_user': ['POST', 'search_user', False]
}


@configure.utility(provides=IOAuth)
class OAuth(object):
    """Object implementing OAuth Utility."""

    def __init__(self, settings=None, loop=None):
        self.loop = loop

    @property
    def configured(self):
        return 'oauth_settings' in app_settings

    @property
    def attr_id(self):
        if 'attr_id' in app_settings['oauth_settings']:
            return app_settings['oauth_settings']['attr_id']
        else:
            return 'mail'

    @property
    def server(self):
        return app_settings['oauth_settings']['server']

    @property
    def client_id(self):
        return app_settings['oauth_settings']['client_id']

    @property
    def client_password(self):
        return app_settings['oauth_settings']['client_password']

    async def initialize(self, app=None):
        self.app = app
        self._service_token = None
        if 'oauth_settings' not in app_settings:
            logger.warn('No oauth settings found, oauth will not function')
            return

        while True:
            logger.debug('Renew token')
            now = timegm(datetime.utcnow().utctimetuple())
            try:
                await self.service_token
                expiration = self._service_token['exp']
                time_to_sleep = expiration - now - 60  # refresh before we run out of time...
                await asyncio.sleep(time_to_sleep)
            except (aiohttp.client_exceptions.ClientConnectorError,
                    ConnectionRefusedError):
                logger.warn('Could not connect to oauth host, oauth will not work')
                await asyncio.sleep(10)  # wait 10 seconds before trying again
            except:
                logger.warn('Error renewing service token', exc_info=True)
                await asyncio.sleep(30)  # unknown error, try again in 30 seconds

    async def finalize(self, app=None):
        pass

    async def auth_code(self, scopes, client_id):
        result = await self.call_auth('get_authorization_code', {
            'client_id': client_id,
            'service_token': await self.service_token,
            'scopes': scopes,
            'response_type': 'code'
        })
        if result:
            return result['auth_code']
        return None

    @property
    async def service_token(self):
        if self._service_token:
            now = timegm(datetime.utcnow().utctimetuple())
            if (self._service_token['exp'] - 60) > now:
                return self._service_token['service_token']
        logger.warn('Getting new service token')
        result = await self.call_auth('get_service_token', {
            'client_id': self.client_id,
            'client_secret': self.client_password,
            'grant_type': 'service'
        })
        if result:
            self._service_token = result
            raw_service_token = self._service_token['service_token']
            logger.warn(f'New service token issued: {raw_service_token[:10]}...')
            return raw_service_token
        else:
            logger.warn('No token returned from oauth')
        return None

    async def getUsers(self, request):
        scope = request.container.id
        header = {
            'Authorization': request.headers['Authorization']
        }

        result = await self.call_auth(
            'get_users',
            params={
                'service_token': self._service_token['service_token'],
                'scope': scope
            },
            headers=header
        )
        return result

    async def searchUsers(self, request, page=0, num_x_page=30, term=''):
        scope = request.container.id
        header = {
            'Authorization': request.headers['Authorization']
        }

        payload = {
            'criteria': '{"mail": "' + term + '*"}',
            'exact_match': False,
            'attrs': '["mail"]',
            'page': page,
            'num_x_page': num_x_page,
            'service_token': self._service_token['service_token'],
            'scope': scope
        }
        result = await self.call_auth(
            'search_user',
            params=payload,
            headers=header
        )
        return result

    async def validate_token(self, request, token):
        scope = request.container.id
        result = await self.call_auth(
            'valid_token',
            params={
                'code': self._service_token['service_token'],
                'token': token,
                'scope': scope
            }
        )
        if result:
            if 'user' in result:
                return result['user']
            else:
                return None
        return None

    async def call_auth(self, url, params, headers={}, future=None, **kw):
        method, needs_decode = REST_API[url]

        result = None
        with aiohttp.ClientSession() as session:
            if method == 'GET':
                logger.debug('GET ' + self.server + url)
                async with session.get(
                        self.server + url,
                        params=params,
                        headers=headers,
                        timeout=30) as resp:
                    if resp.status == 200:
                        try:
                            result = jwt.decode(
                                await resp.text(),
                                app_settings['jwt']['secret'],
                                algorithms=[app_settings['jwt']['algorithm']])
                        except jwt.InvalidIssuedAtError:
                            logger.error('Error on Time at OAuth Server')
                            result = jwt.decode(
                                await resp.text(),
                                app_settings['jwt']['secret'],
                                algorithms=[app_settings['jwt']['algorithm']],
                                options=NON_IAT_VERIFY)
                    else:
                        logger.error(
                            'OAUTH SERVER ERROR %d %s' % (
                                resp.status,
                                await resp.text()))
                    await resp.release()
            elif method == 'POST':
                logger.debug('POST ' + self.server + url)
                async with session.post(
                        self.server + url,
                        data=json.dumps(params),
                        headers=headers,
                        timeout=30) as resp:
                    if resp.status == 200:
                        if needs_decode:
                            try:
                                result = jwt.decode(
                                    await resp.text(),
                                    app_settings['jwt']['secret'],
                                    algorithms=[app_settings['jwt']['algorithm']])
                            except jwt.InvalidIssuedAtError:
                                logger.error('Error on Time at OAuth Server')
                                result = jwt.decode(
                                    await resp.text(),
                                    app_settings['jwt']['secret'],
                                    algorithms=[app_settings['jwt']['algorithm']],
                                    options=NON_IAT_VERIFY)
                        else:
                            result = await resp.json()
                    else:
                        logger.error(
                            'OAUTH SERVER ERROR %d %s' % (
                                resp.status,
                                await resp.text()))
                    await resp.release()
            session.close()
        if future is not None:
            future.set_result(result)
        else:
            return result


class OAuthJWTValidator(object):

    for_validators = ('bearer',)

    def __init__(self, request):
        self.request = request

    async def validate(self, token):
        """Return the user from the token."""
        if token.get('type') != 'bearer':
            return None

        if '.' not in token.get('token', ''):
            # quick way to check if actually might be jwt
            return None

        try:
            try:
                validated_jwt = jwt.decode(
                    token['token'],
                    app_settings['jwt']['secret'],
                    algorithms=[app_settings['jwt']['algorithm']])
            except jwt.exceptions.ExpiredSignatureError:
                logger.warn("Token Expired")
                raise HTTPUnauthorized()
            except jwt.InvalidIssuedAtError:
                logger.warn("Back to the future")
                validated_jwt = jwt.decode(
                    token['token'],
                    app_settings['jwt']['secret'],
                    algorithms=[app_settings['jwt']['algorithm']],
                    options=NON_IAT_VERIFY)

            token['id'] = validated_jwt['login']

            oauth_utility = getUtility(IOAuth)

            # Enable extra validation
            # validation = await oauth_utility.validate_token(
            #    self.request, validated_jwt['token'])
            # if validation is not None and \
            #        validation == validated_jwt['login']:
            #    # We validate that the actual token belongs to the same
            #    # as the user on oauth

            scope = self.request._container_id if hasattr(self.request, '_container_id') else 'root'
            t1 = time.time()
            result = await oauth_utility.call_auth(
                'get_user',
                params={
                    'service_token': await oauth_utility.service_token,
                    # 'user_token': validated_jwt['token'],
                    'scope': scope,
                    'user': validated_jwt['login']
                },
                headers={
                    'Authorization': 'Bearer ' + token['token']
                }
            )
            tdif = t1 - time.time()
            logger.info('Time OAUTH %f' % tdif)
            if result:
                try:
                    user = OAuthGuillotinaUser(
                        self.request, result, oauth_utility.attr_id)
                except Unauthorized:
                    return None

                user.name = validated_jwt['name']
                user.token = validated_jwt['token']
                if user and user.id == token['id']:
                    return user

        except jwt.exceptions.DecodeError:
            pass

        return None


class OAuthGuillotinaUser(GuillotinaUser):

    def __init__(self, request, data, attr_id='mail'):
        super(OAuthGuillotinaUser, self).__init__(request)
        self._attr_id = attr_id
        self._init_data(data)
        self._properties = {}

    def _init_data(self, user_data):
        self._roles = {}
        for key in user_data['roles']:
            self._roles[key] = Allow
        self._groups = [key for key
                        in user_data['groups']]
        self.id = user_data[self._attr_id]


@configure.service(context=IApplication, name='@oauthgetcode', method='POST',
                   permission='guillotina.GetOAuthGrant', allow_access=True)
@configure.service(context=IContainer, name='@oauthgetcode', method='POST',
                   permission='guillotina.GetOAuthGrant', allow_access=True)
@configure.service(context=IApplication, name='@oauthgetcode', method='GET',
                   permission='guillotina.GetOAuthGrant', allow_access=True)
@configure.service(context=IContainer, name='@oauthgetcode', method='GET',
                   permission='guillotina.GetOAuthGrant', allow_access=True)
async def oauth_get_code(context, request):
    oauth_utility = getUtility(IOAuth)
    if 'client_id' in request.GET:
        client_id = request.GET['client_id']
    else:
        client_id = oauth_utility.client_id

    scopes = []
    if hasattr(request, '_container_id'):
        scopes.append(request._container_id)
    elif 'scope' in request.GET:
        scopes.append(request.GET['scope'])

    result = await oauth_utility.auth_code(scopes, client_id)
    return {
        'auth_code': result
    }
