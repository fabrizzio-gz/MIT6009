# No Imports Allowed!

## Test input
inp = {
            'rate': 20,
            'left': [1,2,3,4,5,6],
            'right': [7,6,5,4,3,2],
        }



def backwards(sound):
    backwards_sound = {}
    backwards_sound['rate'] = sound['rate']
    backwards_sound['left'] = list(reversed(sound['left']))
    backwards_sound['right'] = list(reversed(sound['right']))

    return backwards_sound


def mix(sound1, sound2, p):
    mixed = {}
    mixed['rate'] = sound1['rate']
    mixed['left'] = []
    mixed['right'] = []

    # Different sound rates return None
    if (sound1['rate'] != sound2['rate']):
        return None

    # Return mixed sound of shortest duration
    duration = min(len(sound1['left']), len(sound2['left']))
    left1, left2 = sound1['left'][:duration], sound2['left'][:duration]
    right1, right2 = sound1['right'][:duration], sound2['right'][:duration]

    # sound1*p, sound2*(1-p)
    mixed['left'] = list(map(lambda x, y: x*p + y*(1-p), left1, left2))
    mixed['right'] = list(map(lambda x, y: x*p + y*(1-p), right1, right2))

    return mixed


def echo(sound, num_echos, delay, scale):
    echo_sound = {}
    echo_sound['rate'] = sound['rate']

    # Echo sound is num_echos*sample_delay samples longer
    sample_delay = round(delay * sound['rate'])
    echo_sound['left'] = sound['left'] + [0] * (num_echos * sample_delay)
    echo_sound['right'] = sound['right'] + [0] * (num_echos * sample_delay)

    echo_right = sound['right']
    echo_left = sound['left']
    for echo_run in range(num_echos):

        # At each run, the echo is scaled down
        echo_right = list(map(lambda x: x * scale, echo_right))
        echo_left = list(map(lambda x: x * scale, echo_left))

        # Adding echo with a sample delay
        for index in range(len(echo_right)):
            echo_sound['left'][index + sample_delay] += echo_left[index]
            echo_sound['right'][index + sample_delay] += echo_right[index]

        # Sample delay will be incremented for next run of echo
        sample_delay += round(delay * sound['rate'])

    return echo_sound


def pan(sound):
    pan_sound = {}
    pan_sound['rate'] = sound['rate']
    pan_sound['left'] = sound['left'][:]
    pan_sound['right'] = sound['right'][:]
    samples = len(pan_sound['left'])

    for i in range(samples):
        scale_factor = i / (samples - 1)
        pan_sound['right'][i] *= scale_factor
        pan_sound['left'][i] *= (1 - scale_factor)

    return pan_sound


def remove_vocals(sound):
    no_vocals = {}
    no_vocals['rate'] = sound['rate']

    # Sound is mono: left-right will delete the mono part of samples
    no_vocals_samples = list(map(lambda x, y: x - y, sound['left'], sound['right']))
    no_vocals['left'] = no_vocals_samples
    no_vocals['right'] = no_vocals_samples

    return no_vocals


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct

def load_wav(filename):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    left = []
    right = []
    for i in range(count):
        frame = f.readframes(1)
        if chan == 2:
            left.append(struct.unpack('<h', frame[:2])[0])
            right.append(struct.unpack('<h', frame[2:])[0])
        else:
            datum = struct.unpack('<h', frame)[0]
            left.append(datum)
            right.append(datum)

    left = [i/(2**15) for i in left]
    right = [i/(2**15) for i in right]

    return {'rate': sr, 'left': left, 'right': right}


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, 'w')
    outfile.setparams((2, 2, sound['rate'], 0, 'NONE', 'not compressed'))

    out = []
    for l, r in zip(sound['left'], sound['right']):
        l = int(max(-1, min(1, l)) * (2**15-1))
        r = int(max(-1, min(1, r)) * (2**15-1))
        out.append(l)
        out.append(r)

    outfile.writeframes(b''.join(struct.pack('<h', frame) for frame in out))
    outfile.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    hello = load_wav('sounds/coffee.wav')
    write_wav(echo(hello, 5, .3, .6), 'hello_reversed.wav')
