"""Colored MNIST Data set."""

from pathlib import Path

import matplotlib.pyplot as plt
import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split

download_path = Path(__file__).parent / "downloads"


def colorize(image, color):
    """Turn a grayscale image into a single-colored image."""
    return torch.stack(tuple(image * x for x in color), dim=1).squeeze()


def get_color(condition_labels, condition, sample):
    """Get matplotlib color based on condition and random sample.

    Parameters
    ----------
    condition_labels: List[str]
        List of available conditions; i.e. `matplotlib` colormaps.
    condition: int
        The index of the condition
    sample: float
        Sampling value for the colormap, must be between 0 and 1.

    Returns
    -------
    color: np.array
        (3,) array of RGB values
    """
    color = plt.cm.get_cmap(condition_labels[condition])(sample)[:-1]
    return color


class ColoredMNIST(torchvision.datasets.MNIST):
    """MNIST with added color.

    The original MNIST images make up the content of the data set.
    They are styled with colors sampled from `matplotlib` colormaps.
    The colormaps correspond to the data's condition.
    """

    def __init__(self, root, classes=None, train=True, download=False):
        """
        Parameters
        ----------
        root: Union[str, pathlib.Path]
            Data root for download; defaults to ./downloads
        classes: List[str]
            The names of the `matplotlib` colormaps to use; defaults to the
            conditions: `['spring', 'summer', 'autumn', 'winter']`.
        train: bool
            Passed to `torchvision.datasets.MNIST`; default is True
        download: bool
            Passed to `torchvision.datasets.MNIST`; default is True
        """
        super().__init__(root, train=train, download=download)
        if classes is None:
            self.classes = ["spring", "summer", "autumn", "winter"]
        else:
            self.classes = classes
        # Initialise a random set of conditions, of the same length as the data
        self.conditions = torch.randint(len(self.classes), (len(self),))
        # Initialise a set of style values, the actual color will be dependent
        # on the condition
        self.style_values = torch.rand((len(self),))
        self.colors = [
            get_color(self.classes, condition, sample)
            for condition, sample in zip(
                self.conditions.numpy(), self.style_values.numpy()
            )
        ]

    def __getitem__(self, item):
        image, label = super().__getitem__(item)
        image = transforms.ToTensor()(image)
        color = torch.Tensor(self.colors[item])
        condition = self.conditions[item]
        label = torch.tensor(label)
        return colorize(image, color), condition