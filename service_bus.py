import json

import click
import colorama
import config
from message_parser import ServiceBusMessageParser
from queue_process import QueueProcess
from topic_process import TopicProcess


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--verbose', '-v', is_flag=True,
              help="Increase output verbosity level")
@click.option('--queue_name', '-qn', required=False, help="Name of the message bus queue")
@click.option('--topic_name', '-tn', required=False, help="Name of the message bus topic")
@click.option('--subscription_name', '-sn', required=False, help="Name of the message bus subscription")
@click.option('--log_path', '-l', required=False, default=None, type=click.Path(exists=True), help="Path to log console outputs")
def main(ctx, verbose, queue_name, topic_name, subscription_name, log_path):
    group_commands = ['peek_queue', 'purge_queue']
    """
        serviceBusPythonExplorer is a command line tool that helps management Azure Service Bus.\n
          example: python service_bus.py peek_queue -n [queue_name]
    """
    ctx.obj = {} if not ctx.obj else ctx.obj

    if ctx.invoked_subcommand is None:
        click.echo("Specify one of the commands below")
        print(*group_commands, sep='\n')

    ctx.obj['VERBOSE'] = verbose
    ctx.obj['QUEUE_NAME'] = queue_name
    ctx.obj['TOPIC_NAME'] = topic_name
    ctx.obj['SUBSCRIPTION_NAME'] = subscription_name
    ctx.obj['LOG_PATH'] = log_path

    set_console_color()

    if queue_name is not None:
        print(queue_name)
    if topic_name is not None:
        print(topic_name)
    if subscription_name is not None:
        print(subscription_name)
    #config_obj = config.Config()
    #config_obj.init()


def set_console_color():
    config_obj = config.Config()
    config_obj.init()

    style = None
    try:
        style = config_obj.config_export['DEFAULT']['Style']
    except Exception:
        pass

    if style == 'LIGHTYELLOW_EX':
        colorama.init()
        print(colorama.Fore.LIGHTYELLOW_EX)
    elif style == 'LIGHTRED_EX':
        colorama.init()
        print(colorama.Fore.LIGHTRED_EX)
    elif style == 'LIGHTMAGENTA_EX':
        colorama.init()
        print(colorama.Fore.LIGHTMAGENTA_EX)
    elif style == 'LIGHTBLUE_EX':
        colorama.init()
        print(colorama.Fore.LIGHTBLUE_EX)
    elif style == 'LIGHTCYAN_EX':
        colorama.init()
        print(colorama.Fore.LIGHTCYAN_EX)
    elif style == 'LIGHTGREEN_EX':
        colorama.init()
        print(colorama.Fore.LIGHTGREEN_EX)
    elif style == 'LIGHTWHITE_EX':
        colorama.init()
        print(colorama.Fore.LIGHTWHITE_EX)


@main.command('peek_queue')
@click.pass_context
@click.option('--max_message_count', '-mc', required=False, default=5, help="Max message count. Default is 5")
@click.option('--pages', required=False, default=1, help="Number of pages to run. Default is 1")
@click.option('--get_queue_properties', '-qp', is_flag=True, help="Get queue properties")
@click.option('--dead_letter', '-dl', is_flag=True, help="Peek messages from dead letter")
@click.option('--pretty', is_flag=True, help="Pretty json log messages")
def peek_queue(ctx, max_message_count, pages, get_queue_properties, dead_letter, pretty):
    """
            :   Peek messages from queue.
    """
    ctx.obj['MAX_MESSAGE_COUNT'] = max_message_count
    ctx.obj['PAGES'] = pages
    ctx.obj['GET_QUEUE_PROPERTIES'] = get_queue_properties
    ctx.obj['DEAD_LETTER'] = dead_letter
    ctx.obj['PRETTY'] = pretty

    queue_process_obj = QueueProcess(ctx)
    queue_process_obj.spying_message_queue()


@main.command('peek_sub')
@click.pass_context
@click.option('--max_message_count', '-mc', required=False, default=5, help="Max message count. Default is 5")
@click.option('--pages', required=False, default=1, help="Number of pages to run. Default is 1")
@click.option('--get_queue_properties', '-qp', is_flag=True, help="Get queue properties")
@click.option('--dead_letter', '-dl', is_flag=True, help="Peek messages from dead letter")
@click.option('--pretty', is_flag=True, help="Pretty json log messages")
def peek_sub(ctx, max_message_count, pages, get_queue_properties, dead_letter, pretty):
    """
            :   Peek messages from subscription.
    """
    ctx.obj['MAX_MESSAGE_COUNT'] = max_message_count
    ctx.obj['PAGES'] = pages
    ctx.obj['GET_QUEUE_PROPERTIES'] = get_queue_properties
    ctx.obj['DEAD_LETTER'] = dead_letter
    ctx.obj['PRETTY'] = pretty

    queue_process_obj = TopicProcess(ctx)
    queue_process_obj.spying_message()


@main.command('purge_queue')
@click.pass_context
@click.option('--confirm', prompt='Please type the word [confirm]')
@click.option('--dead_letter', '-dl', is_flag=True, help="Purge dead letter messages")
@click.option('--max_message_count', '-mc', required=False, default=50, help="Max message count. Default is 50")
@click.option('--to_dead_letter', is_flag=True, help="Sends messages to dead_letter")
def purge_queue(ctx, confirm, dead_letter, max_message_count, to_dead_letter):
    """
            :   Purge all messages from queue.
    """

    if confirm.lower() == "confirm":
        ctx.obj['MAX_MESSAGE_COUNT'] = max_message_count
        ctx.obj['DEAD_LETTER'] = dead_letter
        ctx.obj['TO_DEAD_LETTER'] = to_dead_letter
        queue_process_obj = QueueProcess(ctx)
        queue_process_obj.purge()
    else:
        colorama.init()
        print(colorama.Fore.LIGHTRED_EX + 'Invalid word the operation will not proceed')


@main.command('purge_sub')
@click.pass_context
@click.option('--confirm', prompt='Please type the word [confirm]')
@click.option('--dead_letter', '-dl', is_flag=True, help="Purge dead letter messages")
@click.option('--max_message_count', '-mc', required=False, default=50, help="Max message count. Default is 50")
@click.option('--to_dead_letter', is_flag=True, help="Sends messages to dead_letter")
def purge_subscription(ctx, confirm, dead_letter, max_message_count, to_dead_letter):
    """
            :   Purge all messages from subscription
    """

    if confirm.lower() == "confirm":
        ctx.obj['MAX_MESSAGE_COUNT'] = max_message_count
        ctx.obj['DEAD_LETTER'] = dead_letter
        ctx.obj['TO_DEAD_LETTER'] = to_dead_letter
        topic_process_obj = TopicProcess(ctx)
        topic_process_obj.purge()
    else:
        colorama.init()
        print(colorama.Fore.LIGHTRED_EX + 'Invalid word the operation will not proceed')


@main.command('message_queue')
@click.pass_context
@click.option('--input_file', '-i', type=click.File('rb'), required=True, help="Directory to get message file")
def message_queue(ctx, input_file):
    """
            :   Send messages to a service bus queue
    """

    queue_process_obj = QueueProcess(ctx)
    queue_process_obj.message(input_file)


if __name__ == '__main__':
    main()

