_base_ = "base.py"


classes = ('D00', 'D10', 'D20', 'D40')
dataset_type = 'CocoDataset'

data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        ann_file="/notebooks/pave/semi_supervised_pavement_detector/data/semisup_fifty/annotations/rddc_coco_train_sup_50_perc.json",
        img_prefix="/notebooks/pave/semi_supervised_pavement_detector/data/semisup_fifty/train2017/",
        classes=classes
    ),
    val=dict(
        type=dataset_type,
        ann_file="/notebooks/pave/semi_supervised_pavement_detector/data/semisup_fifty/annotations/rddc_coco_test.json",
        img_prefix="/notebooks/pave/semi_supervised_pavement_detector/data/semisup_fifty/val2017/",
        classes=classes
    ),
)

optimizer = dict(lr=0.02)
lr_config = dict(step=[120000 * 4, 160000 * 4])
runner = dict(_delete_=True, type="IterBasedRunner", max_iters=180000 * 4)

model = dict(
    roi_head=dict(
        bbox_head=dict(
            type='Shared2FCBBoxHead',
            num_classes=4,
        )
    )
)