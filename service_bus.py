import click
import colorama
from queue_process import QueueProcess


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--verbose', '-v', is_flag=True,
              help="Increase output verbosity level")
@click.option('--queue_name', '-qn', required=False, help="Name of the message bus queue")
@click.option('--topic_name', '-tn', required=False, help="Name of the message bus topic")
@click.option('--subscription_name', '-sn', required=False, help="Name of the message bus subscription")
def main(ctx, verbose, queue_name, topic_name, subscription_name):
    group_commands = ['queue', 'topic']
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
    #config_obj = config.Config()
    #config_obj.init()


@main.command('peek_queue')
@click.pass_context
@click.option('--max_message_count', '-mc', required=False, default=None, help="Max message count")
@click.option('--log_path', '-l', required=False, default=None, help="Path to log console outputs")
@click.option('--get_queue_properties', '-qp', is_flag=True, help="Get queue properties")
@click.option('--dead_letter', '-dl', is_flag=True, help="Peek messages from dead letter queue")
def peek_messages(ctx, max_message_count, log_path, get_queue_properties, dead_letter):
    """
            :   Peek messages from queue.
    """
    ctx.obj['MAX_MESSAGE_COUNT'] = max_message_count
    ctx.obj['LOG_PATH'] = log_path
    ctx.obj['GET_QUEUE_PROPERTIES'] = get_queue_properties
    ctx.obj['DEAD_LETTER'] = dead_letter

    queue_process_obj = QueueProcess(ctx)
    queue_process_obj.spying_message_queue()


@main.command('purge_queue')
@click.pass_context
@click.option('--queue_name', '-qn', required=True, help="Name of the message bus queue")
@click.option('--confirm', prompt='Please type the word [confirm]')
@click.option('--log_path', '-l', required=False, default=None, help="Path to log console outputs")
@click.option('--dead_letter', '-dl', is_flag=True, help="Purge dead letter messages")
@click.option('--max_message_count', '-mc', required=False, default=None, help="Max message count")
def purge_queue(ctx, queue_name, confirm, log_path, dead_letter, max_message_count):
    """
            :   Peek messages from queue.
    """

    if confirm.lower() == "confirm":
        ctx.obj['MAX_MESSAGE_COUNT'] = max_message_count
        ctx.obj['LOG_PATH'] = log_path
        ctx.obj['DEAD_LETTER'] = dead_letter
        ctx.obj['QUEUE_NAME'] = queue_name
        queue_process_obj = QueueProcess(ctx)
        queue_process_obj.purge_queue()
    else:
        colorama.init()
        print(colorama.Fore.LIGHTRED_EX + 'Invalid word the operation will not proceed')


if __name__ == '__main__':
    main()

