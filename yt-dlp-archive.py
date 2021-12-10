#!/usr/bin/env bash
import subprocess
import argparse

def write_ver():
    stdout_file_path = 'yt_dlp_ver_stdout.txt'
    stderr_file_path = 'yt_dlp_ver_stderr.txt'
    
    with open(stdout_file_path,'w') as stdout_file,\
    open(stderr_file_path,'w') as stderr_file:
        subprocess.run(['yt-dlp', '--version'],
                       stdout=stdout_file,
                       stderr=stderr_file)

def dl_vid(url):
    subprocess.run(['yt-dlp',
                    '--write-info-json',
                   '--write-comments',
                   '--write-thumbnail',
                   '--write-subs',
                    url])

def write_finish_tag():
    finish_tag_file_path = 'finished.txt'
    
    with open(finish_tag_file_path, 'w') as finish_tag_file:
        finish_tag_file.write('finished.txt')
        
    
def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('url')
    args = arg_parser.parse_args()
    write_ver()
    dl_vid(args.url)
    write_finish_tag()

if __name__ == '__main__':
    main()
    
