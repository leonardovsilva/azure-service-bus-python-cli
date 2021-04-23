import click
from queue_process import QueueProcess


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--verbose', '-v', is_flag=True,
              help="Increase output verbosity level")
def main(ctx, verbose):
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
    #config_obj = config.Config()
    #config_obj.init()


@main.command('peek_queue')
@click.pass_context
@click.option('--queue_name', '-n', required=True, help="Name of the message queue that will be peek")
@click.option('--max_message_count', '-mc', required=False, default=None, help="Max message count")
@click.option('--log_path', '-l', required=False, default=None, help="Path to log console outputs")
@click.option('--get_queue_properties', '-qp', is_flag=True, help="Get queue properties")
@click.option('--dead_letter', '-dl', is_flag=True, help="Peek messages from dead letter queue")
def peek_messages(ctx, queue_name, max_message_count, log_path, get_queue_properties, dead_letter):
    """
            :   Peek messages from queue.
    """
    ctx.obj['QUEUE_NAME'] = queue_name
    ctx.obj['MAX_MESSAGE_COUNT'] = max_message_count
    ctx.obj['LOG_PATH'] = log_path
    ctx.obj['GET_QUEUE_PROPERTIES'] = get_queue_properties
    ctx.obj['DEAD_LETTER'] = dead_letter

    queue_process_obj = QueueProcess()
    queue_process_obj.spying_message_queue(ctx)


if __name__ == '__main__':
    main()

