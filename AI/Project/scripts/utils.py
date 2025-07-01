from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data import DataLoader

def load_data(data_dir='Dataset', img_size=(128, 128), batch_size=32):
    transform = transforms.Compose([
        transforms.Resize(img_size),
        transforms.ToTensor(),
    ])

    train_dataset = ImageFolder(f'{data_dir}/Train Data', transform=transform)
    test_dataset = ImageFolder(f'{data_dir}/Test Data', transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    return train_loader, test_loader, train_dataset.classes
