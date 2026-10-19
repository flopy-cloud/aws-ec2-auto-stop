import boto3

ec2 = boto3.client("ec2")


def lambda_handler(event, context):
    action = event.get("action")
    if action not in ("start", "stop"):
        raise ValueError("action debe ser 'start' o 'stop'")

    # Solo toca instancias con la etiqueta AutoStop=true
    estado_origen = "stopped" if action == "start" else "running"
    respuesta = ec2.describe_instances(
        Filters=[
            {"Name": "tag:AutoStop", "Values": ["true"]},
            {"Name": "instance-state-name", "Values": [estado_origen]},
        ]
    )

    ids = [
        i["InstanceId"]
        for r in respuesta["Reservations"]
        for i in r["Instances"]
    ]

    if not ids:
        print(f"No hay instancias para {action}")
        return {"action": action, "instances": []}

    if action == "stop":
        ec2.stop_instances(InstanceIds=ids)
    else:
        ec2.start_instances(InstanceIds=ids)

    print(f"{action}: {ids}")
    return {"action": action, "instances": ids}