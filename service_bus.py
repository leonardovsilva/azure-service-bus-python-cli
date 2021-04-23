import click
import config
from queue_process import QueueProcess

'''if __name__ == '__main__':
    config_obj = config.Config()
    config_obj.init()
    time.sleep(0.1)
    mainMenu = main_menu.MainMenu()
    mainMenu.display()'''


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--verbose', '-v', is_flag=True,
              help="Increase output verbosity level")
def main(ctx, verbose):
    group_commands = ['queue', 'topic']
    """
        serviceBusPythonExplorer is a command line tool that helps management Azure Service Bus.\n
          example: python service_bus.py peek -n [queue_name]
    """
    ctx.obj = {} if not ctx.obj else ctx.obj

    if ctx.invoked_subcommand is None:
        click.echo("Specify one of the commands below")
        print(*group_commands, sep='\n')

    config_obj = config.Config()
    config_obj.init(verbose)
    ctx.obj['VERBOSE'] = verbose


@main.command('peek')
@click.pass_context
@click.option('--queue_name', '-n', prompt=True, default=None,
              required=True, help="Peek messages from queue")
def peek_messages(ctx, queue_name):
    """
            :   Peek messages from queue.
    """
    queue_process_obj = QueueProcess()
    queue_process_obj.spying_message_queue(queue_name, ctx)


if __name__ == '__main__':
    main()

