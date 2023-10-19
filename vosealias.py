#! /usr/bin/env python3

import numpy as np


def main():

    """Vose's Alias Method for sampling from a discrete probability distribution."""

    probabilities = np.random.randint(low=1, high=101, size=8)
    probabilities = probabilities / np.sum(probabilities)
    print(probabilities)
    scaled = probabilities * len(probabilities)
    low = []
    high = []
    for i, p in enumerate(scaled):
        if scaled[i] < 1:
            low.append((p, i))
        else:
            high.append((p, i))
    alias = np.zeros(len(probabilities), dtype=np.uint32)
    while low and high:
        pl, il = low.pop()
        ph, ih = high.pop()
        probabilities[il] = pl
        alias[il] = ih
        ph = (ph + pl) - 1
        if ph < 1:
            low.append((ph, ih))
        else:
            high.append((ph, ih))
    while high:
        ph, ih = high.pop()
        probabilities[ih] = 1
    while low:
        pl, il = low.pop()
        probabilities[il] = 1

    size = 1<<20

    # One at a time...
    # counts = np.zeros(len(probabilities), dtype=np.uint32)
    # for i in range(size):
    #     choice = np.random.randint(0, len(probabilities), size=1)
    #     if probabilities[choice] == 1:
    #         counts[choice] += 1
    #     elif np.random.random() < probabilities[choice]:
    #         counts[choice] += 1
    #     else:
    #         counts[alias[choice]] += 1

    # Vectorized...
    choices = np.random.randint(0, len(probabilities), size=size)
    mask = np.random.random(size=size) > probabilities[choices]
    choices[mask] = alias[choices[mask >= probabilities[choices]]]
    _, counts = np.unique(choices, return_counts=True)

    counts = counts / np.sum(counts)
    print(counts)

    return


if __name__ == "__main__":
    main()
