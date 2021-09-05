from events import Events

class EventHandler(Events):

    __events__ = (
        'on_connected',
        'on_disconnected',
        'on_reconnect',
        'on_ping',
        'on_join', 
        'on_part', 
        'on_message', 
        'on_notice', 
        'on_command',
        'on_user_notice',
        'on_user_state',
        'on_room_state',
        'on_clear_message',
        'on_host_target',
        'on_startup',
        'on_shutdown',
        'on_error',
        'on_newday'
    )