import os; os.environ['GLOG_minloglevel'] = '2'
import caffe
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
caffe.set_mode_cpu();
from time import time

cap = cv2.VideoCapture(0)
# Hand structure
o1_parent = np.concatenate([
    [0], np.arange(0,4),
    [0], np.arange(5,8),
    [0], np.arange(9,12),
    [0], np.arange(13,16),
    [0], np.arange(17,20),
])
net = caffe.Net('RegNet_deploy.prototxt','RegNet_weights.caffemodel',caffe.TEST);
plt.ion()
fig = plt.figure()
ax = fig.gca(projection='3d')
plt.ion()

fig.show()
fig.canvas.draw()

while True:
    _, img = cap.read()
    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'): break

    #resize and normalize
    tight_crop_sized = cv2.resize(img, dsize=(128,128), interpolation=cv2.INTER_CUBIC)
    tight_crop_sized = np.subtract(np.divide(tight_crop_sized,127.5), 1)
    tight_crop_sized = np.reshape(np.moveaxis(tight_crop_sized, (0,1,2), (2,0,1)), (1,3,128,128))
    # assert(tight_crop_sized.shape == net.blobs[net.inputs[0]].data.shape)
    net.blobs[net.inputs[0]].data[...] = tight_crop_sized
    pred = net.forward()

    pred_3D = np.reshape(pred['joints3D_final_vec'], (21,3)).T
    ax.clear()
    for segment in range(pred_3D.shape[1]):
        ax.plot(
            [pred_3D[0,segment], pred_3D[0,o1_parent[segment]]],
            [pred_3D[1,segment], pred_3D[1,o1_parent[segment]]],
            [pred_3D[2,segment], pred_3D[2,o1_parent[segment]]],
        )
    fig.canvas.draw()
