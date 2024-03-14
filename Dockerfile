# Use the official Miniconda image as a parent image
FROM --platform=linux/amd64 continuumio/miniconda3:latest

# Set the working directory in the container to /app
WORKDIR /app

# Copy only the environment.yml file to avoid rebuilding the entire environment
# every time other files change
COPY environment.yml /app/environment.yml

# Create the Conda environment using the environment file
RUN conda env create -f environment.yml

# Make sure the environment is activated:
# This makes sure the environment is activated
# It's a good practice to explicitly add the path to ensure the right Python interpreter is used
ENV PATH /opt/conda/envs/bayesian-env/bin:$PATH

# Copy the rest of your application's code into the container
COPY . /app

# Make port 5000 available outside this container
EXPOSE 5000

# Run app.py when the container launches
# The Conda environment is activated by specifying the full path to the Python executable
CMD ["python", "run.py"]
