world = [[] for _ in range(6)]
camera = None

def add_object(o, depth = 0):
    world[depth].append(o)


def add_objects(ol, depth = 0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return

    raise ValueError('Cannot delete non existing object')


def move_object(o, new_depth):
    for layer in world:
        if o in layer:
            layer.remove(o)
            world[new_depth].append(o)
            return
    raise ValueError('Cannot move non existing object')


def clear():
    global world

    for layer in world:
        layer.clear()


def collide(a, b):
    if a is None or b is None:
        return False
    if not hasattr(a, 'get_bb') or not hasattr(b, 'get_bb'):
        return False

    try:
        left_a, bottom_a, right_a, top_a = a.get_bb()
        left_b, bottom_b, right_b, top_b = b.get_bb()
    except Exception:
        return False

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True

collision_pairs = {}
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[],[]]
    if a and a not in collision_pairs[group][0]:
        collision_pairs[group][0].append(a)
    if b and b not in collision_pairs[group][1]:
        collision_pairs[group][1].append(b)


def handle_collisions():
    for group,pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a,b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)