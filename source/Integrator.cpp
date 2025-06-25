#include "Integrator.hpp"

void Integrator::stepRK4(DoublePendulum& system)
{
    Vec4 state = system.getState();
    const double dt = timeStep_;

    Vec4 k1 = dt * system.computeRHS(state);
    Vec4 k2 = dt * system.computeRHS(state + 0.5 * k1);
    Vec4 k3 = dt * system.computeRHS(state + 0.5 * k2);
    Vec4 k4 = dt * system.computeRHS(state + k3);

    Vec4 newState = state + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0;
    system.updateState(newState);
}