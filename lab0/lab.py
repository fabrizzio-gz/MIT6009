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
    raise NotImplementedError


def pan(sound):
    raise NotImplementedError


def remove_vocals(sound):
    raise NotImplementedError


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


def main():
    hello = load_wav('./sounds/mystery.wav')
    write_wav(backwards(hello), 'hello_reversed.wav')
    
if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    hello = load_wav('sounds/mystery.wav')

    write_wav(backwards(hello), 'hello_reversed.wav')
