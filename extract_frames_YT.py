mport
youtube_dl

import sys
import os
import subprocess
import argparse


# ydl_opts = {}
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     meta = ydl.extract_info(
#         'https://www.youtube.com/watch?v=Vh9msqaoJZw', download=False)
#     print(meta['id'], meta['ext'])


def download_and_extract(download_url):
    # Get video meta info and then download using youtube-dl

    ydl_opts = {}

    # get meta info from the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            download_url, download=False)

    # download the video
    out = meta['id']
    extension = meta['ext']
    print("EXT:", extension)
    video_out = out + '.' + extension
    cmd = ['youtube-dl', '-f bestvideo[height<=?720]', '-o', video_out, download_url]
    subprocess.call(cmd)

    ffmpeg = '/bin/ffmpeg'
    # # call iframe-extraction : ffmpeg
    imgFilenames = 'frames/' + out + '_%03d.png'
    total_frames = meta['duration'] * meta['fps'] // 200
    fps_every = meta['duration'] // 10

    # keyframe
    bashCommand1 = "ffmpeg -i " + video_out + " -vf select='eq(pict_type\,I), gt(scene\,0.5), crop=in_h*16/9:in_h, scale=-2:460, crop=640:360:50:50' " + " -frames:v 200 -vsync vfr -vf fps=fps=1/10 " + imgFilenames

    # -i yosemiteA.mp4 -vf  "select=gt(scene\,0.5), scale=640:360" -vsync vfr yosemiteThumb%03d.png
    # scale=640:360,crop=in_h*16/9:in_h,scale=-2:360

    # thumbnail
    # bashCommand2 = "ffmpeg -ss 10 -i " + video_out + " -vf thumbnail=" + str(total_frames) + ",crop=in_h*16/9:in_h,scale=-2:360" + ",setpts=N/TB -r 1 " + imgFilenames
    bashCommand2 = "ffmpeg -ss 10 -i " + video_out + " -vf select=gt(scene\,0.3),scale=640:360,crop=in_h*16/9:in_h,scale=-2:360" + " -frames:v 200 -vsync vfr -vf fps=fps=1/" + str(
        fps_every) + " " + imgFilenames

    bashCommand3 = "ffmpeg -i " + video_out + " -vf select='gt(scene\,0.5),crop=in_h*16/9:in_h,scale=-2:460,crop=640:360:50:50' " + " -frames:v 200 -vsync vfr -vf fps=fps=1/10 "

    bashCommand4 = 'ffmpeg -i ' + 'video_out' + ' -ss 10 -vf "select=gt(scene\,0.3), crop=in_h*16/9:in_h, scale=-2:400,crop=640:360" -vsync vfr ' + imgFilenames

    # ffmpeg -ss 10 -i nQk7DWW4mz8.webm -vf "select=gt(scene\,0.5)" -frames:v 200 -vsync vfr -vf fps=fps=1/5 frames/out_%03d.png

    # bashCommand2 = "ffmpeg -i " + video_out + " -vf thumbnail=300,setpts=N/TB -r 1 " + imgFilenames

    print("COMMAND:", bashCommand1)
    print("total_frames:", total_frames)
    print("Frame every:", fps_every)

    # process = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()

    # subprocess.call(bashCommand1)

    os.system(bashCommand4)

    # Remove video the file afterwards
    # os.remove(video_out)

    return meta


def check_arg(args=None):
    # Command line options
    # Currently, only the url option is used

    parser = argparse.ArgumentParser(description='download video')
    parser.add_argument('-u', '--url',
                        help='download url', )
    parser.add_argument('-l', '--list',
                        help='list of YT URLs', )

    results = parser.parse_args(args)
    return (results.url, results.list)


'''
Usage sample:
    syntax: python iframe_extract.py -u url
    (ex) python iframe_extract.py -u https://www.youtube.com/watch?v=dP15zlyra3c
'''
if __name__ == '__main__':
    u, l = check_arg(sys.argv[1:])

    # if a txt is passed call the main function for each element
    if l:
        for line in open(l):
            download_and_extract(line)

    elif u:
        download_and_extract(u)