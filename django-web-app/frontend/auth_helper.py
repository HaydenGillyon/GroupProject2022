
import yaml
import msal
import os
import time


stream = open('oauth_settings.yml', 'r')
settings = yaml.load(stream, yaml.SafeLoader)

def load_cache(request):
  cache = msal.SerializableTokenCache()
  if request.session.get('token_cache'):
    cache.deserialize(request.session['token_cache'])

  return cache

def save_cache(request, cache):
  if cache.has_state_changed:
    request.session['token_cache'] = cache.serialize()

def get_msal_app(cache=None):
  auth_app = msal.ConfidentialClientApplication(
    settings['app_id'],
    authority=settings['authority'],
    client_credential=settings['app_secret'],
    token_cache=cache)

  return auth_app

def get_sign_in_flow():
  auth_app = get_msal_app()

  return auth_app.initiate_auth_code_flow(
    settings['scopes'],
    redirect_uri=settings['redirect'])

def get_token_from_code(request):
  cache = load_cache(request)
  auth_app = get_msal_app(cache)

  flow = request.session.pop('auth_flow', {})

  result = auth_app.acquire_token_by_auth_code_flow(flow, request.GET)
  save_cache(request, cache)

  return result

def store_user(request, user):
  try:
    request.session['user'] = {
      'is_authenticated': True,
      'name': user['displayName'],
      'email': user['mail'] if (user['mail'] != None) else user['userPrincipalName'],
      'timeZone': user['mailboxSettings']['timeZone'] if ('timeZone' in user['mailboxSettings']) else 'UTC'
    }
  except Exception as e:
    print(e)

def get_token(request):
  cache = load_cache(request)
  auth_app = get_msal_app(cache)

  accounts = auth_app.get_accounts()
  if accounts:
    result = auth_app.acquire_token_silent(
      settings['scopes'],
      account=accounts[0])

    save_cache(request, cache)

    return result['access_token']

def remove_user_and_token(request):
  if 'token_cache' in request.session:
    del request.session['token_cache']

  if 'user' in request.session:
    del request.session['user']
