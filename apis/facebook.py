
def feed_summary_url(page_id, page_access_token):
    """
    Returns the URL for the Facebook feed summary API.
    """
    FEED_SUMMARY_API = f'https://graph.facebook.com/v22.0/{page_id}/feed?fields=message,created_time,reactions.summary(true),comments.summary(true),full_picture,attachments{{media}}&access_token={page_access_token}'

    return FEED_SUMMARY_API
