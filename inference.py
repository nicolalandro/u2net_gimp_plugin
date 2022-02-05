import copy

import numpy as np
import onnxruntime

from PIL import Image


def run_inference(onnx_session, input_size, image):
    # リサイズ
    temp_image = copy.deepcopy(image)
    x = temp_image.resize((input_size, input_size))

    # 前処理
    x = np.array(x, dtype=np.float32)
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    x = (x / 255 - mean) / std
    x = x.transpose(2, 0, 1).astype('float32')
    x = x.reshape(-1, 3, input_size, input_size)

    # 推論
    input_name = onnx_session.get_inputs()[0].name
    output_name = onnx_session.get_outputs()[0].name
    onnx_result = onnx_session.run([output_name], {input_name: x})

    # 後処理
    onnx_result = np.array(onnx_result).squeeze()
    min_value = np.min(onnx_result)
    max_value = np.max(onnx_result)
    onnx_result = (onnx_result - min_value) / (max_value - min_value)
    onnx_result *= 255
    onnx_result = onnx_result.astype('uint8')

    return onnx_result

# Load model
onnx_session = onnxruntime.InferenceSession("u2net.onnx")

def create_rgba(mode, image):
    out = run_inference(
        onnx_session,
        320,
        image,
    )
    out = Image.fromarray(out)
    mask = out.resize((image.width, image.height))

    if mode == "binary":
        resize_image = np.asarray(mask)
        resize_image[resize_image > 255] = 255
        resize_image[resize_image < 125] = 0
        mask = Image.fromarray(resize_image)


    rgba_image = image.convert('RGBA')
    rgba_image.putalpha(mask)

    return rgba_image

if __name__ == '__main__':
    modes = ["binary", "smooth"]
    mode = modes[0]

    img = Image.open('imgs/Parrot.jpg')

    create_rgba(mode, img).save('imgs/ParrotSeg.png')