# Weekly progress journal

## Instructions

In this journal you will document your progress of the project, making use of weekly milestones. In contrast to project 1, you will need to define yourself detailed milestones.

Every week you should 

1. define **on Wednesday** detailed milestones for the week (according to the
   high-level milestones listed in the review issue).
   Then make a short plan of how you want to 
   reach these milestones. Think about how to distribute work in the group, 
   what pieces of code functionality need to be implemented. 
2. write about your progress **before** the Tuesday in the next week with
   respect to the milestones. Substantiate your progress with links to code,
   pictures or test results. Reflect on the relation to your original plan.

Note that there is a break before the deadline of the first week review
issue. Hence the definition of milestones and the plan for week 1 should be
done on or before 15 April.

We will give feedback on your progress on Tuesday before the following lecture. Consult the 
[grading scheme](https://computationalphysics.quantumtinkerer.tudelft.nl/proj2-grading/) 
for details how the journal enters your grade.

Note that the file format of the journal is *markdown*. This is a flexible and easy method of 
converting text to HTML. 
Documentation of the syntax of markdown can be found 
[here](https://docs.gitlab.com/ee/user/markdown.html#gfm-extends-standard-markdown). 
You will find how to include [links](https://docs.gitlab.com/ee/user/markdown.html#links) and 
[images](https://docs.gitlab.com/ee/user/markdown.html#images) particularly
useful.

## Week 1

### Introduction to the Metropolis Algorithm

The pseudo code to each run of the [Metropolis algorithm](https://www.asc.ohio-state.edu/braaten.1/statphys/Ising_MatLab.pdf) can be written as:

* Calculate E<sub>current</sub>.
* Choose a random spin to flip its sign.
* Calculate E<sub>trial</sub>.
* Calculate ΔE=E<sub>current</sub>-E<sub>trial</sub>.
* If ΔE ≤ 0
  * set E<sub>current</sub>=E<sub>trial</sub>
* Else
  * Choose random number *r* ∈ [0,1].
  * Compute W=exp(-βΔE)
  * If r < W
    * set E<sub>current</sub>=E<sub>trial</sub>
  * Else
    * Do nothing.

Note that the *E* here refers to the *total energy* of the system.

### Calculating the total energy of the system

### Results of the Metropolis(2D) Ising model simulation

<img src="simulation_images/Metropolis_J2_TTc0.01_h0.gif" width="256" height="256" />

<img src="simulation_images/Metropolis_J2_TTc1.5_h0.gif" width="256" height="256" />

<img src="simulation_images/Metropolis_J2_TTc1.5_h20.gif" width="256" height="256" />

## Week 2
(due before 28 April)


## Week 3
(due before 5 May)


