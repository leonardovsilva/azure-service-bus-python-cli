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
@click.option('--queue_name', '-n', required=True, help="Peek messages from queue")
@click.option('--max_message_count', '-mc', required=False, default=None, help="Max message count")
@click.option('--log_path', '-l', required=False, default=None, help="Path to log console outputs")
def peek_messages(ctx, queue_name, max_message_count, log_path):
    """
            :   Peek messages from queue.
    """
    ctx.obj['QUEUE_NAME'] = queue_name
    ctx.obj['MAX_MESSAGE_COUNT'] = max_message_count
    ctx.obj['LOG_PATH'] = log_path

    queue_process_obj = QueueProcess()
    queue_process_obj.spying_message_queue(ctx)


if __name__ == '__main__':
    main()

