import boto3
import logging
import os

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    action = event.get("action", "").lower()
    if action not in ["start", "stop"]:
        return {"statusCode": 400, "body": f"Invalid action: {action}. Use 'start' or 'stop'."}

    # Gather data from all supported formats
    # 1. 'regions' dictionary format: {"us-east-1": ["i-1"], "us-west-2": ["i-2"]}
    region_to_ids = event.get("regions", {})
    
    # 2. Singular/List formats (backward compatibility)
    instance_id = event.get("instance_id")
    instance_ids = event.get("instance_ids", [])
    default_region = event.get("region") or os.environ.get("AWS_REGION", "us-east-1")

    # Consolidate backward compatibility inputs into the mapping
    if instance_id or instance_ids:
        all_ids = set(instance_ids)
        if instance_id:
            all_ids.add(instance_id)
        
        if default_region not in region_to_ids:
            region_to_ids[default_region] = []
        region_to_ids[default_region].extend(list(all_ids))

    if not region_to_ids:
        return {"statusCode": 400, "body": "Missing instance IDs or regions"}

    results = []
    errors = []

    for region, ids in region_to_ids.items():
        if not ids:
            continue
            
        try:
            logger.info(f"Performing action '{action}' on instances in {region}: {ids}")
            ec2 = boto3.client('ec2', region_name=region)
            
            if action == "start":
                ec2.start_instances(InstanceIds=ids)
            elif action == "stop":
                ec2.stop_instances(InstanceIds=ids)

            results.append({
                "region": region,
                "status": f"Successfully {'started' if action == 'start' else 'stopped'}",
                "instance_ids": ids
            })
        except Exception as e:
            err_msg = f"Error in {region}: {str(e)}"
            logger.error(err_msg)
            errors.append(err_msg)

    status_code = 200 if not errors else (207 if results else 500)
    
    return {
        "statusCode": status_code,
        "body": {
            "action": action,
            "results": results,
            "errors": errors
        }
    }