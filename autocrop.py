#!/usr/bin/env python

import sys
import Image
import ImageChops

def trim(image, border_color):
    mask = Image.new(image.mode, image.size, border_color)
    diff = ImageChops.difference(image, mask)
    bounds = diff.getbbox()
    if bounds:
        return image.crop(bounds)
    else:
        return None

def update(color_frequency, color):
    if color in color_frequency:
        color_frequency[color] += 1
    else:
        color_frequency[color] = 1

def find_background_color(image):
    '''Returns the most frequently occurring pixel colour along the border of the image.'''
    width, height = image.size
    color_frequency = {}
    for x in xrange(width - 1):
        for y in [0, height - 1]:
            update(color_frequency, image.getpixel((x, y)))
    for y in xrange(1, height - 2):
        for x in [0, width - 1]:
            update(color_frequency, image.getpixel((x, y)))
    
    ranked = color_frequency.items()
    ranked.sort(key=lambda x: -x[1])
    return ranked[0][0]

def main():
    if len(sys.argv) < 2:
        print >>sys.stderr, 'Usage: %s source [destination]' % sys.argv[0]
        exit(1)
     
    source = sys.argv[1]
    
    if len(sys.argv) >= 3:
        destination = sys.argv[2]
    else:
        destination = source
     
    image = Image.open(source)
    background_color = find_background_color(image)
    image = trim(image, background_color)
    if image:
        image.save(destination)
    else:
        print >>sys.stderr, 'Image is empty.  Bailing out.'
        exit(1)

if __name__ == '__main__':
    main()
