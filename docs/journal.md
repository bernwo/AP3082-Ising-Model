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

We note that in the first week, there is not much structure in the repository yet. However, in the upcoming weeks, we plan to clean up the directory as the direction of the project becomes clearer.

**Also note that all of the Metropolis functions can be found in `Metropolis_functions.py`.** We will repeat this several times to avoid confusion.

### Week 1 Milestones

* **Implementing the Metropolis Algorithm**
  * We mention that where the algorithm was implemented in section [Introduction to the Metropolis Algorithm](#Introduction-to-the-Metropolis-Algorithm).
  * Then, the *main* building blocks of the whole algorithm are explained throughout the whole of [Week 1](#week-1).
* **Finding out about Metropolis Algorithm**
  * Achieved in section [Introduction to the Metropolis Algorithm](#Introduction-to-the-Metropolis-Algorithm)
* **Find out how to calculate the total energy and energy of individual spin**
  * Achieved in section [Calculating the total energy of the system](#Calculating-the-total-energy-of-the-system)
* **Find exact critical temperature of the 2D square lattice Ising Model**
  * Achieved in section [Critical Temperature](#Critical-Temperature)
* **Obtain evolution of Ising model under the Metropolis algorithm**
  * Achieved in section [Results of the Metropolis(2D) Ising model simulation](#Results-of-the-Metropolis(2D)-Ising-model-simulation)
* **Obtain the magnetisation with respect to $`T/T_c`$**
  * Achieved in section [Absolute of average magnetisation |⟨M⟩|](#Absolute-of-average-magnetisation-|⟨M⟩|)

### Introduction to the Metropolis Algorithm

The pseudo code to each run of the [Metropolis algorithm](https://www.asc.ohio-state.edu/braaten.1/statphys/Ising_MatLab.pdf) can be written as:

* Calculate E<sub>current</sub>.
* Choose a [random spin to flip its sign](#Flipping-a-random-single-spin).
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
    * Do nothing. (i.e. the lattice stays the same)

Note that the *E* here refers to the *total energy* of the system.

The whole algorithm was packaged into `Metropolis2D(N,spins,J,T,h,creategif=False,plot_interval=100)` in `Metropolis_functions.py`.

### Calculating the total energy of the system

Let us denote $`E_{tot}`$ as the **total energy** for clarity.

The equation to calculate $`E_{tot}`$ is given by:

$`E_{tot}=\sum^{N\times N}_{i=1}E_i`$

where $`E_{i}`$ is the **energy of an individual spin** $`E_{i}=-\frac{J}{2}\sum_{j=i±1}s_is_j`$. To clarify, $`\sum_{j=i±1}`$ means the sum over the nearest neighbours of spin indexed $`i`$.
This expression was obtained from [here](http://star-www.dur.ac.uk/~tt/MSc/Lecture8.pdf).

The calculation of **energy of an individual spin** is achieved using the function `get_energy_singlespin(J,h,neighbour_sums,spins)` within the file `Metropolis_functions.py` which yields a 2D array. To calculate the sum of the neighbours of each of the spins, we utilised `scipy.ndimage.convolve` which allows us to efficiently calculate the sum of each of the spins over the entire lattice with a mere few lines of code. In the `convolve` function, we specified `mode='wrap'` to indicate that we enforce a [periodic boundary condition](https://en.wikipedia.org/wiki/Periodic_boundary_conditions).

Then, the **total energy** is just the sum of every element in the 2D array as implemented in the function `get_energy_total(E)`.

### Flipping a random single spin

This was implemented in the function `flip_a_spin(spins)`. To choose a random spin, we use `numpy.random.randint()` to randomly index a spin on the lattice. Then, to flip the sign of the spin, we used `numpy.negative`.

### Critical Temperature

From this [reference](https://cpb-us-w2.wpmucdn.com/u.osu.edu/dist/3/67057/files/2018/09/Ising_model_MFT-25b1klj.pdf), we note that the **exact critical temperature for 2D square lattice Ising model** is given as:

$`T_c=\frac{2.27J}{k_B}`$

where $`k_B`$ is the Boltzmann factor.

### Results of the Metropolis(2D) Ising model simulation

The `.gif`'s in this section is obtain by running `generate_Ising_gif.py`. Note the dependency on `imageio` as you might be lacking this library. The `imageio` library is used in conjunction with `os` and `matplotlib.pyplot` to obtain plots and convert them into an animated `gif`.

#### Ising Model evolution with external magnetic field, h=0

In this section we see the Ising model evolution for $`T<T_c`$ (left) and $`T>T_c`$ (right) while we fix the external magnetic field $`h=0`$. As we can see below, for $`T<T_c`$, the lattice stablises into big chunks of homogeneous islands while for $`T>T_c`$, the system does not stabilise and continues to be rather chaotic. This behaviour is expected and is indicative that our code is working as intended.

<img src="simulation_images/Metropolis_J2_TTc0.01_h0.gif" width="256" height="256" />
<img src="simulation_images/Metropolis_J2_TTc1.5_h0.gif" width="256" height="256" /><br />

#### Ising Model evolution with external magnetic field, h=10

In the previous section we saw the Ising model evolution for $`T>T_c`$ with $`h=0`$ stayed chaotic. Now, we still use the same $`T`$ while turning on the external magnetic field and set $`h=20`$. As we can see below, eventhough we are in the $`T>T_c`$ regime, the the system stabilised in fully positive spins. This behaviour is expected because the presence of external magnetic field destroys symmetry.

<img src="simulation_images/Metropolis_J2_TTc1.5_h20.gif" width="256" height="256" />

### Observables

#### Absolute of average magnetisation |⟨M⟩|

The figure in this section is obtained by running `generate_Ising_magnetisation`.

We ran in total 10 sets of Metropolis simulations each of 100000 runs and the lattice consists of $`64\times64`$ and $`h=0`$. The evaluation of magnetisation is done with this line: `M[i] = np.abs(np.mean(final_spins))` within `generate_Ising_magnetisation.py`.
From the figure below, we see that in fact the average magnetisation falls somewhat sharply to 0 at $`\frac{T}{T_c}\approx1`$, which is again an expected behaviour and is indicative that our code is working correctly.

The fluctuations are expected and the magnetisation not falling to 0 at exactly $`\frac{T}{T_c}=1`$ can be attributed to the insufficient size of the lattice.

<img src="simulation_images/Absolute_magnetisation_h0.png" width="256" height="256" /><br />

## Week 2

(due 2 May 2021, 23:59 (no lecture on King’s Day, 27 April))


## Week 3

(due 9 May 2021, 23:59)


