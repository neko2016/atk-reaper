# **************************************
# 
# sine example 2:
# 
# generate, display, and write out
# an two enveloped sine waves, in quadrature
# 
# sin_1 code has been modified in a few ways:
# --phase is now a list of two values
#   which will generate an interleaved
#   quadrature signal pair
# 
# --then, the envelope must be interleaved
#   so it will broadcast correctly when
#   multiplied against the signal
# 
# --additionally, the sound file output
#   needs to be set for two channels out
# 
# the signal is generated 'all at once'
# using functional syntax
# 
# **************************************

from muse import *              # import muse, for DSP
import pylab as pl              # import pylab, for viewing

# parameters
sr = 44100                      # sr!

gain = -3.                      # in dB
dur = .1                        # in secs
freq = 110.                     # in Hz
phase = [0., halfPi]            # in radians
env_durs = dur * array([.1, .5, 1.]) # env breakpoints, in sec

# parameters for output file
file_type   = 'wav'             # 'wav' chosen as both PSL and scikits.audiolab
encoding    = 'pcm24'           #       support read/write 'pcm24
channels    = 2                 # stereo out

file_path   = '/Volumes/Audio/test/'
file_name   = 'sin_2'
out_file    = file_path + file_name + '.' + file_type[:3]


# calulate values from parameters
T = 1./sr                                # sampling period
scale = db_to_amp(gain)                  # scale from gain
nframes = dur_to_nframes(dur, sr)        # number of frames of signal
Wn = freq_to_Wn(freq, T)                 # Wn from freq
env_nframes = dur_to_nframes(env_durs, sr) # env breakpoints, in nframes


# generate sines: as phase lists two values
#                 two signals are generate
sig = fsinosc(Wn, phase, nframes)

# generate envelope: interleaved to scale
#                    interleaved signals
env = scale * interleave(
    linen(env_nframes, 'hann')
    )

# envelope
env_sig = env * sig

# display
pl.xlabel('Time (frames)')      # label x-axis
pl.ylabel('Amp (scale)')        # label y-axis

pl.axhline()                    # draw the x-axis
pl.plot(env_sig)                # plot the signal
pl.ylim(-1,1)                   # set the y display limit
pl.show()                       # show the thing!!

# instantiate output soundfile for writing
# Sndfile(filename, mode=r, Format, channels, samplerate)
out_sfile =  Sndfile(
    out_file,
    'w',
    Format(file_type, encoding),    # Format(type, encoding, endianness=file)
    channels,
    sr
    )

# write to output
out_sfile.write_frames(
    env_sig                     # signal for output
)

# now close file
out_sfile.close()

# close pylab
pl.close()

print "Done!!"