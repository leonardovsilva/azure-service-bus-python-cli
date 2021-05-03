<h1 align="center">Python Service Bus Explorer</h1>

<p align="center">🚀 Command line software to manage azure service bus service. Made in pyhton for cross-platform compatibility</p>

Table of contents
=================
<!--ts-->
   * [Usage examples](#usage)
<!--te-->

### Features

- [x] Send messages to a service bus queue
- [ ] Send messages to a service bus subscription
- [x] Peek messages from queue
- [x] Peek messages from subscription
- [x] Purge all messages from queue
- [x] Purge all messages from subscription
- [ ] Search engine and sorting
- [ ] Topic, subscription and queue management
- [ ] Rescheduling messages

<h3 id="usage">Usage examples</h3>

Help command - Commands and options available

```console
python service_bus.py --help  
python service_bus.py peek_queue --help 
```

Peek queue command - Checks messages in the queue without receiving messages

```console
python service_bus.py peek_queue
```

peek_queue - Options

--pretty: Make pretty JSON in the console :sparkles:

```console
python service_bus.py peek_queue --pretty
```


### Author
---

Made with ❤️ by Leonardo Viana Silva

[![Linkedin Badge](https://img.shields.io/badge/-Leonardo-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/leonardo-viana-silva/)](https://www.linkedin.com/in/leonardo-viana-silva/)[![Gmail Badge](https://img.shields.io/badge/-leonardovsilva@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:leonardovsilva@gmail.com)](mailto:leonardovsilva@gmail.com)
