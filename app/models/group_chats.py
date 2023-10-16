def get_messages_in_bundles_of_timestamp(message, bundle_size=100, page=1):
    """Gets a list of messages in bundles of timestamp using indexing and pagination to fetch messages in smaller, more manageable chunks.

  Args:
    message: The Message object.
    bundle_size: The number of messages to include in each bundle.
    page: The page number of the results to fetch.

  Returns:
    A list of bundles of messages, where each bundle is a list of messages with the same timestamp.
  """

    # Get the total number of messages in the conversation.
    total_messages = len(message.messages)

    # Calculate the start and end indices for the current page.
    start_index = (page - 1) * bundle_size
    end_index = min(start_index + bundle_size, total_messages)

    # Get the messages for the current page.
    messages = message.messages[start_index:end_index]

    # Group the messages by timestamp.
    messages_by_timestamp = {}
    for message in messages:
        timestamp = message.timestamp.date()
        if timestamp not in messages_by_timestamp:
            messages_by_timestamp[timestamp] = []
        messages_by_timestamp[timestamp].append(message)

    # Return the list of bundles of messages.
    bundles = []
    for timestamp, messages in messages_by_timestamp.items():
        bundles.append({
            'timestamp': timestamp,
            'messages': messages
        })
    return bundles


"""# Example usage:

# Get the first page of messages in bundles of 100 messages.
bundles = get_messages_in_bundles_of_timestamp(message, bundle_size=100, page=1)

# Get the second page of messages in bundles of 100 messages.
bundles = get_messages_in_bundles_of_timestamp(message, bundle_size=100, page=2)"""
