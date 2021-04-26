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
    #config_obj = config.Config()
    #config_obj.init()


@main.command('peek_queue')
@click.pass_context
@click.option('--max_message_count', '-mc', required=False, default=5, help="Max message count. Default is 5")
@click.option('--pages', required=False, default=1, help="Number of pages to run. Default is 1")
@click.option('--get_queue_properties', '-qp', is_flag=True, help="Get queue properties")
@click.option('--dead_letter', '-dl', is_flag=True, help="Peek messages from dead letter queue")
@click.option('--pretty', is_flag=True, help="Pretty json log messages")
def peek_messages(ctx, max_message_count, pages, get_queue_properties, dead_letter, pretty):
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


@main.command('purge_queue')
@click.pass_context
@click.option('--queue_name', '-qn', required=True, help="Name of the message bus queue")
@click.option('--confirm', prompt='Please type the word [confirm]')
@click.option('--dead_letter', '-dl', is_flag=True, help="Purge dead letter messages")
@click.option('--max_message_count', '-mc', required=False, default=50, help="Max message count. Default is 50")
@click.option('--to_dead_letter', is_flag=True, help="Sends messages to dead_letter")
def purge_queue(ctx, queue_name, confirm, dead_letter, max_message_count, to_dead_letter):
    """
            :   Purge all messages from queue.
    """

    if confirm.lower() == "confirm":
        ctx.obj['MAX_MESSAGE_COUNT'] = max_message_count
        ctx.obj['DEAD_LETTER'] = dead_letter
        ctx.obj['TO_DEAD_LETTER'] = to_dead_letter
        print('TO_DEAD_LETTER')
        ctx.obj['QUEUE_NAME'] = queue_name
        queue_process_obj = QueueProcess(ctx)
        queue_process_obj.purge_queue()
    else:
        colorama.init()
        print(colorama.Fore.LIGHTRED_EX + 'Invalid word the operation will not proceed')


if __name__ == '__main__':
    main()

