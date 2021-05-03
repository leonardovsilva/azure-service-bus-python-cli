Usage examples

python service_bus.py --help  

Usage: service_bus.py [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose                  Increase output verbosity level
  -qn, --queue_name TEXT         Name of the message bus queue
  -tn, --topic_name TEXT         Name of the message bus topic
  -sn, --subscription_name TEXT  Name of the message bus subscription
  -l, --log_path PATH            Path to log console outputs
  --help                         Show this message and exit.

Commands:
  message_queue  : Send messages to a service bus queue
  peek_queue     : Peek messages from queue.
  peek_sub       : Peek messages from subscription.
  purge_queue    : Purge all messages from queue.
  purge_sub      : Purge all messages from subscription


