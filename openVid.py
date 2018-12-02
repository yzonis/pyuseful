import subprocess as sp
import matplotlib.pyplot
import os

def openVid(outPath,dims):
    '''
    openVid(outPath,dims) opens an ffmpeg process to write a new video
    in the given path 'outPath', with the image dimensions 'dims', and
    returns the process' handle so that the user could send the binary
    images to it through stdin. The images should be sent as a binary
    series with size (dims[0]xdims[1]x3)-bytes

    :param outPath: path to write the video to - video is in .mp4 format
    :param dims: dimensions of the video image in pixels

    :return: a handle to the process (using python subprocess package)
             pending images from its stdin
    '''

    ffmpegPath = 'ffmpeg.exe'
    ffmpegPath = os.path.realpath(ffmpegPath)
    outPath    = os.path.realpath(outPath)

    ########
    # Action
    ########

    command = [ ffmpegPath,
                '-y', # (optional) overwrite output file if it exists
                '-f', 'rawvideo',
                '-vcodec','rawvideo',
                '-s', str(dims[0])+'x'+str(dims[1]), # size of one frame
                '-pix_fmt', 'rgb24',
                '-r', '20', # frames per second
                '-i', '-', # The input comes from a pipe
                '-an', # Tells FFMPEG not to expect any audio
                '-vcodec', 'mpeg4',
                '-b:v','5M', # target bit-rate
                outPath ]

    return sp.Popen(command,shell=True,stdin=sp.PIPE,stderr=sp.PIPE)

def addFrame(proc,fig):
    fig.canvas.draw()
    proc.stdin.write(fig.canvas.tostring_rgb())

def closeVid(proc):
    if proc:
        proc.stdin.close()
        if proc.stderr is not None:
            proc.stderr.close()
        proc.wait()
