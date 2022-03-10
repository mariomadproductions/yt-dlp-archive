#!/usr/bin/env python3
import subprocess
import argparse
import datetime
import json
from pathlib import Path
import unicodedata
import re

#from https://github.com/django/django/blob/
#67b5f506a600a54658405cf821c14ada4080e61f/django/utils/text.py#L400
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")

def mk_video_dir(base_dir,url):
    video_dir = base_dir.joinpath(slugify(url,allow_unicode=False))
    video_dir.mkdir()
    return video_dir

def get_json_name_noext(video_dir):
    SUFFIX = '.info.json'
    for path in video_dir.glob(f'*{SUFFIX}'):
        return path.name[:-len(SUFFIX)]

def ren_video_dir(video_dir):
    new_name = Path(get_json_name_noext(video_dir))
    if new_name.exists():
        raise ValueError('New directory name already exists')
    else:
        video_dir.rename(new_name)

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
    result = subprocess.run(['yt-dlp', '--version'],
                             stdout=subprocess.PIPE)
    yt_dlp_ver = result.stdout.decode('utf8').strip()
    validate_yt_dlp_ver(yt_dlp_ver)
    return yt_dlp_ver

def dl_vid(yt_dlp_options,url,video_dir):
    subprocess.run(['yt-dlp'] + yt_dlp_options + [url],
    cwd=video_dir)

def write_info_file(date,yt_dlp_ver,yt_dlp_options,
                    video_dir):
    INFO_FILE_NAME = 'info.json'
    INFO_FILE_PATH = video_dir.joinpath(INFO_FILE_NAME)
    info_dict = {}
    info_dict['date_downloaded_on'] = date
    info_dict['yt_dlp_version'] = yt_dlp_ver
    info_dict['yt_dlp_options'] = yt_dlp_options

    with open(INFO_FILE_PATH, 'w') as info_file:
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

    video_dir = mk_video_dir(Path('.'),URL)
    dl_vid(YT_DLP_OPTIONS,URL,video_dir)
    write_info_file(DATE,YT_DLP_VER,YT_DLP_OPTIONS,
                    video_dir)
    ren_video_dir(video_dir)

if __name__ == '__main__':
    main()

