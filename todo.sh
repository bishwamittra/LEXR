echo "Rank is: ${OMPI_COMM_WORLD_RANK}"

ulimit -t unlimited
shopt -s nullglob
# numthreads=$((OMPI_COMM_WORLD_SIZE))
mythread=$((OMPI_COMM_WORLD_RANK))

# tlimit="2000"
memlimit="16000000"
ulimit -v $memlimit


python3 run.py --thread=$mythread  --timeout=400 --random > output/$(date +"%d-%m-%Y-%T"-$mythread.txt)
