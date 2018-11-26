import youtube_dl
import sys
import os
import subprocess
import argparse

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

    # set ffmpeg according to your system <-- UPDATE
    ffmpeg = '/bin/ffmpeg'

    # call frame-extraction : ffmpeg
    imgFilenames = 'frames/' + out + '_%03d.png'
    total_frames = meta['duration'] * meta['fps']

    # define extracted frames per seconds. This formula ensures that no part of the video will be ignored in command1
    if meta['duration'] < 600:
        fps_every = "1/6"
    else:
        fps_every = "1/"+str(meta['duration']//100)

    # selects one representative frame from each set of x frames. This formula ensures that no part of the video will be ignored in command3
    if meta['duration'] < 600:
        thumbnail_every = 6*abs(meta['fps'])
    else:
        thumbnail_every = (meta['duration']//100)*meta['fps']

    # Define a way to extract images
    # # -frames:v sets maximum number of extracted images per input
    # # -ss sets start time in seconds

    # # keyframe. fps=fps=10/60 means 10 frames out of 60 every seconds
    bashCommand1 = "ffmpeg -i " + video_out + " -ss 5 -t " + str(meta['duration']-15) + " -vf 'select=eq(pict_type\,I),fps=fps="+fps_every+",scale=-2:380,crop=640:360' -frames:v 150 -vsync vfr  " + imgFilenames

    # # scene differentiator
    bashCommand2 = "ffmpeg -i " + video_out + " -ss 5 -t " + str(meta['duration']-15) + " -vf 'select=gt(scene\,0.7),scale=-2:380,crop=640:360' -frames:v 150 -vsync vfr  " + imgFilenames

    # # create thumbnail out of certain number of frames. setpts and r are set to avoid duplicates
    bashCommand3 = "ffmpeg -i " + video_out + " -ss 5 -t " + str(meta['duration']-15) + " -vf 'thumbnail=" + str(thumbnail_every) + ",scale=-2:380,crop=640:360',setpts=N/TB -r 1 -frames:v 150 " + imgFilenames
    

    # ffmpeg -ss 10 -i nQk7DWW4mz8.webm -vf "select=gt(scene\,0.5)" -frames:v 200 -vsync vfr -vf fps=fps=1/5 frames/out_%03d.png

    # bashCommand2 = "ffmpeg -i " + video_out + " -vf thumbnail=300,setpts=N/TB -r 1 " + imgFilenames

    print("COMMAND:", bashCommand1)
    print("total_frames:", total_frames)
    print("Frame every:", fps_every)
    print("Thumbnail every:", thumbnail_every)


    # process = subprocess.Popen(bashCommand1.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()

    # subprocess.call(bashCommand1)
    # call frame-extraction : ffmpeg
    os.system(bashCommand1)

    # Remove video the file afterwards
    os.remove(video_out)

    return meta


def check_arg(args=None):

    # Command line options
    parser = argparse.ArgumentParser(description='download video')
    parser.add_argument('-u', '--url',
                        help='download url', )
    parser.add_argument('-l', '--list',
                        help='list of YT URLs', )

    results = parser.parse_args(args)
    return (results.url, results.list)


'''
Usage sample:
    Install ffmpeg on your system and also youtube_dl using pip.
    syntax:
    (ex) python iframe_extract.py -l list_of_yt_links.txt
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