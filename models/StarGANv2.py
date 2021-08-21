import torch
from PIL import Image
from munch import Munch
from torchvision import transforms

from models.StarGANv2_model import Generator, MappingNetwork, StyleEncoder
from utils import load_weights, set_eval_mode, save_images, to_device

nets = Munch()
transform_list = []
args = Munch()


def init(device='cpu'):
    # Basic configuration
    global args
    args = Munch({
        "img_size": 256,
        "style_dim": 64,
        "latent_dim": 16,
        "num_domains": 3,
        "w_hpf": 0,
        "device": device
    })
    # Prepare image transform list
    norm_mean = [0.5, 0.5, 0.5]
    norm_std = [0.5, 0.5, 0.5]
    global transform_list
    transform_list = [
        transforms.Resize([args.img_size, args.img_size]),
        transforms.ToTensor(),
        transforms.Normalize(mean=norm_mean, std=norm_std),
    ]

    # Instantiate models
    generator = Generator(args.img_size, args.style_dim, w_hpf=args.w_hpf)
    mapping_network = MappingNetwork(args.latent_dim, args.style_dim, args.num_domains)
    style_encoder = StyleEncoder(args.img_size, args.style_dim, args.num_domains)
    global nets
    nets = Munch(generator=generator,
                 mapping_network=mapping_network,
                 style_encoder=style_encoder)

    # Load parameters
    weight_path = "starganv2_afhq.ckpt"
    download_path = "https://github.com/justsong-lab/releases/releases/download/v0.1/starganv2_afhq.ckpt"
    weight_dict = load_weights(weight_path, download_path, args.device)

    # Apply parameters to models
    for name, module in nets.items():
        module.load_state_dict(weight_dict[name])

    # Set model to eval mode
    set_eval_mode(nets)

    # To device
    to_device(nets, device)
    return nets


def preprocess(img):
    if img is None:
        return None
    assert len(transform_list) != 0
    # TODO: let the frontend do image preprocessing
    for transform in transform_list:
        img = transform(img)
    img = img.to(args.device)
    img = torch.unsqueeze(img, dim=0)
    return img


@torch.no_grad()
def inference(x_src, x_ref, y=0, seed=0, mode='latent'):
    batch_size = x_src.shape[0]
    y = torch.LongTensor(batch_size).to(args.device).fill_(y)
    if mode == 'latent':
        torch.manual_seed(seed)
        z = torch.randn(batch_size, args.latent_dim).to(args.device)
        s = nets.mapping_network(z, y)
    elif mode == "reference":
        s = nets.style_encoder(x_ref, y)
    else:
        assert False, f"No such mode: {mode}"
    x_fake = nets.generator(x_src, s)
    return x_fake


def stargan_v2(x_src, x_ref, y=None, seed=0, mode='latent'):
    """
    StarGANv2 model
    :param x_src: source image
    :param x_ref: reference image
    :param y: reference image's label or target image
    :param seed: random seed for latent mode
    :param mode: available options: reference, latent
    :return:
    """
    res = Munch({
        "success": False,
        "message": "default message",
        "data": None
    })

    if nets is None:
        res.message = "model not initialized"
    if mode not in ['latent', 'reference']:
        res.message = f"no such mode: {mode}"
    res.success = True
    x_src = preprocess(x_src)
    x_ref = preprocess(x_ref)

    fake_images = inference(x_src, x_ref, y, seed, mode)
    filenames = save_images(fake_images)
    res.data = filenames

    return res.__dict__


def controller(request):
    mode = request.form['mode']
    y = request.form['y']
    y = int(y)
    src_img = Image.open(request.files['src_img'])
    if mode == 'reference':
        ref_img = Image.open(request.files['ref_img'])
        res = stargan_v2(src_img, ref_img, y=y, mode=mode)
    else:
        seed = request.form['seed']
        res = stargan_v2(src_img, x_ref=None, y=y, seed=seed, mode=mode)
    return res


if __name__ == '__main__':
    def main():
        init('cuda')
        src_img_path = "./temp/cat.jpg"
        ref_img_path = "./temp/dog.jpg"
        y = 0
        src_img = Image.open(src_img_path).convert('RGB')
        ref_img = Image.open(ref_img_path).convert('RGB')
        res = stargan_v2(src_img, ref_img, y, mode='reference')
        print(res)
        res = stargan_v2(src_img, ref_img, y, mode='latent')
        print(res)


    main()
