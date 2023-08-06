import os
import sys

if os.name == 'posix' and not sys.platform.startswith('darwin'):
    from .nm import list_providers, store_provider, delete_provider, connect_provider, status_provider
else:
    from .other import list_providers, store_provider, delete_provider, connect_provider, status_provider
