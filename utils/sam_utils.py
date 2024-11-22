"""
Helper functions for SAM visualization and plotting.
"""

import numpy as np
import matplotlib.pyplot as plt

# Helper functions for SAM2 segmentation map visualization.
def show_mask(mask, plt, random_color=False, borders=True):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([255/255, 40/255, 50/255, 0.6])

    h, w = mask.shape[-2:]
    mask = mask.astype(np.uint8)
    mask_image =  mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    
    if borders:
        import cv2
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_NONE
        )
        # Try to smooth contours
        contours = [
            cv2.approxPolyDP(
                contour, epsilon=0.01, closed=True
            ) for contour in contours
        ]
        mask_image = cv2.drawContours(
            mask_image, 
            contours, 
            -1, 
            (color[0], color[1], color[1], 1), 
            thickness=2
        ) 
    plt.imshow(mask_image)

def add_labels(ax, clip_label, labels, pos_points, neg_points):
    # Add custom text labels for points
    pos_labels = [clip_label[i] for i in range(len(labels)) if labels[i] == 1]
    neg_labels = [clip_label[i] for i in range(len(labels)) if labels[i] == 0]
    
    # Add labels for positive points
    for (x, y), label in zip(pos_points, pos_labels):
        ax.text(
            x, y, label, 
            color='green', fontsize=12, ha='center', va='center', 
            bbox=dict(facecolor='white', edgecolor='green', alpha=0.6, boxstyle='round,pad=0.3')
        )
    
    # Add labels for negative points
    for (x, y), label in zip(neg_points, neg_labels):
        ax.text(
            x, y, label, 
            color='red', fontsize=8, ha='center', va='center', 
            bbox=dict(facecolor='white', edgecolor='red', alpha=0.6, boxstyle='round,pad=0.3')
        )
    
    ax.legend()  # Add legend to differentiate between positive and negative points
    return ax

def show_points(coords, labels, ax, clip_label, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(
        pos_points[:, 0], 
        pos_points[:, 1], 
        color='green', 
        marker='.', 
        s=marker_size, 
        edgecolor='white', 
        linewidth=1.25
    )
    ax.scatter(
        neg_points[:, 0], 
        neg_points[:, 1], 
        color='red', 
        marker='.', 
        s=marker_size, 
        edgecolor='white', 
        linewidth=1.25
    )   

    if clip_label is not None:
        ax = add_labels(
            ax, 
            clip_label=clip_label, 
            labels=labels, 
            pos_points=pos_points, 
            neg_points=neg_points
        )

def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle(
        (x0, y0), 
        w, 
        h, 
        edgecolor='green', 
        facecolor=(0, 0, 0, 0), 
        lw=2)
    )    

def show_masks(
    image, 
    masks, 
    scores, 
    point_coords=None, 
    box_coords=None, 
    input_labels=None, 
    borders=True,
    clip_label=None
):
    dpi = plt.rcParams['figure.dpi']
    figsize = image.shape[1] / dpi, image.shape[0] / dpi

    plt.figure(figsize=figsize)
    plt.imshow(image)

    for i, (mask, score) in enumerate(zip(masks, scores)):
        if i == 0:  # Only show the highest scoring mask.
            show_mask(mask, plt.gca(), random_color=False, borders=borders)
    if point_coords is not None:
        assert input_labels is not None
        show_points(
            coords=point_coords, 
            labels=input_labels, 
            ax=plt.gca(), 
            clip_label=clip_label
        )
    if box_coords is not None:
        show_box(box_coords, plt)

    plt.tight_layout()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.axis('off')
    return plt

def show_video_mask(mask, ax, obj_id=None, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        cmap = plt.get_cmap('tab10')
        cmap_idx = 0 if obj_id is None else obj_id
        color = np.array([*cmap(cmap_idx)[:3], 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    ax.axis('off')