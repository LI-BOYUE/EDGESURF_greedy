# Edge Surf Greedy Playing(Black)

This programme is an intelligent obstacle avoidance programme based on the greedy algorithm, which is mainly used for automatic operation of edge surf characters

<img src=../IMAGE/test.png width="700px" height="400px" alt="TEST"/>

## Identification❔

We plan four regions as image grabbing regions are left view, right view, front view and obstacle view. When the program starts, the computer will only identify and calculate the colour block pixels (black) of these areas and store them in the instance to be compared later.

Request:

- Left view: upper left coordinate y is higher than the character, lower right coordinate y is lower than the character.
- Right view: same requirements and area equal to left view
- Front view: width <= right view bottom right horizontal coordinate - left view top left horizontal coordinate
- Obstacle view: width equal to the character's width, height according to the computer's running speed and operating delay

<img src=../IMAGE/loca.png width="700px" height="400px" alt="loca"/>

## Greedy

Overall logic and special logic:

- By comparing the ‘black’ counts of the left and right directions, the direction with the lowest ‘black’ counts is preferred.
- The whole process is evaluated in real time and the rules are corrected to support debugging output for easy analysis. Ensures optimal decision making in a dynamic environment.
- Avoid obstacles when the whole lower part moves forward. When black is recognised in the lower direction, only left or right direction is selected.
- When the difference between left and right directions is small, choose the ‘down’ direction by ignoring the error.

## Performance

1. Applicable mode is endless mode at low speed**s**
2. Successful distance about 4,000 metres on average
3. Easy to fall into local optimal solutions
4. Prone to obstacle rubbing
5. Different computers and usage patterns require manual positioning

## Versions

**Last version :** 1.0

## Requirement

* Python(latest)
* Modules or libraries for importing: pyautogui, time,PIL, math

## Special Thanks

* **FzF_StormZ**- Works: https://github.com/FzFStormZ/EdgeSurfBOT.git (box grabbing)
* **Dhiman Seal**- Works: https://github.com/Dhi13man/edge-surf-pid.git (using blue color for counting)

## Licence

This project haven't a licence
