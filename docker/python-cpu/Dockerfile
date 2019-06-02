# docker pull bvlc/caffe:cpu
FROM bvlc/caffe:cpu
MAINTAINER abhijeetsutrave@gmail.com

COPY proj_layer_caffe/heatmaps_from_vec_layer.hpp $CAFFE_ROOT/include/caffe/layers/
COPY proj_layer_caffe/heatmaps_from_vec_layer.cpp $CAFFE_ROOT/src/caffe/layers/

WORKDIR $CAFFE_ROOT/build
RUN cmake -DCPU_ONLY=1 .. && \
    make -j"$(nproc)"

RUN apt-get update && apt-get install -y --no-install-recommends \
	python-opencv \
	python-tk \
# Only needed on ubuntu host for some reason
	x11-apps \
	libcanberra-gtk-module

# FIXME: upstream caffe should probably have installed this
RUN pip install --upgrade pip
RUN pip install scikit-image --ignore-installed scipy

WORKDIR /workspace
ADD RegNet_deploy.prototxt RegNet_weights.caffemodel ./


# From: $GANerated_hands_root
# docker build -f docker/python-cpu/Dockerfile -t ganerated_hands .
# xhost +
# MacOS host
# IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}');\
# docker stop ganerated_hands;\
# docker run --rm -e DISPLAY=$IP:0 -v /tmp/.X11-unix:/tmp/.X11-unix \
# --device=/dev/video0:/dev/video0 \
# 	-ti \
# 	--name ganerated_hands ganerated_hands:latest \
# 	python eval.py

# Linux host
# docker stop ganerated_hands;
# docker run --rm -e DISPLAY=":0" -v /tmp/.X11-unix:/tmp/.X11-unix \
# --device=/dev/video0:/dev/video0 \
# 	-d \
# 	--name ganerated_hands ganerated_hands:latest \
# 	python eval.py

ADD *.png ./ && eval.py .
