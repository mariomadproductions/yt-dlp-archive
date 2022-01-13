#!/usr/bin/env bash
import subprocess
import argparse
import datetime
import json

def get_date():
    #from https://stackoverflow.com/a/28147286/2352336
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

def validate_yt_dlp_ver(yt_dlp_ver):
    if len(yt_dlp_ver) != 10:
        raise ValueError('Date too short')
    #from https://stackoverflow.com/a/16870699/2352336
    try:
        datetime.datetime.strptime(yt_dlp_ver, '%Y.%m.%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        
def get_yt_dlp_ver():
    result = subprocess.run(['yt-dlp', '--version'],stdout=subprocess.PIPE)
    yt_dlp_ver = result.stdout.decode('utf8').strip()
    validate_yt_dlp_ver(yt_dlp_ver)
    return yt_dlp_ver

def dl_vid(yt_dlp_options,url):
    subprocess.run(['yt-dlp'] + yt_dlp_options + [url])

def write_info_file(date,yt_dlp_ver,yt_dlp_options):
    INFO_FILE_NAME = 'info.json'
    
    info_dict = {}
    info_dict['date_downloaded_on'] = date
    info_dict['yt_dlp_version'] = yt_dlp_ver
    info_dict['yt_dlp_options'] = yt_dlp_options
    
    with open(INFO_FILE_NAME, 'w') as info_file:
        json.dump(info_dict,info_file, indent=4)

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('url')
    args = arg_parser.parse_args()
    
    YT_DLP_OPTIONS = ['--write-info-json',
                      '--write-thumbnail',
                      '--write-annotations',
                      '--write-sub',
                      '--all-subs',
                      '--write-comments']
    DATE = get_date()
    YT_DLP_VER = get_yt_dlp_ver()
    URL = args.url
    
    dl_vid(YT_DLP_OPTIONS,URL)
    write_info_file(DATE,YT_DLP_VER,YT_DLP_OPTIONS)

if __name__ == '__main__':
    main()

