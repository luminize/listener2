### Problems with using interpolator from the listener2 callback

#### Description:
The values of `curr-pos` do not get calculated: `-nan`

### "Stock" example

first the situation where interpolation gets done with the interpolator example
I modified the feed-interpolator.py so it would print the value of `tp`

These HAL values show all the pins from `halrun -I interpolator.hal`

```
halcmd: show pin
Component Pins:
  Comp   Inst Type  Dir         Value  Name                             Epsilon         Flags
    75     76 float OUT      4.672682  ip.0.curr-acc                 	0.000010	0
    75     76 float OUT     -6.271527  ip.0.curr-pos                 	0.000010	0
    75     76 float OUT    -0.1000745  ip.0.curr-vel                 	0.000010	0
    75     76 float OUT             0  ip.0.end-acc                  	0.000010	0
    75     76 float OUT     -6.272924  ip.0.end-pos                  	0.000010	0
    75     76 float OUT             0  ip.0.end-vel                  	0.000010	0
    75     76 u32   IN     0x00000005  ip.degree                     			0
    75     76 float OUT             1  ip.duration                   	0.000010	0
    75     76 float IN         0.0001  ip.epsilon                    	0.000010	0
    75     76 bit   IN           TRUE  ip.jitter-correct             			0
    75     76 float OUT         0.959  ip.progress                   	0.000010	0
    75     76 s32   OUT             0  ip.serial                     			0
    75     76 s32   OUT          2880  ip.update.time                			0
   100        s32   OUT          2112  scope.sample.time             			0
```

the output in the terminal of `print str(tp)`
```
positions: -6.27292431121
velocities: 0.0
accelerations: 0.0
effort: 1.03576818105
time_from_start: 8.0
serial: 7
```

### listener2.py with the same interpolate.hal

```
halcmd: show pin
Component Pins:
  Comp   Inst Type  Dir         Value  Name                             Epsilon         Flags
    75     76 float OUT          -nan  ip.0.curr-acc                 	0.000010	0
    75     76 float OUT          -nan  ip.0.curr-pos                 	0.000010	0
    75     76 float OUT          -nan  ip.0.curr-vel                 	0.000010	0
    75     76 float OUT      0.981631  ip.0.end-acc                  	0.000010	0
    75     76 float OUT    0.07848956  ip.0.end-pos                  	0.000010	0
    75     76 float OUT     -0.335073  ip.0.end-vel                  	0.000010	0
    75     76 u32   IN     0x00000005  ip.degree                     			0
    75     76 float OUT     0.1655875  ip.duration                   	0.000010	0
    75     76 float IN         0.0001  ip.epsilon                    	0.000010	0
    75     76 bit   IN           TRUE  ip.jitter-correct             			0
    75     76 float OUT           0.1  ip.progress                   	0.000010	0
    75     76 s32   OUT             0  ip.serial                     			0
    75     76 s32   OUT          2232  ip.update.time                			0
   100        s32   OUT           888  scope.sample.time             			0
```

where this is the `print str(tp)` from the tp value at the `listener2` side which
gets put into the ringbuffer

```
positions: 0.0784895563066
velocities: -0.335073019322
accelerations: 0.981630980844
effort: 0.0
time_from_start: 1.299183482
duration: 0.165587465
serial: 61
```

### How to reproduce the situation

- clone and build the listener2 node
- run the `halrun -I interpolator.hal`
- in a new terminal `roscore` starts ROS
- in a new terminal `rosrun listener2 listener2.py` (make sure listener2.py is
  executable)
- in a new terminal `rostopic echo /joint_path_command`
- in a new terminal `rosbag play 2016-02-17-10-27-49.bag`

to view:
- make 2 halmeter probes of `ip.0.end-pos` and `ip.0.curr-pos`
- see `ip.0.end-pos` change with rosbag playout
- see `ip.0.curr-pos` have the value ``-nan`
