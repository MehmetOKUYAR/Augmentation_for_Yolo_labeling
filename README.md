# Augmentation for Yolo labeling
 
You can easily augmentation labeled images and txt files in yolo format.

Augmentation types:
- Horizantal Flip
- Vertical Flip
- Horizantal and Vertical Flip
- Random Brightness


### Run the application

The input parameters can be changed using the command line :
~~~
yolo_aug.py -i <input_dir> -t <aug_type (hflip,vflip,hvflip,bright)> -e <image extension (jpg,jpeg,png ...)> -o <output_dir>
~~~~~~~~~
For running example :
~~~~
python3 yolo_aug.py -i images -t hflip -e jpg -o aug
~~~~~~~~~

### Example Output

<table>
  <tr>
    <td> <b>Original image </b> <img src="https://github.com/MehmetOKUYAR/Augmentation_for_Yolo_labeling/blob/main/aug_example/example/frame_007252.jpg" alt="1" width = 640px height = 360px ></td>
    <td><b>Vertical image </b><img src="https://github.com/MehmetOKUYAR/Augmentation_for_Yolo_labeling/blob/main/aug_example/example/horizantal.png" alt="2" width = 640px height = 360px></td>
   </tr>
   
   <tr>
      <td><b>Horizantal and Vertical image </b><img src="https://github.com/MehmetOKUYAR/Augmentation_for_Yolo_labeling/blob/main/aug_example/example/horizantal_and_vertical.png" alt="3" width = 640px height = 360px></td>
      <td><b>Horizantal image </b><img src="https://github.com/MehmetOKUYAR/Augmentation_for_Yolo_labeling/blob/main/aug_example/example/vertical.png" alt="4" width = 640px height = 360px>
  </td>
  </tr>
</table>
