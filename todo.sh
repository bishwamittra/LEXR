echo "Rank is: ${OMPI_COMM_WORLD_RANK}"

ulimit -t unlimited
shopt -s nullglob
numthreads=$((OMPI_COMM_WORLD_SIZE))
mythread=$((OMPI_COMM_WORLD_RANK))

# tlimit="2000"
# memlimit="8000000"


python -m memory_profiler email_match_test.py > output/$(date +"%d-%m-%Y-%T".txt)
