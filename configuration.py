import torch

class training_configuration():
    training_set_dir = "/cluster/sorona/hyu/ptdcv/ballet/"
    training_gt_dir = "/cluster/sorona/hyu/ptdcv/gt_ballet/"
    train_batch_size = 2
    train_number_epochs = 8
    learning_rate = 0.0001
    contrastive_margin = 1.0
    resnet_depth = 18
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    number_workers = 4
    plot_frequency = 1
    
class Training_Data_Config():
    number_keypoints = 400
    stride = 4
    training_data_size = 2

class Validation_Data_Config():
    number_keypoints = 416
    stride = 4
    validation_data_size = 2
    validation_set_dir = "/cluster/sorona/hyu/ptdcv/goalkeeper/"
    validation_gt_dir = "/cluster/sorona/hyu/ptdcv/gt_goalkeeper/"
