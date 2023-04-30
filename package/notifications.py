
# Import internal modules
import package.helpers as helpers

# Variables
DESCRIPTION_SHORT_CUTOFF = 100

class Notification():
    """
        `title (str)`: The title of the notification. Presented in bold at the top of a ui toast. 
        `description_full (str)`: The full description of the notification.
        `description_short (str)`: A shortened version of `description_full`. If `description_short` is not passed as an argument, then `description_full` will be used & cut at XXX characters.
        `alert_level (int)`: The level of how important the notification is to the user.
        `origin (str)`: This is the uuid of where the notification came from. If it came from another app, the apps uuid is provided.
        `url (str)`: This is a url which redirects the user to the relevant page.
        `is_unread (bool)`: Whether the notification has been read by the user.
        `notification_uuid (str)`: A uuid which is assigned to every notification.
        `datetime (datetime.datetime)`: The ISO 8601 format of when the notification was created.
    """
    def __init__(self, title: str, description_full: str, alert_level: int, origin: str, url: str, description_short: str = None) -> None:
        if description_short is None:
            description_short = description_full[:DESCRIPTION_SHORT_CUTOFF-3] + '...'
    
        self.title = title
        self.description_full = description_full
        self.description_short = description_short
        self.alert_level = alert_level
        self.origin = origin
        self.url = url
        self.is_unread = False
        self.notification_uuid = helpers.get_uuid()
        self.datetime = helpers.get_iso_dt()