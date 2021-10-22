from random import randrange
import augmentations
import numpy as np
from PIL import Image

def dispNorm(mixed,filename=None):
  _min = np.amin(mixed)
  _max = np.amax(mixed)
  disp_norm = (mixed - _min) * 255.0 / (_max - _min)
  disp_norm = np.uint8(disp_norm)
  disp_img = Image.fromarray(disp_norm)
  disp_img.show(title="Hello")

  if filename != None:
      disp_img.save(filename)

# Image file path
img_file = "../dataset_1/CD_66000.jpg"

# Load the image
image = Image.open(img_file)
# Resize the image from 1200x800 to 384x256
width, height = image.size  # 1200, 800
nwidth, nheight = 384, 256
nImg = image.resize((nwidth, nheight))
# nImg.save("resized.jpg") # Save the image

# Crop the image for (IMAGE_SIZE x IMAGE_SIZE)
x1 = randrange(0, nwidth - augmentations.IMAGE_SIZE)
y1 = randrange(0, nheight - augmentations.IMAGE_SIZE + 1)
cropped_img = nImg.crop((x1, y1, x1 + augmentations.IMAGE_SIZE, y1 + augmentations.IMAGE_SIZE))
# cropped_img.save("cropped.jpg")

# Randomly create augmented image
img_aug = cropped_img.copy()
severity = 3
width_augment_chain = 3
img_list = []
for i in range(width_augment_chain):
    image_aug = cropped_img.copy()
    d = np.random.randint(1, 4)
    for _ in range(d):
        op = np.random.choice(augmentations.augmentations_all)
        image_aug = op(image_aug, severity)
        img_list.append(image_aug)

# Create brightness and sharpness-variant augmented images
brightImg = augmentations.brightness(cropped_img, severity)
blurImg = augmentations.sharpness(cropped_img, severity)
# Append the extra augmented images
img_list.append(brightImg)

# CIFAR-10 constants -- Modify to custom dataset
MEAN = [0.4914, 0.4822, 0.4465]
STD = [0.2023, 0.1994, 0.2010]

alpha, wt = 1., 5
ws = np.float32(np.random.dirichlet([alpha] * wt))
m = np.float32(np.random.beta(alpha, alpha))
print(ws)

mix = np.zeros_like(cropped_img, dtype=np.float32)
for i in range(wt):
    data = np.asarray(img_list[i], dtype=np.float32)
    mix += ws[i] * data
    mix /= 255.0

dispNorm(mix)
