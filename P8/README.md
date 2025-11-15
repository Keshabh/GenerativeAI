#here we will create crew ai agentic application
which can work with multiple agents together to achieve a task

#We need to define all the tools first.
#Then we need to create multiple agents using these tools.
#Then we need to create Tasks using these Agents and Tools.

#Using 1 agent we will first go through all videos in a youtube channel.
#Then using another agent , we will create blog using the result of agent 1.


#.venv environment setup is pip based, where we can install libs in a seperate folder, and used that environment.
#conda environment setup is heavier and more powerful, controlled by anaconda, where we can have control over python version + libs as well.

#conda environment create
conda create -p venv python==3.10

conda activate C:\Users\<your-username>\Projects\venv or conda activate ./venv