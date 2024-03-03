
# Particle Filter (PF) implementation in Python for my PF series on Medium

![ParticleFilter](https://github.com/mathiasmantelli/ParticleFilter/blob/main/figs/particles-spread.png?raw=true)


> **Particle Filter Part 4 Script/Blog**
>
> <a href="https://medium.com/@mathiasmantelli" target="_blank">Medium blog post</a>

## Getting Started Dependencies and Installation
I assume you have already installed Python 3.10. Now, Start by installing the dependency: 
```
sudo apt-get install python3-pip python3-dev  
sudo pip3 install pygame
```

Next, to run the code you just need to clone this repo and run the `main_pf.py` file:
```
git clone git@github.com:mathiasmantelli/ParticleFilter.git
cd ParticleFilter
python main_pf.py <width> <height> <number_of_landmarks> <number_of_particles>
```
## Examples
* `python my_pf.py 900 400 3 2000`, with high sigma values 
    ![Demo1](https://github.com/mathiasmantelli/ParticleFilter/blob/main/figs/demo1.png)
* `python my_pf.py 900 400 3 2000`, with low sigma values
    ![Demo2](https://github.com/mathiasmantelli/ParticleFilter/blob/main/figs/demo2.png)
