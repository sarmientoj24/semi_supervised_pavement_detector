# semi_supervised_pavement_detector

## Installation
1. Create conda environment of Python3.6
    `conda create -n softteacher python=3.6`
2. Activate environment
    `conda activate softteacher`
3. Install dependencies
    `make install`
4. Add dataset to directory
5. Edit config files as needed


## Config Files
1. 50% supervision
Only Labeled:  
`configs/baseline/faster_rcnn_r50_caffe_fpn_coco_full_720.py`  
```
_base_ = "base.py"


classes = ('D00', 'D10', 'D20', 'D40')
dataset_type = 'CocoDataset'

data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        ann_file="/path/to/pave/semi_supervised_pavement_detector/data/semisup_fifty/annotations/rddc_coco_train_sup_50_perc.json",
        img_prefix="/path/to/pave/semi_supervised_pavement_detector/data/semisup_fifty/train2017/",
        classes=classes
    ),
    val=dict(
        type=dataset_type,
        ann_file="/path/to/pave/semi_supervised_pavement_detector/data/semisup_fifty/annotations/rddc_coco_test.json",
        img_prefix="/path/to/pave/semi_supervised_pavement_detector/data/semisup_fifty/val2017/",
        classes=classes
    ),
)

optimizer = dict(lr=0.02)
lr_config = dict(step=[120000 * 4, 160000 * 4])
# Change max_iters from 720K to 180K
runner = dict(_delete_=True, type="IterBasedRunner", max_iters=180000)

model = dict(
    roi_head=dict(
        bbox_head=dict(
            type='Shared2FCBBoxHead',
            num_classes=4,
        )
    )
)
```

Semi-Supervised:  
`configs/soft_teacher/soft_teacher`
```
_base_ = "base.py"


classes = ('D00', 'D10', 'D20', 'D40')
dataset_type = 'CocoDataset'

data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        ann_file="/path/to/pave/semi_supervised_pavement_detector/data/semisup_fifty/annotations/rddc_coco_train_sup_50_perc.json",
        img_prefix="/path/to/pave/semi_supervised_pavement_detector/data/semisup_fifty/train2017/",
        classes=classes
    ),
    unsup=dict(
        type=dataset_type,
        ann_file="/path/to/pave/semi_supervised_pavement_detector/data/semisup_fifty/annotations/rddc_coco_semisup_50_perc.json",
        img_prefix="/path/to/pave/semi_supervised_pavement_detector/data/semisup_fifty/unlabeled2017/",
    ),
    val=dict(
        type=dataset_type,
        ann_file="/path/to/pave/semi_supervised_pavement_detector/data/semisup_fifty/annotations/rddc_coco_test.json",
        img_prefix="/path/to/pave/semi_supervised_pavement_detector/data/semisup_fifty/val2017/",
        classes=classes
    ),
    sampler=dict(
        train=dict(
            sample_ratio=[1, 4],
        )
    ),
)

# Change max_iters from 720K to 180K
runner = dict(_delete_=True, type="IterBasedRunner", max_iters=180000)

model = dict(
    roi_head=dict(
        bbox_head=dict(
            type='Shared2FCBBoxHead',
            num_classes=4,
        )
    )
)

work_dir = "work_dirs/soft_teacher_faster_rcnn_r50_caffe_fpn_coco_180k/50"
log_config = dict(
    interval=50,
    hooks=[
        dict(type="TextLoggerHook"),
        dict(
            type="WandbLoggerHook",
            init_kwargs=dict(
                project="pre_release",
                name="${cfg_name}",
                config=dict(
                    percent="50",
                    work_dirs="${work_dir}",
                    total_step="${runner.max_iters}",
                ),
            ),
            by_epoch=False,
        ),
    ],
)


```
2. 25% supervision
3. 10% supervision

uninstall gitpython
get mmdet 2.17.0