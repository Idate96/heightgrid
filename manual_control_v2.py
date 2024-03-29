#!/usr/bin/env python3

from heightgrid.envs_v2.hole import HoleEnv5x5_1x1, HoleEnv5x5_3x3, HoleEnv7x7_3x3
from heightgrid.envs_v2.trench import TrenchEnv7x7_3x1, TrenchEnv5x5_1x1, TrenchEnv5x5_3x1, ProceduralTrenchEnv
from heightgrid.envs_v2.trench import ConnectedTrenchEnv
import argparse


def redraw():
    if not args.agent_view:
        img = env.render("rgb_array", tile_size=args.tile_size)

    env.window.show_img(img)
    # env.window_target.show_img(img_target)


def reset():
    obs = env.reset()
    env.level_up()
    if args.seed != -1:
        env.seed(args.seed)

    if hasattr(env, "mission"):
        print("Mission: %s" % env.mission)
        env.window.set_caption(env.mission)

    redraw()

def key_handler(event):
    print("pressed", event.key)

    if event.key == "escape":
        env.window.close()
        env.window_target.close()

    if event.key == "backspace":
        reset()

    if event.key == "left":
        obs, reward, done, info = env.step(env.actions.rotate_base_counter)
        parse_step(obs, reward, done, info)

    if event.key == "right":
        obs, reward, done, info = env.step(env.actions.rotate_base_clock)
        parse_step(obs, reward, done, info)

    if event.key == "up":
        obs, reward, done, info = env.step(env.actions.forward)
        parse_step(obs, reward, done, info)

    if event.key == "down":
        obs, reward, done, info = env.step(env.actions.backward)
        parse_step(obs, reward, done, info)

    if event.key == "a":
        obs, reward, done, info = env.step(env.actions.rotate_cabin_counter)
        parse_step(obs, reward, done, info)

    if event.key == "d":
        obs, reward, done, info = env.step(env.actions.rotate_cabin_clock)
        parse_step(obs, reward, done, info)

    if event.key == " ":
        obs, reward, done, info = env.step(env.actions.do)
        parse_step(obs, reward, done, info)
        return

    if event.key == "backspace":
        print("resetting")
        parse_step(0, 0, 0, 0)

    if event.key == "enter":
        # obs, reward, done, info =  (env.actions.done)
        print("resetting")
        env.reset()
        redraw()
        return


def parse_step(obs, reward, done, info):
    redraw()
    # print("Observations [:, :, 0] \n", obs['image'][:, :, 0])
    # print("Observations [:, :, 1] \n", obs['image'][:, :, 1])
    # print("Observations [:, :, 2] \n", obs['image'][:, :, 2])
    # print("obs \n", obs)
    # print("obs \n", obs)

    print("Reward :", reward)
    print("Done: ", done)


parser = argparse.ArgumentParser()

parser.add_argument(
    "--env", help="gym environment to load", default="HeightGrid-Empty-5x5-v0"
)
parser.add_argument(
    "--seed", type=int, help="random seed to generate the environment with", default=-1
)
parser.add_argument(
    "--tile_size", type=int, help="size at which to render tiles", default=32
)
parser.add_argument(
    "--agent_view", 
    default=False,
    help="draw the agent sees (partially observable view)",
    action="store_true",
)

args = parser.parse_args()

# grid_height = np.zeros((5,5))
# grid_height[1, 3] = 1
# env = gym.make(args.env)
# env = EmptyEnv5x5()
rewards = {"collision_reward": -1, # against wall 0, ok
           "longitudinal_step_reward": -0.1,
           "base_turn_reward": -0.2, # ok
           "dig_reward": 1, # ok
           "dig_wrong_reward": -2, # ok
           "move_dirt_reward": 1,
           "existence_reward": -0.05, # ok
           "cabin_turn_reward": -0.05, # ok
           "terminal_reward": 10}

env = ConnectedTrenchEnv()
print(env)
env.seed = 24
env.reset()
# if args.agent_view:
#     env = FullyObsWrapper(env)
# env = ImgObsWrapper(env)

# window = Window('heightgrid - ' + args.env)
env.render(block=True, key_handler=key_handler)
# env.window.reg_key_handler(key_handler)
# env.window_target.reg_key_handler(key_handler)

# # reset()

# # # Blocking event loop
# env.window.show(block=True)
# env.window_target.show(block=True)
