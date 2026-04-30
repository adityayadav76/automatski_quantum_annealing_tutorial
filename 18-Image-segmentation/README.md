# Image Segmentation (QUBO)

## Overview
Image segmentation partitions an image into meaningful regions. We formulate it as QUBO by grouping similar pixels together.

## QUBO Formulation
- Binary variables for pixel assignments to segments
- Similarity costs for grouping similar pixels
- One-hot constraint for each pixel

## Running the Example
```bash
python step18_image_segmentation.py
```

## Source Code
See `step18_image_segmentation.py` for complete implementation.