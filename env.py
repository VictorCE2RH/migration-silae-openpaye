import os


def getLogs(domain) -> tuple[str, str]:
    envKey = f"OP_LOGS_{domain}"
    op_logs = os.getenv(envKey)
    if not op_logs:
        raise Exception(
            f"Env '{envKey}' does not exist, add it to var env : {envKey}=\"email,password\""
        )
    logs = op_logs.split(",")
    if len(logs) != 2:
        raise Exception(
            f'Env var {envKey} wrong format. valid format: {envKey}="email,password"'
        )

    return logs[0], logs[1]
