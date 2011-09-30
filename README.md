# Parlament

## Instructions to fetch the images from the parliament website
1. create directory: admin/images/
2. php admin/fetch_images.php
3. the images are saved in the directory

> convert $file -resize 160x240^ -gravity center -extent 160x240 -quality 95 $file