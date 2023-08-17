def get_objects_to_render(self):
    #     self.objects_to_render = []
    #     for ray, values in enumerate(self.ray_casting_result):
    #         depth, proj_height, texture, offset = values

    #         if proj_height < HEIGHT:
    #             wall_column = self.textures[texture].subsurface(
    #                 offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
    #             )
    #             wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
    #             wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
    #         else:
    #             texture_height = TEXTURE_SIZE * HEIGHT / proj_height
    #             wall_column = self.textures[texture].subsurface(
    #                 offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
    #                 SCALE, texture_height
    #             )
    #             wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
    #             wall_pos = (ray * SCALE, 0)

    #         self.objects_to_