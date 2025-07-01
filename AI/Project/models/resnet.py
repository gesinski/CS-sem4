from torchvision.models import resnet18
import torch.nn as nn

def get_resnet18_model():
    model = resnet18(pretrained=True)
    for param in model.parameters():
        param.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, 5)
    return model
