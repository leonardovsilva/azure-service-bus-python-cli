# Python Service Bus Explorer

🚀 Command line software to manage azure service bus service. Made in pyhton for cross-platform compatibility.

![CLI usage](https://user-images.githubusercontent.com/3792091/117333961-dac6da00-ae6f-11eb-8bb6-44ad8cf55431.png)

# Table of contents

<!--ts-->
   * [Usage examples](#usage-examples)
   * [Root options](#root-options) 
   * [Environment variables](#environment-variables)
   * [Important](#important)
   * [Author](#author)
<!--te-->

# Features :running:

- [x] Send messages to a service bus queue
- [x] Send messages to a service bus subscription
- [x] Peek messages from queue
- [x] Peek messages from subscription
- [x] Purge all messages from queue
- [x] Purge all messages from subscription
- [ ] Search engine and sorting
- [ ] Topic, subscription and queue management
- [ ] Rescheduling messages
- [ ] Receive messages from queue
- [ ] Receive messages from subscription

<h1><a href="#usage-examples">Usage examples</a></h1>

## Help command

Commands and options available.

```console
python service_bus.py --help  
python service_bus.py peek_queue --help 
```

## Peek queue command

Check messages in the queue without receiving messages.

```console
python service_bus.py peek_queue
```

peek_queue - Options

--pretty: Make pretty JSON in the console :sparkles:

```console
python service_bus.py peek_queue --pretty
```

dl or --dead_letter:  Peek messages from the dead letter :ghost:

## Peek subscription command

Check messages in the subscription without receiving messages.

```console
python service_bus.py peek_sub
```

## Purge queue command 

Purge all messages from the queue.

```console
python service_bus.py purge_queue
```

purge_queue - Options

dl or --dead_letter:  from the dead letter :ghost:

## Purge subscription command

Purge all messages from the subscription. :finnadie:

```console
python service_bus.py purge_sub
```

purge_sub - Options

dl or --dead_letter:  from the dead letter :ghost:

## Send messages command

Send messages to a service bus queue or topic using a json template. The model file is at the root of the project

```console
python service_bus.py message_queue -i file
```

```console
python service_bus.py message_topic -i file
```

<h1><a href="#root-options">Root options</a></h1>

- --queue_name or, -qn: Name of the message bus queue (optional)
- --topic_name or -tn: Name of the message bus topic (optional)
- --subscription_name or -sn: Name of the message bus subscription (optional)
- --log_path or -l: Path to generate file log console outputs (optional)

```console
python service_bus.py -l system_path peek_sub
```

There is a configuration file at the root of the project where it is possible to add the service 
bus settings more easily. 

It is loaded by default at the root of the main file folder. It can also be configured via environment.

<h1><a href="#environment-variables">Environment variables</a></h1>

- SERVICE_BUS_CONNECTION_STR
- SERVICE_BUS_QUEUE_NAME
- SERVICE_BUS_TOPIC_NAME
- SERVICE_BUS_SUBSCRIPTION_NAME
- SERVICEBUS_CONF (Path of config file)

<h1><a href="#important">Important :exclamation:</a></h1>

There is a variety of options see use --help to view other.

<h1><a href="#author">Author</a></h1>

Made with ❤️ by Leonardo Viana Silva

[![Linkedin Badge](https://img.shields.io/badge/-Leonardo-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/leonardo-viana-silva/)](https://www.linkedin.com/in/leonardo-viana-silva/)[![Gmail Badge](https://img.shields.io/badge/-leonardovsilva@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:leonardovsilva@gmail.com)](mailto:leonardovsilva@gmail.com)
