from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import math
from PIL import Image


class Skill:
    def __init__(self,owner):
        self.owner = owner
        self.cooldown = 5.0
        self.cooldown_timer = 0
        self.is_active = False
        self.duration = 0
        self.duration_timer = 0

    def use(self):
        if self.is_active:
            print("스킬이 이미 사용 중입니다.")
            return False
        if self.cooldown_timer > 0:
            print(f"쿨타임 남음: {self.cooldown_timer:.1f}초")
            return False
        self.is_active = True
        self.cooldown_timer = self.cooldown
        self.duration_timer = self.duration
        self.on_use()
        return True

    def on_use(self):
        pass

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= game_framework.frame_time

        if self.is_active:
            self.duration_timer -= game_framework.frame_time
            self.on_update()

            if self.duration_timer <= 0:
                self.is_active = False
                self.on_end()

    def on_update(self):
        pass

    def on_end(self):
        print(f"{self.__class__.__name__} 종료")

    def draw(self):
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass

class AlchemistSkill(Skill):
    image = None

    def __init__(self, owner):
        super().__init__(owner)
        if AlchemistSkill.image is None:
            AlchemistSkill.image = load_image('asset/Weapon/alchemist_1.png')

        self.cooldown = 0.5
        self.duration = 0.5
        self.damage = 40
        self.range = 250
        self.frame = 0
        self.throw_x = 0
        self.throw_y = 0
        self.target_x = 0
        self.target_y = 0
        self.skill_dir_x = 1
        self.skill_dir_y = 0
        self.explosion_timer = 0
        self.should_show_mark = True
        self.hit_monsters = set()

    def check_collision_at_target(self, x, y):
        try:
            import map as game_map

            if game_map.current_map == "Lobby":
                from lobby import is_lobby_collision
                if is_lobby_collision(x, y):
                    return False
                return True


            import round1
            if round1._collision_data is None:
                return True

            scale = 10000.0 / round1._collision_width
            img_x = int(x / scale)
            img_y = int(y / scale)

            if img_x < 0 or img_x >= round1._collision_width or img_y < 0 or img_y >= round1._collision_height:
                return False

            pil_y = round1._collision_height - 1 - img_y
            pixel = round1._collision_data[img_x, pil_y]

            if round1._image_mode == 'L':
                r = g = b = pixel
            elif round1._image_mode == 'RGB':
                r, g, b = pixel
            elif round1._image_mode == 'RGBA':
                r, g, b, a = pixel
            else:
                r = g = b = pixel if isinstance(pixel, int) else pixel[0]

            if r < 1 and g < 1 and b < 1:
                return False

            return True
        except:
            return True

    def on_use(self):
        self.start_x = self.owner.x
        self.start_y = self.owner.y

        self.skill_dir_x = self.owner.last_move_dir_x
        self.skill_dir_y = self.owner.last_move_dir_y


        if self.skill_dir_x == 0 and self.skill_dir_y == 0:
            self.skill_dir_x = 1

        self.target_x = self.start_x + (self.range * self.skill_dir_x)
        self.target_y = self.start_y + (self.range * self.skill_dir_y)
        self.frame = 0
        self.explosion_timer = 0

        self.hit_monsters.clear()

        self.should_show_mark = self.check_collision_at_target(self.target_x, self.target_y)

    def on_update(self):
        progress = 1.0 - (self.duration_timer / self.duration)
        self.frame = int(progress * 5) % 6


        self.throw_x = self.start_x + (self.range * self.skill_dir_x * progress)
        self.throw_y = self.start_y + (self.range * self.skill_dir_y * progress)


        arc_offset = math.sin(progress * math.pi) * 50
        if abs(self.skill_dir_x) > abs(self.skill_dir_y):
            # 좌우 이동
            self.throw_y += arc_offset
        else:
            # 상하 이동
            self.throw_x += arc_offset * self.skill_dir_x if self.skill_dir_x != 0 else arc_offset

    def on_end(self):
        if self.should_show_mark:
            self.explosion_timer = 0.5
        else:
            game_world.remove_object(self)

    def update(self):
        super().update()
        if not self.is_active and self.explosion_timer > 0:
            self.explosion_timer -= game_framework.frame_time
            if self.explosion_timer <= 0:
                game_world.remove_object(self)

    def draw(self):

        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.throw_x, self.throw_y)
            tx, ty = cam.to_camera(self.target_x, self.target_y)
        else:
            sx, sy = self.throw_x, self.throw_y
            tx, ty = self.target_x, self.target_y

        if self.is_active:
            if self.image:
                self.image.clip_draw(0, 0, 21, 21, sx, sy, 30, 30)

        if not self.is_active and self.explosion_timer > 0 and self.should_show_mark:
            if self.image:
                self.image.clip_draw(82, 0, 61, 61, tx, ty, 60, 60)

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.is_active:
            return 0, 0, 0, 0

        if self.explosion_timer > 0 and self.should_show_mark:
            return self.target_x - 30, self.target_y - 30, self.target_x + 30, self.target_y + 30
        return 0, 0, 0, 0

    def handle_collision(self, group, other):
        if group == 'skill:monster' and (not self.is_active) and self.explosion_timer > 0 and self.should_show_mark:
            if hasattr(other, 'hp') and getattr(other, 'alive', True) and other not in self.hit_monsters:
                self.hit_monsters.add(other)

                from monster import Boss1
                if isinstance(other, Boss1):
                    if not other.take_damage(self.damage):
                        return
                else:
                    other.hp -= self.damage
                    print(f"스킬 폭발 피격: 몬스터 HP={other.hp}")
                    if other.hp <= 0:
                        other.alive = False
                        game_world.move_object(other, 2)
                        import round1
                        if round1.current_room in round1.rooms:
                            round1.rooms[round1.current_room]['num'] -= 1

                        from round_1_mode import CoinUI
                        CoinUI.coin_count += 1

                        if round1.current_room == 1 and all(not m.alive for m in round1.monsters):
                            round1.change_map('asset/Map/round1_map.png', 'asset/Map/round1_collision.png', 1, self.owner)

                        if round1.current_room == 2 and all(not m.alive for m in round1.monsters):
                            round1.change_map('asset/Map/round1_map.png', 'asset/Map/round1_collision.png', 2, self.owner)
        elif group == 'skill:bullet' and (not self.is_active) and self.explosion_timer > 0 and self.should_show_mark:
            if hasattr(other, 'alive'):
                other.alive = False
                print(f"총알 파괴")


class SwordAfterimage:
    def __init__(self, x, y, dir_x, dir_y, image, owner):
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.image = image
        self.owner = owner

        self.start_x = x
        self.start_y = y
        self.move_distance = 140
        self.duration = 0.3
        self.timer = self.duration
        self.is_alive = True
        self.damage = 30
        self.hit_monsters = set()

        if abs(dir_x) > abs(dir_y):
            if dir_x > 0:
                self.angle = 0
            else:
                self.angle = 180
        else:
            if dir_y > 0:
                self.angle = 90
            else:
                self.angle = -90

    def update(self):
        if self.timer > 0:
            self.timer -= game_framework.frame_time

            progress = 1.0 - (self.timer / self.duration)

            self.x = self.start_x + (self.dir_x * self.move_distance * progress)
            self.y = self.start_y + (self.dir_y * self.move_distance * progress)


            if self.check_out_of_bounds():
                self.is_alive = False
                return

            if self.timer <= 0:
                self.is_alive = False

    def check_out_of_bounds(self):
        try:
            import map as game_map
            import round1
            from lobby import is_lobby_collision


            if game_map.current_map == "Lobby":
                if is_lobby_collision(self.x, self.y):
                    return True


            elif game_map.current_map == "Round_1":
                if round1._collision_data is None:
                    return False

                scale = 10000.0 / round1._collision_width
                img_x = int(self.x / scale)
                img_y = int(self.y / scale)

                if img_x < 0 or img_x >= round1._collision_width or img_y < 0 or img_y >= round1._collision_height:
                    return True

                pil_y = round1._collision_height - 1 - img_y
                pixel = round1._collision_data[img_x, pil_y]

                if round1._image_mode == 'RGB':
                    r, g, b = pixel
                elif round1._image_mode == 'RGBA':
                    r, g, b, a = pixel
                else:
                    r = g = b = pixel if isinstance(pixel, int) else pixel[0]

                if r < 1 and g < 1 and b < 1:
                    return True

            return False
        except:
            return False

    def draw(self):
        if not self.is_alive:
            return

        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.x, self.y)
        else:
            sx, sy = self.x, self.y

        if self.image:
            self.image.clip_composite_draw(
                52, 0, 28, 96,
                math.radians(self.angle), '',
                sx, sy, 42, 144
            )

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.is_alive:
            return 0, 0, 0, 0

        if abs(self.dir_x) > abs(self.dir_y):
            return self.x - 21, self.y - 72, self.x + 21, self.y + 72
        else:
            return self.x - 72, self.y - 21, self.x + 72, self.y + 21

    def handle_collision(self, group, other):
        if group == 'afterimage:monster' and self.is_alive:
            if hasattr(other, 'hp') and getattr(other, 'alive', True) and other not in self.hit_monsters:
                self.hit_monsters.add(other)

                from monster import Boss1
                if isinstance(other, Boss1):
                    if not other.take_damage(self.damage):
                        return
                else:
                    other.hp -= self.damage
                    print(f"잔상 피격: 몬스터 HP={other.hp}")
                    if other.hp <= 0:
                        other.alive = False
                        game_world.move_object(other, 2)
                        import round1
                        if round1.current_room in round1.rooms:
                            round1.rooms[round1.current_room]['num'] -= 1

                        from round_1_mode import CoinUI
                        CoinUI.coin_count += 1

                        if round1.current_room == 1 and all(not m.alive for m in round1.monsters):
                            round1.change_map('asset/Map/round1_map.png', 'asset/Map/round1_collision.png', 1, self.owner)

                        if round1.current_room == 2 and all(not m.alive for m in round1.monsters):
                            round1.change_map('asset/Map/round1_map.png', 'asset/Map/round1_collision.png', 2, self.owner)
        elif group == 'afterimage:bullet' and self.is_alive:
            if hasattr(other, 'alive'):
                other.alive = False
                print(f"총알 파괴")


class AssassinSkill(Skill):
    image = None

    def __init__(self, owner):
        super().__init__(owner)
        if AssassinSkill.image is None:
            AssassinSkill.image = load_image('asset/Weapon/assassin_1.png')

        self.cooldown = 0.2
        self.duration = 0.2
        self.damage = 30

        self.skill_dir_x = 1
        self.skill_dir_y = 0

        self.swing_angle = 0
        self.afterimage = None  # 잔상
        self.hit_monsters = set()

    def can_use(self):
        if self.afterimage and self.afterimage.is_alive:
            return False
        return True

    def on_use(self):
        self.skill_dir_x = self.owner.last_move_dir_x
        self.skill_dir_y = self.owner.last_move_dir_y

        if self.skill_dir_x == 0 and self.skill_dir_y == 0:
            self.skill_dir_x = 1

        self.hit_monsters.clear()

        afterimage_x = self.owner.x
        afterimage_y = self.owner.y

        if abs(self.skill_dir_x) > abs(self.skill_dir_y):
            afterimage_x += self.skill_dir_x * 30
        else:
            afterimage_y += self.skill_dir_y * 30

        self.afterimage = SwordAfterimage(
            afterimage_x, afterimage_y,
            self.skill_dir_x, self.skill_dir_y,
            AssassinSkill.image,
            self.owner
        )

        game_world.add_object(self.afterimage, 2)
        for obj in list(game_world.world[3]):
            game_world.add_collision_pair('afterimage:monster', self.afterimage, obj)

        for obj in list(game_world.world[5]):
            game_world.add_collision_pair('afterimage:bullet', self.afterimage, obj)

    def on_update(self):
        progress = 1.0 - (self.duration_timer / self.duration)

        self.swing_angle = -90 + (progress * 180)

    def on_end(self):
        pass

    def update(self):
        super().update()

        if self.afterimage:
            if not self.afterimage.is_alive and self.afterimage in game_world.world[2]:
                game_world.remove_object(self.afterimage)

    def draw(self):

        if not self.is_active:
            return

        cam = game_world.camera

        sword_width = 50
        sword_height = 50

        base_angle = 0
        flip_mode = ''
        offset_x = 0
        offset_y = 0

        if abs(self.skill_dir_x) > abs(self.skill_dir_y):
            if self.skill_dir_x > 0:
                base_angle = 0
                flip_mode = ''
                offset_x = 20
            else:
                base_angle = 180
                flip_mode = ''
                offset_x = -20
        else:
            if self.skill_dir_y > 0:
                base_angle = 90
                flip_mode = ''
                offset_y = 20
            else:
                base_angle = -90
                flip_mode = ''
                offset_y = -20

        px = self.owner.x + offset_x
        py = self.owner.y + offset_y

        final_angle = base_angle + self.swing_angle

        if cam:
            sx, sy = cam.to_camera(px, py)
        else:
            sx, sy = px, py

        if self.image:
            angle_rad = math.radians(final_angle)

            offset_distance_x = sword_width / 2
            offset_distance_y = sword_height / 2

            draw_x = sx + offset_distance_x * math.cos(angle_rad) - offset_distance_y * math.sin(angle_rad)
            draw_y = sy + offset_distance_x * math.sin(angle_rad) + offset_distance_y * math.cos(angle_rad)

            self.image.clip_composite_draw(
                0, 58, 38, 38,
                angle_rad, flip_mode,
                draw_x, draw_y, sword_width, sword_height
            )

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.is_active:
            return 0, 0, 0, 0

        offset_x = 0
        offset_y = 0

        if abs(self.skill_dir_x) > abs(self.skill_dir_y):
            if self.skill_dir_x > 0:
                offset_x = 35
            else:
                offset_x = -35
        else:
            if self.skill_dir_y > 0:
                offset_y = 35
            else:
                offset_y = -35

        center_x = self.owner.x + offset_x
        center_y = self.owner.y + offset_y

        return center_x - 25, center_y - 25, center_x + 25, center_y + 25

    def handle_collision(self, group, other):
        if group == 'skill:monster' and self.is_active:
            if hasattr(other, 'hp') and getattr(other, 'alive', True) and other not in self.hit_monsters:
                self.hit_monsters.add(other)

                from monster import Boss1
                if isinstance(other, Boss1):
                    if not other.take_damage(self.damage):
                        return
                else:
                    other.hp -= self.damage
                    print(f"어쌔신 스킬 피격: 몬스터 HP={other.hp}")
                    if other.hp <= 0:
                        other.alive = False
                        game_world.move_object(other, 2)
                        import round1
                        if round1.current_room in round1.rooms:
                            round1.rooms[round1.current_room]['num'] -= 1

                        from round_1_mode import CoinUI
                        CoinUI.coin_count += 1

                        if round1.current_room == 1 and all(not m.alive for m in round1.monsters):
                            round1.change_map('asset/Map/round1_map.png', 'asset/Map/round1_collision.png', 1, self.owner)

                        if round1.current_room == 2 and all(not m.alive for m in round1.monsters):
                            round1.change_map('asset/Map/round1_map.png', 'asset/Map/round1_collision.png', 2, self.owner)
        elif group == 'skill:bullet' and self.is_active:
            if hasattr(other, 'alive'):
                other.alive = False
                print(f"총알 파괴")


class OfficerSkill(Skill):
    image = None

    def __init__(self, owner):
        super().__init__(owner)
        if OfficerSkill.image is None:
            OfficerSkill.image = load_image('asset/Weapon/officer_1.png')

        self.cooldown = 0
        self.duration = 0.4
        self.damage = 25

        self.start_x = 0
        self.start_y = 0

        self.arrow_x = 0
        self.arrow_y = 0

        self.skill_dir_x = 1
        self.skill_dir_y = 0


        self.move_distance = 200

        self.frame = 0
        self.total_frames = 6
        self.hit_monsters = set()

    def can_use(self):
        return not self.is_active

    def on_use(self):

        self.skill_dir_x = self.owner.last_move_dir_x
        self.skill_dir_y = self.owner.last_move_dir_y

        if self.skill_dir_x == 0 and self.skill_dir_y == 0:
            self.skill_dir_x = 1

        self.hit_monsters.clear()

        self.start_x = self.owner.x
        self.start_y = self.owner.y

        if abs(self.skill_dir_x) > abs(self.skill_dir_y):
            self.start_x += self.skill_dir_x * 30
        else:
            self.start_y += self.skill_dir_y * 30

        self.arrow_x = self.start_x
        self.arrow_y = self.start_y
        self.frame = 0

    def on_update(self):
        progress = 1.0 - (self.duration_timer / self.duration)


        self.arrow_x = self.start_x + (self.skill_dir_x * self.move_distance * progress)
        self.arrow_y = self.start_y + (self.skill_dir_y * self.move_distance * progress)

        self.frame = int(progress * self.total_frames)
        if self.frame >= self.total_frames:
            self.frame = self.total_frames - 1

        if self.check_out_of_bounds():
            self.is_active = False
            self.duration_timer = 0

    def check_out_of_bounds(self):
        try:
            import map as game_map
            import round1
            from lobby import is_lobby_collision

            if game_map.current_map == "Lobby":
                if is_lobby_collision(self.arrow_x, self.arrow_y):
                    return True

            elif game_map.current_map == "Round_1":
                if round1._collision_data is None:
                    return False

                scale = 10000.0 / round1._collision_width
                img_x = int(self.arrow_x / scale)
                img_y = int(self.arrow_y / scale)

                if img_x < 0 or img_x >= round1._collision_width or img_y < 0 or img_y >= round1._collision_height:
                    return True

                pil_y = round1._collision_height - 1 - img_y
                pixel = round1._collision_data[img_x, pil_y]

                if round1._image_mode == 'RGB':
                    r, g, b = pixel
                elif round1._image_mode == 'RGBA':
                    r, g, b, a = pixel
                else:
                    r = g = b = pixel if isinstance(pixel, int) else pixel[0]

                if r < 1 and g < 1 and b < 1:
                    return True

            return False
        except:
            return False

    def on_end(self):
        pass

    def draw(self):
        if not self.is_active:
            return

        cam = game_world.camera
        if cam:
            sx, sy = cam.to_camera(self.arrow_x, self.arrow_y)
        else:
            sx, sy = self.arrow_x, self.arrow_y

        if self.image:
            angle = 0
            if abs(self.skill_dir_x) > abs(self.skill_dir_y):
                if self.skill_dir_x > 0:
                    angle = 0
                else:
                    angle = 180
            else:
                if self.skill_dir_y > 0:
                    angle = 90
                else:
                    angle = -90

            self.image.clip_composite_draw(
                int(self.frame) * 25, 0, 25, 9,
                math.radians(angle), '',
                sx, sy, 100, 36
            )

        if game_framework.show_bb:
            if cam:
                l, b, r, t = self.get_bb()
                sl, sb = cam.to_camera(l, b)
                sr, st = cam.to_camera(r, t)
                draw_rectangle(sl, sb, sr, st)
            else:
                draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.is_active:
            return 0, 0, 0, 0

        if abs(self.skill_dir_x) > abs(self.skill_dir_y):
            return self.arrow_x - 50, self.arrow_y - 18, self.arrow_x + 50, self.arrow_y + 18
        else:
            return self.arrow_x - 18, self.arrow_y - 50, self.arrow_x + 18, self.arrow_y + 50

    def handle_collision(self, group, other):
        if group == 'skill:monster' and self.is_active:
            if hasattr(other, 'hp') and getattr(other, 'alive', True) and other not in self.hit_monsters:
                self.hit_monsters.add(other)

                from monster import Boss1
                if isinstance(other, Boss1):
                    if not other.take_damage(self.damage):
                        return
                else:
                    other.hp -= self.damage
                    print(f"오피서 스킬 피격: 몬스터 HP={other.hp}")
                    if other.hp <= 0:
                        other.alive = False
                        game_world.move_object(other, 2)
                        import round1
                        if round1.current_room in round1.rooms:
                            round1.rooms[round1.current_room]['num'] -= 1

                        from round_1_mode import CoinUI
                        CoinUI.coin_count += 1

                        if round1.current_room == 1 and all(not m.alive for m in round1.monsters):
                            round1.change_map('asset/Map/round1_map.png', 'asset/Map/round1_collision.png', 1, self.owner)

                        if round1.current_room == 2 and all(not m.alive for m in round1.monsters):
                            round1.change_map('asset/Map/round1_map.png', 'asset/Map/round1_collision.png', 2, self.owner)
        elif group == 'skill:bullet' and self.is_active:
            if hasattr(other, 'alive'):
                other.alive = False
                print(f"총알 파괴")

def create_skill(job_name,owner):
    skill_map = {
        'alchemist': AlchemistSkill,
        'assassin': AssassinSkill,
        'officer': OfficerSkill
    }
    skill_class = skill_map.get(job_name)
    if skill_class:
        return skill_class(owner)
    else:
        print(f"없는 직업: {job_name}")
        return None