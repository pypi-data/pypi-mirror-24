#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys

from .yugen_core import list_api_keys, get_lambdas, delete_api, \
    export_to_swagger, create_api_key, list_apis, \
    create_custom_domain, delete_api_key, deploy_api
from . import utils
from .gcdt_cmd_dispatcher import cmd
from . import gcdt_lifecycle


# creating docopt parameters and usage help
DOC = '''Usage:
        yugen deploy
        yugen delete -f
        yugen export
        yugen list
        yugen apikey-create <keyname>
        yugen apikey-list
        yugen apikey-delete
        yugen custom-domain-create
        yugen version

-h --help           show this
'''


# TODO support changing API keys
# TODO investigate base path problem


@cmd(spec=['version'])
def version_cmd():
    utils.version()


@cmd(spec=['list'])
def list_cmd(**tooldata):
    context = tooldata.get('context')
    awsclient = context.get('_awsclient')
    return list_apis(awsclient)


@cmd(spec=['deploy'])
def deploy_cmd(**tooldata):
    context = tooldata.get('context')
    config = tooldata.get('config')
    awsclient = context.get('_awsclient')

    #api_name = conf.get('api.name')
    api_name = config['api'].get('name')
    api_description = config['api'].get('description')
    target_stage = config['api'].get('targetStage')
    api_key = config['api'].get('apiKey')
    lambdas = get_lambdas(awsclient, config, add_arn=True)
    cache_cluster_enabled=config['api'].get('cacheClusterEnabled', False)
    exit_code = deploy_api(
        awsclient=awsclient,
        api_name=api_name,
        api_description=api_description,
        stage_name=target_stage,
        api_key=api_key,
        lambdas=lambdas,
        cache_cluster_enabled=cache_cluster_enabled
    )
    if 'customDomain' in config:
        domain_name = config['customDomain'].get('domainName')
        route_53_record = config['customDomain'].get('route53Record')
        ssl_cert = {
            'name': config['customDomain'].get('certificateName'),
            'body': config['customDomain'].get('certificateBody'),
            'private_key': config['customDomain'].get('certificatePrivateKey'),
            'chain': config['customDomain'].get('certificateChain')
        }
        hosted_zone_id = config['customDomain'].get('hostedDomainZoneId')
        api_base_path = config['customDomain'].get('basePath')
        create_custom_domain(
            awsclient=awsclient,
            api_name=api_name,
            api_target_stage=target_stage,
            api_base_path=api_base_path,
            domain_name=domain_name,
            route_53_record=route_53_record,
            ssl_cert=ssl_cert,
            hosted_zone_id=hosted_zone_id
        )
    return exit_code


@cmd(spec=['delete', '-f'])
def delete_cmd(force, **tooldata):
    context = tooldata.get('context')
    config = tooldata.get('config')
    awsclient = context.get('_awsclient')

    exit_code = delete_api(
        awsclient=awsclient,
        api_name=config['api'].get('name')
    )
    return exit_code


@cmd(spec=['export'])
def export_cmd(**tooldata):
    context = tooldata.get('context')
    config = tooldata.get('config')
    awsclient = context.get('_awsclient')
    api_name = config['api'].get('name')
    target_stage = config['api'].get('targetStage')
    api_description = config['api'].get('description')

    lambdas = get_lambdas(awsclient, config, add_arn=True)
    return export_to_swagger(
        awsclient=awsclient,
        api_name=api_name,
        stage_name=target_stage,
        api_description=api_description,
        lambdas=lambdas,
        custom_hostname=(config['customDomain'].get('domainName')
                         if 'customDomain' in config else False),
        custom_base_path=(config['customDomain'].get('basePath')
                          if 'customDomain' in config else False)
    )


@cmd(spec=['apikey-create', '<keyname>'])
def apikey_create_cmd(keyname, **tooldata):
    context = tooldata.get('context')
    config = tooldata.get('config')
    awsclient = context.get('_awsclient')
    api_name = config['api'].get('name')
    create_api_key(awsclient, api_name, keyname)


@cmd(spec=['apikey-delete'])
def apikey_delete_cmd(**tooldata):
    context = tooldata.get('context')
    config = tooldata.get('config')
    awsclient = context.get('_awsclient')
    api_key = config['api'].get('apiKey')
    delete_api_key(awsclient, api_key)


@cmd(spec=['apikey-list'])
def apikey_list_cmd(**tooldata):
    context = tooldata.get('context')
    awsclient = context.get('_awsclient')
    list_api_keys(awsclient)


@cmd(spec=['custom-domain-create'])
def custom_domain_create_cmd(**tooldata):
    context = tooldata.get('context')
    config = tooldata.get('config')
    awsclient = context.get('_awsclient')
    api_name = config['api'].get('name')
    api_target_stage = config['api'].get('targetStage')

    domain_name = config['customDomain'].get('domainName')
    route_53_record = config['customDomain'].get('route53Record')
    api_base_path = config['customDomain'].get('basePath')
    ssl_cert = {
        'name': config['customDomain'].get('certificateName'),
        'body': config['customDomain'].get('certificateBody'),
        'private_key': config['customDomain'].get('certificatePrivateKey'),
        'chain': config['customDomain'].get('certificateChain')
    }
    hosted_zone_id = config['customDomain'].get('hostedDomainZoneId')

    return create_custom_domain(
        awsclient=awsclient,
        api_name=api_name,
        api_target_stage=api_target_stage,
        api_base_path=api_base_path,
        domain_name=domain_name,
        route_53_record=route_53_record,
        ssl_cert=ssl_cert,
        hosted_zone_id=hosted_zone_id
    )


def main():
    sys.exit(gcdt_lifecycle.main(
        DOC, 'yugen', dispatch_only=['version', 'clean']))


if __name__ == '__main__':
    main()
