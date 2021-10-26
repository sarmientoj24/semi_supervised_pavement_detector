pre:
	conda install pytorch==1.9.0 torchvision==0.10.0 cudatoolkit=11.1 -c pytorch -c conda-forge
	pip install mmcv-full==1.3.9 -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.9.0/index.html
	pip install mmdet==2.17.0
	mkdir -p thirdparty
	git clone https://github.com/open-mmlab/mmdetection.git thirdparty/mmdetection
	cd thirdparty/mmdetection && python -m pip install --ignore-installed -e .
	apt-get update
	apt-get install ffmpeg libsm6 libxext6 -y
install:
	make pre
	python -m pip install -e .
clean:
	rm -rf thirdparty
	rm -r ssod.egg-info