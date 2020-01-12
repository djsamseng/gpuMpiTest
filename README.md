# MPI and CUDA
Cuda aware MPI allows you to run GPU nodes with the nodes sending each other messages. Thus if a node is running a long time with state it can receive input from other nodes

## GPU
Need an NVIDIA GPU - CUDA. To enable CUDA/GPUs uncomment `@cuda.jit` from code

## Install
1) Download and install OpenMPI https://www.open-mpi.org/faq/?category=building
2) Install mpi4py 
```bash
$ pip install mpi4py 
$ mpiexec -n 5 python3 -m mpi4py.bench helloworld # Test
```
3) Install CUDA https://docs.nvidia.com/cuda/cuda-installation-guide-mac-os-x/index.html
4) install OpenMPI with cuda https://www.open-mpi.org/faq/?category=building
```bash
$ cd ./openmpi-4.0.2
$ ./configure --with-cuda
```

## Python
- Pip installed mpi4py for python 3 so use `python3` alias to python3

