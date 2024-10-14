import sys
sys.path.append('egor@egor-laptop:~/Work/Room-navigation')

import cv2
import heapq
import os
# import building.school_1.graph as ln
from modules.function import processing_data_user_and_image

# Основная функция
def main():
    processing_data_user_and_image()


if __name__ == "__main__":
    main()