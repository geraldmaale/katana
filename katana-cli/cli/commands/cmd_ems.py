import os
import requests
import json
import yaml
import subprocess
import click
import datetime

@click.group()
def cli():
    """Manage EMS"""
    pass


@click.command()
def ls():
    """
    List WIMs
    """

    url = "http://localhost:8000/api/ems"
    r = None
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        json_data = json.loads(r.content)
        print(console_formatter("EMS_ID", "CREATED AT"))
        for i in range(len(json_data)):
            print(console_formatter(
                json_data[i]["_id"],
                datetime.datetime.fromtimestamp(json_data[i]["created_at"]).strftime('%Y-%m-%d %H:%M:%S')))

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)


@click.command()
@click.argument('id')
def inspect(id):
    """
    Display detailed information of EMS
    """
    url = "http://localhost:8000/api/ems/"+id
    r = None
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        json_data = json.loads(r.content)
        click.echo(json.dumps(json_data, indent=2))
        if not json_data:
            click.echo("Error: No such EMS: {}".format(id))
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)


@click.command()
@click.option('-f', '--file', required=True, type=str, help='yaml file with EMS details')
def add(file):
    """
    Add new EMS
    """
    with open(file, 'r') as stream:
        data = yaml.load(stream)

    url = "http://localhost:8000/api/ems"
    r = None
    try:
        r = requests.post(url, json=json.loads(json.dumps(data)), timeout=10)
        r.raise_for_status()

        click.echo(r.content)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        click.echo(r.content)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)


cli.add_command(ls)
cli.add_command(inspect)
cli.add_command(add)


def console_formatter(uuid,created_at):
    return '{0: <40}{1: <25}'.format(
        uuid,
        created_at
    )