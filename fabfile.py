# -*- coding: utf-8 -*-
from fabric.api import task, env, cd, run, require, local
from fabutils.env import set_env_from_json_file

@task
def environment(env_name):
    set_env_from_json_file('environments.json', env_name)

@task
def download_video(url):
    env.url = url
    require( 'site_dir' )
    with cd(env.site_dir):
        run("""youtube-dl {0}""".format(env.url))

@task
def add_video(url):
    env.url = url
    require( 'site_dir' )
    with cd(env.site_dir):
        run (""" echo '{url}' >> .config/youtube-dl/list_videos""".format(**env))

@task
def remove_all_videos():
    run(""" rm /media/storage/youtube/* """)

@task
def refresh_list():
    run("""rm ~/.config/youtube-dl/list_videos""")
    run("""touch ~/.config/youtube-dl/list_videos""")

@task
def download_list_videos():
    run(""" youtube-dl -a {site_dir}/.config/youtube-dl/list_videos""".format(**env))

@task
def sync_files(local_folder="/home/ripper/mysync"):

    env.local_folder= local_folder
    local("""rsync -chrtvzP -e "ssh -i /home/ripper/.ssh/personal" {user}@{hosts[0]}:{remote_folder} {local_folder}""".format(**env))

@task 
def trans_add(url, paused=True):
    env.torrent_url = url
    if( paused ):
        run("""transmission-remote {hosts[0]}:9091 --auth={transmission_user}:{transmission_pass} -aS {torrent_url}""".format(**env))
    else:
        run("""transmission-remote {hosts[0]}:9091 --auth={transmission_user}:{transmission_pass} -as {torrent_url}""".format(**env))

@task
def trans_ls():
    require('transmission_user', 'transmission_pass')
    run("""transmission-remote {hosts[0]}:9091 --auth={transmission_user}:{transmission_pass} -l""".format(**env))

@task
def trans_start_all():
    require('transmission_user', 'transmission_pass')
    run("""transmission-remote {hosts[0]}:9091 --auth={transmission_user}:{transmission_pass} -tall --start""".format(**env))

@task
def trans_stop_all():
    require('transmission_user', 'transmission_pass')
    run("""transmission-remote {hosts[0]}:9091 --auth={transmission_user}:{transmission_pass} -tall --stop""".format(**env))


