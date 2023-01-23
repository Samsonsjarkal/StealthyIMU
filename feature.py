import torch
from speechbrain.processing.features import (
    STFT,
    spectral_magnitude,
    Filterbank,
    DCT,
    Deltas,
    ContextWindow,
)

class AccSpec(torch.nn.Module):
    """Generate features for input to the speech pipeline.

    Arguments
    ---------
    context : bool (default: False)
        Whether or not to append forward and backward contexts to
        the features.
    sample_rate : int (default: 16000)
        Sampling rate for the input waveforms.
    win_length : float (default: 25)
        Length (in ms) of the sliding window used to compute the STFT.
    hop_length : float (default: 10)
        Length (in ms) of the hop of the sliding window used to compute
        the STFT.
    n_fft : int (default: 400)
        Number of samples to use in each stft.
    left_frames : int (default: 5)
        Number of frames of left context to add.
    right_frames : int (default: 5)
        Number of frames of right context to add.

    Example
    -------
    >>> import torch
    >>> inputs = torch.randn([10, 500])
    >>> feature_maker = Fbank()
    >>> feats = feature_maker(inputs)
    >>> feats.shape
    torch.Size([10, 101, 40])
    """

    def __init__(
        self,
        context=False,
        sample_rate=500,
        n_fft=80,
        left_frames=5,
        right_frames=5,
        win_length=80,
        hop_length=20,
    ):
        super().__init__()
        self.context = context
        self.compute_STFT = STFT(
            sample_rate=sample_rate,
            n_fft=n_fft,
            win_length=win_length,
            hop_length=hop_length,
        )
        self.context_window = ContextWindow(
            left_frames=left_frames, right_frames=right_frames,
        )

    def forward(self, wav):
        """Returns a set of features generated from the input Acc waveforms.

        Arguments
        ---------
        wav : tensor
            A batch of Acc signals to transform to features.
        """
        with torch.no_grad():
            STFT = self.compute_STFT(wav)
            mag = spectral_magnitude(STFT)

            if self.context:
                mag = self.context_window(mag)
                
        # mag[:,:,16:41]
        # mag[:,:,10:41]
        # mag[:,:,:]
        return mag[:,:,10:]