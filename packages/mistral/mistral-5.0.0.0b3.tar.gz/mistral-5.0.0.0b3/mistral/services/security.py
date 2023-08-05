# Copyright 2013 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from oslo_config import cfg
from oslo_log import log as logging

from mistral import context as auth_ctx
from mistral.utils.openstack import keystone


LOG = logging.getLogger(__name__)
CONF = cfg.CONF

# Make sure to import 'auth_enable' option before using it.
# TODO(rakhmerov): Try to find a better solution.
CONF.import_opt('auth_enable', 'mistral.config', group='pecan')


DEFAULT_PROJECT_ID = "<default-project>"


def get_project_id():
    if CONF.pecan.auth_enable and auth_ctx.has_ctx():
        return auth_ctx.ctx().project_id
    else:
        return DEFAULT_PROJECT_ID


def create_trust():
    client = keystone.client()

    ctx = auth_ctx.ctx()

    trustee_id = keystone.client_for_admin(
        CONF.keystone_authtoken.admin_tenant_name).user_id

    return client.trusts.create(
        trustor_user=client.user_id,
        trustee_user=trustee_id,
        impersonation=True,
        role_names=ctx.roles,
        project=ctx.project_id
    )


def create_context(trust_id, project_id):
    """Creates Mistral security context.

    :param trust_id: Trust Id.
    :param project_id: Project Id.
    :return: Mistral security context.
    """

    if CONF.pecan.auth_enable:
        client = keystone.client_for_trusts(trust_id)

        return auth_ctx.MistralContext(
            user=client.user_id,
            tenant=project_id,
            auth_token=client.auth_token,
            is_trust_scoped=True,
            trust_id=trust_id,
        )

    return auth_ctx.MistralContext(
        user=None,
        tenant=None,
        auth_token=None,
        is_admin=True
    )


def delete_trust(trust_id):
    if not trust_id:
        return

    ctx = auth_ctx.ctx()

    # If this trust is already in the context then it means that
    # context already has trust scoped token from exactly this trust_id.
    # So we don't need request the token from the trust one more time.
    if ctx.is_trust_scoped and ctx.trust_id == trust_id:
        keystone_client = keystone.client()
    else:
        keystone_client = keystone.client_for_trusts(trust_id)

    try:
        keystone_client.trusts.delete(trust_id)
    except Exception as e:
        LOG.warning("Failed to delete trust [id=%s]: %s", trust_id, e)


def add_trust_id(secure_object_values):
    if cfg.CONF.pecan.auth_enable:
        trust = create_trust()
        secure_object_values.update({
            'trust_id': trust.id
        })
