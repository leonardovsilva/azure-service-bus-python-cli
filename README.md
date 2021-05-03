<h1 align="center">Python Service Bus Explorer</h1>

<p align="center">🚀 Command line software to manage azure service bus service. Made in pyhton for cross-platform compatibility</p>

Table of contents
=================
<!--ts-->
   * [Usage examples](#usage)
<!--te-->

### Features

- [x] Send messages to a service bus queue
- [ ]  Send messages to a service bus subscription
- [x] Peek messages from queue
- [x] Peek messages from subscription
- [x] Purge all messages from queue
- [x] Purge all messages from subscription

<h3 id="usage">Usage examples</h3>

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

python service_bus.py peek_queue --help 

Usage: service_bus.py peek_queue [OPTIONS]

  :   Peek messages from queue.

Options:
  -mc, --max_message_count INTEGER
                                  Max message count. Default is 5
  --pages INTEGER                 Number of pages to run. Default is 1
  -qp, --get_queue_properties     Get queue properties
  -dl, --dead_letter              Peek messages from dead letter
  --pretty                        Pretty json log messages
  --help                          Show this message and exit.

### Author
---

Made with ❤️ by Leonardo Viana Silva

[![Linkedin Badge](https://img.shields.io/badge/-Leonardo-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/leonardo-viana-silva/)](https://www.linkedin.com/in/leonardo-viana-silva/)[![Gmail Badge](https://img.shields.io/badge/-leonardovsilva@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:leonardovsilva@gmail.com)](mailto:leonardovsilva@gmail.com)
