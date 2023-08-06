import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

class BookPermissionCacheItem(Model):
    """
    Cached record for book permission
    """
    class Meta:
        environment = os.environ.get('AWS_ENV') or 'dev'
        region = os.environ.get('AWS_DEFAULT_REGION', 'ap-southeast-1')
        table_name = "book-permission-cache-{}".format(environment.lower())
    user_asset_manager_id = UnicodeAttribute(range_key=True)
    """
    'asset_manager_id_book' will be a concatenated string of the two columns
    'asset_manager_id' and 'book_id' in the book_permission table in SQL database.
    The concatenation will use a space key ' ' as the delimiter to combine the 
    two strings. This arrangement is due to dynamoDB's restriction that composite 
    primary key can have maximum 2 attributes and we need 3 attributes (asset_manager_id, 
    book_id, user_asset_manager_id) to pin down a permission.
    """
    asset_manager_id_book = UnicodeAttribute(hash_key=True)
    permission = UnicodeAttribute(null = False)
    permission_status = UnicodeAttribute(null = False)


    @staticmethod
    def update_book_permission_cache(asset_manager_id, book_id, user_asset_manager_id, permission, permission_status, action):
        try:
            asset_manager_id_book = str(asset_manager_id) + " " + str(book_id)
            if action == 'new':
                try:   # check if there are existing 'Inactive' permission. Although there shouldn't be
                       # existing permission found when calling 'new', if there is, update the existing's
                       # status to the passed in 'Active' status.
                    existing = BookPermissionCacheItem.get(asset_manager_id_book, str(user_asset_manager_id))
                    existing.update({'permission':{'value': permission, 'action':'put'}, 
                                     'permission_status':{'value':permission_status, 'action':'put'}})
                except BookPermissionCacheItem.DoesNotExist:
                    permission_item = BookPermissionCacheItem(asset_manager_id_book = asset_manager_id_book, 
                                                        user_asset_manager_id = user_asset_manager_id,
                                                        permission = permission,
                                                        permission_status = permission_status)
                    permission_item.save()
            elif action == 'amend':
                try:
                    existing = BookPermissionCacheItem.get(asset_manager_id_book, str(user_asset_manager_id))
                    existing.update({'permission':{'value': permission, 'action':'put'}, 
                                     'permission_status':{'value':permission_status, 'action':'put'}})
                except BookPermissionCacheItem.DoesNotExist:
                    raise AttributeError('Invalid amend action, no existing permission found.')
            else:
                raise ValueError('Unsupported cache update type: %s' % action)
        except Exception as ex: 
            raise

    @staticmethod
    def check_book_permission_cache(asset_manager_id, user_asset_manager_id, book_id):
        """
        This method takes in an asset_manager_id, book_id and user_asset_manager_id. It returns 
        the permission ('read' or 'write') if an active permission is found in dynamoDB. None is
        returned if no permission is found or the relationship found is inactive
        """
        asset_manager_id_book = str(asset_manager_id) + " " + str(book_id)
        try: 
            existing =  BookPermissionCacheItem.get(asset_manager_id_book, str(user_asset_manager_id))
            if existing.permission_status != 'Active':
                return None
            return existing.permission
        except BookPermissionCacheItem.DoesNotExist:
            return None


# test case below, uncomment to run. Expect to have book-permission-cache-dev dynamoDB table created on AWS
'''
if __name__ == '__main__':
    CacheItem = BookPermissionCacheItem()
    CacheItem.update_book_permission_cache(asset_manager_id = '12', book_id = 'europe', user_asset_manager_id = '23',
                                                                    permission='write',permission_status='Active',action='new')     
    item = CacheItem.check_book_permission_cache(asset_manager_id=12,book_id='europe',user_asset_manager_id=23)
    print("Test expecting output: %s , retrieved output: %s"%('write', item))
    CacheItem.update_book_permission_cache(asset_manager_id = '12', book_id = 'europe', user_asset_manager_id = '23',
                                                                    permission='read',permission_status='Active',action='amend')
    item = CacheItem.check_book_permission_cache(asset_manager_id=12,book_id='europe',user_asset_manager_id=23)
    print("Test expecting output: %s , retrieved output: %s"%('read', item))
    CacheItem.update_book_permission_cache(asset_manager_id = '12', book_id = 'europe', user_asset_manager_id = '23',
                                                                    permission='read',permission_status='Inactive',action='amend')
    item = CacheItem.check_book_permission_cache(asset_manager_id=12,book_id='europe',user_asset_manager_id=23)
    print("Test expecting output: %s , retrieved output: %s"%('None', item))
'''
    