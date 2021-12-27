import pygame


def get_axis_center_coords(parent_size, container_size, parent_offset=0):
    return (parent_size - container_size) / 2.0 + parent_offset


def get_center_coordinates(parent_size, container_size, parent_offset=(0, 0)):
    return (get_axis_center_coords(parent_size[0], container_size[0], parent_offset[0]),
            get_axis_center_coords(parent_size[1], container_size[1], parent_offset[1]))


def cut_out_tiles(image, start_pos, tile_size, tile_step):
    tiles = []

    current_y = start_pos[1]

    while current_y + tile_size[1] < image.get_height():
        current_x = start_pos[0]

        while current_x + tile_size[0] < image.get_width():
            tiles.append(image.subsurface((pygame.Rect((current_x, current_y), tile_size))))

            current_x += tile_size[0] + tile_step[0]

        current_y += tile_size[1] + tile_step[1]

    return tiles


def organize_cards(cards):
    organized_cards = []

    for j in range(4):
        for i in range(6, 13):
            organized_cards.append(cards[13 * j + i])

        organized_cards.append(cards[13 * j])

    return organized_cards


def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


def get_suit(card):
    return int(card / 8)


def is_same_number(card1, card2):
    return card1 % 8 == card2 % 8


class Alignment:
    START = 0
    CENTER = 1
    END = 2


deck = [i for i in range(32)]
black_cards = {0, 1, 2, 3, 4, 5, 6, 7, 24, 25, 26, 27, 28, 29, 30, 31}
red_cards = {i for i in range(8, 24)}
