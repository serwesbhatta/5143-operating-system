from texttable import Texttable
from .call_api import call_api
from .get_flags import get_flags
from cmd_pkg.fs_state_manager import Fs_state_manager
from .get_owner_name import get_owner_name


def human_readable_size(size):
    """Convert size in bytes to a human-readable format."""
    for unit in ["", "K", "M", "G", "T", "P"]:
        if size < 1024:
            return f"{size:.1f}{unit}B"
        size /= 1024
    return f"{size:.1f}PB"  # In case size is very large


def format_permissions(user_permissions, world_permissions, is_directory=False):
    """Convert permission numbers into rwx format for user/group/others."""
    permission_str = "d" if is_directory else "-"

    permission_str += "r" if user_permissions[0] == 1 else "-"
    permission_str += "w" if user_permissions[1] == 1 else "-"
    permission_str += "x" if user_permissions[2] == 1 else "-"

    permission_str += "---"

    permission_str += "r" if world_permissions[0] == 1 else "-"
    permission_str += "w" if world_permissions[1] == 1 else "-"
    permission_str += "x" if world_permissions[2] == 1 else "-"

    return permission_str


def ls(params=None):
    """Simulates the ls command with flags -a, -l, and -h."""
    # Parse the parameters (flags)
    show_hidden = False
    long_format = False
    human_format = False

    allowed_flags = ["l", "a", "h"]
    flags_response = get_flags(allowed_flags, params)
    if flags_response["invalid_flags"]:
        return {
            "status": "fail",
            "message": "\nInvalid flags"
        }
    flags = flags_response["flags"]

    if flags:
        if "a" in flags:
            show_hidden = True
        if "l" in flags:
            long_format = True
        if "h" in flags:
            human_format = True


    # Fetch files and directories from the database
    pid = Fs_state_manager.get_pid()
    oid = Fs_state_manager.get_oid()

    try:
        # Fetch files from the 'files' table
        file_filters = {"oid": oid, "pid": pid}
        files_response = call_api("files", params=file_filters)

    except:
        return {
            "status": "fail",
            "message": "\nCannot make a call to api for getting files",
        }

    try:
        # Fetch directories from the 'directories' table
        dir_filters = {"oid": oid, "pid": pid}
        dirs_reponse = call_api("dirs", params=dir_filters)

    except:
        return {
            "status": "fail",
            "message": "\nCannot make a call to api for getting directories",
        }

    if files_response["status"] == "fail" and dirs_reponse["status"] == "fail":
        return {"status": "fail", "message": "\nNo files or directories found."}

    files = files_response["message"]
    directories = dirs_reponse["message"]

    # Prepare table output
    table = Texttable()
    table.set_deco(Texttable.HEADER)

    # Set a maximum width
    table.set_max_width(0)  # 0 allows for unlimited width

    # If long format, add headers for permissions, owner, size, and date
    if long_format:
        table.header(
            ["Permissions", "Owner", "Owner ID", "Size", "Created", "Modified", "Name"]
        )

    if dirs_reponse["status"] == "success":
        # Process directories first
        for directory in directories:
            dir_name = directory["name"]
            dir_user_permissions = []

            read_permission = directory["read_permission"]
            write_permission = directory["write_permission"]
            execute_permission = directory["execute_permission"]
            dir_user_permissions = [read_permission, write_permission, execute_permission]

            world_read = directory["world_read"]
            world_write = directory["world_write"]
            world_execute = directory["world_execute"]
            dir_world_permissions = [world_read, world_write, world_execute]

            dir_owner_id = directory["oid"]
            dir_owner_name = get_owner_name(dir_owner_id)
            dir_created_at = directory["created_at"]
            dir_modified_at = directory["modified_at"]

            # Skip hidden directories unless -a is provided
            if not show_hidden and dir_name.startswith("."):
                continue

            if long_format:
                # Build the output for long listing (-l) format
                permissions_str = format_permissions(
                    dir_user_permissions, dir_world_permissions, is_directory=True
                )
                table.add_row(
                    [
                        permissions_str,
                        dir_owner_name,
                        dir_owner_id,
                        0,
                        dir_created_at,
                        dir_modified_at,
                        f"{dir_name}/",
                    ]
                )
            else:
                table.add_row([f"{dir_name}/"])

    if files_response["status"] == "success":
        # Process files
        for file_entry in files:
            file_name = file_entry["name"]
            file_size = file_entry["size"]

            read_permission = file_entry["read_permission"]
            write_permission = file_entry["write_permission"]
            execute_permission = file_entry["execute_permission"]
            file_user_permissions = [read_permission, write_permission, execute_permission]

            world_read = file_entry["world_read"]
            world_write = file_entry["world_write"]
            world_execute = file_entry["world_execute"]
            file_world_permissions = [world_read, world_write, world_execute]

            file_owner_id = file_entry["oid"]
            file_owner_name = get_owner_name(file_owner_id)
            file_created_at = file_entry["creation_date"]
            file_modified_at = file_entry["modified_date"]

            # Skip hidden files unless -a is provided
            if not show_hidden and file_name.startswith("."):
                continue

            if long_format:
                # Convert size to human-readable format if -h is provided
                if human_format:
                    file_size = human_readable_size(file_size)

                # Build the output for long listing (-l) format
                permissions_str = format_permissions(
                    file_user_permissions, file_world_permissions
                )
                table.add_row(
                    [
                        permissions_str,
                        file_owner_name,
                        file_owner_id,
                        file_size,
                        file_created_at,
                        file_modified_at,
                        file_name,
                    ]
                )
            else:
                table.add_row([file_name])

    table_str = table.draw()

    # Return the formatted table as a string
    return {"status": "success", "message": f"\n{table_str}"}
