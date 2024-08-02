import sys
import json
import boto3
import logging
import datetime
import requests
import subprocess
import pandas as pd
from pick import pick
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
from rich.console import Console



## Add console session
console = Console()

# Add logging
log_date = str(datetime.datetime.now().strftime("%d-%m-%y--%HH-%MM-%SS"))
Path("./log/").mkdir(parents=True, exist_ok=True)
sleep(1)
logging.basicConfig(filename="./log/trace-log-"+log_date+'.log', encoding='utf-8', level=logging.DEBUG)


## Check aws-vault credential
def run_aws_vault():
    cmd = f"aws-vault list --profiles"

    with console.status("[bold green]Checking aws-vault credentials...") as status:
        sleep(1)
        try:
            cmd_exec = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            console.log(f"[green]Done Listing AWS Profile from local machine !")
            vault_list = cmd_exec.stdout.splitlines()

        except subprocess.CalledProcessError as e:
            console.log(f"Error while running command : {e}")
            logging.error(f"Error while running command : {e}")

    pass

    return vault_list


## Select AWS Profie
def select_aws_profile():
    
    options = run_aws_vault()
    title = f"[AWS] Select AWS Profiles: "
    option, index = pick(options, title, indicator="\b>>", default_index=1)

    console.log(f"[bold dodger_blue2]AWS Profile used:[/bold dodger_blue2]",option)

    pass

    return option

def select_aws_region():

    url = "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')

    region_table_data = []

    for row in table.find_all('tr'):
        # Get all cells in the row
        cells = row.find_all('td')
        # Extract the text from each cell and store it in a list
        row_data = [cell.get_text(strip=True) for cell in cells]
        # Append the row data to the region_table_data list if the row is not empty
        if row_data:
            region_table_data.append(row_data)

    df = pd.DataFrame(region_table_data, columns=['region_code', 'region_name', 'opt_in_status'])

    df['region_code'] = df['region_code'].str.replace(r"[\[\]']", '', regex=True)

    filter_df = df['region_code']

    df_region_data = filter_df.values.tolist()

    options = df_region_data
    title = f"[AWS] Select AWS Region: "
    option, index = pick(options, title, indicator="\b>>", default_index=1)
    console.log(f"[bold dodger_blue2]AWS Region used:[/bold dodger_blue2]",option)

    selected_region = option

    pass

    return selected_region

## Login with aws-vault profile
def run_profile_login(profile, region):
    cmd = f"aws-vault login {profile} --region={region}"
    
    with console.status("[bold dark_orange3]Logging into AWS with aws-vault...") as status:
        sleep(1)
        try:
            cmd_exec = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            console.log(f"[green]Done Logging into AWS with aws-vault !")

        except subprocess.CalledProcessError as e:
            console.log(f"Error while running command : {e}")
            logging.error(f"An error occurred while logging into AWS with aws-vault: {e}")

## Check AWS Profile Session
def check_aws_session(profile, region):
    export_profile = f"export AWS_PROFILE={profile} && export AWS_REGION={region}"
    
    cmd = f"{export_profile} && aws sts get-caller-identity"

    with console.status("[bold dark_orange3]Checking AWS Session...") as status:
        sleep(1)
        try:

            cmd_exec = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(cmd_exec.stdout)
            console.log(f"[green]Done Checking AWS Session !")

            aws_session = cmd_exec.stdout

        except subprocess.CalledProcessError as e:
            console.log(f"Error while running command : {e}")
            logging.error(f"An error occurred while checking AWS session: {e}")

        return aws_session

## Run AWS Elasticache Function to get data
def elasticache_func(profile, region):
    boto3.setup_default_session(profile_name=profile, region_name=region)

    ecache = boto3.client('elasticache')
    get_ecache_clusters = ecache.describe_cache_clusters()

    json_obj = json.dumps(get_ecache_clusters, indent=4, default=str)

    elasticache_path =  "./exported-elasticache/"
    Path("./exported-elasticache/").mkdir(parents=True, exist_ok=True)

    ecache_json_filename = elasticache_path+"elasticache-"+profile+"-"+region+".json"

    try:
        with open(ecache_json_filename, "w") as json_output_file:
            json_output_file.write(json_obj)
        console.log(f"[green]Done getting data for elasticache !")

    except Exception as e:
        console.log(f"Error while running command : {e}")
        logging.error(f"An error occurred while getting elasticache data: {e}")


## Define main function process
def main():
    
    ## Pass AWS Profile selection
    profile = select_aws_profile()
    region = select_aws_region()

    try:
        run_profile_login(profile, region)
        check_aws_session(profile, region)
        elasticache_func(profile, region)
    except Exception as e:
        console.log(f"Error while running command : {e}")
        logging.error(f"An error occurred, refer to this error: {e}")
        sys.exit(1)


## Run all function process
if __name__ == "__main__":
    main()
