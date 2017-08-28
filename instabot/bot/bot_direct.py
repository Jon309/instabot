from tqdm import tqdm

from . import delay


def send_message(self, text, user_ids, thread_id=None):
    """
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or one user_id for send to one person
    :param thread_id: thread_id
    """
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(text, str) and type(user_ids) not in (list, str):
        self.logger.error('Text must be an string, user_ids must be an list or string')
        return False
    delay.small_delay(self)
    if super(self.__class__, self).sendDirectItem('message', user_ids, text=text, thread=thread_id):
        # ToDo: need to add counter
        return True
    self.logger.info("Message to {user_ids} wasn't sended".format(user_ids=user_ids))
    return False


def send_messages(self, text, user_ids):
    broken_items = []
    if len(user_ids) == 0:
        self.logger.info("User must be at least one.")
        return broken_items
    self.logger.info("Going to send %d messages." % (len(user_ids)))
    for user in tqdm(user_ids):
        if not self.send_message(text, user):
            delay.error_delay(self)
            broken_items = user_ids[user_ids.index(user):]
            break
    return broken_items


def _get_user_ids(self, user_ids):
    if isinstance(user_ids, str):
        user_ids = self.convert_to_user_id(user_ids)
        return [user_ids]
    return [self.convert_to_user_id(user) for user in user_ids]
