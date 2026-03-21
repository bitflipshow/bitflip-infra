ENABLE_OAUTH = True
OAUTH_CREATE_UNKNOWN_USER = True
OAUTH_ACTIVATE_USER_AFTER_CREATION = True

OAUTH_CLIENT_ID = "{{ vault_seafile_oidc_client_id }}"
OAUTH_CLIENT_SECRET = "{{ vault_seafile_oidc_client_secret }}"
OAUTH_REDIRECT_URL = "https://{{ seafile_domain }}/oauth/callback/"

OAUTH_PROVIDER_DOMAIN = "{{ seafile_oidc_provider_domain }}"
OAUTH_PROVIDER = "{{ seafile_oidc_provider }}"
OAUTH_AUTHORIZATION_URL = "{{ seafile_oidc_authorization_url }}"
OAUTH_TOKEN_URL = "{{ seafile_oidc_token_url }}"
OAUTH_USER_INFO_URL = "{{ seafile_oidc_userinfo_url }}"
OAUTH_SCOPE = {{ seafile_oidc_scope | to_json }}
OAUTH_ATTRIBUTE_MAP = {
    "uid": (True, "uid"),
    "username": (False, "name"),
    "email": (False, "contact_email"),
}

SITE_NAME = "Bitflip Seafile"
SITE_TITLE = "Bitflip Seafile"
