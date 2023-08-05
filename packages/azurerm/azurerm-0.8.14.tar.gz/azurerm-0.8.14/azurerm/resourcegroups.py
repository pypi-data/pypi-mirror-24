# resourcegroups.py - azurerm functions for Resource Groups
import json
from .restfns import do_delete, do_get, do_put
from .settings import get_rm_endpoint, BASE_API


# create_resource_group(access_token, subscription_id, rgname, location)
# create a resource group in the specified location
def create_resource_group(access_token, subscription_id, rgname, location):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '?api-version=', BASE_API])
    rg_body = {'location': location}
    body = json.dumps(rg_body)
    return do_put(endpoint, body, access_token)

# delete_resource_group(access_token, subscription_id, rgname)
# delete the named resource group
def delete_resource_group(access_token, subscription_id, rgname):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourcegroups/', rgname,
                        '?api-version=', BASE_API])
    return do_delete(endpoint, access_token)


# get_resource_group(access_token, subscription_id, rgname)
# get details about the named resource group
def get_resource_group(access_token, subscription_id, rgname):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/', rgname,
                        '?api-version=', BASE_API])
    return do_get(endpoint, access_token)


# list_resource_groups(access_token, subscription_id)
def list_resource_groups(access_token, subscription_id):
    endpoint = ''.join([get_rm_endpoint(),
                        '/subscriptions/', subscription_id,
                        '/resourceGroups/',
                        '?api-version=', BASE_API])
    return do_get(endpoint, access_token)
