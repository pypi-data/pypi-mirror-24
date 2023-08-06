import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

class AssetManagerRelationshipCacheItem(Model):
    """
    Cached record for asset manager
    """
    class Meta:
        environment = os.environ.get('AWS_ENV') or 'dev'
        region = os.environ.get('AWS_DEFAULT_REGION', 'ap-southeast-1')
        table_name = "asset-manager-relationship-cache-{}".format(environment.lower())
    asset_manager_id = UnicodeAttribute(hash_key=True)
    related_id = UnicodeAttribute(range_key=True)
    relationship_type = UnicodeAttribute(null = False)
    relationship_status = UnicodeAttribute(null = False)    