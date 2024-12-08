#!/bin/bash

DO_TEST=false
DO_LINT=false
DO_RUN=false
DO_CLEAN=false
EXCLUDE_COVERAGE=false

usage() {
    echo "Usage: $0 [--test|-t] [--lint|-l] [--run|-r] [--clean|-c] [--all|-a]"
    exit 1
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --test|-t) DO_TEST=true ;;
        --lint|-l) DO_LINT=true ;;
        --run|-r) DO_RUN=true ;;
        --clean|-c) DO_CLEAN=true ;;
        --no-coverage) EXCLUDE_COVERAGE=true ;;
        ## All skips clean so that the last output is the program output 
        --all|-a) DO_TEST=true; DO_LINT=true; DO_RUN=true ;;
        *) usage ;;
    esac
    shift
done

script_dir=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")

execute_test() {
    cd "$script_dir/src"
    coverage="--cov --cov-config=${script_dir}/config/.coveragerc --cov-report=html:../output/coverage"
    if $EXCLUDE_COVERAGE; then 
        coverage=""
    fi 
    pytest ${coverage} tests/* 
    return $?
}

execute_lint() {
    cd "$script_dir/src"
    pylint --rcfile="${script_dir}/config/.pylintrc" *
    return $?
}

execute_run() {
    ## Ignoring arguments, no real value to passing them. Use config file instead. 
    python3 ${script_dir}/src/main.py ${script_dir}/config/main.ini
    return $?
}

execute_clean() {
    
    find "${script_dir}" -type d -name ".pytest_cache*" -exec rm -rf {} + || { return 1; }
    find "${script_dir}" -type d -name "__pycache__*" -exec rm -rf {} + || { return 1; }
    find "${script_dir}" -type d -name ".coverage*" -exec rm -rf {} + || { return 1; }
    rm -rf "${script_dir}/output/coverage"
    ## TODO: Extend to support specific envirionment 
    return 0
}


pushd . > /dev/null 

fail_and_exit() { 
    echo "$1"
    popd > /dev/null
    exit 1
}

if $DO_LINT; then
    echo ""
    echo "-- Running Linting --" 
    echo "" 
    execute_lint || fail_and_exit "[ERROR] Linting Failed"
fi

if $DO_TEST; then
    echo ""
    echo "-- Running Tests --" 
    echo "" 
    execute_test || fail_and_exit "[ERROR] Test Execution Failed"
fi

if $DO_RUN; then
    echo ""
    echo "-- Running Program --" 
    echo "" 
    execute_run || fail_and_exit "[ERROR] Run Execution"
fi

if $DO_CLEAN; then
    execute_clean || fail_and_exit "[ERROR] Cleanup Execution Failed"
fi

popd . > /dev/null
echo "All requested operations completed successfully."