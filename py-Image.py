from PIL import Image  

def resize_auto(image_path, desired_size = 1024):
    img = Image.open(image_path)
    original_width, original_height = img.size
    
    if max(original_width, original_height) <= desired_size:
        return img
    
    ratio = 0

    if original_height >= original_width:
        ratio += original_width / float(original_height)
        new_width = int(desired_size * ratio)
        return img.resize((new_width, desired_size))
    else:   
        ratio += original_height / float(original_width)
        new_height = int(desired_size * ratio)
        return img.resize((desired_size, new_height))



image_path = './sloth3.jpg'

resized_image = resize_auto(image_path)
resized_image.save('resized.jpg')