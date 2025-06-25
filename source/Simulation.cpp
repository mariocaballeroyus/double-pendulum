#include "Simulation.hpp"

void Simulation::run()
{
    double time = 0.0;
    trajectory_.clear();
    trajectory_.push_back(system_.getState());

    while (time < timeEnd_)
    {
        integrator_.stepRK4(system_);
        time += integrator_.getTimeStep();
        trajectory_.push_back(system_.getState());
    }
}