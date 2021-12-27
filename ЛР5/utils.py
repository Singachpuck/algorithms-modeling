import pygame


def get_axis_center_coords(parent_size, container_size, parent_offset=0):
    return (parent_size - container_size) / 2.0 + parent_offset


def get_center_coordinates(parent_size, container_size, parent_offset=(0, 0)):
    return (get_axis_center_coords(parent_size[0], container_size[0], parent_offset[0]),
            get_axis_center_coords(parent_size[1], container_size[1], parent_offset[1]))


class Alignment:
    START = 0
    CENTER = 1
    END = 2
