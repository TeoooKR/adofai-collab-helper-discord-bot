# Discord Music Management Bot
This is a bot that helps manage game ADOFAI collab on discord.

## Invite Bot
https://discord.com/oauth2/authorize?client_id=1285786090069950536&permissions=8&integration_type=0&scope=applications.commands+bot

## Commands

- `/map_add <song_name> [deadline]` - Add a map.
- `/map_delete <song_name>` - Delete a map.
- `/map_set <song_name> <new_name> [new_deadline]` - Modify map information.
- `/part_add <song_name> <part_name> [start_time] [end_time] [deadline]` - Add a part to a map.
- `/part_delete <song_name> <part_name>` - Delete a part from a map.
- `/part_set <song_name> <part_name> [new_part_name] [start_time] [end_time] [deadline]` - Modify part information.
- `/editor_add <user> <song_name> [part_name] [role] [display_name]` - Add an editor to a map or part.
- `/editor_delete <user> <song_name> [part_name]` - Delete an editor from a map or part.
- `/editor_set <user> <song_name> [part_name] [new_role] [new_display_name]` - Modify editor information.
- `/progress <song_name> [part_name] [progress_status]` - Update progress status for a map or part.\
- `/list` - List all registered tracks and parts.

