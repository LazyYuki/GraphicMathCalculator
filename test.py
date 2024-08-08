# import pygame

# ### generate basic pygame structure without comments

# screen = pygame.display.set_mode((1200, 800))

# while True:
#     events = pygame.event.get()
#     for event in events:
#         match event.type:
#             case pygame.QUIT:
#                 break

#             case pygame.KEYDOWN:
#                 print(event.key)

#             case pygame.KEYUP:
#                 print(event.key)

#     pygame.display.flip()

# import os

# def fast_scandir(dirname):
#     subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
#     for dirname in list(subfolders):
#         subfolders.extend(fast_scandir(dirname))
#     return subfolders

# print(fast_scandir("Apps"))
# print([f.path for f in os.scandir("Apps/Algebra/Matrix") if f.is_file()])

import importlib

mod = importlib.import_module("Apps.Algebra.Matrizen.1_Einführung")
mod.HelloWorld()