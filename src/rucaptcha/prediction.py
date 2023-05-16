"""file name says it all"""
# Credits: https://github.com/pythonlessons/CAPTCHA-solver

import os
import time
import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


PATH_TO_FROZEN_GRAPH = os.path.join(os.getcwd(), 'src/rucaptcha','rucaptcha_model_370.pb')
PATH_TO_LABELS =  os.path.join(os.getcwd(), 'src/rucaptcha', 'labels.pbtxt')
NUM_CLASSES = 24

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


# Detection
def captcha_detection(image_path: str, average_distance_error: int=3) -> str:
    """Reads a captcha and cracks its contents"""
    with detection_graph.as_default():
        with tf.compat.v1.Session(graph=detection_graph) as sess:
            image_np = cv2.imread(image_path)
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name(
                'num_detections:0')
            # Visualization of the results of a detection.
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=2)

            # Bellow we do filtering stuff
            captcha_array = [] #captcha_array will  correct symbols but not in correct order
            for i, b in enumerate(boxes[0]):
                for symbol in range(37):
                    if round(classes[0][i]) == symbol:
                        if scores[0][i] >= 0.65:
                            mid_x = (boxes[0][i][1]+boxes[0][i][3])/2  # (xmin + xmax) / 2
                            captcha_array.append(
                                [category_index[symbol].get('name'), mid_x, scores[0][i]])

            for _ in range(20):
                for captcha_number in range(len(captcha_array)-1):
                    if captcha_array[captcha_number][1] > captcha_array[captcha_number+1][1]:
                        temporary_captcha = captcha_array[captcha_number]
                        captcha_array[captcha_number] = captcha_array[captcha_number+1]
                        captcha_array[captcha_number+1] = temporary_captcha

            # Get final string from filtered CAPTCHA array
            captcha_string = []
            for d in captcha_array:
                captcha_string.append(d[0])
            return ''.join(captcha_string)

if __name__ == "__main__":
    captcha = captcha_detection('example/rucaptcha/d.png')
    print(captcha)
