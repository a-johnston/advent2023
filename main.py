#! /usr/bin/env python3
import importlib
import os
import sys
from datetime import datetime


def _get_days(arg):
    latest = -1
    for file in os.listdir('.'):
        if os.path.isdir(file) and file.startswith('day'):
            latest = max(latest, int(file[3:]))

    def _int(x):
        x = int(x)
        if x < 0:
            x = latest + x + 1
        return x

    indices = []
    for part in arg.replace('day', '').split(','):
        if '..' in part:
            a, b = part.split('..', 1)
            a = _int(a or 1)
            b = _int(b or latest)
            indices.extend(range(a, b + 1))
        else:
            indices.append(_int(part))
    for idx in indices:
        yield f'day{idx}'


def _get_solvers(day):
    solvers = {}
    try:
        mod = importlib.import_module(day + '.main')
        for name in dir(mod):
            if name.startswith('solve'):
                solver = getattr(mod, name)
                solvers[name[6:]] = solver
    except ModuleNotFoundError:
        pass
    if not solvers:
        print(f'no solvers for {day}')
        sys.exit(1)
    return solvers


def _get_text_files(root, for_solver, solver_names):
    for path in sorted(os.listdir(root)):
        if path.endswith('.txt'):
            if not any(name in path for name in solver_names) or for_solver in path:
                yield os.path.join(root, path)


def _run_solver(solver, file):
    filename = os.path.split(file)[1]
    with open(file) as fp:
        start = datetime.now()
        lines = (l.rstrip('\n') for l in fp.readlines())
        solution = str(solver(lines, *sys.argv[2:]))
        if '\n' in solution:
            solution = '\n  ' + solution.replace('\n', '\n  ')
        print(f'\n {filename:<12}: {solution}')
        duration = (datetime.now() - start).total_seconds()
        print(f' Completed in {duration:0.4f}s')


def main():
    start = datetime.now()
    is_batch = len(sys.argv) > 1 and '..' in sys.argv[1]
    days = _get_days(sys.argv[1] if len(sys.argv) > 1 else '-1')
    print('Running AoC23 with args: ' + (' '.join(sys.argv[1:]) or '(none)'))
    for day in days:
        solvers = _get_solvers(day)
        print('\n' + day.replace('day', 'Day '))
        print('-' * 20)
        for name, solver in solvers.items():
            if name:
                print('\n' + name.replace('p', 'Part '))
            if is_batch and 'slow' in (solver.__doc__ or '').lower():
                print(' Skipping slow case in batch mode')
                continue
            for file in _get_text_files(day, name, set(solvers)):
                _run_solver(solver, file)
    duration = (datetime.now() - start).total_seconds()
    print(f'\nOverall completed in {duration:0.4f}s')


if __name__ == '__main__':
    main()
