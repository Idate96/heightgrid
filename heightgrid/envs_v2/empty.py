from numpy import random

from heightgrid.heightgrid_v2 import *
from heightgrid.register import register


class EmptyActions(IntEnum):
    # Turn left, turn right, move forward
    left = 0
    right = 1
    forward = 2

    # dig in the cell in from of you
    # dig = 3
    # Drop an soil that was dug
    # drop = 4
    # make a ramp
    # toggle = 5

    # Done completing task
    # done = 6


class FlatEnv(GridWorld):
    """
    Empty grid environment, no obstacles, sparse reward
    """

    def __init__(
            self,
            grid_height,
            target_grid_height,
            agent_start_pos=(1, 1),
            agent_start_dir=0,
            step_cost: float = -0.05,
            max_steps: int = 256,
            **kwargs
    ):
        self.global_rewards = {"collision_reward": -0.001,  # against wall 0, ok
                               "longitudinal_step_reward": -0.0005,
                               "base_turn_reward": -0.002,  # ok
                               "dig_reward": .1,  # ok
                               "dig_wrong_reward": -2,  # ok
                               "move_dirt_reward": .1,
                               "existence_reward": -0.0005,  # ok
                               "cabin_turn_reward": -0.0005,  # ok
                               "reward_scaling": 1,  # ok
                               "terminal_reward": 1}
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        super().__init__(
            target_grid_height=target_grid_height,
            heightgrid=grid_height,
            rewards=self.global_rewards,
            **kwargs
        )

        # dont allow digging
        self._actions = EmptyActions
        self.action_space = spaces.Discrete(len(EmptyActions))

        self._goal = True

    def reset(self, agent_pose=(0, 0, 0)):
        restart = super().reset(agent_pose=agent_pose)
        self.agent_start_pos = (agent_pose[0], agent_pose[1])
        # print("start pos : ", self.agent_start_pos)
        self.agent_start_dir = agent_pose[2]
        self.agent_position = self.agent_start_pos
        self.agent_dir = self.agent_start_dir
        return restart

    def goal_pos(self, agent_pos):
        random_pos_goal = np.random.randint(0, self.x_dim * self.y_dim)
        agent_id = agent_pos[0] * self.x_dim + agent_pos[1]
        while random_pos_goal == agent_id:
            random_pos_goal = np.random.randint(0, self.x_dim * self.y_dim)
        return np.array([random_pos_goal // self.x_dim, random_pos_goal % self.y_dim])


class EmptyEnv5x5(FlatEnv):
    def __init__(self, random=False, **kwargs):
        super().__init__(
            grid_height=np.zeros((5, 5)), target_grid_height=np.zeros((5, 5)), **kwargs
        )
        self.random = random
        self._goal = True
        self.place_obj_at_pos(Goal(), np.array([4, 4]))

    def reset(self):
        i = np.random.randint(0, 5)
        j = np.random.randint(0, 4)
        k = np.random.randint(0, 4)
        restart = super().reset(agent_pose=(i, j, k))
        self.place_obj_at_pos(Goal(), np.array([4, 4]))
        return restart


class EmptyRandomEnv5x5(FlatEnv):
    def __init__(self):
        super().__init__(
            grid_height=np.zeros((5, 5)),
            target_grid_height=np.zeros((5, 5)),
            agent_start_pos=None,
        )
        i = np.random.randint(0, 5)
        j = np.random.randint(0, 5)
        self.place_obj_at_pos(Goal(), np.array([i, j]))
        self._goal = True

    def reset(self):
        i = np.random.randint(0, 5)
        j = np.random.randint(0, 5)
        k = np.random.randint(0, 4)
        restart = super().reset(agent_pose=(i, j, k))
        goal_pos = self.goal_pos(agent_pos=[i, j])
        # print("goal ", goal_pos)
        self.place_obj_at_pos(Goal(), goal_pos)
        print("goal pos ", goal_pos)
        return restart


class EmptyEnv6x6(FlatEnv):
    def __init__(self, **kwargs):
        super().__init__(
            grid_height=np.zeros((6, 6)), target_grid_height=np.zeros((6, 6)), **kwargs
        )


class EmptyRandomEnv6x6(FlatEnv):
    def __init__(self):
        super().__init__(
            grid_height=np.zeros((6, 6)),
            target_grid_height=np.zeros((6, 6)),
            agent_start_pos=None,
        )


class EmptyEnv16x16(FlatEnv):
    def __init__(self, **kwargs):
        super().__init__(
            grid_height=np.zeros((16, 16)),
            target_grid_height=np.zeros((16, 16)),
            **kwargs
        )


class EmptyEnv8x8(FlatEnv):
    def __init__(self, random=False, **kwargs):
        super().__init__(
            grid_height=np.zeros((8, 8)),
            target_grid_height=np.zeros((8, 8)),
            max_steps=256,
            **kwargs
        )
        self.random = random
        self._goal = True
        self.place_obj_at_pos(Goal(), np.array([7, 4]))

    def reset(self):
        i = np.random.randint(0, 7)
        j = np.random.randint(0, 8)
        k = np.random.randint(0, 4)
        restart = super().reset(agent_pose=(i, j, k))
        self.place_obj_at_pos(Goal(), np.array([7, 4]))
        return restart


class EmptyRandomEnv8x8(FlatEnv):
    def __init__(self):
        super().__init__(
            grid_height=np.zeros((8, 8)),
            target_grid_height=np.zeros((8, 8)),
            max_steps=256,
            agent_start_pos=None,
        )
        i = np.random.randint(0, 8)
        j = np.random.randint(0, 8)
        self.place_obj_at_pos(Goal(), np.array([i, j]))
        self._goal = True

    def reset(self):
        i = np.random.randint(0, 8)
        j = np.random.randint(0, 8)
        k = np.random.randint(0, 4)
        restart = super().reset(agent_pose=(i, j, k))
        goal_pos = self.goal_pos([i, j])
        self.place_obj_at_pos(Goal(), goal_pos)
        return restart


class EmptyEnv14x14(FlatEnv):
    def __init__(self, random=False, **kwargs):
        super().__init__(
            grid_height=np.zeros((16, 16)),
            target_grid_height=np.zeros((16, 16)),
            max_steps=256,
            **kwargs
        )
        self.random = random
        self._goal = True
        self.place_obj_at_pos(Goal(), np.array([13, 4]))

    def reset(self):
        i = np.random.randint(0, 13)
        j = np.random.randint(0, 14)
        k = np.random.randint(0, 4)
        restart = super().reset(agent_pose=(i, j, k))
        self.place_obj_at_pos(Goal(), np.array([15, 4]))
        return restart


class EmptyRandomEnv14x14(FlatEnv):
    def __init__(self):
        super().__init__(
            grid_height=np.zeros((14, 14)),
            target_grid_height=np.zeros((14, 14)),
            max_steps=256,
            agent_start_pos=None,
        )
        i = np.random.randint(0, 14)
        j = np.random.randint(0, 14)
        self.place_obj_at_pos(Goal(), np.array([i, j]))
        self._goal = True

    def reset(self):
        i = np.random.randint(0, 14)
        j = np.random.randint(0, 14)
        k = np.random.randint(0, 4)
        restart = super().reset(agent_pose=(i, j, k))
        goal_pos = self.goal_pos([i, j])

        self.place_obj_at_pos(Goal(), goal_pos)
        return restart


class EmptyEnv16x16(FlatEnv):
    def __init__(self, random=False, **kwargs):
        super().__init__(
            grid_height=np.zeros((16, 16)),
            target_grid_height=np.zeros((16, 16)),
            max_steps=256,
            **kwargs
        )
        self.random = random
        self._goal = True
        self.place_obj_at_pos(Goal(), np.array([15, 4]))

    def reset(self):
        i = np.random.randint(0, 15)
        j = np.random.randint(0, 16)
        k = np.random.randint(0, 4)
        restart = super().reset(agent_pose=(i, j, k))
        self.place_obj_at_pos(Goal(), np.array([15, 4]))
        return restart


class EmptyRandomEnv16x16(FlatEnv):
    def __init__(self):
        super().__init__(
            grid_height=np.zeros((16, 16)),
            target_grid_height=np.zeros((16, 16)),
            max_steps=512,
            agent_start_pos=None,
        )
        i = np.random.randint(0, 16)
        j = np.random.randint(0, 16)
        self.place_obj_at_pos(Goal(), np.array([i, j]))
        self._goal = True

    def reset(self):
        i = np.random.randint(0, 16)
        j = np.random.randint(0, 16)
        k = np.random.randint(0, 4)
        restart = super().reset(agent_pose=(i, j, k))
        goal_pos = self.goal_pos([i, j])
        self.place_obj_at_pos(Goal(), goal_pos)
        return restart


class EmptyEnv32x32(FlatEnv):
    def __init__(self, random=False, **kwargs):
        super().__init__(
            grid_height=np.zeros((32, 32)),
            target_grid_height=np.zeros((32, 32)),
            max_steps=512,
            **kwargs
        )
        self.random = random
        self._goal = True
        self.place_obj_at_pos(Goal(), np.array([18, 4]))

    def reset(self):
        i = np.random.randint(0, 32)
        j = np.random.randint(0, 32)
        k = np.random.randint(0, 4)
        restart = super().reset(agent_pose=(i, j, k))
        self.place_obj_at_pos(Goal(), np.array([18, 4]))
        return restart


class EmptyRandomEnv32x32(FlatEnv):
    def __init__(self):
        super().__init__(
            grid_height=np.zeros((32, 32)),
            target_grid_height=np.zeros((32, 32)),
            max_steps=512,
            agent_start_pos=None,
        )
        i = np.random.randint(0, 32)
        j = np.random.randint(0, 32)
        self.place_obj_at_pos(Goal(), np.array([i, j]))
        self._goal = True

    def reset(self):
        i = np.random.randint(0, 32)
        j = np.random.randint(0, 32)
        k = np.random.randint(0, 4)
        restart = super().reset(agent_pose=(i, j, k))
        goal_pos = self.goal_pos([i, j])
        self.place_obj_at_pos(Goal(), goal_pos)
        return restart


register(id="HeightGrid-Empty-5x5-v0", entry_point="heightgrid.envs_v2:EmptyEnv5x5")

register(
    id="HeightGrid-Empty-Random-5x5-v0", entry_point="heightgrid.envs_v2:EmptyRandomEnv5x5"
)

register(id="HeightGrid-Empty-8x8-v0", entry_point="heightgrid.envs_v2:EmptyEnv8x8")

register(
    id="HeightGrid-Empty-Random-8x8-v0", entry_point="heightgrid.envs_v2:EmptyRandomEnv8x8"
)

register(id="HeightGrid-Empty-6x6-v0", entry_point="heightgrid.envs_v2:EmptyEnv6x6")

register(
    id="HeightGrid-Empty-Random-6x6-v0", entry_point="heightgrid.envs_v2:EmptyRandomEnv6x6"
)

register(id="HeightGrid-Empty-16x16-v0", entry_point="heightgrid.envs_v2:EmptyEnv16x16")
register(
    id="HeightGrid-Empty-Random-16x16-v0", entry_point="heightgrid.envs_v2:EmptyRandomEnv16x16"
)

register(id="HeightGrid-Empty-32x32-v0", entry_point="heightgrid.envs_v2:EmptyEnv32x32")
