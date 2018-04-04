import main
import play
import behavior
import robocup
import main
import skills.move
import constants
import math
import enum
import role_assignment

## Testing class for facing one direction and strafing
class TestStrafe(play.Play):

    class State(enum.Enum):
        turning = 1
        moving = 2

    def __init__(self,
                 pos=robocup.Point(0, constants.Field.Length / 4.0),
                 angle=90):
        super().__init__(continuous=False)

        self.add_state(TestStrafe.State.turning, behavior.Behavior.State.running)
        self.add_state(TestStrafe.State.moving, behavior.Behavior.State.running)


        self.add_transition(behavior.Behavior.State.start,
            TestStrafe.State.turning, lambda: True,
                            "immediately")

        self.add_transition(TestStrafe.State.turning,
            TestStrafe.State.moving, lambda: self.subbehavior_with_name('move').state == behavior.Behavior.State.completed, 'at target position')

        self.add_transition(TestStrafe.State.moving,
            behavior.Behavior.State.completed, lambda: self.subbehavior_with_name('move').state == behavior.Behavior.State.completed, 'at target position')

        self.pos = pos
        self.angle = angle

    ## the position to move to (a robocup.Point object)
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    #turning
    def calculate_facing(self):
        target = robocup.Point(1.0,0.0)
        move = self.subbehavior_with_name('move')
        if (move.robot != None):
            target.rotate(move.robot.pos, self.angle)
            return target

    def is_at_target_angle(self):
        if self.robot != None:
            diff = abs(robocup.fix_angle_radians(self.robot.angle -
                                                 self.angle))
            return diff < (math.pi / 64.0)
        else:
            return False

    ##initial move to get to first strafing position
    def on_enter_turning(self):
        print("on enter turning")
        # Note these are offsets
        targetx = 1
        targety = 1
        targetx = self.pos.x + targetx if (self.pos.x + targetx) < constants.Field.Length else constants.Field.Length
        targety = self.pos.y + targety if (self.pos.y + targety) < constants.Field.Length else constants.Field.Length
        m = skills.move.Move(robocup.Point(targetx, targety))
        self.add_subbehavior(m, 'move', required=False)
        move = self.subbehavior_with_name('move')
        if (move.robot != None):
            move.robot_change_cost(float('inf'))

    def execute_turning(self):
        move1 = self.subbehavior_with_name('move')
        if (move1.robot != None):
            move1.robot.face(self.calculate_facing())

    #moving
    def on_enter_moving(self):
        print("on enter moving")
        print(self.subbehavior_with_name('move').state == behavior.Behavior.State.completed)
        # Note these are offsets
        targetx = 2
        targety = 2
        targetx = self.pos.x + targetx if (self.pos.x + targetx) < constants.Field.Length else constants.Field.Length
        targety = self.pos.y + targety if (self.pos.y + targety) < constants.Field.Length else constants.Field.Length
        move = self.subbehavior_with_name('move')
        move.pos = robocup.Point(targetx, targety)

    def execute_moving(self):
        print("EXECUTE MOVING")
        print(self.subbehavior_with_name('move').state == behavior.Behavior.State.completed)
        move = self.subbehavior_with_name('move')
        if (move.robot != None):
            move.robot.face(self.calculate_facing())

    def on_exit_moving(self):
        print("on exit moving")
        print(self.subbehavior_with_name('move').state == behavior.Behavior.State.completed)
        self.remove_subbehavior('move')
