from simulation import Simulation

mapping = {
  0: [1, 2, 3],
  1: [2, 5],
  2: [1, 4],
  14:[7],
}

ctrl = Simulation()
ctrl.analyze(mapping)