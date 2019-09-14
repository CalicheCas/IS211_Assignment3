#!/usr/bin/env python3

import csv
from datetime import datetime
import argparse
import requests
import re

parser = argparse.ArgumentParser("text_processor")
parser.add_argument(
    "url",
    help="processes csv file data. Expects a url as args",
    type=str
)

args = parser.parse_args()


def download_data(url):
    """
    Function downloads csv content from a given
    url and returns a reader object with comma delimiter.

    :param str url:
    :return: list
    """

    with requests.Session() as session:
        download = session.get(url)

        decoded_content = download.content.decode('utf-8')

        csv_reader = csv.reader(decoded_content.splitlines(), delimiter=',')

        return list(csv_reader)


def image_file_finder(data):
    """
    Function iterates over a list (cvs) finds the total number of
    image type files (.jpg, .gif or .png ) and return the percentage
    of image files found in the list.

    :param data:
    :return: percentage
    """

    regex = "\.jpg|\.gif|\.png"
    image_list = list()

    for entry in data:
        # Get file path.
        file_path = entry[0]

        if re.search(regex, file_path, re.IGNORECASE):
            image_list.append(file_path)

    return percentage_calculator(len(data), len(image_list))


def percentage_calculator(dividend, divisor):
    return (divisor / dividend) * 100


def user_agent_finder(data):
    """
    Function returns a dictionary with total web browser counts.
    :param data:
    :return: dict
    """

    regx1 = 'Chrome'
    regx2 = 'Firefox'
    regx3 = 'Safari'
    regx4 = 'Trident'

    result = {"Chrome": 0,
              "Safari": 0,
              "Firefox": 0,
              "IE": 0,
              "Other": 0}

    for entry in data:
        # Get User Agent.
        user_agent = entry[2]

        # Find Chrome
        if re.search(regx1, user_agent):
            result['Chrome'] += 1
        # Find Firefox
        elif re.search(regx2, user_agent):
            result['Firefox'] += 1
        # Find IE
        elif re.search(regx3, user_agent):
            result['IE'] += 1
        # Find Safari
        elif re.search(regx4, user_agent):
            result['Safari'] += 1
        # Find Others
        else:
            result['Other'] += 1

        ordered = {}
        for key, value in reversed(sorted(result.items(), key=lambda item: item[1])):
            ordered[key] = value

    return ordered


def date_analyzer(data):
    hits_dict = {}
    for entry in data:
        # Get datetime.
        date_time = datetime.strptime(entry[1], '%Y-%m-%d %H:%M:%S')
        hour = date_time.hour

        if hour in hits_dict:
            hits_dict[hour] += 1
        else:
            hits_dict[hour] = 0

    ordered_dict = {}

    for key, value in hits_dict.items():
        ordered_dict[key] = value

    return ordered_dict


def main(args):

    csv_file = download_data(args)

    percentage = image_file_finder(csv_file)

    print("Image requests account for {:.2f} % of all requests \n".format(percentage))

    # Get ordered dictionary of user agents
    ua = user_agent_finder(csv_file)
    keys = list(ua.keys())
    key = keys[0]
    value = ua[key]

    # Print most popular browser
    print("The most popular browser is {:s} with {:d} hits \n".format(key, value))

    # Print all browsers ordered by popularity
    print("Browser Ranking \n===============")
    for k, v in ua.items():
        print("{:s}\t= {:d}".format(k, v))

    # Get ordered hits
    hits = date_analyzer(csv_file)

    # Print ordered hits ordered by hour
    print("\nHits per Hour\n=============")

    for k, v in hits.items():
        print("Hour {:d} has {:d} hits.".format(k, v))


if __name__ == "__main__":

    main(args.url)
