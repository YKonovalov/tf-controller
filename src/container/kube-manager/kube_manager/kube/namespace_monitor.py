#
# Copyright (c) 2017 Juniper Networks, Inc. All rights reserved.
#

from __future__ import print_function

from kube_manager.common.kube_config_db import NamespaceKM
from kube_manager.kube.kube_monitor import KubeMonitor


class NamespaceMonitor(KubeMonitor):

    def __init__(self, args=None, logger=None, q=None):
        super(NamespaceMonitor, self).__init__(
            args, logger, q, NamespaceKM, resource_type='namespace')

    def process_event(self, event):
        namespace_data = event['object']
        event_type = event['type']
        kind = event['object'].get('kind')
        name = event['object']['metadata'].get('name')

        if self.db:
            namespace_uuid = self.db.get_uuid(event['object'])
            if event_type != 'DELETED':
                # Update Namespace DB.
                namespace = self.db.locate(namespace_uuid)
                namespace.update(namespace_data)
            else:
                # Remove the entry from Namespace DB.
                self.db.delete(namespace_uuid)
        else:
            namespace_uuid = event['object']['metadata'].get('uid')

        msg = "%s - Got %s %s %s:%s" \
              % (self.name, event_type, kind, name, namespace_uuid)
        print(msg)
        self.logger.debug(msg)
        self.q.put(event)
