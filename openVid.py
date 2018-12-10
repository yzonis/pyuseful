import subprocess as sp
import os
import time

class VideoWriter:
    '''
    VideoWriter uses an ffmpeg process to write a new .mp4 video
    in a given path. Image dimensions and total duration have
    to be provided by the user.

    ************
    Initializing
    ************

    v = VideoWriter(outPath,dims,dur)

    - outPath : the path to the output .mp4 video
    - dims    : an iterator with two integer elements, the first
                being the width and the second being the height of
                the video, in pixels
    - dur     : the total duration of the video in seconds

    NOTE: at this point no video file is created, instead a raw data
          file is created, it will contain all of the frames that the
          user will provide. The video file will be created after the
          user has finished filling all of the frames.

    **************
    Adding a frame
    **************

    v.addFrame(frame)

    frame : a 'bytes' type array of the raw rgb bytes of the frame.
            overall there should be 3xdims[0]xdims[1] bytes in the
            array. the bytes should be ordered such that the three
            bytes of each pixels are adjacent, and the order of
            pixels is either row by row or column by column, you'll
            have to try it out...

    ************
    Adding audio
    ************

    v.addAudio(audioPath)

    - audioPath : the path to the .wav file which the user wishes
                  to add to the video. should be the same duration
                  as the video

    **********************
    Writing the video file
    **********************

    v.writeVideo()

    Should be called after all frames and audio have been added.
    After writeVideo() is called, the video object is closed and
    is useless.

    '''

    def __init__(self,outPath,dims,vidFps,nFrames):
        self.outPath   = os.path.realpath(outPath)
        self.audioPath = ''

        ffmpegPath = '../ffmpeg/bin/ffmpeg.exe'
        ffmpegPath = os.path.realpath(ffmpegPath)

        self.command = [ ffmpegPath,
                         '-y', # (optional) overwrite output file if it exists
                         '-f', 'rawvideo',
                         '-vcodec','rawvideo',
                         '-s', str(dims[0])+'x'+str(dims[1]), # size of one frame
                         '-pix_fmt', 'rgb24',
                         '-r', str(vidFps), # frames per second
                         '-i', 'tmpVid.bin', # The input comes from the raw data file
                         '-an', # Tells FFMPEG not to expect any audio
                         '-vcodec', 'mpeg4',
                         '-b:v','5M', # target bit-rate
                         '-t',str(nFrames/vidFps), # video duration
                         outPath ]

        self.fid = open('tmpVid.bin','wb')

    def addFrame(self,frame):
        self.fid.write(frame)

    def addAudio(self,audioPath):
        audioPath_ = os.path.realpath(audioPath)
        self.command[14] = '-i'
        self.command.insert(15,audioPath_)

    def writeVideo(self):
        self.fid.close()
        time.sleep(1)
        p = sp.Popen(self.command,shell=True,stdin=sp.PIPE,stderr=sp.PIPE)
        p.wait()
        os.remove('tmpVid.bin')
